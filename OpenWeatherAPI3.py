import requests
import json

API_KEY = "97afb3c84a9f644b9bd5b9586ea5497a"

while True:
    try:
        sehir_enlem = float(input("Şehir enlem bilgisini giriniz: "))
        sehir_boylam = float(input("Şehir boylam bilgisini giriniz: "))
    except ValueError:
        print("Lütfen geçerli sayısal bir değer girin!")
        continue

    with open("open_weather.json", "r", encoding="utf-8") as f:
        sehirler = json.load(f)

    lat = lon = None
    for sehir in sehirler:
        if sehir["coord"]["lat"] == sehir_enlem and sehir["coord"]["lon"] == sehir_boylam:
            lat = sehir["coord"]["lat"]
            lon = sehir["coord"]["lon"]
            break

    if lat is not None and lon is not None:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=tr"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"\n {data['name']} için hava durumu:")
                print(f"Sıcaklık: {data['main']['temp']}°C")
                print(f"Hava: {data['weather'][0]['description']}")
                print(f"Nem: {data['main']['humidity']}%")
                print(f"Rüzgar: {data['wind']['speed']} m/s\n")
                break
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

    if flag:
        break