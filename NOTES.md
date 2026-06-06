# NOTES — Buleu Mihai Andrei

---

## 1. Probleme găsite și fixate

### Problemă #1 (docker-compose.yml)
- **Simptom:** Nu puteam accesa aplicația la adresa cerută `http://localhost:8000`.
- **Cum am diagnosticat-o:** Am rulat `docker ps` și am văzut că portul expus era 8080.
- **Cum am fixat-o și de ce:** Am schimbat portul de host din 8080 în 8000 pentru a corespunde cerințelor.

### Problemă #2 (docker-compose.yml)
- **Simptom:** Am primit cod de eroare 500 pe endpoint-ul `/visits`.
- **Cum am diagnosticat-o:** Am rulat `docker compose logs` și am observat `ConnectionError` către `localhost:6379` în serviciul web.
- **Cum am fixat-o și de ce:** Am schimbat `REDIS_HOST` din `localhost` în `redis`, deoarece în Docker `localhost` indică propriul container, iar comunicația se face prin numele serviciilor.


### Problemă #3 (CI)
- **Simptom:** Pipeline-ul CI eșua la pasul `Set up Python`.
- **Cum am diagnosticat-o:** Am verificat log-urile de execuție din GitHub Actions (și local cu `act`) și am văzut o eroare la versiunea de Python.
- **Cum am fixat-o și de ce:** Am actualizat versiunea de Python la 3.11 pentru compatibilitate și am adăugat un pas de instalare a dependențelor din `requirements.txt` deoarece `pytest` și librăriile aplicației nu erau prezente în mediul de rulare, CI-ul dând fail fără.

### Problemă #4 (app/main.py)
- **Simptom:** Endpoint-ul `/health` raporta `{"redis": true}` chiar și atunci când Redis era oprit.
- **Cum am diagnosticat-o:** Am citit codul din `app/main.py` și am observat că variabila `redis_ok` este mereu `True`. Am confirmat acest bug prin pornirea containerului și oprirea serviciului redis cu `docker compose stop redis`.
- **Cum am fixat-o și de ce:** Am corectat logica de eroare pentru a returna codul HTTP 503, `{"redis": false}` și statusul `unhealthy` atunci când Redis este indisponibil, pentru a reflecta corect starea serviciului.

---

## 2. Healthcheck-ul adăugat

- **Cum funcționează:** Folosește o comandă Python `one-liner` care accesează endpoint-ul `/health`. Am folosit biblioteca standard urllib. Dacă API-ul returnează un cod de eroare (cum ar fi 503-ul implementat anterior), comanda eșuează, iar Docker marchează containerul ca `unhealthy`.
- **De ce ai ales configurarea asta (interval, retries, timeout):**
  - **Interval (15s):** Oferă un echilibru între monitorizarea rapidă și consumul redus de resurse.
  - **Timeout (5s):** Suficient timp pentru un răspuns normal, dar destul de scurt pentru a detecta o aplicație blocată.
  - **Retries (3):** Evită alertele false cauzate de mici fluctuații temporare de rețea.
  - **Start Period (15s):** Oferă aplicației timp să pornească serverul Uvicorn înainte de prima verificare.

---

## 3. Folosirea AI-ului

- **Ce ai folosit:** Am folosit Gemini, in special varianta GeminiCLI.
- **Unde te-a ajutat cel mai mult:**
  - M-a ajutat la prototiparea rapidă a ideilor de rezolvare
  - L-am folosit pentru validarea schimbărilor înainte de commit.
  - M-a ajutat la scrierea unor parametri/flaguri/opțiuni. Ex. flagul --system în comanda adduser pentru securitate și evitarea scrierii parolei.
  - M-a ajutat la spell checking (scrierea diacriticelor)..
- **Unde te-a încurcat sau ți-a dat un răspuns greșit:** (foarte interesant pentru noi!)
  - Mi-a sugerat să creez userul abia după instalarea pachetelor cu pip. Asta ar face build-ul mai lent, pentru că Docker ar fi obligat să creeze userul din nou de fiecare dată când modific ceva în requirements.txt. Am corectat ordinea și am mutat crearea utilizatorului mai sus, ca să profit de layer caching (crearea userului nu are motiv de schimbare).
  - Mi-a generat un pas de formatter când cream jobul de lint. Acest lucru e greșit deoarece standardele de formatare nu au fost specificate în cerințele proiectului, iar blocarea pipeline-ului pentru motive pur estetice face mai mult rău decât bine dacă acestea nu sunt un requirement.
  - La healthcheck a recomandat folosirea curl, însă am optat pentru python pentru că imaginea folosită nu are curl instalat și am vrut să evit instalarea pachetelor suplimentare, păstrând imaginea lightweight.
  - La healthcheck, în cod, a lăsat error code 200 chiar dacă redis era indisponibil. Eu am optat pentru codul 503 care reflectă mai corect starea aplicației.
  - În implementarea /index, AI-ul a accesat direct baza de date Redis pentru a prelua numărul de vizite, ignorând endpoint-ul /visits. Acest bug l-am rezolvat într-un commit ulterior.
  - A sugerat includerea comenzii pip install --upgrade pip în Dockerfile. Am optat împotriva acesteia pentru a păstra mediul cu o versiune clară, previzibilă și deterministă.
- **Cum ai verificat ce-a generat:**
  - Am citit mereu toate liniile de cod înainte să fie aplicate pe codebase.
  - Am luat problemele pe rând, astfel m-am asigurat că generarea codului are impact mic.
  - La schimbări majore de configurație (Dockerfile și docker-compose.yml), am rulat docker compose up --build -d pentru a forța reconstrucția imaginii și a verifica dacă aplicația pornește corect.
  - Am testat local CI cu un tool local act.
  - Endpoint-urile au fost testate cu curl și prin browser.
---

## 4. Ce-ai face cu mai mult timp

  - Aș activa persistența Redis + volum montat, ca datele să supraviețuiască restarturilor.
  - Aș adăuga un stage de build & push imagine pe GHCR care rulează doar pe main dacă CI-ul actual este verde.
  - Aș implementa rate limiting la nivel de aplicație prin slowapi (ex. 50 req/minut pe toate endpoint-urile).
  - Aș extinde healthcheck-ul cu mai multe metrici relevante (ex: versiune, uptime, latency etc.).

---

## 5. Întrebări / observații

**(În lucru...)**
