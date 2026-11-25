import os, locale

def detect_os_lang():
    lang = os.environ.get("LANG", "") or (locale.getdefaultlocale() or "")
    return "tr" if lang.lower().startswith("tr") else "en"

STRINGS = {
    "tr": {
        "nav": ["Namaz Vakitleri", "Kur'an-ı Kerim", "Hadis Kitaplığı", "Dini Günler", "Namaz Rehberi", "Hakkında"],
        "city_ph": "Şehir (Örn: Sungurlu)", "country_ph": "Ülke (Örn: Turkey)", "upd_btn": "Konumu Güncelle",
        "next_fmt": "{city} • {prayer} vaktine kalan süre:", "wait_next": "{city} • Yarınki İmsak bekleniyor",
        "err_time": "Vakitler hesaplanamadı", "prayers": ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"],
        "surah_ph": "Sure ara...", "play": "▶ Dinle", "pause": "⏸ Duraklat", "resume": "▶ Devam Et",
        "hadith_ph": "Hadislerde konu veya kelime ara...", "no_hadith": "Aramanızla eşleşen hadis bulunamadı.",
        "source": "Kaynak", "days_left": "({d} gün kaldı)", "today": "(Bugün)", "passed": "(Geçti)",
        "theme_lbl": "Tema:", "themes": ["Otomatik", "Açık", "Koyu"], "lang_lbl": "Dil:", "font_lbl": "Yazı:"
    },
    "en": {
        "nav": ["Prayer Times", "Holy Quran", "Hadith Library", "Islamic Days", "Prayer Guide", "About"],
        "city_ph": "City (e.g. London)", "country_ph": "Country (e.g. UK)", "upd_btn": "Update Location",
        "next_fmt": "{city} • Time left until {prayer}:", "wait_next": "{city} • Waiting for tomorrow's Fajr",
        "err_time": "Could not calculate times", "prayers": ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"],
        "surah_ph": "Search Surah...", "play": "▶ Listen", "pause": "⏸ Pause", "resume": "▶ Resume",
        "hadith_ph": "Search Hadiths by topic or keyword...", "no_hadith": "No matching Hadiths found.",
        "source": "Source", "days_left": "({d} days left)", "today": "(Today)", "passed": "(Passed)",
        "theme_lbl": "Theme:", "themes": ["Auto", "Light", "Dark"], "lang_lbl": "Lang:", "font_lbl": "Font:"
    }
}
