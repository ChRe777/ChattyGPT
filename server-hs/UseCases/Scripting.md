Hier ist ein einfaches Beispiel für **Scripting/Automation mit Python**, bei dem ein LLM (z. B. GPT-4) ein lokales Tool steuert – in diesem Fall ein Shell-Kommando oder ein API-Aufruf – basierend auf Benutzereingaben.

---

## 🛠️ Beispiel: GPT-gestützte Dateiverwaltung über die Shell

Ziel: Der Benutzer gibt eine natürliche Sprache ein (z. B. *„Liste alle .txt-Dateien im Downloads-Ordner“*) und das Skript interpretiert das und führt den passenden Befehl aus.

### 🔧 Voraussetzungen:

* OpenAI-API-Key
* `openai`-Python-Paket
* Zugriff auf das lokale Dateisystem / Shell

### 📜 Code:

```python
import openai
import subprocess

# 🔑 Setze deinen OpenAI API-Schlüssel
openai.api_key = "sk-..."

def prompt_to_command(prompt_text):
    system_prompt = (
        "Du bist ein hilfreicher Assistent, der Benutzereingaben in Shell-Befehle übersetzt. "
        "Gib nur den Befehl zurück, ohne Erklärung. Zielsystem ist Linux/macOS bash."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def run_shell_command(command):
    print(f"📦 Führe aus: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout or result.stderr

# 🧪 Beispiel-Nutzung
user_input = input("Was möchtest du tun? (z.B. 'Zeige alle PDF-Dateien im Desktop-Ordner')\n> ")
shell_command = prompt_to_command(user_input)
output = run_shell_command(shell_command)
print("🔎 Ergebnis:\n", output)
```

---

### 🧠 Beispiel-Dialog:

```
Was möchtest du tun?
> Alle PNG-Dateien im Ordner Bilder anzeigen

📦 Führe aus: ls ~/Bilder/*.png

🔎 Ergebnis:
bild1.png
screenshot.png
```

---

### 🔒 Sicherheitshinweis:

Dies ist ein leistungsfähiges, aber potenziell gefährliches Skript – ungefilterte Shell-Kommandos können Schaden anrichten. In produktiven Umgebungen sollte man:

* Nur erlaubte Befehle zulassen (Whitelist)
* Keine destruktiven Befehle (z. B. `rm`, `sudo`)
* Den Output vor Ausführung anzeigen und bestätigen lassen

---

Wenn du ein Beispiel mit API-Steuerung statt Shell willst (z. B. eine Notiz in Notion oder einen Task in Todoist erstellen), kann ich das auch liefern. Sag einfach Bescheid.
