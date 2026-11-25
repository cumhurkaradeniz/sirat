import os, sys, json
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QStackedWidget, QGridLayout, QComboBox)
from modules.prayer import detect_location, get_today_times
from modules.theme import is_dark_mode, get_stylesheet
from modules.i18n import detect_os_lang, STRINGS
from modules.quran import QuranWidget
from modules.hadith import HadithWidget
from modules.days import DaysWidget
from modules.guide import GuideWidget

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.expanduser("~/.sirat_config.json")
PRAYER_KEYS = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]

from PyQt5.QtWidgets import QTextBrowser

class AboutWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        l = QVBoxLayout(self); l.setContentsMargins(24,24,24,24)
        self.v = QTextBrowser(); self.v.setStyleSheet("border:none;"); l.addWidget(self.v)
        self.set_prefs(lang, fsize)

    def set_prefs(self, lang, fsize):
        self.v.setHtml(f"""
        <div style='font-size:{fsize}px; line-height:1.7; max-width:720px;'>
            <h2 style='color:#10B981;'>☪ Sirat — v1.0.0</h2>
            <p><b>TR:</b> Bu uygulama, dünyanın dört bir yanındaki Müslümanların günlük ibadetlerini kolaylaştırmak ve İslami ilimlere erişimini desteklemek amacıyla ücretsiz ve açık kaynaklı olarak geliştirilmiştir. Lütfen bu eserin hazırlanmasında emeği geçen yapımcısı <b>Cumhur Karadeniz</b> ve tüm İslam âlemi için hayır dualarınızı eksik etmeyiniz.</p>
            <p><b>EN:</b> This application was developed as a free, open-source project to assist Muslims around the world in their daily worship and learning. Please remember its developer, <b>Cumhur Karadeniz</b>, and the entire Ummah in your sincere prayers (Dua).</p>
            <p dir='rtl' align='right' style='font-size:{fsize+2}px; color:#10B981;'><b>AR:</b> تم تطوير هذا التطبيق مجاناً لوجه الله تعالى لتيسير العبادات اليومية للمسلمين في جميع أنحاء العالم. نسألكم الدعاء الصالح لمطور التطبيق <b>جمهور قره دنيز</b> ولسائر المسلمين.</p>
            <p dir='rtl' align='right' style='font-size:{fsize+1}px;'><b>UR:</b> یہ ایپلیکیشن دنیا بھر کے مسلمانوں کی روزمرہ عبادات میں آسانی کے لیے مفت تیار کی گئی ہے۔ براہ کرم اس کے بنانے والے <b>جمہور قرہ دنیز</b> اور پوری امتِ مسلمہ کو اپنی نیک دعاؤں میں یاد رکھیں۔</p>
            <p><b>ID / MS:</b> Aplikasi ini dibuat secara gratis untuk memudahkan ibadah harian umat Islam di seluruh dunia. Mohon doakan kebaikan bagi pengembangnya, <b>Cumhur Karadeniz</b>, serta seluruh umat Islam.</p>
            <hr style='border:0; border-top:1px solid rgba(128,128,128,0.25); margin:16px 0;'>
            <p style='font-size:{max(12,fsize-2)}px; opacity:0.8;'>GitHub: github.com / cumhurkaradeniz / sirat • License: GPL-3.0</p>
        </div>
        """)

class SiratApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sirat"); self.setWindowIcon(QIcon(os.path.join(BASE, "icon.png"))); self.resize(1060, 700)
        self.cfg = json.load(open(CFG)) if os.path.exists(CFG) else {}
        if "city" not in self.cfg:
            c, co = detect_location(); self.cfg["city"], self.cfg["country"] = c, co
        self.cfg.setdefault("lang", detect_os_lang())
        self.cfg.setdefault("theme", "auto")
        self.cfg.setdefault("fsize", 14)
        self.save_cfg()
        self.times = {}
        self.init_ui(); self.apply_all_prefs(); self.load_times()
        self.tm = QTimer(self); self.tm.timeout.connect(self.tick); self.tm.start(1000)

    def save_cfg(self): json.dump(self.cfg, open(CFG, "w"))

    def init_ui(self):
        cw = QWidget(); self.setCentralWidget(cw); root = QHBoxLayout(cw); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        sb = QFrame(); sb.setObjectName("Sidebar"); sb.setFixedWidth(225); sbl = QVBoxLayout(sb); sbl.setContentsMargins(12,18,12,18)
        title = QLabel("<b>☪ Sirat</b>"); title.setStyleSheet("font-size: 20px; color: #10B981; margin-bottom: 12px;"); sbl.addWidget(title)
        self.nav_btns = []
        for idx in range(6):
            b = QPushButton(); b.setObjectName("NavBtn"); b.clicked.connect(lambda _, i=idx: self.switch_tab(i)); sbl.addWidget(b); self.nav_btns.append(b)
        sbl.addStretch()

        r_th = QHBoxLayout(); self.lbl_th = QLabel()
        self.btn_th = QPushButton(); self.btn_th.setObjectName("MiniBtn"); self.btn_th.clicked.connect(self.cycle_theme)
        r_th.addWidget(self.lbl_th); r_th.addWidget(self.btn_th); sbl.addLayout(r_th)

        r_ln = QHBoxLayout(); self.lbl_ln = QLabel()
        self.btn_ln = QPushButton(); self.btn_ln.setObjectName("MiniBtn"); self.btn_ln.clicked.connect(self.toggle_lang)
        r_ln.addWidget(self.lbl_ln); r_ln.addWidget(self.btn_ln); sbl.addLayout(r_ln)

        r_fn = QHBoxLayout(); self.lbl_fn = QLabel()
        b_m = QPushButton("A-"); b_m.setObjectName("MiniBtn"); b_m.clicked.connect(lambda: self.chg_font(-1))
        b_p = QPushButton("A+"); b_p.setObjectName("MiniBtn"); b_p.clicked.connect(lambda: self.chg_font(1))
        r_fn.addWidget(self.lbl_fn); r_fn.addWidget(b_m); r_fn.addWidget(b_p); sbl.addLayout(r_fn)
        root.addWidget(sb)

        self.stack = QStackedWidget(); root.addWidget(self.stack)
        p_page = QWidget(); pl = QVBoxLayout(p_page); pl.setContentsMargins(28,24,28,24); pl.setSpacing(18)
        top = QHBoxLayout()
        self.in_city = QLineEdit(self.cfg["city"]); self.in_country = QLineEdit(self.cfg["country"])
        self.btn_upd = QPushButton(); self.btn_upd.setObjectName("ActionBtn"); self.btn_upd.clicked.connect(self.update_loc)
        top.addWidget(self.in_city); top.addWidget(self.in_country); top.addWidget(self.btn_upd); pl.addLayout(top)

        cd_card = QFrame(); cd_card.setObjectName("Card"); cdl = QVBoxLayout(cd_card); cdl.setContentsMargins(20,20,20,20)
        self.lbl_next = QLabel("..."); self.lbl_next.setStyleSheet("color: #10B981; font-weight: bold;")
        self.lbl_cd = QLabel("--:--:--"); self.lbl_cd.setStyleSheet("font-size: 34px; font-weight: bold;")
        cdl.addWidget(self.lbl_next); cdl.addWidget(self.lbl_cd); pl.addWidget(cd_card)
        grid = QGridLayout(); grid.setSpacing(14); self.time_lbls, self.name_lbls = {}, {}
        for i, v in enumerate(PRAYER_KEYS):
            card = QFrame(); card.setObjectName("Card"); cl = QVBoxLayout(card); cl.setContentsMargins(16,16,16,16)
            lbl_n = QLabel(v); lbl_t = QLabel("--:--"); lbl_t.setStyleSheet("font-size: 22px; font-weight: bold;")
            cl.addWidget(lbl_n); cl.addWidget(lbl_t); grid.addWidget(card, i // 3, i % 3)
            self.name_lbls[v], self.time_lbls[v] = lbl_n, lbl_t
        pl.addLayout(grid); pl.addStretch(); self.stack.addWidget(p_page)

        self.w_quran = QuranWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_hadith = HadithWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_days = DaysWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_guide = GuideWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_about = AboutWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        for w in (self.w_quran, self.w_hadith, self.w_days, self.w_guide, self.w_about): self.stack.addWidget(w)
        self.switch_tab(0)
    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_btns): b.setProperty("active", "true" if i == idx else "false"); b.style().unpolish(b); b.style().polish(b)
    def cycle_theme(self): order = ["auto", "light", "dark"]; self.cfg["theme"] = order[(order.index(self.cfg["theme"]) + 1) % 3]; self.save_cfg(); self.apply_all_prefs()
    def toggle_lang(self): self.cfg["lang"] = "en" if self.cfg["lang"] == "tr" else "tr"; self.save_cfg(); self.apply_all_prefs()
    def chg_font(self, d): self.cfg["fsize"] = max(11, min(22, self.cfg["fsize"] + d)); self.save_cfg(); self.apply_all_prefs()
    def apply_all_prefs(self):
        l, fs = self.cfg["lang"], self.cfg["fsize"]; s = STRINGS.get(l, STRINGS["en"])
        for b, txt in zip(self.nav_btns, s["nav"]): b.setText(txt)
        self.lbl_th.setText(s["theme_lbl"]); self.lbl_ln.setText(s["lang_lbl"]); self.lbl_fn.setText(s["font_lbl"]); t_auto, t_light, t_dark = s["themes"]; self.btn_th.setText({"auto": t_auto, "light": t_light, "dark": t_dark}[self.cfg["theme"]]); self.btn_ln.setText("Türkçe" if l == "tr" else "English")
        self.in_city.setPlaceholderText(s["city_ph"]); self.in_country.setPlaceholderText(s["country_ph"]); self.btn_upd.setText(s["upd_btn"])
        for k, tr_name in zip(PRAYER_KEYS, s["prayers"]): self.name_lbls[k].setText(tr_name)
        self._dk = None; self.sync_theme()
        for w in (self.w_quran, self.w_hadith, self.w_days, self.w_guide, self.w_about): w.set_prefs(l, fs + 1)
    def sync_theme(self):
        dk = is_dark_mode(self.cfg["theme"])
        if getattr(self, "_dk", None) != dk: self._dk = dk; self.setStyleSheet(get_stylesheet(dk, self.cfg["fsize"]))
    def update_loc(self): self.cfg["city"], self.cfg["country"] = self.in_city.text().strip(), self.in_country.text().strip(); self.save_cfg(); self.load_times()
    def load_times(self):
        try:
            self.times = get_today_times(self.cfg["city"], self.cfg["country"])
            for k, v in self.times.items(): self.time_lbls[k].setText(v)
        except Exception: self.lbl_next.setText(STRINGS.get(self.cfg["lang"], STRINGS["en"])["err_time"])
    def tick(self):
        self.sync_theme()
        if not self.times: return
        now = datetime.now(); s = STRINGS.get(self.cfg["lang"], STRINGS["en"])
        for k, disp_name in zip(PRAYER_KEYS, s["prayers"]):
            h, m = map(int, self.times[k].split(":")); t = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if t > now: self.lbl_next.setText(s["next_fmt"].format(city=self.cfg["city"], prayer=disp_name)); self.lbl_cd.setText(next(iter(str(t - now).split(".")))); return
        self.lbl_next.setText(s["wait_next"].format(city=self.cfg["city"])); self.lbl_cd.setText("00:00:00")

sys.argv[0] = "sirat"; app = QApplication(sys.argv); app.setDesktopFileName("sirat"); w = SiratApp(); w.show(); sys.exit(app.exec_())
