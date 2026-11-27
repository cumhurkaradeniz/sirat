import os, sys, json, subprocess
from datetime import datetime, date
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QStackedWidget, QGridLayout,
                             QTextBrowser, QSystemTrayIcon, QMenu, QAction, QComboBox)
from modules.prayer import detect_location, get_today_times
from modules.theme import is_dark_mode, get_stylesheet
from modules.i18n import detect_os_lang, STRINGS, SUPPORTED_LANGS
from modules.quran import QuranWidget
from modules.hadith import HadithWidget
from modules.days import DaysWidget
from modules.guide import GuideWidget
from modules.dhikr import DhikrWidget
from modules.calendar_leaf import CalendarLeafWidget
from modules.locations import TR_CITIES, WORLD_COUNTRIES

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.expanduser("~/.sirat_config.json")
PRAYER_KEYS = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]

def make_pin_icon():
    from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
    from PyQt5.QtCore import QPointF
    pm = QPixmap(24, 24); pm.fill(Qt.transparent)
    p = QPainter(pm); p.setRenderHint(QPainter.Antialiasing)
    col = QColor("#10B981")
    p.setPen(QPen(col, 2.0)); p.setBrush(Qt.NoBrush)
    p.drawEllipse(QPointF(12, 20.5), 7.5, 2.2)
    p.setPen(Qt.NoPen); p.setBrush(col)
    p.drawEllipse(QPointF(12, 9), 6.5, 6.5)
    p.drawPolygon([QPointF(6.2, 11.8), QPointF(17.8, 11.8), QPointF(12, 20.2)])
    p.setBrush(QColor("#ffffff"))
    p.drawEllipse(QPointF(12, 9), 2.7, 2.7)
    p.end()
    return QIcon(pm)

def get_hijri_str(lang="tr"):
    jd = date.today().toordinal() + 1721425
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    m_tr = ["Muharrem", "Safer", "Rebîülevvel", "Rebîülâhir", "Cemâziyelevvel", "Cemâziyelâhir", "Recep", "Şaban", "Ramazan", "Şevval", "Zilkade", "Zilhicce"]
    m_en = ["Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani", "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
    name = (m_tr if lang == "tr" else m_en)[max(0, min(11, m - 1))]
    return f"{d} {name} {y}"

class AboutWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        from PyQt5.QtWidgets import QSizePolicy
        l = QVBoxLayout(self)
        l.setContentsMargins(28, 12, 28, 24)
        l.setSpacing(12)

        hdr = QHBoxLayout()
        lbl_t = QLabel(f"<img src='file://{os.path.join(BASE, 'icon.png')}' width='22' height='22' style='vertical-align:middle;'> <b style='font-size:18px; color:#10B981;'>Sirat — v1.1.0</b>")
        lbl_g = QLabel("<a href='https://github.com/cumhurkaradeniz' style='color:#10B981; text-decoration:none;'>github.com/cumhurkaradeniz</a>  •  GPL-3.0")
        lbl_g.setOpenExternalLinks(True)
        hdr.addWidget(lbl_t); hdr.addStretch(); hdr.addWidget(lbl_g)
        l.addLayout(hdr)

        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.boxes = []
        for i in range(10):
            tb = QTextBrowser()
            tb.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            tb.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            tb.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            tb.setStyleSheet("border: 1px solid rgba(16,185,129,0.35); border-radius: 10px; background: rgba(16,185,129,0.05); padding: 8px;")
            self.grid.addWidget(tb, i // 5, i % 5)
            self.boxes.append(tb)
        for r in range(2): self.grid.setRowStretch(r, 1)
        for c in range(5): self.grid.setColumnStretch(c, 1)
        l.addLayout(self.grid, 1)
        self.set_prefs(lang, fsize)

    def set_prefs(self, lang, fsize):
        fs = max(11, fsize - 2)
        items = [
            ("ltr", "TR • Türkçe", "Bu uygulama, Müslümanların günlük ibadetlerini kolaylaştırmak amacıyla ücretsiz ve açık kaynaklı geliştirilmiştir. Yapımcısı <b>Cumhur Karadeniz</b> ve tüm İslam âlemi için hayır dualarınızı bekleriz."),
            ("ltr", "EN • English", "Developed as a free, open-source project to assist Muslims in their daily worship and learning. Please remember its developer, <b>Cumhur Karadeniz</b>, and the Ummah in your prayers (Dua)."),
            ("ltr", "FR • Français", "Développée gratuitement et en open source pour faciliter l'adoration quotidienne des musulmans. Veuillez garder son développeur, <b>Cumhur Karadeniz</b>, et la Oumma dans vos prières (Doua)."),
            ("ltr", "ES • Español", "Desarrollada como un proyecto gratuito y de código abierto para facilitar la adoración diaria de los musulmanes. Recuerde en sus súplicas (Dua) a <b>Cumhur Karadeniz</b> y a toda la Ummah."),
            ("ltr", "PT • Português", "Desenvolvido como um projeto gratuito e de código aberto para auxiliar os muçulmanos na adoração diária. Lembre-se de seu desenvolvedor, <b>Cumhur Karadeniz</b>, e da Ummah em suas orações."),
            ("ltr", "ID • Indonesia", "Dibuat gratis dan sumber terbuka untuk memudahkan ibadah harian umat Islam di seluruh dunia. Mohon doakan kebaikan bagi pengembangnya, <b>Cumhur Karadeniz</b>, serta seluruh umat Islam."),
            ("ltr", "RU • Русский", "Бесплатный проект с открытым исходным кодом для помощи мусульманам в ежедневном поклонении. Пожалуйста, не забывайте в своих дуа разработчика <b>Джумхура Карадениза</b> и всю умму."),
            ("ltr", "ZH • 中文", "本免费开源应用旨在为全球穆斯林提供日常礼拜便利。请在您真诚的祈祷（杜阿）中记念开发者 <b>Cumhur Karadeniz</b> 以及全世界的穆斯林。"),
            ("rtl", "AR • العربية", "تم تطوير هذا التطبيق مجاناً لوجه الله لتيسير العبادات اليومية للمسلمين. نسألكم الدعاء الصالح لمطور التطبيق <b>جمهور قره دنيز</b> ولسائر المسلمين."),
            ("rtl", "UR • اردو", "یہ ایپ مسلمانوں کی روزمرہ عبادات میں آسانی کے لیے مفت تیار کی گئی ہے۔ اس کے بنانے والے <b>جمہور قرہ دنیز</b> اور امتِ مسلمہ کو دعاؤں میں یاد رکھیں۔")
        ]
        for tb, (d, title, txt) in zip(self.boxes, items):
            align = "right" if d == "rtl" else "left"
            cur_fs = fs if d == "rtl" else fs
            lh = "1.35" if d == "rtl" else "1.45"
            tb.setHtml(f"<div dir='{d}' align='{align}' style='font-size:{cur_fs}px; line-height:{lh};'><b style='color:#10B981;'>{title}</b><br><span style='opacity:0.92;'>{txt}</span></div>")


class SiratApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon = QIcon(os.path.join(BASE, "icon.png"))
        self.setWindowTitle("Sirat"); self.setWindowIcon(self.icon); self.resize(1060, 700)
        self.cfg = json.load(open(CFG)) if os.path.exists(CFG) else {}
        if "city" not in self.cfg:
            c, co = detect_location(); self.cfg["city"], self.cfg["country"] = c, co
        self.cfg.setdefault("lang", detect_os_lang())
        self.cfg.setdefault("theme", "auto")
        self.cfg.setdefault("fsize", 14)
        self.cfg.setdefault("notif", True)
        self.cfg.setdefault("pstyle", 0)
        self.cfg.setdefault("sound", "zil_1.wav")
        self.save_cfg()
        self.times, self.notified_today, self.force_quit, self.bg_warned = {}, set(), False, False
        self.adhan_player = QMediaPlayer(self)
        self.init_ui(); self.init_tray(); self.apply_all_prefs(); self.load_times()
        self.tm = QTimer(self); self.tm.timeout.connect(self.tick); self.tm.start(1000)

    def save_cfg(self): json.dump(self.cfg, open(CFG, "w"))

    def init_tray(self):
        self.tray = QSystemTrayIcon(self.icon, self)
        self.tray_menu = QMenu()
        self.act_info = QAction("Sirat", self); self.act_info.setEnabled(False)
        self.act_show = QAction(self); self.act_show.triggered.connect(self.toggle_win)
        self.act_quit = QAction(self); self.act_quit.triggered.connect(self.quit_app)
        self.tray_menu.addAction(self.act_info); self.tray_menu.addSeparator()
        self.act_stop_adhan = QAction("🔇 Ezanı Durdur", self); self.act_stop_adhan.triggered.connect(self.adhan_player.stop)
        self.tray_menu.addAction(self.act_stop_adhan); self.tray_menu.addAction(self.act_show); self.tray_menu.addAction(self.act_quit)
        self.tray.setContextMenu(self.tray_menu)
        self.tray.activated.connect(lambda r: self.toggle_win() if r == QSystemTrayIcon.Trigger else None)
        self.tray.show()

    def toggle_win(self):
        if self.isVisible(): self.hide()
        else: self.showNormal(); self.activateWindow()

    def quit_app(self): self.force_quit = True; self.tray.hide(); QApplication.quit()

    def closeEvent(self, e):
        if self.force_quit or not self.tray.isVisible(): e.accept()
        else:
            e.ignore(); self.hide()
            if not self.bg_warned:
                self.bg_warned = True
                self.send_notif("Sirat", STRINGS.get(self.cfg["lang"], STRINGS["en"])["tray_bg"])

    def play_adhan(self):
        import shutil
        wav = os.path.join(BASE, "data", self.cfg.get("sound", "zil_1.wav"))
        if not os.path.exists(wav): return
        for cmd in ("pw-play", "paplay", "aplay", "ffplay"):
            if shutil.which(cmd):
                args = [cmd, "-nodisp", "-autoexit", wav] if cmd == "ffplay" else [cmd, wav]
                subprocess.Popen(args)
                return

    def send_notif(self, title, body, is_prayer=False):
        try: subprocess.Popen(["notify-send", "-i", os.path.join(BASE, "icon.png"), title, body])
        except Exception: self.tray.showMessage(title, body, QSystemTrayIcon.Information, 6000)
        if is_prayer: self.play_adhan()

    def init_ui(self):
        cw = QWidget(); self.setCentralWidget(cw); root = QVBoxLayout(cw); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        sb = QFrame(); sb.setObjectName("Sidebar"); sb.setFixedHeight(56); sbl = QHBoxLayout(sb); sbl.setContentsMargins(14,6,14,6); sbl.setSpacing(6)
        brand_w = QWidget(); bl = QHBoxLayout(brand_w); bl.setContentsMargins(0,0,8,0); bl.setSpacing(8)
        b_ico = QLabel(); b_ico.setPixmap(self.icon.pixmap(26, 26))
        title = QLabel("<b>Sirat</b>"); title.setStyleSheet("font-size: 20px; color: #10B981;")
        bl.addWidget(b_ico); bl.addWidget(title); sbl.addWidget(brand_w)
        self.nav_btns = []
        for idx in range(7):
            b = QPushButton(); b.setObjectName("NavBtn"); b.clicked.connect(lambda _, i=idx: self.switch_tab(i)); sbl.addWidget(b); self.nav_btns.append(b)
        sbl.addStretch()
        root.addWidget(sb)

        top_bar = QFrame(); top_bar.setObjectName("SubBar")
        tbl = QVBoxLayout(top_bar); tbl.setContentsMargins(28, 12, 28, 6); tbl.setSpacing(10)

        hdr = QHBoxLayout()
        self.lbl_loc_hdr = QLabel(); self.lbl_loc_hdr.setFixedHeight(32); self.lbl_loc_hdr.setAlignment(Qt.AlignVCenter); self.lbl_loc_hdr.setStyleSheet("font-weight: 600; opacity: 0.9;")
        self.btn_edit_loc = QPushButton(); self.btn_edit_loc.setIcon(make_pin_icon()); self.btn_edit_loc.setObjectName("MiniBtn"); self.btn_edit_loc.setFixedSize(38, 32); self.btn_edit_loc.setStyleSheet("padding:0px; border:1.5px solid #10B981; background:rgba(16,185,129,0.14);")
        self.btn_edit_loc.clicked.connect(self.toggle_loc_box)
        self.cmb_sound = QComboBox(); self.cmb_sound.setObjectName("MiniBtn"); self.cmb_sound.setFixedSize(155, 32); self.cmb_sound.setStyleSheet("padding: 2px 8px; font-size: 12px;")
        self.sound_opts = [("zil_1.wav", "🔔 Klasik Çan", "🔔 Classic Bell"), ("zil_2.wav", "🕌 Derin Gong", "🕌 Deep Gong"), ("zil_3.wav", "✨ Kristal Zil", "✨ Crystal Chime"), ("zil_4.wav", "🎶 Huzurlu Melodi", "🎶 Peaceful Melody")]
        for fn, lbl_tr, lbl_en in self.sound_opts: self.cmb_sound.addItem(lbl_tr, fn)
        cur_idx = next((i for i, (fn, _, _) in enumerate(self.sound_opts) if fn == self.cfg.get("sound")), 0)
        self.cmb_sound.setCurrentIndex(cur_idx)
        self.cmb_sound.currentIndexChanged.connect(self.on_sound_changed)
        self.btn_test_notif = QPushButton("▶ Test"); self.btn_test_notif.setObjectName("MiniBtn"); self.btn_test_notif.setFixedSize(72, 32); self.btn_test_notif.setStyleSheet("padding: 2px 8px; font-size: 12px;")
        self.btn_test_notif.clicked.connect(self.test_adhan_notif)

        hdr.addWidget(self.btn_edit_loc)
        hdr.addWidget(self.lbl_loc_hdr)
        hdr.addStretch()
        self.btn_nt = QPushButton(); self.btn_nt.setObjectName("MiniBtn"); self.btn_nt.clicked.connect(self.toggle_notif)
        self.btn_th = QPushButton(); self.btn_th.setObjectName("MiniBtn"); self.btn_th.clicked.connect(self.cycle_theme)
        self.btn_pl = QPushButton(); self.btn_pl.setObjectName("MiniBtn"); self.btn_pl.clicked.connect(self.cycle_pstyle)
        self.btn_ln = QPushButton(); self.btn_ln.setObjectName("MiniBtn")
        self.lang_menu = QMenu(self)
        self.lang_menu.setStyleSheet("QMenu{padding:4px;border-radius:8px;} QMenu::item{padding:5px 14px;border-radius:5px;} QMenu::item:selected{background:#10B981;color:#fff;}")
        for l_code, l_label in SUPPORTED_LANGS:
            act = self.lang_menu.addAction(l_label)
            act.triggered.connect(lambda _, code=l_code: self.set_lang(code))
        self.btn_ln.setMenu(self.lang_menu)
        b_m = QPushButton("A-"); b_m.setObjectName("MiniBtn"); b_m.clicked.connect(lambda: self.chg_font(-1))
        b_p = QPushButton("A+"); b_p.setObjectName("MiniBtn"); b_p.clicked.connect(lambda: self.chg_font(1))
        for w_btn in (self.btn_nt, self.btn_th, self.btn_pl, self.btn_ln, b_m, b_p):
            w_btn.setFixedHeight(32)
            w_btn.setStyleSheet("QPushButton{padding: 2px 8px; font-size: 12px;} QPushButton::menu-indicator{image:none;width:0px;}")
            hdr.addWidget(w_btn)
        hdr.addWidget(self.cmb_sound)
        hdr.addWidget(self.btn_test_notif)
        tbl.addLayout(hdr)

        self.loc_box = QWidget(); top = QHBoxLayout(self.loc_box); top.setContentsMargins(0,0,0,0); top.setSpacing(10)
        cmb_css = "QComboBox { combobox-popup: 0; padding: 2px 8px; } QComboBox QAbstractItemView { max-height: 260px; }"
        self.cmb_country = QComboBox(); self.cmb_country.setFixedHeight(34); self.cmb_country.setMaxVisibleItems(10); self.cmb_country.setStyleSheet(cmb_css)
        self.cmb_city = QComboBox(); self.cmb_city.setFixedHeight(34); self.cmb_city.setMaxVisibleItems(10); self.cmb_city.setStyleSheet(cmb_css)
        self.cmb_district = QComboBox(); self.cmb_district.setFixedHeight(34); self.cmb_district.setMaxVisibleItems(10); self.cmb_district.setStyleSheet(cmb_css)
        self.cmb_country.addItems(list(WORLD_COUNTRIES.keys()))
        self.cmb_country.setCurrentText(self.cfg.get("country", "Turkey"))
        self.cmb_country.currentTextChanged.connect(self.on_country_changed)
        self.cmb_city.currentTextChanged.connect(self.on_city_changed)
        self.on_country_changed(self.cmb_country.currentText())
        cur_c = self.cfg.get("city", "Sungurlu, Çorum")
        if ", " in cur_c:
            d_part, c_part = cur_c.split(", ", 1)
            self.cmb_city.setCurrentText(c_part)
            self.cmb_district.setCurrentText(d_part)
        else:
            self.cmb_city.setCurrentText(cur_c)
        self.btn_upd = QPushButton(); self.btn_upd.setObjectName("ActionBtn"); self.btn_upd.setFixedHeight(34); self.btn_upd.clicked.connect(self.update_loc)
        top.addWidget(self.cmb_country, 2); top.addWidget(self.cmb_city, 2); top.addWidget(self.cmb_district, 2); top.addWidget(self.btn_upd, 1)
        self.loc_box.setVisible(False); tbl.addWidget(self.loc_box)
        root.addWidget(top_bar)

        self.stack = QStackedWidget(); root.addWidget(self.stack)
        p_page = QWidget()
        p_main = QHBoxLayout(p_page)
        p_main.setContentsMargins(28, 12, 28, 24)
        p_main.setSpacing(18)

        left_wrap = QWidget()
        pl = QVBoxLayout(left_wrap)
        pl.setContentsMargins(0, 0, 0, 0)
        pl.setSpacing(14)

        cd_card = QFrame(); cd_card.setObjectName("HeroCard"); cdl = QVBoxLayout(cd_card); cdl.setContentsMargins(20,18,20,18)
        self.lbl_next = QLabel("..."); self.lbl_next.setAlignment(Qt.AlignCenter); self.lbl_next.setStyleSheet("color: #10B981; font-weight: bold;")
        self.lbl_cd = QLabel("--:--:--"); self.lbl_cd.setAlignment(Qt.AlignCenter); self.lbl_cd.setStyleSheet("font-size: 34px; font-weight: bold; font-family: 'JetBrains Mono', 'Ubuntu Mono', monospace;")
        cdl.addWidget(self.lbl_next); cdl.addWidget(self.lbl_cd); pl.addWidget(cd_card, 1)

        grid = QGridLayout(); grid.setSpacing(14); self.time_lbls, self.name_lbls, self.prayer_cards = {}, {}, {}
        for i, v in enumerate(PRAYER_KEYS):
            card = QFrame(); card.setObjectName("Card"); cl = QVBoxLayout(card); cl.setContentsMargins(16,14,16,14)
            lbl_n = QLabel(v); lbl_n.setStyleSheet("opacity: 0.75; font-weight: 500;")
            lbl_t = QLabel("--:--"); lbl_t.setStyleSheet("font-size: 22px; font-weight: bold; font-family: 'JetBrains Mono', 'Ubuntu Mono', monospace;")
            cl.addStretch(); cl.addWidget(lbl_n); cl.addWidget(lbl_t); cl.addStretch()
            grid.addWidget(card, i // 2, i % 2)
            self.name_lbls[v], self.time_lbls[v], self.prayer_cards[v] = lbl_n, lbl_t, card
        for r in range(3): grid.setRowStretch(r, 1)
        for c in range(2): grid.setColumnStretch(c, 1)
        pl.addLayout(grid, 3)

        self.w_cal_leaf = CalendarLeafWidget(self.cfg["lang"], self.cfg["fsize"])
        from PyQt5.QtWidgets import QSizePolicy
        left_wrap.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.w_cal_leaf.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        p_main.addWidget(left_wrap, 1)
        p_main.addWidget(self.w_cal_leaf, 1)
        self.stack.addWidget(p_page)

        self.w_quran = QuranWidget(self.cfg["lang"], self.cfg["fsize"] + 1, self.cfg.get("pstyle", 0))
        self.w_hadith = HadithWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_days = DaysWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_guide = GuideWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_dhikr = DhikrWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        self.w_about = AboutWidget(self.cfg["lang"], self.cfg["fsize"] + 1)
        for w in (self.w_quran, self.w_hadith, self.w_days, self.w_guide, self.w_dhikr, self.w_about): self.stack.addWidget(w)
        self.switch_tab(0)

    def test_adhan_notif(self):
        s = STRINGS.get(self.cfg["lang"], STRINGS["en"])
        if not self.cfg.get("notif", True):
            msg = s["test_off"]
            self.send_notif("Sirat", msg, is_prayer=False)
            return
        self.send_notif(
            s["notif_title"],
            s["notif_body"].format(city=self.cfg["city"], prayer="Test", time=datetime.now().strftime("%H:%M")),
            is_prayer=True
        )

    def on_sound_changed(self, idx):
        self.cfg["sound"] = self.cmb_sound.itemData(idx)
        self.save_cfg()

    def toggle_loc_box(self): self.loc_box.setVisible(not self.loc_box.isVisible())
    def switch_tab(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_btns): b.setProperty("active", "true" if i == idx else "false"); b.style().unpolish(b); b.style().polish(b)
    def cycle_pstyle(self):
        self.cfg["pstyle"] = (self.cfg.get("pstyle", 0) + 1) % 4
        self.save_cfg(); self.w_quran.apply_player_style(self.cfg["pstyle"]); self.btn_pl.setText(f"🎵 {self.cfg['pstyle']+1}/4")
    def toggle_notif(self): self.cfg["notif"] = not self.cfg.get("notif", True); self.save_cfg(); self.apply_all_prefs()
    def cycle_theme(self): order = ["auto", "light", "dark"]; self.cfg["theme"] = order[(order.index(self.cfg["theme"]) + 1) % 3]; self.save_cfg(); self.apply_all_prefs()
    def set_lang(self, code):
        self.cfg["lang"] = code
        self.save_cfg()
        self.apply_all_prefs()

    def chg_font(self, d): self.cfg["fsize"] = max(11, min(22, self.cfg["fsize"] + d)); self.save_cfg(); self.apply_all_prefs()

    def apply_all_prefs(self):
        l, fs = self.cfg["lang"], self.cfg["fsize"]; s = STRINGS.get(l, STRINGS["en"])
        icons = ["🕌", "📖", "📜", "🌙", "🧭", "📿", "ℹ️"]
        for b, txt, ic in zip(self.nav_btns, s["nav"], icons): b.setText(f"  {ic}   {txt}")
        self.btn_nt.setText(("🔔 " + s["on"]) if self.cfg.get("notif", True) else ("🔕 " + s["off"])); self.btn_nt.setToolTip(s["notif_lbl"])
        self.btn_th.setText({"auto": "🌓 Oto", "light": "☀️ Açık", "dark": "🌙 Koyu"}[self.cfg["theme"]] if l == "tr" else {"auto": "🌓 Auto", "light": "☀️ Light", "dark": "🌙 Dark"}[self.cfg["theme"]]); self.btn_th.setToolTip(s["theme_lbl"])
        self.btn_pl.setText(f"🎵 {self.cfg.get('pstyle', 0)+1}/4"); self.btn_ln.setText(f"🌐 {l.upper()}")
        self.btn_test_notif.setText(s["test_btn"])
        for i, snd_lbl in enumerate(s["sounds"]): self.cmb_sound.setItemText(i, snd_lbl); self.btn_ln.setToolTip(s["lang_lbl"])
        self.lbl_loc_hdr.setText(f"📍  {self.cfg['city']}, {self.cfg['country']}   •   {get_hijri_str(l)}")
        self.act_show.setText(s["tray_show"]); self.act_quit.setText(s["tray_quit"])
        pass; pass; self.btn_upd.setText(s["upd_btn"])
        for k, tr_name in zip(PRAYER_KEYS, s["prayers"]): self.name_lbls[k].setText(tr_name)
        self._dk = None; self.sync_theme()
        for w in (self.w_quran, self.w_hadith, self.w_days, self.w_guide, self.w_dhikr, self.w_about): w.set_prefs(l, fs + 1)
        if hasattr(self, 'w_cal_leaf'): self.w_cal_leaf.set_prefs(l, fs); self.w_cal_leaf.refresh(get_hijri_str(l))

    def sync_theme(self):
        dk = is_dark_mode(self.cfg["theme"])
        if getattr(self, "_dk", None) != dk: self._dk = dk; self.setStyleSheet(get_stylesheet(dk, self.cfg["fsize"]))
    def on_country_changed(self, country):
        self.cmb_city.blockSignals(True); self.cmb_city.clear()
        cities = WORLD_COUNTRIES.get(country, [])
        if cities: self.cmb_city.addItems(cities)
        self.cmb_city.blockSignals(False)
        self.on_city_changed(self.cmb_city.currentText())

    def on_city_changed(self, city):
        self.cmb_district.clear()
        if self.cmb_country.currentText() in ("Turkey", "Türkiye") and city in TR_CITIES:
            self.cmb_district.setVisible(True); self.cmb_district.addItems(TR_CITIES[city])
        else:
            self.cmb_district.setVisible(False)

    def update_loc(self):
        country = self.cmb_country.currentText().strip()
        city = self.cmb_city.currentText().strip()
        dist = self.cmb_district.currentText().strip() if self.cmb_district.isVisible() else ""
        if not city or not country: return
        target = f"{dist}, {city}" if (dist and dist != "Merkez") else city
        self.cfg["city"], self.cfg["country"] = target, country
        self.save_cfg(); self.apply_all_prefs(); self.load_times(); self.loc_box.setVisible(False)
    def load_times(self):
        try:
            self.times = get_today_times(self.cfg["city"], self.cfg["country"])
            for k, v in self.times.items(): self.time_lbls[k].setText(v)
        except Exception: self.lbl_next.setText(STRINGS.get(self.cfg["lang"], STRINGS["en"])["err_time"])

    def tick(self):
        self.sync_theme()
        if not self.times: return
        now = datetime.now(); s = STRINGS.get(self.cfg["lang"], STRINGS["en"])
        today_str = now.strftime("%Y-%m-%d"); next_key = None
        for k, disp_name in zip(PRAYER_KEYS, s["prayers"]):
            h, m = map(int, self.times[k].split(":")); t = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if now.hour == h and now.minute == m:
                uid = f"{today_str}_{k}"
                if uid not in self.notified_today:
                    self.notified_today.add(uid)
                    if self.cfg.get("notif", True):
                        self.send_notif(s["notif_title"], s["notif_body"].format(city=self.cfg["city"], prayer=disp_name, time=self.times[k]), is_prayer=True)
            if t > now and next_key is None:
                next_key = k; cd_txt = next(iter(str(t - now).split(".")))
                self.lbl_next.setText(s["next_fmt"].format(city=self.cfg["city"], prayer=disp_name)); self.lbl_cd.setText(cd_txt)
                info = f"{disp_name} ({self.times[k]}) • {cd_txt}"; self.tray.setToolTip(f"Sirat — {info}"); self.act_info.setText(info)
        for k, card in self.prayer_cards.items():
            target_name = "ActivePrayerCard" if k == next_key else "Card"
            if card.objectName() != target_name: card.setObjectName(target_name); card.style().unpolish(card); card.style().polish(card)
        if next_key is None and "İmsak" in self.times:
            from datetime import timedelta
            ih, im = map(int, self.times["İmsak"].split(":"))
            tomorrow_imsak = (now + timedelta(days=1)).replace(hour=ih, minute=im, second=0, microsecond=0)
            cd_txt = next(iter(str(tomorrow_imsak - now).split(".")))
            self.lbl_next.setText(s["wait_next"].format(city=self.cfg["city"]))
            self.lbl_cd.setText(cd_txt)
            self.tray.setToolTip(f"Sirat — {cd_txt}")

sys.argv = ["sirat"]; app = QApplication(sys.argv); app.setDesktopFileName("sirat"); app.setQuitOnLastWindowClosed(False); w = SiratApp(); w.show(); sys.exit(app.exec_())
