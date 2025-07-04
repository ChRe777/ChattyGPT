 **Code Agents**: Schreiben, testen und debuggen von Code anhand von Aufgabenstellungen.

Gerne! Hier ist ein konkretes **Python-Beispiel für "Code Agents"**, also ein System, das eine **Aufgabenstellung versteht, Code schreibt, testet und bei Fehlern debuggt** – vollautomatisch.

---

## 🧠 Was ist ein "Code Agent"?

Ein **Code Agent** ist ein intelligentes System (z. B. basierend auf einem LLM wie GPT-4), das Aufgabenstellungen entgegennimmt und daraus automatisch:

1. **Code generiert**
2. **Tests durchführt**
3. **Fehler erkennt und debuggt**
4. **Code iterativ verbessert**

---

## 🔧 Beispiel: Finde die größte Primzahl unterhalb von N

Wir simulieren hier einen einfachen Code Agent mit diesen Fähigkeiten:

### 🧪 1. Aufgabenstellung

> *"Schreibe eine Funktion `groesste_primzahl(n)`, die die größte Primzahl unterhalb von `n` zurückgibt."*

---

### 🧠 Code Agent in Python

```python
import traceback

def aufgabe_verstehen():
    aufgabe = "Schreibe eine Funktion groesste_primzahl(n), die die größte Primzahl unterhalb von n zurückgibt."
    return aufgabe

def code_generieren():
    code = """
def groesste_primzahl(n):
    def ist_prim(z):
        if z < 2:
            return False
        for i in range(2, int(z ** 0.5) + 1):
            if z % i == 0:
                return False
        return True

    for i in range(n - 1, 1, -1):
        if ist_prim(i):
            return i
    return None
"""
    return code

def code_ausfuehren(code, tests):
    scope = {}
    try:
        exec(code, scope)
        func = scope.get("groesste_primzahl")
        for eingabe, erwartet in tests:
            ergebnis = func(eingabe)
            assert ergebnis == erwartet, f"Fehler: Eingabe {eingabe}, Erwartet {erwartet}, Bekommen {ergebnis}"
        return "✅ Alle Tests bestanden!"
    except Exception as e:
        return f"❌ Fehler:\n{traceback.format_exc()}"

def code_agent():
    print("📘 Aufgabe:", aufgabe_verstehen())
    code = code_generieren()
    print("\n🧾 Generierter Code:\n", code)

    tests = [(10, 7), (20, 19), (3, 2), (2, None)]
    print("\n🧪 Teste Code...")
    ergebnis = code_ausfuehren(code, tests)
    print(ergebnis)

if __name__ == "__main__":
    code_agent()
```

---

### 🧠 Was passiert hier?

* Der Agent "versteht" eine Aufgabe (fest codiert, aber auch dynamisch möglich)
* Er **generiert Python-Code**
* Führt diesen Code mit **Tests** aus
* Erkennt Fehler und gibt Feedback

---

## 💡 Erweiterungsideen

Du kannst das Beispiel ausbauen zu einem echten Code-Agenten mit:

* **LLM-Integration**: GPT ruft `code_generieren()` und `debugge_code()` auf Basis des Fehlers
* **Feedbackschleife**: Wenn Tests fehlschlagen, wird der Code automatisch verbessert
* **GUI oder Chat-Interface**: Der Nutzer gibt die Aufgabe als Text ein
* **Tool-Unterstützung**: Einsatz von `pytest`, `black`, `mypy`, usw.

---

Möchtest du ein Beispiel mit einem echten **LLM-gesteuerten Debug-Loop**, oder soll ich zeigen, wie man dies mit `openai` oder `transformers` integriert?

----

Super! Hier kommt ein erweitertes Beispiel für einen echten **Code Agent mit LLM-gestütztem Debugging-Loop**, basierend auf der `openai`-API. Dabei schreibt der LLM Code, führt Tests durch, und **debuggt automatisch**, falls Fehler auftreten – eine Art selbst-verbessernder Mini-Copilot.

---

## 🧠 Ziel:

> Ein LLM-generierter Codeagent, der:
> ✅ Aufgabe versteht → ✅ Code schreibt → ✅ Tests ausführt → 🔁 Fehler erkennt → 🔁 automatisch verbessert

---

## 🔧 Voraussetzungen

1. Installiere `openai`:

```bash
pip install openai
```

2. Setze deine OpenAI-API:

```python
import openai
openai.api_key = "DEIN_API_KEY"
```

---

## 🧪 Beispiel-Workflow mit `openai.ChatCompletion`

```python
import openai
import traceback

openai.api_key = "DEIN_API_KEY"  # Setze hier deinen echten Key

AUFGABE = "Schreibe eine Python-Funktion `ist_palindrom(s: str) -> bool`, die prüft, ob ein String ein Palindrom ist."

TESTFÄLLE = [
    ("anna", True),
    ("otto", True),
    ("python", False),
    ("Lagerregal", True),
    ("Haus", False),
]


def frage_llm(aufgabe, fehler=None):
    system_msg = "Du bist ein hilfreicher Programmierassistent."
    user_msg = aufgabe if not fehler else f"{aufgabe}\nDer folgende Fehler trat auf:\n{fehler}\nBitte verbessere den Code."

    antwort = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
    )
    return antwort.choices[0].message.content.strip()


def teste_code(code_str):
    scope = {}
    try:
        exec(code_str, scope)
        func = scope["ist_palindrom"]
        for eingabe, erwartet in TESTFÄLLE:
            ergebnis = func(eingabe.lower())  # Normalisieren
            assert ergebnis == erwartet, f"Fehler: {eingabe} → Erwartet {erwartet}, Bekommen {ergebnis}"
        return True, "✅ Alle Tests bestanden!"
    except Exception as e:
        return False, traceback.format_exc()


def code_agent():
    max_iterationen = 3
    code = frage_llm(AUFGABE)
    print("🧾 Generierter Code:\n", code)

    for i in range(max_iterationen):
        print(f"\n🔁 Iteration {i+1} – Tests laufen...")
        success, result = teste_code(code)
        print(result)

        if success:
            break
        else:
            print("🔧 LLM wird zur Verbesserung aufgerufen...")
            code = frage_llm(AUFGABE, result)
            print("\n🆕 Verbesserter Code:\n", code)


if __name__ == "__main__":
    code_agent()
```

---

## 🧠 Was passiert hier?

1. 📝 Der LLM schreibt initial den Code
2. 🧪 Der Agent testet den Code gegen definierte Fälle
3. 🐞 Wenn Fehler auftreten, wird der Stacktrace an das LLM zurückgegeben
4. 🔁 Der LLM generiert daraufhin eine verbesserte Version
5. ✅ Das wiederholt sich bis zum Erfolg oder zur maximalen Iteration

---

## 📦 Beispielausgabe

```text
🧾 Generierter Code:
def ist_palindrom(s: str) -> bool:
    return s == s[::-1]

🔁 Iteration 1 – Tests laufen...
Fehler: Lagerregal → Erwartet True, Bekommen False
🔧 LLM wird zur Verbesserung aufgerufen...

🆕 Verbesserter Code:
def ist_palindrom(s: str) -> bool:
    s = s.lower()
    return s == s[::-1]

✅ Alle Tests bestanden!
```

---

## 🧩 Was du daraus machen kannst:

* Einen **Code Tutor Bot**, der User-Aufgaben bewertet und automatisch Feedback gibt
* Einen **Autocoder für Interviews oder Wettbewerbe**
* Automatisches Refactoring, Linting, Typing, Docstring-Generator
* Integration mit GitHub Copilot oder VS Code

---

Möchtest du eine **GUI** oder **Web-Oberfläche** daraus bauen? Oder soll ich das Beispiel auf eine **komplexere Programmieraufgabe** erweitern (z. B. ein Spiel, Datenanalyse oder Webserver)?
