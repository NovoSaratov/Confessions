# Sikkerhetsveiledning for Confessions-applikasjonen

## Produksjonsdeployering

Det er kritisk viktig å deploye applikasjonen på en sikker måte i produksjonsmiljøet. Følg Flask sin offisielle deployeringsveiledning for beste praksis:
[Flask Deployeringsveiledning](https://flask.palletsprojects.com/en/3.0.x/deploying/)

### Viktige punkter for deployering:
- Bruk en WSGI-server som Gunicorn
- Aktiver HTTPS med gyldig SSL-sertifikat
- Sett opp en reverse proxy (f.eks. Nginx)
- Deaktiver debug-modus
- Bruk miljøvariabler for sensitive data

## Sikkerhetsnøkler og Passord

### Hemmelig nøkkel (Secret Key)
- Endre den hardkodede hemmelige nøkkelen i `app.py`
- Bruk en sterk, tilfeldig generert nøkkel
- Eksempel på generering:
```python
import secrets
secret_key = secrets.token_hex(32)
```
- Lagre nøkkelen i en miljøvariabel:
```bash
export FLASK_SECRET_KEY='din_genererte_nøkkel'
```

### Admin-passord
- Endre standardpassordet (`admin123`)
- Bruk et sterkt passord med:
  - Minst 12 tegn
  - Blanding av store og små bokstaver
  - Tall og spesialtegn
  - Unngå vanlige ord og personlig informasjon

## Andre Viktige Sikkerhetstiltak

### Ordfilter
Implementer et ordfilter for å blokkere uønsket innhold:
```python
BLOCKED_WORDS = [
    # Legg til uønskede ord her
]

def contains_blocked_words(text):
    return any(word in text.lower() for word in BLOCKED_WORDS)
```

### Rate Limiting
Implementer rate limiting for å forhindre misbruk:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### CSRF-beskyttelse
Aktiver CSRF-beskyttelse for skjemainnsendinger:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

### Input-validering
- Valider all brukerinput
- Sanitizer tekst før lagring
- Begrens lengden på innsendte data

### Logging og Overvåking
- Implementer sikker logging av admin-aktiviteter
- Overvåk for mistenkelig aktivitet
- Sette opp varsler for uvanlig bruk

### Database-sikkerhet
- Bruk parameteriserte spørringer (allerede implementert)
- Begrens database-tilgang
- Ta regelmessige sikkerhetskopier

## Oppdateringer og Vedlikehold
- Hold alle avhengigheter oppdaterte
- Følg sikkerhetsvarsler for brukte biblioteker
- Test sikkerhetsoppdateringer i et testmiljø før produksjonsdeployering

## Kontakt
Ved funn av sikkerhetsproblemer, vennligst rapporter til meg 