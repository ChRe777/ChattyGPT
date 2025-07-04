```markdown
Die Idee einer **Produktberatung mit Entscheidungslogik durch ein LLM** (z. B. „Welche Versicherung passt zu mir?“) funktioniert **nicht als Faktenfrage**, sondern als **interaktiver, kontextsensitiver Dialog**, oft unterstützt durch Regeln, Präferenzen oder Profile.

---

## 🧭 Ziel: Assistenz mit Beratungskompetenz

Beispiel: Ein User fragt:

> "Ich bin 29, lebe in einer Mietwohnung, fahre kein Auto, und bin berufstätig. Brauche ich eine Haftpflichtversicherung oder reicht Hausrat?"

Ein klassischer Bot kann das **nicht gut entscheiden** – aber ein LLM **mit Entscheidungslogik** kann genau das:

---

## ✅ 3 Ansätze, wie das geht:

---

### 🔹 1. **LLM als interaktiver Entscheidungsbaum (Rule-based Prompting)**

Du gibst dem LLM eine Art eingebettete Entscheidungslogik als Prompt:

```text
Du bist ein Versicherungsberater. Entscheide basierend auf den folgenden Kriterien, welche Versicherung empfohlen wird:

Regeln:
- Jeder Erwachsene sollte eine private Haftpflichtversicherung haben.
- Eine Hausratversicherung ist sinnvoll, wenn man hochwertige Gegenstände in der Wohnung hat oder in einem Risikogebiet wohnt.
- Eine Berufsunfähigkeitsversicherung ist besonders für Berufstätige sinnvoll.
- Eine Kfz-Versicherung ist nur nötig, wenn man ein Auto besitzt.

Nutzerprofil:
- Alter: 29
- Wohnsituation: Mietwohnung
- Auto: Nein
- Beruf: Berufstätig
- Besondere Werte in der Wohnung: Keine

Welche Versicherungen empfiehlst du, und warum?
```

> 💡 Das LLM analysiert den Text, interpretiert die Regeln und gibt personalisierte Empfehlungen mit Begründung.

---

### 🔹 2. **LLM + Tool Calls (Entscheidungs-API)**

Du baust eine kleine Entscheidungs-Engine, z. B. als Python-Funktion oder Backend-API:

```python
def versicherungsempfehlung(profil):
    empf = []
    if profil["alter"] > 18:
        empf.append("Private Haftpflichtversicherung")
    if profil["berufstaetig"]:
        empf.append("Berufsunfähigkeitsversicherung")
    if profil["auto"]:
        empf.append("Kfz-Versicherung")
    return empf
```

Dann machst du **Tool Calls** aus dem LLM:

```json
"tool_calls": [
  {
    "function": {
      "name": "versicherungsempfehlung",
      "arguments": {
        "alter": 29,
        "berufstaetig": true,
        "auto": false
      }
    }
  }
]
```

LLM → ruft Tool auf → Tool gibt Ergebnis → LLM erklärt Empfehlung

---


📄 Generierter Bericht:

**Vertriebsbericht Juni 2025**

Wir sind stolz darauf, dass wir in diesem Monat unsere Ziele mit überzeugender Leistung übertroffen haben. Der Gesamtumsatz für Juni 2025 beträgt 184.500 €, was einer Erholung von etwa 5,4 % gegenüber dem Vorjahresmonat entspricht.

Unser Umsatzziel für den Monat lag bei 175.000 €, und wir haben es mit einer Übertreibung von etwa 5,6 % geschafft, diese Ziele zu erreichen. Dies ist ein Zeichen dafür, dass unsere Vertriebsstrategie und unser Team gut auf die veränderten Marktbedingungen reagiert sind.

Ein besonderes Lob für Laura König gilt, unserer besten Mitarbeiterin, die in diesem Monat wieder einmal überzeugend und effektiv gearbeitet hat. Ihre hervorragende Leistung trägt dazu bei, dass wir unsere Ziele auch auf regionale Ebene erreichen konnten.

Ein wichtiger Faktor für unseren Erfolg ist die erfolgreiche neue Kampagne im Norden. Hier erlebt man einen starken Anstieg der Umsätze, was zeigt, dass unsere Marketingstrategie sich gut durchgesetzt hat und wir unser Ziel zu treffen wissen, das Ziel des Vorjahres zu überbieten.

Die regionale Einnahmenverteilung zeigt auch, dass wir nicht nur auf ein einzelnes Gebiet setzen, sondern unsere Geschäftsaktivitäten auf verschiedene Regionen ausdehnen. So erzielen wir im Nordteil 64.000 €, im Südteil 57.000 €, im Westteil 40.500 € und im Ostteil 23.000 €.

Zusammenfassend können wir sagen, dass wir in diesem Monat unsere Ziele mit überzeugender Leistung übertroffen haben. Wir sind stolz auf unsere Erfolge und danken unseren Mitarbeitern für ihre hervorragende Arbeit. Wir werden weiterhin darauf achten, unsere Strategie anzupassen und neue Herausforderungen anzunehmen.

**Fazit:** Unsere Leistung im Juni 2025 ist ein Zeichen dafür, dass wir auf dem richtigen Weg sind. Wir werden uns weiterhin bemühen, unsere Ziele zu erreichen und besser zu werden.

Mit freundlichen Grüßen,
[Dein Name]
