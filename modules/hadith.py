import os, json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextBrowser,
                             QLabel, QListWidget, QListWidgetItem, QPushButton)
from modules.i18n import STRINGS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TR_BOOKS = {'1': 'Vahiy Başlangıcı', '2': 'İman', '3': 'İlim', '4': 'Abdest (Vudû)', '5': 'Gusül', '6': 'Hayız', '7': 'Teyemmüm', '8': 'Namaz (Salât)', '9': 'Namaz Vakitleri', '10': 'Ezan ve İkamet', '11': 'Cuma Namazı', '12': 'Korku Namazı', '13': 'İki Bayram', '14': 'Vitir Namazı', '15': 'Yağmur Duası', '16': 'Küsûf (Güneş Tutulması)', '17': 'Tilâvet Secdesi', '18': 'Namazları Kısaltma', '19': 'Teheccüd', '20': 'Mescid-i Nebevî Fazileti', '21': 'Namazda Hareketler', '22': 'Sehiv Secdesi', '23': 'Cenâiz (Cenazeler)', '24': 'Zekât', '25': 'Hac', '26': 'Umre', '27': 'Muhsar (İhram Engeli)', '28': 'Av Cezası', '29': "Medine'nin Fazileti", '30': 'Oruç (Savm)', '31': 'Teravih Namazı', '32': 'Kadir Gecesi Fazileti', '33': "İ'tikâf", '34': "Alışveriş (Büyû')", '35': 'Selem', '36': "Şuf'a", '37': 'İcâre (Kira)', '38': 'Havâle', '39': 'Kefâlet', '40': 'Vekâlet', '41': 'Ziraat ve Ortaklık', '42': 'Su ve Sulama (Müsâkât)', '43': 'Borçlar ve İflas', '44': 'Husûmetler (Davalar)', '45': 'Buluntu Eşya (Lukata)', '46': 'Mezâlim (Haksızlıklar)', '47': 'Şirket (Ortaklık)', '48': 'Rehin', '49': 'Köle Azadı', '50': 'Mükâtebe', '51': 'Hibe ve Hediyeler', '52': 'Şahitlikler', '53': 'Sulh (Barış)', '54': 'Şartlar', '55': 'Vasiyetler', '56': 'Cihâd ve Siyer', '57': 'Humus (Ganimet Beşte Biri)', '58': 'Cizye ve Antlaşmalar', '59': 'Yaratılış Başlangıcı', '60': 'Peygamberler', '61': 'Menâkıb (Faziletler)', '62': 'Sahâbe Faziletleri', '63': "Ensâr'ın Faziletleri", '64': 'Megâzî (Gazveler)', '65': "Kur'an Tefsiri", '66': "Kur'an'ın Faziletleri", '67': 'Nikâh', '68': 'Talâk (Boşanma)', '69': 'Nafakalar', '70': 'Yiyecekler', '71': 'Akîka', '72': 'Av ve Kesim (Zebâih)', '73': 'Kurban (Edâhî)', '74': 'İçecekler', '75': 'Hastalar', '76': 'Tıp ve Tedavi', '77': 'Giyim ve Kuşam', '78': 'Edeb ve Güzel Ahlâk', '79': "İzin İsteme (İsti'zân)", '80': 'Dualar (Deavât)', '81': 'Rikâk (Kalp İnceliği)', '82': 'Kader', '83': 'Yeminler ve Adaklar', '84': 'Yemin Kefâreti', '85': 'Ferâiz (Miras)', '86': 'Hudûd (Cezalar)', '87': 'Diyetler', '88': 'Mürtedler', '89': 'İkrâh (Zorlama)', '90': 'Hiyel (Çıkış Yolları)', '91': 'Rüya Tabirleri', '92': 'Fiten (Fitneler)', '93': 'Ahkâm (Hükümler)', '94': 'Temennî', '95': 'Haber-i Vâhid', '96': 'Kitap ve Sünnete Sarılma', '97': 'Tevhîd'}

class HadithWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.lang, self.fsize, self.cache, self.sec_id, self.page = lang, fsize, {}, "all", 0
        root = QHBoxLayout(self); root.setContentsMargins(16,16,16,16); root.setSpacing(14)

        left = QVBoxLayout(); root.addLayout(left, 2)
        self.q = QLineEdit(); self.q.textChanged.connect(self.on_search); left.addWidget(self.q)
        self.sec_list = QListWidget(); self.sec_list.setMinimumWidth(240); self.sec_list.itemClicked.connect(self.on_sec); left.addWidget(self.sec_list)

        right = QVBoxLayout(); root.addLayout(right, 4)
        self.v = QTextBrowser(); self.v.setStyleSheet("border:none;"); right.addWidget(self.v)
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("◀"); self.btn_prev.setObjectName("MiniBtn"); self.btn_prev.clicked.connect(lambda: self.chg_page(-1))
        self.lbl_pg = QLabel(""); self.lbl_pg.setAlignment(Qt.AlignCenter)
        self.btn_next = QPushButton("▶"); self.btn_next.setObjectName("MiniBtn"); self.btn_next.clicked.connect(lambda: self.chg_page(1))
        nav.addWidget(self.btn_prev); nav.addWidget(self.lbl_pg, 1); nav.addWidget(self.btn_next); right.addLayout(nav)
        self.set_prefs(lang, fsize)

    def load_data(self):
        if self.lang not in self.cache:
            fn = "bukhari_tr.json" if self.lang == "tr" else "bukhari_en.json"
            raw = json.load(open(os.path.join(DATA_DIR, fn), encoding="utf-8"))
            en_secs = raw.get("metadata", {}).get("sections", {})
            secs = {k: (TR_BOOKS.get(str(k), v) if self.lang == "tr" else v) for k, v in en_secs.items() if v}
            hadiths = [(str(h.get("reference", {}).get("book", "")), h.get("hadithnumber", ""), h.get("text", "").strip()) for h in raw.get("hadiths", []) if h.get("text", "").strip()]
            self.cache[self.lang] = (secs, hadiths)
        return self.cache[self.lang]

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        self.q.setPlaceholderText(STRINGS.get(lang, STRINGS["en"])["hadith_ph"])
        secs, _ = self.load_data()
        self.sec_list.clear()
        all_it = QListWidgetItem("📚 Tüm Bölümler (7.521)" if lang == "tr" else "📚 All Books (7,521)")
        all_it.setData(Qt.UserRole, "all"); self.sec_list.addItem(all_it)
        for k, name in secs.items():
            it = QListWidgetItem(f"{k}. {name}"); it.setData(Qt.UserRole, str(k)); self.sec_list.addItem(it)
        self.render()

    def on_sec(self, it): self.sec_id = it.data(Qt.UserRole); self.page = 0; self.render()
    def on_search(self): self.page = 0; self.render()
    def chg_page(self, d): self.page = max(0, self.page + d); self.render()

    def render(self):
        secs, all_h = self.load_data()
        f = self.q.text().lower().strip()
        filtered = [(b, n, t) for b, n, t in all_h if (self.sec_id == "all" or b == self.sec_id) and (not f or f in t.lower() or f == str(n))]
        per_page = 25; max_p = max(0, (len(filtered) - 1) // per_page); self.page = min(self.page, max_p)
        chunk = filtered[self.page * per_page : (self.page + 1) * per_page]
        self.lbl_pg.setText(f"{self.page + 1} / {max_p + 1}  ({len(filtered)} Hadis)")
        src = "Sahih-i Buhârî" if self.lang == "tr" else "Sahih al-Bukhari"
        html = "".join([f"<div style='margin-bottom:14px; padding:14px; border-left:4px solid #10B981; background:rgba(16,185,129,0.06); border-radius:6px;'><div style='font-weight:bold; color:#10B981; font-size:{max(12,self.fsize-1)}px;'>{src} • {secs.get(b, '')} (#{n})</div><div style='margin-top:8px; font-size:{self.fsize}px; line-height:1.6;'>“{t}”</div></div>" for b, n, t in chunk])
        self.v.setHtml(html or f"<p>{STRINGS.get(self.lang, STRINGS['en'])['no_hadith']}</p>")
