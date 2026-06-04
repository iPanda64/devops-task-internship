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
