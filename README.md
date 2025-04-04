# Confessions

En enkel webapplikasjon hvor brukere kan dele anonyme bekjennelser. Prosjektet er bygget med Flask og bruker SQLite som database.

## Funksjoner

- Del anonyme bekjennelser
- Admin panel for å moderere bekjennelser
- Responsivt design som fungerer på alle enheter
- Realtids oppdatering av bekjennelser

## Installasjon

1. Klon prosjektet:
```bash
git clone [https://github.com/NovoSaratov/Confessions.git]
cd confessions  
```

2. Opprett et virtuelt miljø og aktiver det:
```bash
python -m venv venv
source venv/bin/activate
```

3. Installer avhengigheter:
```bash
pip install -r requirements.txt
```

4. Start applikasjonen:
```bash
python3 app.py
```

Applikasjonen vil nå være tilgjengelig på `http://localhost:5000`

## Bruk

### For brukere
1. Gå til hjemmesiden
2. Skriv inn din bekjennelse i tekstfeltet
3. Klikk på "Submit Confession"
4. Din bekjennelse vil nå vises på siden

### For administratorer
1. Gå til `/admin` for å åpne admin-panelet
2. Logg inn med følgende standardinnstillinger:
   - Brukernavn: `admin`
   - Passord: `admin123`
3. I admin-panelet kan du:
   - Se alle bekjennelser
   - Slette uønskede bekjennelser
   - Se statistikk over antall bekjennelser

## Teknisk informasjon

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Responsivt design med moderne CSS

## Sikkerhet

For produksjonsmiljøet anbefales følgende sikkerhetstiltak:
1. Deploy aplikasjonen gjennom flask
2. Implementer HTTPS
3. Legg til CSRF-beskyttelse
4. Implementer rate limiting
5. Legg til ordfilter

## BRUKSANVISNING
[Dette er hvor du kan lese på hvordan man bruker nettsiden](userguide.md)

## Lisens

[Dette prosjektet er lisensiert under MIT-lisensen](LICENSE)

