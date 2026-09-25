# Akıllı Sinema Bilet & Salon Yönetim Sistemi
# Terminal üzerinden çalışan sinema yönetim uygulaması:
# film listeleme, koltuk seçimi, bilet satışı/iptali,
# doluluk oranı, günlük satış raporu ve yönetici paneli.

# --- Veriler ---

filmler = [
    {"ad": "Interstellar", "tur": "Bilim Kurgu", "sure": 169, "fiyat": 180, "salon": 1, "yas_siniri": 13},
    {"ad": "Dune", "tur": "Bilim Kurgu", "sure": 155, "fiyat": 200, "salon": 2, "yas_siniri": 13},
    {"ad": "The Batman", "tur": "Aksiyon", "sure": 176, "fiyat": 190, "salon": 3, "yas_siniri": 16},
    {"ad": "Shrek", "tur": "Animasyon", "sure": 90, "fiyat": 150, "salon": 4, "yas_siniri": 7},
]

# Her salonda A1-D5 arası 20 koltuk var, başlangıçta hepsi boş (False)
salonlar = {}
for film in filmler:
    koltuklar = {}
    for harf in ["A", "B", "C", "D"]:
        for numara in range(1, 6):
            koltuklar[harf + str(numara)] = False
    salonlar[film["salon"]] = koltuklar

satilan_biletler = []   # her satış bir sözlük olarak eklenir
bilet_sayaci = 1        # her satışta 1 artar
YONETICI_SIFRESI = "1234"


# --- Fonksiyonlar ---

def filmleri_goster():
    print("\n====== FİLMLER ======")
    sira = 1
    for film in filmler:
        print(str(sira) + ". " + film["ad"])
        print("   Tür: " + film["tur"])
        print("   Süre: " + str(film["sure"]) + " dakika")
        print("   Fiyat: " + str(film["fiyat"]) + " TL")
        print("   Salon: " + str(film["salon"]))
        print("   Yaş sınırı: " + str(film["yas_siniri"]) + "+")
        print("-------------------")
        sira += 1


def film_sec():
    filmleri_goster()
    secim = input("Film numarası: ")

    if not secim.isdigit():
        print("Geçersiz film seçimi.")
        return None

    secim = int(secim)
    if secim < 1 or secim > len(filmler):
        print("Geçersiz film seçimi.")
        return None

    return filmler[secim - 1]


def koltuklari_goster(salon_no):
    print("\nSALON " + str(salon_no))
    koltuklar = salonlar[salon_no]
    for koltuk in koltuklar:
        if koltuklar[koltuk]:
            durum = "[DOLU]"
        else:
            durum = "[BOŞ]"
        print(koltuk + " " + durum)
        if koltuk.endswith("5"):
            print()


def indirim_hesapla(fiyat, yas, ogrenci_mi):
    # Öğrenci ve yaş indirimi aynı anda uygulanmaz.
    # Önce yaş indirimine bakılır, yoksa öğrenci indirimi denenir.
    if yas <= 12:
        indirim = fiyat * 0.50
        aciklama = "Çocuk indirimi (%50)"
    elif yas >= 65:
        indirim = fiyat * 0.30
        aciklama = "65+ indirimi (%30)"
    elif ogrenci_mi:
        indirim = fiyat * 0.20
        aciklama = "Öğrenci indirimi (%20)"
    else:
        indirim = 0
        aciklama = "İndirim yok"

    odenecek = fiyat - indirim
    return odenecek, aciklama


def bilet_sat():
    global bilet_sayaci

    film = film_sec()
    if film is None:
        return

    yas = input("Yaşınız: ")
    if not yas.isdigit():
        print("Geçersiz yaş girdiniz.")
        return
    yas = int(yas)

    if yas < film["yas_siniri"]:
        print("Bu filmi izlemek için yaşınız yeterli değil.")
        return

    ogrenci = input("Öğrenci misiniz? E/H: ").upper()
    ogrenci_mi = ogrenci == "E"

    adet = input("Kaç bilet almak istiyorsunuz? ")
    if not adet.isdigit() or int(adet) < 1:
        print("Geçersiz bilet adedi.")
        return
    adet = int(adet)

    salon_no = film["salon"]
    koltuklar = salonlar[salon_no]
    koltuklari_goster(salon_no)

    alinan = 0
    while alinan < adet:
        koltuk = input(str(alinan + 1) + ". koltuk: ").upper()

        if koltuk not in koltuklar:
            print("Böyle bir koltuk yok. Başka bir koltuk seçin:")
            continue

        if koltuklar[koltuk]:
            print(koltuk + " dolu. Başka bir koltuk seçin:")
            continue

        # Koltuk boş, satışı gerçekleştir
        koltuklar[koltuk] = True
        odenecek, aciklama = indirim_hesapla(film["fiyat"], yas, ogrenci_mi)

        bilet = {
            "no": bilet_sayaci,
            "film": film["ad"],
            "koltuk": koltuk,
            "fiyat": odenecek,
            "yas": yas,
        }
        satilan_biletler.append(bilet)

        print(koltuk + " koltuğu rezerve edildi.")
        print("Bilet No: " + str(bilet_sayaci))
        print("Normal fiyat: " + str(film["fiyat"]) + " TL")
        print(aciklama)
        print("Ödenecek: " + str(odenecek) + " TL")

        bilet_sayaci += 1
        alinan += 1


def bilet_iptal():
    numara = input("Bilet numarası: ")
    if not numara.isdigit():
        print("Geçersiz bilet numarası.")
        return
    numara = int(numara)

    for bilet in satilan_biletler:
        if bilet["no"] == numara:
            print("Bilet bulundu.")
            print("Film: " + bilet["film"])
            print("Koltuk: " + bilet["koltuk"])
            print("Tutar: " + str(bilet["fiyat"]) + " TL")

            # Koltuğu tekrar boş yap
            for film in filmler:
                if film["ad"] == bilet["film"]:
                    salonlar[film["salon"]][bilet["koltuk"]] = False

            satilan_biletler.remove(bilet)
            print("Bilet iptal edildi.")
            return

    print("Böyle bir bilet bulunamadı.")


def salon_doluluk_goster():
    for salon_no in salonlar:
        koltuklar = salonlar[salon_no]

        dolu_sayisi = 0
        bos_sayisi = 0
        for koltuk in koltuklar:
            if koltuklar[koltuk]:
                dolu_sayisi += 1
            else:
                bos_sayisi += 1

        toplam = dolu_sayisi + bos_sayisi
        doluluk = dolu_sayisi / toplam * 100

        print("\nSalon " + str(salon_no))
        print("Toplam Koltuk: " + str(toplam))
        print("Dolu: " + str(dolu_sayisi))
        print("Boş: " + str(bos_sayisi))
        print("Doluluk: %" + str(int(doluluk)))


def satis_raporu():
    print("\n====== GÜNLÜK RAPOR ======")
    print("Satılan Bilet: " + str(len(satilan_biletler)))

    toplam_kazanc = 0
    for bilet in satilan_biletler:
        toplam_kazanc += bilet["fiyat"]

    print("Toplam Kazanç: " + str(toplam_kazanc) + " TL")

    print("\nFilm Satışları:")
    en_populer = ""
    en_cok_satis = 0
    for film in filmler:
        satis = 0
        for bilet in satilan_biletler:
            if bilet["film"] == film["ad"]:
                satis += 1
        print(film["ad"] + " : " + str(satis))

        if satis > en_cok_satis:
            en_cok_satis = satis
            en_populer = film["ad"]

    if en_cok_satis > 0:
        print("\nEn popüler film: " + en_populer)
        print(str(en_cok_satis) + " bilet satıldı.")


def satislari_goster():
    if len(satilan_biletler) == 0:
        print("Henüz satış yapılmadı.")
        return

    for bilet in satilan_biletler:
        print("\nBilet #" + str(bilet["no"]))
        print("Film: " + bilet["film"])
        print("Koltuk: " + bilet["koltuk"])
        print("Tutar: " + str(bilet["fiyat"]) + " TL")
        print("----------------")


def film_fiyati_degistir():
    film = film_sec()
    if film is None:
        return

    print("Film: " + film["ad"])
    print("Mevcut fiyat: " + str(film["fiyat"]) + " TL")

    yeni_fiyat = input("Yeni fiyat: ")
    if not yeni_fiyat.isdigit():
        print("Geçersiz fiyat girdiniz.")
        return

    # Daha önce satılmış biletlerin fiyatı değişmez,
    # sadece bundan sonraki satışlarda yeni fiyat kullanılır.
    film["fiyat"] = int(yeni_fiyat)
    print("Yeni bilet fiyatı: " + str(film["fiyat"]) + " TL")


def yonetici_paneli():
    sifre = input("Yönetici şifresi: ")
    if sifre != YONETICI_SIFRESI:
        print("Yetkisiz giriş.")
        return

    while True:
        print("\n====== YÖNETİCİ ======")
        print("1 - Satışları Görüntüle")
        print("2 - Film Fiyatını Değiştir")
        print("3 - Salon Durumunu Görüntüle")
        print("0 - Geri Dön")

        secim = input("Seçiminiz: ")

        if secim == "1":
            satislari_goster()
        elif secim == "2":
            film_fiyati_degistir()
        elif secim == "3":
            salon_doluluk_goster()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")


def ana_menu():
    print("Akıllı Sinema Bilet & Salon Yönetim Sistemine Hoş Geldiniz")

    while True:
        print("\n====== ANA MENÜ ======")
        print("1 - Filmleri Görüntüle")
        print("2 - Bilet Satın Al")
        print("3 - Bilet İptal Et")
        print("4 - Salon Doluluk Durumu")
        print("5 - Günlük Satış Raporu")
        print("6 - Yönetici Paneli")
        print("0 - Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            filmleri_goster()
        elif secim == "2":
            bilet_sat()
        elif secim == "3":
            bilet_iptal()
        elif secim == "4":
            salon_doluluk_goster()
        elif secim == "5":
            satis_raporu()
        elif secim == "6":
            yonetici_paneli()
        elif secim == "0":
            print("Programdan çıkılıyor. İyi günler!")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")


ana_menu()
