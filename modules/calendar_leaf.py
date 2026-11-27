import os, json
from datetime import date
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTextBrowser
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from modules.i18n import get_bundle

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

CAL_I18N = {
    "tr": (["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"],
           ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],
           "DİYANET TAKVİM YAPRAĞI", "📖 Günün Ayeti", "📜 Günün Hadisi", "Yılın {d}. Günü", "ltr"),
    "en": (["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
           ["January","February","March","April","May","June","July","August","September","October","November","December"],
           "ISLAMIC CALENDAR LEAF", "📖 Verse of the Day", "📜 Hadith of the Day", "Day {d} of the Year", "ltr"),
    "fr": (["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"],
           ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"],
           "FEUILLET CALENDRIER ISLAMIQUE", "📖 Verset du Jour", "📜 Hadith du Jour", "Jour {d} de l'année", "ltr"),
    "es": (["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],
           ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
           "HOJA DE CALENDARIO ISLÁMICO", "📖 Versículo del Día", "📜 Hadiz del Día", "Día {d} del año", "ltr"),
    "pt": (["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"],
           ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],
           "FOLHA DO CALENDÁRIO ISLÂMICO", "📖 Versículo do Dia", "📜 Hadith do Dia", "Dia {d} do ano", "ltr"),
    "id": (["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"],
           ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"],
           "LEMBAR KALENDER ISLAM", "📖 Ayat Hari Ini", "📜 Hadis Hari Ini", "Hari ke-{d} Tahun Ini", "ltr"),
    "ru": (["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"],
           ["Января","Февраля","Марта","Апреля","Мая","Июня","Июля","Августа","Сентября","Октября","Ноября","Декабря"],
           "ИСЛАМСКИЙ КАЛЕНДАРЬ", "📖 Аят дня", "📜 Хадис дня", "{d}-й день года", "ltr"),
    "zh": (["星期一","星期二","星期三","星期四","星期五","星期六","星期日"],
           ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
           "伊斯兰日历页", "📖 每日古兰经文", "📜 每日圣训", "第 {d} 天", "ltr"),
    "ar": (["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"],
           ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"],
           "ورقة التقويم الإسلامي", "📖 آية اليوم", "📜 حديث اليوم", "اليوم {d} من السنة", "rtl"),
    "ur": (["پیر","منگل","بدھ","جمعرات","جمعہ","ہفتہ","اتوار"],
           ["جنوری","فروری","مارچ","اپریل","مئی","جون","جولائی","اگست","ستمبر","اکتوبر","نومبر","دسمبر"],
           "اسلامی کیلنڈر کا ورق", "📖 آج کی آیت", "📜 آج کی حدیث", "سال کا {d} واں دن", "rtl"),
}

class CalendarLeafWidget(QFrame):
    def __init__(self, lang="tr", fsize=14):
        super().__init__()
        self.setObjectName("Card")
        self.lang, self.fsize, self.cache = lang, fsize, {}
        lay = QVBoxLayout(self); lay.setContentsMargins(16, 16, 16, 16)
        self.browser = QTextBrowser(); self.browser.setStyleSheet("border: none; background: transparent;")
        lay.addWidget(self.browser)
        self.refresh()

    def _get_daily_content(self, lang):
        q_key = lang if os.path.exists(os.path.join(DATA_DIR, f"quran_{lang}.json")) else "en"
        h_key = lang if os.path.exists(os.path.join(DATA_DIR, f"bukhari_{lang}.json")) else "en"
        key = f"{q_key}_{h_key}"
        if key not in self.cache:
            q_data = json.load(open(os.path.join(DATA_DIR, f"quran_{q_key}.json"), encoding="utf-8"))
            h_data = json.load(open(os.path.join(DATA_DIR, f"bukhari_{h_key}.json"), encoding="utf-8")).get("hadiths", [])
            verses = [(s["translation"] if key == "tr" else s["transliteration"], s["id"], v["id"], v["translation"])
                      for s in q_data for v in s["verses"] if 25 <= len(v["translation"]) <= 260]
            hadiths = [(h.get("hadithnumber", ""), h.get("text", "").strip())
                       for h in h_data if 40 <= len(h.get("text", "").strip()) <= 360]
            self.cache[key] = (verses, hadiths)
        return self.cache[key]

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        self.refresh()

    def refresh(self, hijri_str=""):
        today = date.today()
        doy = today.timetuple().tm_yday
        verses, hadiths = self._get_daily_content(self.lang)
        v_surah, v_sid, v_vid, v_txt = verses[doy % len(verses)]
        h_num, h_txt = hadiths[(doy * 7) % len(hadiths)]

        days, months, hdr_t, v_lbl, h_lbl, doy_fmt, d_dir = get_bundle(self.lang)["calendar"]
        m_str = f"{today.day} {months[today.month - 1]} {today.year}"
        w_str = days[today.weekday()]
        sub_cal = doy_fmt.format(d=doy)
        v_ref = f"{v_surah} ({v_sid}:{v_vid})"
        h_ref = f"Sahih al-Bukhari #{h_num}"
        fs = self.fsize
        align = "right" if d_dir == "rtl" else "left"
        b_side = "border-right" if d_dir == "rtl" else "border-left"

        self.browser.setHtml(f"""
        <div dir='{d_dir}' align='{align}' style='font-size:{fs}px; line-height:1.85; text-align:{align};'>
            <div style='text-align:center; padding-bottom:10px; border-bottom:2px solid #10B981;'>
                <div style='font-size:{max(11, fs-3)}px; letter-spacing:1.2px; color:#10B981; font-weight:bold;'>{hdr_t}</div>
                <div style='font-size:{fs+10}px; font-weight:bold; margin-top:4px;'>{m_str}</div>
                <div style='font-size:{fs+2}px; font-weight:600; color:#10B981;'>{w_str}</div>
                <div style='font-size:{max(12, fs-1)}px; opacity:0.8; margin-top:4px;'>{hijri_str} • {sub_cal}</div>
            </div>
            <div style='margin-top:14px; padding:14px 16px; {b_side}:4px solid #10B981; background:rgba(16,185,129,0.07); border-radius:6px;'>
                <div style='font-weight:bold; color:#10B981; font-size:{max(12, fs-1)}px;'>{v_lbl}</div>
                <div style='margin-top:10px; font-style:normal; font-weight:500;'>“{v_txt}”</div>
                <div style='margin-top:10px; font-size:{max(11, fs-2)}px; opacity:0.75; text-align:right;'>— {v_ref}</div>
            </div>
            <div style='margin-top:12px; padding:14px 16px; {b_side}:4px solid #10B981; background:rgba(16,185,129,0.07); border-radius:6px;'>
                <div style='font-weight:bold; color:#10B981; font-size:{max(12, fs-1)}px;'>{h_lbl}</div>
                <div style='margin-top:10px;'>“{h_txt}”</div>
                <div style='margin-top:10px; font-size:{max(11, fs-2)}px; opacity:0.75; text-align:right;'>— {h_ref}</div>
            </div>
        </div>
        """)
        cur = self.browser.textCursor()
        cur.select(QTextCursor.Document)
        bf = QTextBlockFormat()
        bf.setLineHeight(130.0, QTextBlockFormat.ProportionalHeight)
        cur.mergeBlockFormat(bf)
