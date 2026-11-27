<div align="center">
  <img src="icon.png" alt="Sirat Logo" width="96" height="96">
  <h1>☪ Sirat — Universal Islamic Companion for Linux (v1.1.0)</h1>
  <p><b>A modern, offline-ready, open-source Islamic companion application for Linux desktops with full 10-language support.</b></p>
  <p><i>Linux masaüstü sistemleri için 10 dil destekli, modern, çevrimdışı çalışabilen açık kaynaklı İslami yaşam rehberi.</i></p>
</div>

---

## 🌍 Supported Languages / Desteklenen Diller (10 Languages)

The interface and content automatically detect your OS language or can be switched instantly from the top menu:  
*Uygulama arayüzü ve içerikleri işletim sistemi dilini otomatik algılar veya üst menüden anlık olarak değiştirilebilir:*

* **TR** • Türkçe
* **EN** • English
* **FR** • Français
* **ES** • Español
* **PT** • Português
* **ID** • Bahasa Indonesia
* **RU** • Русский
* **ZH** • 中文
* **AR** • العربية (RTL)
* **UR** • اردو (RTL)

---

## ✨ Features / Özellikler

* **🕌 Prayer Times & 3-Tier Location Picker / Namaz Vakitleri & Konum Seçici:**  
  Automatic location detection or cascading dropdown selection (**Country → City/Province → District**), live countdown, prayer alerts, 4 notification chimes, and System Tray support.  
  *Otomatik konum algılama veya 3 kademeli (**Ülke → İl/Şehir → İlçe**) açılır liste seçimi, canlı geri sayım, vakit bildirimleri, 4 farklı bildirim sesi ve sistem tepsisi desteği.*

* **📅 Islamic Calendar Leaf / Takvim Yaprağı:**  
  Daily Gregorian and Hijri dates paired with a daily Quran verse and Hadith.  
  *Miladi ve Hicri tarih bilgileriyle birlikte her güne özel Günün Ayeti ve Günün Hadisi.*

* **📖 Holy Quran & Audio Recitation / Kur'an-ı Kerim & Sesli Tilavet:**  
  All 114 Surahs, Arabic script with multilingual translations, 8 sorting filters (Mushaf order, Revelation order, Verse count, Alphabetical), 9 reciters, and 4 player layouts.  
  *114 surenin tamamı, Arapça metin ve çoklu dil meal desteği, 8 farklı sıralama filtresi (Mushaf sırası, İniş sırası, Ayet sayısı, Alfabetik), 9 hafız seçeneği ve 4 oynatıcı görünüm modu.*

* **📜 Sahih al-Bukhari Hadith Library / Sahih-i Buhârî Hadis Kitaplığı:**  
  Multilingual Hadith archive with chapter filtering and fast keyword search.  
  *Bölüm filtreli ve hızlı arama destekli çok dilli hadis arşivi.*

* **🌙 Islamic Days & Nights / Dini Günler & Geceler:**  
  Countdown and virtue guide for Eid al-Fitr, Eid al-Adha, Ramadan, Three Holy Months, and blessed nights.  
  *Kandiller, bayramlar, üç aylar ve mübarek geceler için geri sayım ve fazilet rehberi.*

* **🧭 Visual Prayer Guide / Görsel Namaz Rehberi:**  
  Step-by-step illustrated guides for Wudu (ablution) and daily prayers.  
  *Adım adım görsel anlatımlı abdest ve namaz kılavuzları.*

* **📿 Digital Tasbih / Dijital Tesbihat:**  
  Preset and custom Dhikr list, target progress bar, persistent counter memory, and total counter reset.  
  *Hazır ve özel zikir listesi, hedef ilerleme çubuğu, kalıcı sayaç hafızası ve toplam zikir sıfırlama.*

* **🎨 Full Customization / Tam Kişiselleştirme:**  
  Light, Dark, and System Auto themes; dynamic font sizing (`A-` / `A+`), and centralized `locales/*.json` translation architecture.  
  *Açık, Koyu ve Sistem Otomatik tema desteği; dinamik yazı boyutu (`A-` / `A+`) ve merkezi `locales/*.json` dil mimarisi.*

---

## 📦 Installation / Kurulum

### 1. Universal Linux Installer / Evrensel Linux Kurulumu (Ubuntu, Debian, Fedora, Arch, openSUSE)

```bash
git clone https://github.com
cd sirat
bash install.sh
```

To uninstall / *Kaldırmak için:*
```bash
bash uninstall.sh
```

### 2. Debian / Ubuntu / Mint / CutefishOS (`.deb` Package)

Download `sirat_1.1.0_all.deb` from the [Releases](https://github.com) page and install:  
*[Releases](https://github.com) sayfasından `sirat_1.1.0_all.deb` paketini indirip kurun:*

```bash
sudo apt install ./sirat_1.1.0_all.deb
```

### 3. Run from Source / Kaynak Koddan Çalıştırma

```bash
python3 app.py
```

---

## 🛠️ Dependencies / Gereksinimler

* `python3`
* `python3-pyqt5` & `python3-pyqt5.qtmultimedia`
* `libqt5multimedia5-plugins`
* `libnotify-bin`

---

## 📄 License / Lisans

Licensed under the **GNU General Public License v3.0 (GPL-3.0)**. See [LICENSE](LICENSE) for details.  
*Bu proje **GNU General Public License v3.0 (GPL-3.0)** kapsamında özgür ve açık kaynaklı olarak lisanslanmıştır.*

**Developer / Geliştirici:** [Cumhur Karadeniz](https://github.com)
