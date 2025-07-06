import requests
import json

API_KEY = "97afb3c84a9f644b9bd5b9586ea5497a"

while True:
    sehir_input = input("Şehir ismini giriniz: ") 
    with open("open_weather.json", "r", encoding="utf-8") as f:
        sehirler = json.load(f)

    bulunan_sehir = None
    for sehir in sehirler:
        if sehir["name"].lower() == sehir_input.lower():
            bulunan_sehir = sehir
            break

    if bulunan_sehir:
        city_id = bulunan_sehir["id"]
        url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric&lang=tr"
        try:
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
                print(f"\n {data['name']} için hava durumu:")
                print(f" Sıcaklık: {data['main']['temp']}°C")
                print(f" Hava: {data['weather'][0]['description']}")
                print(f" Nem: {data['main']['humidity']}%")
                print(f" Rüzgar: {data['wind']['speed']} m/s\n")
                break  # şehir bulundu ve veri başarılı, döngü sonlandır
            else:
                print(f"API Hatası: {response.status_code}")
        except Exception as e:
            print(f"Hava durumu alınamadı. Hata: {e}")
    else:
        print("Şehir bulunamadı.")
    
    while True:
        secim = input("Devam etmek için E, çıkmak için ESC tuşuna basın: ").strip().upper()
        if secim == "ESC":
            print("Çıkılıyor...")
            flag = True
            break
        elif secim == "E":
            flag = False
            break
        else:
            print("Yanlış tercih. Lütfen E ya da ESC tuşuna basın.")
            continue

    if flag:
        break