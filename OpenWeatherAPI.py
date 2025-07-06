import requests
import json

api_key = "97afb3c84a9f644b9bd5b9586ea5497a"
sehir_listesi = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana"]

veriler = []

for sehir in sehir_listesi:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bilgi = {
            "sehir": data['name'],
            "sicaklik": data['main']['temp'],
            "hava": data['weather'][0]['description'],
            "nem": data['main']['humidity'],
            "ulke": data['sys']['country'],
            "id": data['id'],
            "enlem": data['coord']['lat'],
            "boylam": data['coord']['lon']
        }
        veriler.append(bilgi)
    else:
        print(f"❌ {sehir} için veri alınamadı. Hata: {response.status_code}")

# JSON dosyasına yaz
with open("sehirler.json", "w", encoding="utf-8") as f:
    json.dump(veriler, f, ensure_ascii=False, indent=4)

print("✅ sehirler.json dosyasına yazıldı.")