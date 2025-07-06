#Odev 1

#open_weather.json dosyasini olustur
#open_weather.json dosyasiyla calisan hava durumu
#liste icindeki dictionary de her sehrin id, isim, enlem, boylam, ulke bilgisi var
#Yanlis sehir ismi girdin, Devam icin E ya da cikis icin ESC: 
#E ya da ESC demezsen: Yanlis Tercih
#E dersen devam
#sehir dogru ise hava durumunu goster, break
#ESC dersen break
#sehir isimleri input olarak ascii
#sehir ID'si ile
#https://api.openweathermap.org/data/2.5/weather?id={city id}&appid={API key}
#sonra enlem boylama gore yap:
#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

import requests
import json

API_KEY = "97afb3c84a9f644b9bd5b9586ea5497a"

while True:
    sehir_input = input("Lütfen şehir ismini giriniz (Çıkış için ESC): ").strip()
    if sehir_input.lower() == "esc":
        print("Çıkış yapılıyor...")
        break

    with open("open_weather.json", "r", encoding="utf-8") as f:
        sehirler = json.load(f)

    # Şehri bul
    bulunan_sehir = None
    for item in sehirler:
        if item["name"].lower() == sehir_input.lower():
            bulunan_sehir = item
            break

    if bulunan_sehir:
        # Sehir bulundu → API'yi çağır
        city_id = bulunan_sehir["id"]
        url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric&lang=tr"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ {data['name']} için hava durumu:")
            print(f"🌡️ Sıcaklık: {data['main']['temp']}°C")
            print(f"🌥️ Hava: {data['weather'][0]['description']}")
            print(f"💧 Nem: {data['main']['humidity']}%")
            print(f"🌬️ Rüzgar: {data['wind']['speed']} m/s\n")
            break  # Sehir bulunduğu için döngüden çıkıyoruz
        else:
            print("❌ API'den veri alınamadı. Kod:", response.status_code)
            break

    else:
        print("❌ Şehir bulunamadı.")
        tercih = input("Devam etmek için 'E', çıkmak için 'ESC' yazın: ").strip().lower()
        if tercih == "esc":
            print("Çıkış yapılıyor...")
            break
        elif tercih == "e":
            continue
        else:
            print("❌ Geçersiz giriş. Çıkılıyor...")
            break

