import os, json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextBrowser,
                             QLabel, QListWidget, QListWidgetItem, QPushButton)
from modules.i18n import STRINGS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TR_BOOKS = {'1': 'Vahiy Başlangıcı', '2': 'İman', '3': 'İlim', '4': 'Abdest (Vudû)', '5': 'Gusül', '6': 'Hayız', '7': 'Teyemmüm', '8': 'Namaz (Salât)', '9': 'Namaz Vakitleri', '10': 'Ezan ve İkamet', '11': 'Cuma Namazı', '12': 'Korku Namazı', '13': 'İki Bayram', '14': 'Vitir Namazı', '15': 'Yağmur Duası', '16': 'Küsûf (Güneş Tutulması)', '17': 'Tilâvet Secdesi', '18': 'Namazları Kısaltma', '19': 'Teheccüd', '20': 'Mescid-i Nebevî Fazileti', '21': 'Namazda Hareketler', '22': 'Sehiv Secdesi', '23': 'Cenâiz (Cenazeler)', '24': 'Zekât', '25': 'Hac', '26': 'Umre', '27': 'Muhsar (İhram Engeli)', '28': 'Av Cezası', '29': "Medine'nin Fazileti", '30': 'Oruç (Savm)', '31': 'Teravih Namazı', '32': 'Kadir Gecesi Fazileti', '33': "İ'tikâf", '34': "Alışveriş (Büyû')", '35': 'Selem', '36': "Şuf'a", '37': 'İcâre (Kira)', '38': 'Havâle', '39': 'Kefâlet', '40': 'Vekâlet', '41': 'Ziraat ve Ortaklık', '42': 'Su ve Sulama (Müsâkât)', '43': 'Borçlar ve İflas', '44': 'Husûmetler (Davalar)', '45': 'Buluntu Eşya (Lukata)', '46': 'Mezâlim (Haksızlıklar)', '47': 'Şirket (Ortaklık)', '48': 'Rehin', '49': 'Köle Azadı', '50': 'Mükâtebe', '51': 'Hibe ve Hediyeler', '52': 'Şahitlikler', '53': 'Sulh (Barış)', '54': 'Şartlar', '55': 'Vasiyetler', '56': 'Cihâd ve Siyer', '57': 'Humus (Ganimet Beşte Biri)', '58': 'Cizye ve Antlaşmalar', '59': 'Yaratılış Başlangıcı', '60': 'Peygamberler', '61': 'Menâkıb (Faziletler)', '62': 'Sahâbe Faziletleri', '63': "Ensâr'ın Faziletleri", '64': 'Megâzî (Gazveler)', '65': "Kur'an Tefsiri", '66': "Kur'an'ın Faziletleri", '67': 'Nikâh', '68': 'Talâk (Boşanma)', '69': 'Nafakalar', '70': 'Yiyecekler', '71': 'Akîka', '72': 'Av ve Kesim (Zebâih)', '73': 'Kurban (Edâhî)', '74': 'İçecekler', '75': 'Hastalar', '76': 'Tıp ve Tedavi', '77': 'Giyim ve Kuşam', '78': 'Edeb ve Güzel Ahlâk', '79': "İzin İsteme (İsti'zân)", '80': 'Dualar (Deavât)', '81': 'Rikâk (Kalp İnceliği)', '82': 'Kader', '83': 'Yeminler ve Adaklar', '84': 'Yemin Kefâreti', '85': 'Ferâiz (Miras)', '86': 'Hudûd (Cezalar)', '87': 'Diyetler', '88': 'Mürtedler', '89': 'İkrâh (Zorlama)', '90': 'Hiyel (Çıkış Yolları)', '91': 'Rüya Tabirleri', '92': 'Fiten (Fitneler)', '93': 'Ahkâm (Hükümler)', '94': 'Temennî', '95': 'Haber-i Vâhid', '96': 'Kitap ve Sünnete Sarılma', '97': 'Tevhîd'}

AR_BOOKS = {'1': 'بدء الوحي', '2': 'الإيمان', '3': 'العلم', '4': 'الوضوء', '5': 'الغسل', '6': 'الحيض', '7': 'التيمم', '8': 'الصلاة', '9': 'مواقيت الصلاة', '10': 'الأذان', '11': 'الجمعة', '12': 'صلاة الخوف', '13': 'العيدين', '14': 'الوتر', '15': 'الاستسقاء', '16': 'الكسوف', '17': 'سجود القرآن', '18': 'التقصير', '19': 'التهجد', '20': 'فضل الصلاة في مسجد مكة والمدينة', '21': 'العمل في الصلاة', '22': 'السهو', '23': 'الجنائز', '24': 'الزكاة', '25': 'الحج', '26': 'العمرة', '27': 'المحصر', '28': 'جزاء الصيد', '29': 'فضائل المدينة', '30': 'الصوم', '31': 'صلاة التراويح', '32': 'فضل ليلة القدر', '33': 'الاعتكاف', '34': 'البيوع', '35': 'السلم', '36': 'الشفعة', '37': 'الإجارة', '38': 'الحوالات', '39': 'الكفالة', '40': 'الوكالة', '41': 'الحرث والمزارعة', '42': 'المساقاة', '43': 'الاستقراض', '44': 'الخصومات', '45': 'اللقطة', '46': 'المظالم', '47': 'الشركة', '48': 'الرهن', '49': 'العتق', '50': 'المكاتب', '51': 'الهبة وفضلها', '52': 'الشهادات', '53': 'الصلح', '54': 'الشروط', '55': 'الوصايا', '56': 'الجهاد والسير', '57': 'فرض الخمس', '58': 'الجزية والموادعة', '59': 'بدء الخلق', '60': 'أحاديث الأنبياء', '61': 'المناقب', '62': 'فضائل أصحاب النبي ﷺ', '63': 'مناقب الأنصار', '64': 'المغازي', '65': 'تفسير القرآن', '66': 'فضائل القرآن', '67': 'النكاح', '68': 'الطلاق', '69': 'النفقات', '70': 'الأطعمة', '71': 'العقيقة', '72': 'الذبائح والصيد', '73': 'الأضاحي', '74': 'الأشربة', '75': 'المرضى', '76': 'الطب', '77': 'اللباس', '78': 'الأدب', '79': 'الاستئذان', '80': 'الدعوات', '81': 'الرقاق', '82': 'القدر', '83': 'الأيمان والنذور', '84': 'كفارات الأيمان', '85': 'الفرائض', '86': 'الحدود', '87': 'الديات', '88': 'استتابة المرتدين', '89': 'الإكراه', '90': 'الحيل', '91': 'التعبير', '92': 'الفتن', '93': 'الأحكام', '94': 'التمني', '95': 'أخبار الآحاد', '96': 'الاعتصام بالكتاب والسنة', '97': 'التوحيد'}

ALL_BOOKS_LBL = {
    "tr": "📚 Tüm Bölümler (7.521)", "en": "📚 All Books (7,521)", "fr": "📚 Tous les Livres (7 521)",
    "es": "📚 Todos los Libros (7.521)", "pt": "📚 Todos os Livros (7.521)", "id": "📚 Semua Kitab (7.521)",
    "ru": "📚 Все книги (7 521)", "zh": "📚 全部篇目 (7,521)", "ar": "📚 جميع الكتب (٧٥٢١)", "ur": "📚 تمام ابواب (7,521)"
}

class HadithWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.lang, self.fsize, self.cache, self.sec_id, self.page = lang, fsize, {}, "all", 0
        root = QHBoxLayout(self); root.setContentsMargins(28,12,28,24); root.setSpacing(14)

        left = QVBoxLayout(); root.addLayout(left, 2)
        self.q = QLineEdit(); self.q.textChanged.connect(self.on_search); left.addWidget(self.q)
        self.sec_list = QListWidget(); self.sec_list.setMinimumWidth(240); self.sec_list.itemClicked.connect(self.on_sec); left.addWidget(self.sec_list)

        right = QVBoxLayout(); root.addLayout(right, 4)
        self.v = QTextBrowser(); right.addWidget(self.v)
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("◀"); self.btn_prev.setObjectName("MiniBtn"); self.btn_prev.clicked.connect(lambda: self.chg_page(-1))
        self.lbl_pg = QLabel(""); self.lbl_pg.setAlignment(Qt.AlignCenter)
        self.btn_next = QPushButton("▶"); self.btn_next.setObjectName("MiniBtn"); self.btn_next.clicked.connect(lambda: self.chg_page(1))
        nav.addWidget(self.btn_prev); nav.addWidget(self.lbl_pg, 1); nav.addWidget(self.btn_next); right.addLayout(nav)
        self.set_prefs(lang, fsize)

    def load_data(self):
        if self.lang not in self.cache:
            fn = f"bukhari_{self.lang}.json" if os.path.exists(os.path.join(DATA_DIR, f"bukhari_{self.lang}.json")) else "bukhari_en.json"
            raw = json.load(open(os.path.join(DATA_DIR, fn), encoding="utf-8"))
            en_secs = raw.get("metadata", {}).get("sections", {})
            secs = {k: (TR_BOOKS.get(str(k), v) if self.lang == "tr" else (AR_BOOKS.get(str(k), v) if self.lang == "ar" else v)) for k, v in en_secs.items() if v}
            hadiths = [(str(h.get("reference", {}).get("book", "")), h.get("hadithnumber", ""), h.get("text", "").strip()) for h in raw.get("hadiths", []) if h.get("text", "").strip()]
            self.cache[self.lang] = (secs, hadiths)
        return self.cache[self.lang]

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        self.q.setPlaceholderText(STRINGS.get(lang, STRINGS["en"])["hadith_ph"])
        secs, _ = self.load_data()
        self.sec_list.clear()
        all_it = QListWidgetItem(ALL_BOOKS_LBL.get(lang, ALL_BOOKS_LBL["en"]))
        all_it.setData(Qt.UserRole, "all"); self.sec_list.addItem(all_it)
        for k, name in secs.items():
            it = QListWidgetItem(f"{k}. {name}"); it.setData(Qt.UserRole, str(k)); self.sec_list.addItem(it)
        self.render()

    def on_sec(self, it): self.sec_id = it.data(Qt.UserRole); self.page = 0; self.render()
    def on_search(self): self.page = 0; self.render()
    def chg_page(self, d): self.page = max(0, self.page + d); self.render()

    def render(self):
        d_dir = "rtl" if self.lang in ("ar", "ur") else "ltr"
        d_al = "right" if d_dir == "rtl" else "left"
        secs, all_h = self.load_data()
        f = self.q.text().lower().strip()
        filtered = [(b, n, t) for b, n, t in all_h if (self.sec_id == "all" or b == self.sec_id) and (not f or f in t.lower() or f == str(n))]
        per_page = 25; max_p = max(0, (len(filtered) - 1) // per_page); self.page = min(self.page, max_p)
        chunk = filtered[self.page * per_page : (self.page + 1) * per_page]
        self.lbl_pg.setText(f"{self.page + 1} / {max_p + 1}  ({len(filtered)} Hadis)")
        src = "Sahih-i Buhârî" if self.lang == "tr" else "Sahih al-Bukhari"
        html = "".join([f"<div dir='{d_dir}' align='{d_al}' style='margin-bottom:14px; padding:14px; border-left:4px solid #10B981; background:rgba(16,185,129,0.06); border-radius:6px; text-align:{d_al};'><div style='font-weight:bold; color:#10B981; font-size:{max(12,self.fsize-1)}px;'>{src} • {secs.get(b, '')} (#{n})</div><div dir='{d_dir}' align='{d_al}' style='margin-top:8px; font-size:{self.fsize}px; line-height:1.6; text-align:{d_al};'>“{t}”</div></div>" for b, n, t in chunk])
        self.v.setHtml(html or f"<p>{STRINGS.get(self.lang, STRINGS['en'])['no_hadith']}</p>")
