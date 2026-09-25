# Akıllı Sinema Bilet & Salon Yönetim Sistemi

Python ile yazılmış, terminal üzerinden çalışan orta seviye bir sinema yönetim
uygulaması. Filmleri, salonlardaki koltukları, bilet satışlarını ve günlük
kazancı yönetir.

## Özellikler

- Film listeleme (tür, süre, fiyat, salon, yaş sınırı)
- Koltuk haritası görüntüleme (her salonda A1-D5 arası 20 koltuk)
- Bilet satışı: koltuk seçimi, dolu koltuk kontrolü, çoklu bilet alma
- Yaş sınırı kontrolü (film izleme yaşı tutmuyorsa satış yapılmaz)
- İndirim sistemi: çocuk %50, 65+ %30, öğrenci %20 (aynı anda tek indirim)
- Bilet iptali (koltuk tekrar boşa düşer)
- Salon doluluk oranı hesaplama
- Günlük satış raporu ve en popüler film istatistiği
- Şifreli yönetici paneli: satışları görüntüleme, film fiyatı değiştirme

## Kullanılan Konular

Fonksiyonlar, sözlük ve liste veri yapıları, while/for döngüleri, iç içe
döngüler, koşullar, global değişkenler, kullanıcı girdisi doğrulama.

## Çalıştırma

```
python sinema_sistemi.py
```

Yönetici paneli varsayılan şifresi: `1234`
