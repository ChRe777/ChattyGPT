Sehr gerne! Hier ist ein praktisches Beispiel für **Dokumentenverständnis mit einem LLM**, bei dem automatisch **Informationen aus einer Rechnung** extrahiert werden – z. B. **Rechnungsnummer**, **Betrag**, **Rechnungssteller**, **Datum**, **Positionen** usw.

---

## 📄 Ziel:

> Ein intelligenter Agent liest eine unstrukturierte Rechnung und extrahiert strukturierte Daten – nützlich für Buchhaltung, ERP-Systeme oder KI-gestützte Archivierung.

---

## 🧾 Beispiel-Rechnung (unstrukturierter Text):

```text
RECHNUNG

Musterfirma GmbH
Hauptstraße 12
12345 Musterstadt

Rechnungsnummer: 2023-0915
Rechnungsdatum: 15.09.2023
Kundennummer: K-00457

Leistung:
- Webentwicklung für Projekt "Website Relaunch"
  Zeitraum: 01.08.2023 – 31.08.2023
  Stunden: 42 à 85,00 €
  Gesamt: 3.570,00 €

Zahlbar bis: 30.09.2023
Bankverbindung: DE89 3704 0044 0532 0130 00

Mit freundlichen Grüßen
Musterfirma GmbH
```

---

## 🤖 Python-Code: Dokumentenanalyse mit OpenAI (GPT)

```python
import openai

openai.api_key = "DEIN_API_KEY"

def extrahiere_rechnungsdaten(rechnungstext):
    prompt = f"""
Du bist ein Dokumentenanalyse-Agent. Extrahiere die wichtigsten Felder aus dieser Rechnung und gib sie im JSON-Format zurück.

Rechnung:
\"\"\"
{rechnungstext}
\"\"\"

Felder:
- rechnungsnummer
- rechnungsdatum
- kundennummer
- firma
- gesamtbetrag
- zahlungsziel
- leistung (als Liste mit bezeichnung, zeitraum, stunden, stundensatz, gesamt)

Gib bitte nur gültiges JSON zurück.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist ein extraktionsspezialisierter KI-Agent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Test
rechnungstext = """(siehe oben)"""
ergebnis = extrahiere_rechnungsdaten(rechnungstext)
print(ergebnis)
```

---

## 🧾 Beispielausgabe (JSON):

```json
{
  "rechnungsnummer": "2023-0915",
  "rechnungsdatum": "15.09.2023",
  "kundennummer": "K-00457",
  "firma": "Musterfirma GmbH",
  "gesamtbetrag": "3570.00",
  "zahlungsziel": "30.09.2023",
  "leistung": [
    {
      "bezeichnung": "Webentwicklung für Projekt 'Website Relaunch'",
      "zeitraum": "01.08.2023 – 31.08.2023",
      "stunden": 42,
      "stundensatz": 85.00,
      "gesamt": 3570.00
    }
  ]
}
```

---

## 🧠 Anwendungen von Dokumentenverständnis:

* 📥 **Automatisierte Buchhaltung** (z. B. DATEV-Export, Kontierung)
* 🤖 **Vertragsanalyse** (z. B. Fristen, Klauseln, Vertragspartner)
* 🧾 **OCR + NLP** für PDFs & Scans (z. B. mit Tesseract oder Azure Form Recognizer)
* 🧾 **Mehrsprachige Dokumente** extrahieren + normalisieren

---

## 🔁 Erweiterbar mit:

* 📄 **PDF-Verarbeitung**: `pdfplumber`, `PyMuPDF`, `Tika`
* 💬 **RAG (Retrieval-Augmented Generation)** für große Verträge oder Richtlinien
* 🧠 **LangChain / Haystack Pipelines** für komplexe Workflows
* 🗂️ **Batch-Verarbeitung ganzer Dokumentordner**

---

Möchtest du ein Beispiel für:

* Vertragsanalyse (z. B. Kündigungsfristen)?
* Extraktion aus echten PDF-Dateien?
* Integration in ein DMS (Dokumentenmanagementsystem)?

Ich zeig dir gerne mehr!

------



Perfekt! Hier zeige ich dir ein **praktisches Beispiel für Vertragsanalyse mit einem LLM** – ideal für den Einsatz in **LegalTech**, **Compliance**, **Due Diligence** oder zur **Vertragsverwaltung** in Unternehmen.

---

## 🎯 Ziel:

> Ein intelligenter Agent analysiert einen **Vertragstext** und extrahiert juristisch relevante Informationen:

* Vertragspartner
* Vertragsbeginn & Laufzeit
* Kündigungsfrist
* Vertragsgegenstand
* Besondere Klauseln (z. B. Vertraulichkeit, Haftung)

---

## 🧾 Beispiel: Einfacher Vertragstext

```text
Dienstleistungsvertrag

zwischen der Firma SoftSolution GmbH, Musterstraße 1, 12345 Berlin,
– nachfolgend "Auftraggeber" genannt –

und

Herrn Max Mustermann, Freelancer, Musterweg 5, 54321 Köln,
– nachfolgend "Auftragnehmer" genannt –

wird folgender Vertrag geschlossen:

§1 Vertragsgegenstand
Der Auftragnehmer übernimmt die Wartung und Weiterentwicklung der internen Webanwendung des Auftraggebers.

§2 Vertragsdauer
Der Vertrag beginnt am 01.01.2024 und wird auf unbestimmte Zeit geschlossen.

§3 Kündigung
Der Vertrag kann mit einer Frist von 4 Wochen zum Monatsende von beiden Parteien schriftlich gekündigt werden.

§4 Vertraulichkeit
Beide Parteien verpflichten sich zur Vertraulichkeit über alle projektbezogenen Informationen.

Berlin, 15.12.2023
```

---

## 🤖 Python-Code zur Vertragsanalyse mit OpenAI GPT

```python
import openai

openai.api_key = "DEIN_API_KEY"

def analysiere_vertrag(text):
    prompt = f"""
Analysiere den folgenden Vertragstext und extrahiere die folgenden Informationen als JSON:

- vertragspartner: {{"auftraggeber": Name und Adresse, "auftragnehmer": Name und Adresse}}
- vertragsbeginn
- vertragsdauer
- kündigungsfrist
- vertragsgegenstand
- vertraulichkeit (ja/nein)

Vertragstext:
\"\"\"{text}\"\"\"

Gib bitte nur valides JSON zurück.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist ein juristischer Assistent für Vertragsanalyse."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
```

---

## 📋 Beispiel-Ausgabe (strukturierte Analyse als JSON):

```json
{
  "vertragspartner": {
    "auftraggeber": "SoftSolution GmbH, Musterstraße 1, 12345 Berlin",
    "auftragnehmer": "Max Mustermann, Freelancer, Musterweg 5, 54321 Köln"
  },
  "vertragsbeginn": "01.01.2024",
  "vertragsdauer": "unbefristet",
  "kündigungsfrist": "4 Wochen zum Monatsende",
  "vertragsgegenstand": "Wartung und Weiterentwicklung der internen Webanwendung",
  "vertraulichkeit": "ja"
}
```

---

## 💼 Typische Anwendungsszenarien:

| 📌 Use Case                    | Beschreibung                                        |
| ------------------------------ | --------------------------------------------------- |
| **Due Diligence**              | Verträge maschinell auf Risiken & Fristen prüfen    |
| **Fristenmanagement**          | Laufzeiten, Kündigungsfristen automatisch erkennen  |
| **Vertragsklassifikation**     | NDA, Werkvertrag, Dienstvertrag, Lizenzvertrag etc. |
| **Klauselprüfung & Red Flags** | Automatische Prüfung auf z. B. Haftung, SLA, DSGVO  |
| **Vertraulichkeit & IP**       | Extraktion von Schutzklauseln                       |

---

## 🧩 Erweiterbar mit:

* 🔎 **PDF-Parser**: `PyMuPDF`, `pdfplumber`, `Tika` zur Dokumentextraktion
* 🧠 **LangChain + VectorDB**: Retrieval-basiertes Nachschlagen in Klausel-Datenbanken
* 🧾 **Klauselgenerator**: Antwort vorschlagen lassen ("Wie sollte §4 formuliert sein?")
* 📊 **Reporting**: Vertragsdaten automatisiert in Excel/ERP ausgeben

---

## ✅ Möchtest du auch:

* Vertragsanalyse aus **echten PDF-Dateien**?
* **Vergleich von Verträgen** (z. B. "Was unterscheidet Vertrag A von B?")
* Einen Web-Demo-Bot zum Durchsuchen und Prüfen von Verträgen?

Sag einfach Bescheid – ich zeige dir gerne konkrete Lösungen!
