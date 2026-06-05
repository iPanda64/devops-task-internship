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

**(În lucru...)**

---

## 3. Folosirea AI-ului

**(În lucru...)**

---

## 4. Ce-ai face cu mai mult timp

**(În lucru...)**

---

## 5. Întrebări / observații

**(În lucru...)**
