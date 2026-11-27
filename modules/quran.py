import os, json, base64
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
                             QTextBrowser, QPushButton, QLabel, QComboBox, QLineEdit, QFrame, QSlider, QMenu)
from modules.i18n import STRINGS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
NUZUL_ORDER = [
    96,68,73,74,1,111,81,87,92,89,93,94,103,100,108,102,107,109,105,113,114,112,53,80,97,91,85,95,106,
    101,75,104,77,50,90,86,54,38,7,72,36,25,35,19,20,56,26,27,28,17,10,11,12,15,6,37,31,34,39,40,41,42,
    43,44,45,46,51,88,18,16,71,14,21,23,32,52,67,69,70,78,79,82,84,30,29,83,2,8,3,33,60,4,99,57,47,13,
    55,76,65,98,59,24,22,63,58,49,66,64,61,62,48,5,9,110
]
NUZUL_RANK = {sid: idx for idx, sid in enumerate(NUZUL_ORDER)}

RECITERS = {
    "Mishary Rashid Alafasy": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXI4Lm1wM3F1cmFuLm5ldC9hZnMv").decode() + "{:03d}.mp3",
    "Abdul Rahman Al-Sudais": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXIxMS5tcDNxdXJhbi5uZXQvc2RzLw==").decode() + "{:03d}.mp3",
    "Islam Sobhi": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXIxNC5tcDNxdXJhbi5uZXQvaXNsYW0vUmV3YXlhdC1IYWZzLUEtbi1Bc3NlbS8=").decode() + "{:03d}.mp3",
    "Maher Al Muaiqly": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXIxMi5tcDNxdXJhbi5uZXQvbWFoZXIv").decode() + "{:03d}.mp3",
    "Yasser Al-Dosari": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXIxMS5tcDNxdXJhbi5uZXQveWFzc2VyLw==").decode() + "{:03d}.mp3",
    "Nasser Al Qatami": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXI2Lm1wM3F1cmFuLm5ldC9xdG0v").decode() + "{:03d}.mp3",
    "Saad Al-Ghamdi": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXI3Lm1wM3F1cmFuLm5ldC9zX2dtZC8=").decode() + "{:03d}.mp3",
    "Muhammad Siddiq Al-Minshawi": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXIxMC5tcDNxdXJhbi5uZXQvbWluc2gv").decode() + "{:03d}.mp3",
    "Abdul Basit Abdus Samad": base64.b64decode("aHR0cHM6Ly9zZXJ2ZXI3Lm1wM3F1cmFuLm5ldC9iYXNpdC8=").decode() + "{:03d}.mp3"
}

QURAN_UI = {
    "tr": (["📖 Mushaf Sırası (1-114)", "🔢 Ters Mushaf (114-1)", "🕌 İniş Sırası (İlk → Son)", "🕌 İniş Sırası (Son → İlk)", "📉 Kısadan Uzuna (Ayet)", "📈 Uzundan Kısaya (Ayet)", "🔤 Alfabetik (A → Z)", "🔤 Alfabetik (Z → A)"], "{v} Ayet • İniş: {n}."),
    "en": (["📖 Mushaf Order (1-114)", "🔢 Reverse Mushaf (114-1)", "🕌 Revelation Order (1st → Last)", "🕌 Revelation Order (Last → 1st)", "📉 Shortest to Longest", "📈 Longest to Shortest", "🔤 Alphabetical (A → Z)", "🔤 Alphabetical (Z → A)"], "{v} Verses • Revelation: #{n}"),
    "fr": (["📖 Ordre du Mushaf (1-114)", "🔢 Mushaf Inversé (114-1)", "🕌 Ordre de Révélation (1 → 114)", "🕌 Ordre de Révélation (114 → 1)", "📉 Plus courte à plus longue", "📈 Plus longue à plus courte", "🔤 Alphabétique (A → Z)", "🔤 Alphabétique (Z → A)"], "{v} Versets • Révélation : #{n}"),
    "es": (["📖 Orden del Mushaf (1-114)", "🔢 Mushaf Inverso (114-1)", "🕌 Orden de Revelación (1 → 114)", "🕌 Orden de Revelación (114 → 1)", "📉 Más corta a más larga", "📈 Más larga a más corta", "🔤 Alfabético (A → Z)", "🔤 Alfabético (Z → A)"], "{v} Versículos • Revelación: #{n}"),
    "pt": (["📖 Ordem do Mushaf (1-114)", "🔢 Mushaf Inverso (114-1)", "🕌 Ordem de Revelação (1 → 114)", "🕌 Ordem de Revelação (114 → 1)", "📉 Mais curta para mais longa", "📈 Mais longa para mais curta", "🔤 Alfabético (A → Z)", "🔤 Alfabético (Z → A)"], "{v} Versículos • Revelação: #{n}"),
    "id": (["📖 Urutan Mushaf (1-114)", "🔢 Mushaf Terbalik (114-1)", "🕌 Urutan Turun (1 → 114)", "🕌 Urutan Turun (114 → 1)", "📉 Terpendek ke Terpanjang", "📈 Terpanjang ke Terpendek", "🔤 Alfabetis (A → Z)", "🔤 Alfabetis (Z → A)"], "{v} Ayat • Wahyu ke-{n}"),
    "ru": (["📖 Порядок Мусхафа (1-114)", "🔢 Обратный Мусхаф (114-1)", "🕌 Порядок ниспослания (1 → 114)", "🕌 Порядок ниспослания (114 → 1)", "📉 От коротких к длинным", "📈 От длинных к коротким", "🔤 По алфавиту (А → Я)", "🔤 По алфавиту (Я → А)"], "{v} аятов • Ниспослана: #{n}"),
    "zh": (["📖 穆斯哈夫顺序 (1-114)", "🔢 倒序排列 (114-1)", "🕌 降示顺序 (1 → 114)", "🕌 降示顺序 (114 → 1)", "📉 由短到长 (节数)", "📈 由长到短 (节数)", "🔤 按字母顺序 (A → Z)", "🔤 按字母倒序 (Z → A)"], "{v} 节 • 降示顺序: 第{n}章"),
    "ar": (["📖 ترتيب المصحف (١-١١٤)", "🔢 ترتيب المصحف العكسي (١١٤-١)", "🕌 ترتيب النزول (الأول ← الأخير)", "🕌 ترتيب النزول (الأخير ← الأول)", "📉 من الأقصر إلى الأطول", "📈 من الأطول إلى الأقصر", "🔤 ترتيب أبجدي (أ ← ي)", "🔤 ترتيب أبجدي (ي ← أ)"], "{v} آيات • ترتيب النزول: {n}"),
    "ur": (["📖 ترتیبِ مصحف (1-114)", "🔢 الٹی ترتیب (114-1)", "🕌 ترتیبِ نزول (اول ← آخر)", "🕌 ترتیبِ نزول (آخر ← اول)", "📉 مختصر سے طویل", "📈 طویل سے مختصر", "🔤 حروفِ تہجی (ا ← ی)", "🔤 حروفِ تہجی (ی ← ا)"], "{v} آیات • ترتیبِ نزول: {n}")
}

class QuranWidget(QWidget):
    def __init__(self, lang="tr", fsize=15, pstyle=0):
        super().__init__()
        self.lang, self.fsize, self.pstyle, self.cur_num, self.qdata = lang, fsize, pstyle, 1, {}
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.on_pos)
        self.player.durationChanged.connect(self.on_dur)
        self.player.stateChanged.connect(self.on_state)

        root = QHBoxLayout(self); root.setContentsMargins(28,12,28,24); root.setSpacing(14)
        left = QVBoxLayout(); left.setContentsMargins(0,0,0,0); left.setSpacing(8); left_w = QWidget(); left_w.setFixedWidth(195); left_w.setLayout(left); root.addWidget(left_w)
        self.search = QLineEdit(); self.search.textChanged.connect(self.filter_list); left.addWidget(self.search)

        self.cmb_sort = QComboBox()
        self.cmb_sort.setStyleSheet("padding:4px 8px; font-size:12px; border-radius:7px;")
        self.cmb_sort.currentIndexChanged.connect(self.rebuild_list)
        left.addWidget(self.cmb_sort)

        self.s_list = QListWidget(); self.s_list.itemClicked.connect(self.on_select); left.addWidget(self.s_list)

        self.right = QVBoxLayout(); self.right.setContentsMargins(0,0,0,0); self.right.setSpacing(10); root.addLayout(self.right, 3)
        self.top_hdr = QFrame(); self.top_hdr.setObjectName("Card")
        thl = QHBoxLayout(self.top_hdr); thl.setContentsMargins(18,10,18,10)
        self.lbl_hdr_only = QLabel(""); self.lbl_hdr_only.setStyleSheet("font-size:15px; font-weight:bold;")
        thl.addWidget(self.lbl_hdr_only); thl.addStretch()

        self.bar = QFrame(); self.bar.setObjectName("Card"); self.bar.setFixedHeight(86); self.bl = QVBoxLayout(self.bar)
        self.lbl_cur = QLabel("00:00"); self.lbl_tot = QLabel("00:00"); self.lbl_sep = QLabel("/"); self.lbl_sep.setVisible(False)
        self.slider = QSlider(Qt.Horizontal); self.slider.setFixedHeight(16); self.slider.sliderMoved.connect(self.player.setPosition)
        self.lbl_title = QLabel(""); self.lbl_title.setStyleSheet("font-size:15px; font-weight:bold;")

        self.btn_prev = QPushButton("⏮"); self.btn_prev.setFixedSize(32, 32)
        self.btn_prev.setStyleSheet("border:none; background:transparent; font-size:17px;"); self.btn_prev.clicked.connect(lambda: self.step_surah(-1))
        self.btn_play = QPushButton("▶"); self.btn_play.setFixedSize(38, 38)
        self.btn_play.setStyleSheet("QPushButton{background:#10B981;color:#fff;border-radius:19px;font-size:15px;font-weight:bold;border:none;padding:0px;} QPushButton:hover{background:#059669;}")
        self.btn_play.clicked.connect(self.toggle_audio)
        self.btn_next = QPushButton("⏭"); self.btn_next.setFixedSize(32, 32)
        self.btn_next.setStyleSheet("border:none; background:transparent; font-size:17px;"); self.btn_next.clicked.connect(lambda: self.step_surah(1))

        self.cur_reciter = next(iter(RECITERS.keys()))
        self.cmb_reciter = QPushButton(f"🎙️ {self.cur_reciter}")
        self.cmb_reciter.setFixedWidth(260)
        self.reciter_menu = QMenu(self); self.reciter_menu.setFixedWidth(260)
        self.reciter_menu.setStyleSheet(
            "QMenu{padding:4px; border-radius:8px;}"
            "QMenu::item{padding:6px 16px; border-radius:6px;}"
            "QMenu::item:selected{background-color:#10B981; color:#ffffff;}"
        )
        for r in RECITERS.keys():
            act = self.reciter_menu.addAction(f"🎙️ {r}")
            act.triggered.connect(lambda _, name=r: self.select_reciter(name))
        self.cmb_reciter.setMenu(self.reciter_menu)

        self.viewer = QTextBrowser()
        self.right.addWidget(self.top_hdr); self.right.addWidget(self.bar); self.right.addWidget(self.viewer)
        self.apply_player_style(pstyle); self.set_prefs(lang, fsize)

    def clear_layout(self, lay):
        while lay.count():
            it = lay.takeAt(0)
            if it.layout(): self.clear_layout(it.layout())

    def apply_player_style(self, mode):
        from PyQt5.QtWidgets import QSizePolicy
        self.pstyle = mode % 4
        self.clear_layout(self.bl); self.lbl_sep.setVisible(False)
        self.right.removeWidget(self.top_hdr); self.right.removeWidget(self.bar); self.right.removeWidget(self.viewer)
        for l_t in (self.lbl_cur, self.lbl_tot): l_t.setStyleSheet("font-size:11px; opacity:0.8; font-family:monospace;")
        base_sl = "QSlider::groove:horizontal{height:4px;background:rgba(128,128,128,0.28);border-radius:2px;} QSlider::sub-page:horizontal{background:#10B981;border-radius:2px;} QSlider::handle:horizontal{background:#10B981;width:13px;height:13px;margin:-4px 0;border-radius:6px;}"

        self.top_hdr.setVisible(False)
        self.lbl_title.setVisible(True)
        self.lbl_title.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.cmb_reciter.setFixedWidth(260)

        if self.pstyle in (0, 1):
            self.bar.setObjectName("HeroCard" if self.pstyle == 1 else "Card")
            self.cmb_reciter.setStyleSheet("QPushButton{padding:5px 12px; font-size:12px; border-radius:14px; border:none; background:rgba(16,185,129,0.14); text-align:center;} QPushButton::menu-indicator{image:none; width:0px;}" if self.pstyle == 1 else "QPushButton{padding:4px 10px; font-size:12px; border-radius:7px; text-align:center;} QPushButton::menu-indicator{image:none; width:0px;}")
            self.slider.setStyleSheet("QSlider::groove:horizontal{height:3px;background:rgba(16,185,129,0.2);border-radius:1px;} QSlider::sub-page:horizontal{background:#10B981;border-radius:1px;} QSlider::handle:horizontal{background:#10B981;width:9px;height:9px;margin:-3px 0;border-radius:4px;}" if self.pstyle == 1 else base_sl)
            self.bl.setContentsMargins(18,12,18,12); self.bl.setSpacing(10)
            r1 = QHBoxLayout(); r1.setSpacing(12); r1.addWidget(self.lbl_cur); r1.addWidget(self.slider, 1); r1.addWidget(self.lbl_tot)
            r2 = QHBoxLayout(); r2.setSpacing(8)
            r2.addWidget(self.lbl_title, 1)
            ctrl = QHBoxLayout(); ctrl.setSpacing(12); ctrl.addWidget(self.btn_prev); ctrl.addWidget(self.btn_play); ctrl.addWidget(self.btn_next); r2.addLayout(ctrl)
            rb = QHBoxLayout(); rb.addStretch(); rb.addWidget(self.cmb_reciter); r2.addLayout(rb, 1)
            self.bl.addLayout(r1); self.bl.addLayout(r2)
            self.right.addWidget(self.bar); self.right.addWidget(self.viewer)
        elif self.pstyle == 2:
            self.bar.setObjectName("HeroCard"); self.cmb_reciter.setStyleSheet("QPushButton{padding:5px 10px; font-size:12px; border-radius:12px; text-align:center;} QPushButton::menu-indicator{image:none; width:0px;}")
            self.slider.setStyleSheet(base_sl); self.bl.setContentsMargins(18,12,18,12); self.bl.setSpacing(8)
            r_top = QHBoxLayout(); r_top.setSpacing(8)
            r_top.addWidget(self.lbl_title, 1)
            ctrl = QHBoxLayout(); ctrl.setSpacing(12); ctrl.addWidget(self.btn_prev); ctrl.addWidget(self.btn_play); ctrl.addWidget(self.btn_next); r_top.addLayout(ctrl)
            rb = QHBoxLayout(); rb.addStretch(); rb.addWidget(self.cmb_reciter); r_top.addLayout(rb, 1)
            r_bot = QHBoxLayout(); r_bot.setSpacing(10); r_bot.addWidget(self.lbl_cur); r_bot.addWidget(self.slider, 1); r_bot.addWidget(self.lbl_tot)
            self.bl.addLayout(r_top); self.bl.addLayout(r_bot); self.right.addWidget(self.bar); self.right.addWidget(self.viewer)
        elif self.pstyle == 3:
            self.bar.setObjectName("Card"); self.cmb_reciter.setStyleSheet("QPushButton{padding:4px 10px; font-size:12px; border-radius:7px; text-align:center;} QPushButton::menu-indicator{image:none; width:0px;}")
            self.slider.setStyleSheet("QSlider::groove:horizontal{height:3px;background:rgba(128,128,128,0.2);} QSlider::sub-page:horizontal{background:#10B981;} QSlider::handle:horizontal{background:#10B981;width:10px;height:10px;margin:-4px 0;border-radius:5px;}")
            self.bl.setContentsMargins(16,10,16,10); self.bl.setSpacing(8)
            row = QHBoxLayout(); row.setSpacing(8)
            row.addWidget(self.lbl_title, 1)
            ctrl = QHBoxLayout(); ctrl.setSpacing(10); ctrl.addWidget(self.btn_prev); ctrl.addWidget(self.btn_play); ctrl.addWidget(self.btn_next); row.addLayout(ctrl)
            rb = QHBoxLayout(); rb.addStretch(); rb.addWidget(self.cmb_reciter); row.addLayout(rb, 1)
            srow = QHBoxLayout(); srow.setSpacing(10)
            srow.addWidget(self.lbl_cur); srow.addWidget(self.slider, 1); srow.addWidget(self.lbl_tot)
            self.bl.addLayout(row); self.bl.addLayout(srow); self.right.addWidget(self.bar); self.right.addWidget(self.viewer)
        self.bar.style().unpolish(self.bar); self.bar.style().polish(self.bar)

    def fmt_ms(self, ms):
        s = max(0, ms // 1000); return f"{s//60:02d}:{s%60:02d}"
    def on_pos(self, pos):
        if not self.slider.isSliderDown(): self.slider.setValue(pos)
        self.lbl_cur.setText(self.fmt_ms(pos))
        if self.pstyle == 3 and self.player.duration() > 0:
            rem = max(0, self.player.duration() - pos)
            self.lbl_tot.setText(f"-{self.fmt_ms(rem)}")
    def on_dur(self, dur):
        self.slider.setRange(0, dur); self.lbl_tot.setText(self.fmt_ms(dur))
    def on_state(self, st):
        self.btn_play.setText("⏸" if st == QMediaPlayer.PlayingState else "▶")

    def step_surah(self, delta):
        cur_row = self.s_list.currentRow()
        if cur_row < 0:
            for i in range(self.s_list.count()):
                if self.s_list.item(i).data(Qt.UserRole) == self.cur_num: cur_row = i; break
        nxt_row = max(0, min(self.s_list.count() - 1, cur_row + delta))
        if nxt_row == cur_row: return
        it = self.s_list.item(nxt_row)
        nxt = it.data(Qt.UserRole)
        was = self.player.state() == QMediaPlayer.PlayingState; self.stop_audio()
        cur = self.qdata[nxt]; t = cur["name"] if self.lang == "ar" else (cur.get("translation") or cur["transliteration"])
        self.load_surah(nxt, f"{nxt}. {t}")
        self.s_list.setCurrentRow(nxt_row)
        if was: self.toggle_audio()

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize; s = STRINGS.get(lang, STRINGS["en"])
        self.search.setPlaceholderText(s["surah_ph"]); self.btn_play.setToolTip(s["play"])
        fn = f"quran_{lang}.json" if os.path.exists(os.path.join(DATA_DIR, f"quran_{lang}.json")) else "quran_en.json"
        self.qdata = {x["id"]: x for x in json.load(open(os.path.join(DATA_DIR, fn), encoding="utf-8"))}

        prev_mode = self.cmb_sort.currentData() or "mushaf"
        self.cmb_sort.blockSignals(True)
        self.cmb_sort.clear()
        sort_list, _ = QURAN_UI.get(lang, QURAN_UI["en"])
        keys = ["mushaf", "mushaf_rev", "nuzul", "nuzul_rev", "short", "long", "az", "za"]
        opts = list(zip(keys, sort_list))
        for key, lbl in opts: self.cmb_sort.addItem(lbl, key)
        idx = next((i for i, (k, _) in enumerate(opts) if k == prev_mode), 0)
        self.cmb_sort.setCurrentIndex(idx)
        self.cmb_sort.blockSignals(False)

        self.rebuild_list()
        cur = self.qdata.get(self.cur_num, next(iter(self.qdata.values())))
        t = cur["name"] if lang == "ar" else (cur.get("translation") or cur["transliteration"])
        self.load_surah(self.cur_num, f"{self.cur_num}. {t}")

    def tr_key(self, txt):
        order = "abcçdefgğhıijklmnoöprsştuüvyz"
        return [order.index(c) if c in order else ord(c) + 100 for c in txt.lower()]

    def rebuild_list(self):
        if not self.qdata: return
        mode = self.cmb_sort.currentData() or "mushaf"
        items = list(self.qdata.items())
        name_fn = lambda x: x["name"] if self.lang == "ar" else (x.get("translation") or x["transliteration"])

        if mode == "mushaf": items.sort(key=lambda x: x[0])
        elif mode == "mushaf_rev": items.sort(key=lambda x: -x[0])
        elif mode == "nuzul": items.sort(key=lambda x: NUZUL_RANK.get(x[0], 999))
        elif mode == "nuzul_rev": items.sort(key=lambda x: -NUZUL_RANK.get(x[0], 999))
        elif mode == "short": items.sort(key=lambda x: (len(x[1]["verses"]), x[0]))
        elif mode == "long": items.sort(key=lambda x: (-len(x[1]["verses"]), x[0]))
        elif mode == "az": items.sort(key=lambda x: self.tr_key(name_fn(x[1])))
        elif mode == "za": items.sort(key=lambda x: self.tr_key(name_fn(x[1])), reverse=True)

        self.s_list.clear()
        for sid, item in items:
            title = item["name"] if self.lang == "ar" else (item.get("translation") or item["transliteration"])
            v_cnt = len(item["verses"])
            prefix = f"#{NUZUL_RANK[sid]+1} • " if mode in ("nuzul", "nuzul_rev") else f"{sid}. "
            it = QListWidgetItem(f"{prefix}{title} ({v_cnt})")
            it.setData(Qt.UserRole, sid)
            self.s_list.addItem(it)
            if sid == self.cur_num: self.s_list.setCurrentItem(it)
        self.filter_list(self.search.text())

    def filter_list(self, txt):
        for i in range(self.s_list.count()):
            it = self.s_list.item(i); it.setHidden(txt.lower() not in it.text().lower())

    def on_select(self, it):
        self.stop_audio()
        sid = it.data(Qt.UserRole)
        cur = self.qdata[sid]
        t = cur["name"] if self.lang == "ar" else (cur.get("translation") or cur["transliteration"])
        self.load_surah(sid, f"{sid}. {t}")

    def load_surah(self, num, title):
        self.cur_num = num; verses = self.qdata[num]["verses"]
        nuzul_no = NUZUL_RANK.get(num, 0) + 1
        _, sub_fmt = QURAN_UI.get(self.lang, QURAN_UI["en"])
        sub = sub_fmt.format(v=len(verses), n=nuzul_no)
        rich = f"{title}  <span style='font-size:12px; font-weight:normal; opacity:0.65;'>• {sub}</span>"
        self.lbl_title.setText(rich); self.lbl_hdr_only.setText(rich)
        ar_sz = self.fsize + 9
        html = "<table width='100%' cellspacing='0' cellpadding='0'>" + "".join([f"<tr><td align='center' style='padding:14px 12px 18px 12px; border-bottom:1px solid rgba(128,128,128,0.22);'><div dir='rtl' style=\"font-size:{ar_sz}px; line-height:1.6; color:#10B981; font-family:'Amiri','Scheherazade New','Noto Naskh Arabic',serif;\">{v['text']} ﴿{v['id']}﴾</div><div dir='ltr' style='font-size:{self.fsize}px; line-height:1.45; margin-top:4px;'><b>{v['id']}.</b> {v['translation']}</div></td></tr>" for v in verses]) + "</table>"
        self.viewer.setHtml(html)

    def select_reciter(self, name):
        self.cur_reciter = name
        self.cmb_reciter.setText(f"🎙️ {name}")
        self.stop_audio()

    def toggle_audio(self):
        if self.player.state() == QMediaPlayer.PlayingState: self.player.pause()
        else:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                self.player.setMedia(QMediaContent(QUrl(RECITERS[self.cur_reciter].format(self.cur_num))))
            self.player.play()

    def stop_audio(self):
        self.player.stop(); self.player.setMedia(QMediaContent())
        self.slider.setValue(0); self.lbl_cur.setText("00:00"); self.lbl_tot.setText("00:00")
