import requests
import json

# Berichtsdaten
daten = {
    "monat": "Juni 2025",
    "gesamtumsatz_eur": 184500,
    "umsatz_ziele_eur": 175000,
    "bester_mitarbeiter": "Laura König",
    "neukunden": 27,
    "regionen": {
        "Nord": 64000,
        "Süd": 57000,
        "West": 40500,
        "Ost": 23000
    },
    "kommentare": "Starker Anstieg durch neue Kampagne im Norden."
}

# Prompt generieren
prompt = f"""
Schreibe einen professionellen Vertriebsbericht basierend auf diesen Daten:

Monat: {daten['monat']}
Gesamtumsatz: {daten['gesamtumsatz_eur']} €
Umsatzziel: {daten['umsatz_ziele_eur']} €
Bester Mitarbeiter: {daten['bester_mitarbeiter']}
Neukunden: {daten['neukunden']}
Regionale Umsätze:
- Nord: {daten['regionen']['Nord']} €
- Süd: {daten['regionen']['Süd']} €
- West: {daten['regionen']['West']} €
- Ost: {daten['regionen']['Ost']} €
Kommentar: {daten['kommentare']}

Der Bericht soll sachlich, aber positiv formuliert sein. Gliedere ihn sinnvoll in Absätze.
"""

# Anfrage an Ollama senden
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
)

# Antwort auslesen
data = response.json()
print("\n📄 Generierter Bericht:\n")
print(data["response"])
