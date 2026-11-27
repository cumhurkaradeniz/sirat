<div align="center">
  <img src="icon.png" alt="Sirat Logo" width="96" height="96">
  <h1>☪ Sirat — Universal Islamic Companion for Linux</h1>
  <p><b>Linux masaüstü sistemleri için hafif, modern, çevrimdışı destekli ve açık kaynaklı İslami yaşam rehberi.</b></p>
  <p><i>A lightweight, modern, offline-ready, and open-source Islamic companion application for Linux desktops.</i></p>
</div>

---

## ✨ Özellikler / Features

* **🕌 Namaz Vakitleri & Canlı Geri Sayım (Prayer Times):** Otomatik konum algılama veya manuel şehir seçimi, vakit bildirimleri, özelleştirilebilir ezan/zil sesleri ve sistem tepsisi (System Tray) desteği.
* **📅 Diyanet Takvim Yaprağı (Islamic Calendar Leaf):** Miladi, Hicri ve Rûmî tarih bilgileriyle birlikte her güne özel Günün Ayeti ve Günün Hadisi.
* **📖 Kur'an-ı Kerim & Sesli Tilavet (Quran Reader & Audio):** 114 surenin tamamı, Arapça metin ve Türkçe/İngilizce meal desteği, 9 farklı hafız seçeneği ve 4 farklı oynatıcı görünüm modu.
* **📜 Sahih-i Buhârî Hadis Kitaplığı (Hadith Collection):** Hızlı arama özellikli Türkçe ve İngilizce hadis arşivi.
* **🌙 Dini Günler & Geceler (Islamic Days):** Kandiller, bayramlar, üç aylar ve mübarek geceler için geri sayım ve fazilet rehberi.
* **🧭 Namaz Rehberi (Prayer Guide):** Adım adım görsel anlatımlı abdest ve namaz kılavuzları.
* **📿 Dijital Tesbihat (Digital Dhikr Counter):** Özelleştirilebilir hedefler, ilerleme takibi ve kalıcı sayaç hafızası.
* **🎨 Tam Kişiselleştirme (Customization):** Açık, Koyu ve Sistem Otomatik tema desteği; dinamik yazı boyutu (`A-` / `A+`) ve anlık Türkçe/İngilizce (`TR` / `EN`) dil geçişi.

---

## 📦 Kurulum / Installation (Debian / Ubuntu / Mint / CutefishOS)

Hazır `.deb` paketini indirip tek komutla sisteminize kurabilirsiniz:

```bash
sudo apt install ./sirat_1.1.0_all.deb
```

### Kaynak Koddan Çalıştırma / Run from Source

```bash
git clone https://github.com
cd sirat
python3 app.py
```

### Paket Derleme / Build `.deb` Package

```bash
chmod +x build-deb.sh
./build-deb.sh
```

---

## 🛠️ Gereksinimler / Dependencies

* `python3`
* `python3-pyqt5` & `python3-pyqt5.qtmultimedia`
* `libqt5multimedia5-plugins`
* `libnotify-bin`

---

## 📄 Lisans / License

Bu proje **GNU General Public License v3.0 (GPL-3.0)** kapsamında özgür ve açık kaynaklı olarak lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.

**Geliştirici / Developer:** Cumhur Karadeniz
