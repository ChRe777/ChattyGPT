Hier ist ein erweitertes **Python‑Beispiel für Multi‑Step‑Planung**, das reale API‑Abfragen durchführt: einerseits Flüge über das (veraltete) Skyscanner‑SDK, andererseits Hotels per Scraping. Damit lässt sich gut zeigen, wie ein LLM mehrere Schritte orchestriert:

---

## ✈️ Schritt 1: Flugdaten mit Skyscanner‑SDK abrufen

```python
from skyscanner.skyscanner import Flights

def suche_fluege(api_key, origin, dest, outbound, inbound, adults=1):
    flights = Flights(api_key)
    res = flights.get_result(
        country='DE', currency='EUR', locale='de-DE',
        originplace=f'{origin}-sky',
        destinationplace=f'{dest}-sky',
        outbounddate=outbound,
        inbounddate=inbound,
        adults=adults
    ).parsed
    # Beispiel: günstigster Preis
    quote = min(res.Quotes, key=lambda q: q.MinPrice) if res.Quotes else None
    return quote
```

Das SDK liefert Flugpreise live – du benötigst allerdings einen API‑Key von Skyscanner, der jedoch laut offizieller Info veraltet ist und möglicherweise nicht mehr funktioniert ([pypi.org][1], [github.com][2]).

---

## 🏨 Schritt 2: Unterkunft per Scraping holen (Booking.com)

**Variante A: Web‑Scraping mit Selenium**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def suche_hotels_selenium(url):
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Dismiss']"))
        )
        btn.click()
    except:
        pass
    hotels = driver.find_elements(By.CSS_SELECTOR, ".sr_property_block")
    results = []
    for h in hotels[:5]:
        name = h.find_element(By.CSS_SELECTOR, ".sr-hotel__name").text.strip()
        price = h.find_element(By.CSS_SELECTOR, ".bui-price-display__value").text.strip()
        results.append((name, price))
    driver.quit()
    return results
```

**Variante B: API‑Scraping mit externem Service**

```python
import requests

def booking_preise_mit_makcorps(hotel_id, checkin, checkout, api_key):
    url = "https://api.makcorps.com/booking"
    params = {
        "hotelid": hotel_id, "checkin": checkin, "checkout": checkout,
        "currency": "EUR", "adults": 2, "rooms": 1,
        "api_key": api_key
    }
    resp = requests.get(url, params=params)
    return resp.json() if resp.status_code == 200 else None
```

Makcorps bietet eine API für Booking‑Preise, ideal für automatisierte Mehrschritte ([makcorps.com][3]).

---

## 🤖 Schritt 3: Gesamtablauf planen & orchestrieren

Hier ein orchestrierendes Beispiel, wie man beide Schritte in einen Workflow integriert:

```python
def reiseplanung(api_flight_key, api_hotel_key, origin, dest, out, back, hotel_id):
    steps = {}
    steps['flug'] = suche_fluege(api_flight_key, origin, dest, out, back)
    steps['hotelscrape'] = suche_hotels_selenium(
        f"https://www.booking.com/searchresults.de.html?ss={dest}&checkin_year_month_monthday={out}&checkout_year_month_monthday={back}"
    )
    steps['hotelpreise'] = booking_preise_mit_makcorps(hotel_id, out, back, api_hotel_key)
    return steps

if __name__ == "__main__":
    plan = reiseplanung(
        api_flight_key="DEIN_SKYSCANNER_KEY",
        api_hotel_key="DEIN_MAKCORPS_KEY",
        origin="VIE", dest="FRA",
        out="2025-08-01", back="2025-08-10",
        hotel_id="some-booking-id"
    )
    print(plan)
```

---

## 🧠 Warum das ein gutes **Multi‑Step Planning** ist:

1. **Ziel verstehen**: Nutzer will Flug + Hotel buchen
2. **Aufgaben zerlegen**: 	– Flug suchen
   – Hotel‑Infos per Web
   – Hotel‑Preise via API
3. **Werkzeuge orchestrieren**: SDK für Flüge, Selenium/requests für Hotels
4. **Ergebnisse sammeln & zusammenfassen**

Ein echtes LLM könnte noch viel weiter gehen:

* Dynamisch auf Nutzerfeedback reagieren („mehr Budget?“)
* Preisvergleiche in Echtzeit durchführen
* Buchung abschließen (via API)
* Reiseunterlagen zusammenstellen, Wetter prüfen, Packliste generieren

---

Möchtest du ein angepasstes Beispiel, z. B. mit OpenWeather‑API fürs Wetter oder einem interaktiven Chat‑Flow, bei dem ein LLM den Schritt‑Verlauf steuert?

[1]: https://pypi.org/project/skyscanner/?utm_source=chatgpt.com "skyscanner·PyPI"
[2]: https://github.com/Skyscanner/skyscanner-python-sdk?utm_source=chatgpt.com "GitHub - Skyscanner/skyscanner-python-sdk: Skyscanner Python SDK"
[3]: https://www.makcorps.com/blog/extract-booking-com-data-with-python-and-makcorps-api/?utm_source=chatgpt.com "Extract booking.com data with Python and Makcorps Hotel API"
