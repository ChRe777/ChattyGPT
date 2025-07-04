Gerne! Hier ist ein **praktisches Beispiel für ein LLM + formularbasiertes Dialogsystem** (wie ein „ChatWizard“) – ideal für strukturierte, geführte Interaktionen wie:

* 📝 Anträge (z. B. Kredit, Versicherung)
* 🛠️ Supportformulare
* 🤖 Onboarding-Assistenten
* 📄 Behördliche Anfragen

---

## 🎯 Ziel:

Ein **LLM** führt den Nutzer **schrittweise durch ein Formular** – also ein geführter, dialogorientierter Ablauf, bei dem das LLM versteht, warum welche Eingabe nötig ist, und auch passende Rückfragen oder Hilfen liefern kann.

---

## 🧪 Beispiel: **Support-Anfrage für ein defektes Produkt**

Wir simulieren ein System, das:

1. Felder abfragt (Name, Produkt, Problem, Kaufdatum, etc.)
2. Kontext speichert
3. Eine automatisch formulierte Support-Mail oder Antwort generiert

---

## ✅ Umsetzung (Konsolen-Demo)

```python
import openai

openai.api_key = "DEIN_API_KEY"

dialog_context = {}

def frage_stellen(feld, frage):
    antwort = input(frage + " ")
    dialog_context[feld] = antwort

def generiere_supportmail():
    prompt = f"""
Du bist ein Support-Assistent. Der Nutzer hat ein Problem mit einem Produkt. Formuliere basierend auf folgenden Angaben eine professionelle Support-Mail.

Name: {dialog_context.get('name')}
Produkt: {dialog_context.get('produkt')}
Kaufdatum: {dialog_context.get('kaufdatum')}
Problem: {dialog_context.get('problem')}
Wunsch: {dialog_context.get('wunsch')}

Die Antwort soll höflich, klar und auf Deutsch sein.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du bist ein KI-basierter Support-Assistent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def wizard_starten():
    print("🛠️ Willkommen beim Support-Assistenten!")
    frage_stellen("name", "Wie heißen Sie?")
    frage_stellen("produkt", "Welches Produkt betrifft Ihre Anfrage?")
    frage_stellen("kaufdatum", "Wann haben Sie das Produkt gekauft?")
    frage_stellen("problem", "Was genau ist das Problem?")
    frage_stellen("wunsch", "Was wünschen Sie sich vom Support (z. B. Ersatz, Rückerstattung)?")

    print("\n📧 Generierte Support-Anfrage:\n")
    print(generiere_supportmail())


if __name__ == "__main__":
    wizard_starten()
```

---

## 🧾 Beispiel-Dialog (Konsole):

```text
🛠️ Willkommen beim Support-Assistenten!
Wie heißen Sie? Anna Becker
Welches Produkt betrifft Ihre Anfrage? Bluetooth-Kopfhörer Modell X2
Wann haben Sie das Produkt gekauft? 10.05.2024
Was genau ist das Problem? Der rechte Hörer funktioniert nicht mehr.
Was wünschen Sie sich vom Support (z. B. Ersatz, Rückerstattung)? Austauschgerät

📧 Generierte Support-Anfrage:

Sehr geehrtes Support-Team,

mein Name ist Anna Becker und ich habe am 10.05.2024 Ihre Bluetooth-Kopfhörer Modell X2 erworben. Leider funktioniert seit Kurzem der rechte Hörer nicht mehr.

Ich bitte Sie daher um die Zusendung eines Austauschgeräts. Für Rückfragen stehe ich gerne zur Verfügung.

Vielen Dank und freundliche Grüße
Anna Becker
```

---

## 🧠 Warum ist das LLM + Formular-Dialog nützlich?

* Führt Benutzer **gezielt & freundlich durch komplexe Abläufe**
* Kombiniert **strukturierte Eingabe** mit **intelligenter Verarbeitung**
* Reduziert Fehler bei freien Texteingaben
* Ideal für **behördliche oder juristische Texte**, Anträge, Verträge, Support

---

## 💡 Erweiterbar mit:

| Feature                              | Beschreibung                                     |
| ------------------------------------ | ------------------------------------------------ |
| **Web-GUI** (z. B. Streamlit, Flask) | Mach den Wizard als Webformular mit Chat-Optik   |
| **Validierung + Rückfragen**         | "Das Kaufdatum scheint ungültig, stimmt das so?" |
| **Mehrsprachigkeit**                 | Ein- und Ausgabe in mehreren Sprachen            |
| **LLM-gestützte Klassifikation**     | Z. B. „Supportanfrage zu Garantie“ oder „Defekt“ |
| **RAG/FAQ-Verbindung**               | Automatische Antwort aus Wissensdatenbank        |

---

### 👉 Möchtest du:

* das Ganze als Web-App (z. B. mit Streamlit)?
* eine PDF-Antwort generieren (z. B. Supportformular)?
* API-Integration für echten Ticketversand (z. B. an Freshdesk)?

Ich kann dir direkt den Code liefern. Sag einfach, wie du es einsetzen willst!
