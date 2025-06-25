# TOOL_CALL_PROMPT usage

Ja, **absolut richtig erkannt**:
Diesen `TOOL_CALL_PROMPT` solltest du **nicht dauerhaft im sichtbaren Chatverlauf (als Message)** mitsenden, sondern **im Hintergrund** als Teil der **Systemlogik oder einer separaten Tool-Entscheidungsschicht** verwenden.

---

### ✅ Warum du den Prompt **nicht im Chatverlauf** behalten solltest:

1. **Lenkt das Modell dauerhaft auf Toolnutzung:**
   Es beeinflusst jeden Folgeprompt und „konditioniert“ das Modell unnötig stark.

2. **Verhindert natürliche Konversation:**
   Selbst wenn keine Tools gebraucht werden, denkt das Modell ständig an das JSON-Format und mögliche Aufrufe.

3. **Reduziert Flexibilität und Kreativität:**
   Das Modell fühlt sich an den Formatierungsbefehl gebunden – selbst wenn keine JSON-Ausgabe sinnvoll ist.

---

### ✅ Besseres Architektur-Muster:

Stattdessen:

- Verwende den `TOOL_CALL_PROMPT` **in einer separaten Funktion oder Abzweigung**, z. B.:

```python
if needs_tool_response(user_input):
    # Call model with TOOL_CALL_PROMPT as system message
    response = model.chat([
        {"role": "system", "content": TOOL_CALL_PROMPT},
        {"role": "user", "content": user_input}
    ])
else:
    # Normale Konversation ohne Tool-Prompt
    response = model.chat([
        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
        {"role": "user", "content": user_input}
    ])
```

Optional kannst du auch die Erkennung `needs_tool_response()` automatisieren, etwa durch:

- Heuristik (Stichworte wie „aktuell“, „heute“, „suchen“ etc.)
- LLM-gestützte Intent-Erkennung („Benötigt das eine Websuche?“ → ja/nein)

---

### 👇 Kurz gesagt:

- **Ja**, der `TOOL_CALL_PROMPT` sollte **nicht in jede Chat-Nachricht** wandern.
- Verwende ihn **nur temporär und gezielt**, wenn du Tool-Trigger erkennst.
- Danach kannst du wieder mit einem **neutralen Systemprompt** weiterarbeiten.

Wenn du magst, helfe ich dir gern, eine saubere Architektur oder Logik für den Tool-Call-Einsatz zu definieren.
