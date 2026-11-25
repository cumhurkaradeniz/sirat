import os, json, base64
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
                             QTextBrowser, QPushButton, QLabel, QComboBox, QLineEdit, QFrame)
from modules.i18n import STRINGS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
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

class QuranWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.lang, self.fsize, self.cur_num, self.qdata = lang, fsize, 1, {}
        self.player = QMediaPlayer()
        root = QHBoxLayout(self); root.setContentsMargins(16,16,16,16); root.setSpacing(14)

        left = QVBoxLayout(); root.addLayout(left, 1)
        self.search = QLineEdit(); self.search.textChanged.connect(self.filter_list); left.addWidget(self.search)
        self.s_list = QListWidget(); self.s_list.itemClicked.connect(self.on_select); left.addWidget(self.s_list)

        right = QVBoxLayout(); root.addLayout(right, 3)
        bar = QFrame(); bar.setObjectName("Card"); bl = QHBoxLayout(bar)
        self.lbl_title = QLabel(""); bl.addWidget(self.lbl_title); bl.addStretch()
        self.cmb_reciter = QComboBox(); self.cmb_reciter.addItems(RECITERS.keys()); bl.addWidget(self.cmb_reciter)
        self.btn_play = QPushButton(); self.btn_play.setObjectName("ActionBtn"); self.btn_play.clicked.connect(self.toggle_audio); bl.addWidget(self.btn_play)
        btn_stop = QPushButton("■"); btn_stop.clicked.connect(self.stop_audio); bl.addWidget(btn_stop)
        right.addWidget(bar)
        self.viewer = QTextBrowser(); self.viewer.setStyleSheet("border:none;"); right.addWidget(self.viewer)
        self.set_prefs(lang, fsize)

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        s = STRINGS.get(lang, STRINGS["en"])
        self.search.setPlaceholderText(s["surah_ph"])
        self.btn_play.setText(s["pause"] if self.player.state() == QMediaPlayer.PlayingState else s["play"])
        fn = "quran_tr.json" if lang == "tr" else "quran_en.json"
        self.qdata = {x["id"]: x for x in json.load(open(os.path.join(DATA_DIR, fn), encoding="utf-8"))}
        self.s_list.clear()
        for sid, item in sorted(self.qdata.items()):
            title = item["translation"] if lang == "tr" else item["transliteration"]
            it = QListWidgetItem(f"{sid}. {title}"); it.setData(Qt.UserRole, sid); self.s_list.addItem(it)
        cur = self.qdata.get(self.cur_num, next(iter(self.qdata.values())))
        t = cur["translation"] if lang == "tr" else cur["transliteration"]
        self.load_surah(self.cur_num, f"{self.cur_num}. {t}")

    def filter_list(self, txt):
        for i in range(self.s_list.count()):
            it = self.s_list.item(i); it.setHidden(txt.lower() not in it.text().lower())

    def on_select(self, it):
        self.stop_audio(); self.load_surah(it.data(Qt.UserRole), it.text())

    def load_surah(self, num, title):
        self.cur_num = num; self.lbl_title.setText(f"<b>{title}</b>")
        ar_sz = self.fsize + 9
        verses = self.qdata[num]["verses"]
        html = "".join([f"<div style='margin-bottom:14px; padding-bottom:8px; border-bottom:1px solid rgba(128,128,128,0.2);'><div dir='rtl' align='right' style='font-size:{ar_sz}px; line-height:1.8; color:#10B981; padding:4px 8px;'>{v['text']} ﴿{v['id']}﴾</div><div dir='ltr' align='left' style='font-size:{self.fsize}px; line-height:1.5; margin-top:6px; padding:0 8px;'><b>{v['id']}.</b> {v['translation']}</div></div>" for v in verses])
        self.viewer.setHtml(html)

    def toggle_audio(self):
        s = STRINGS.get(self.lang, STRINGS["en"])
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause(); self.btn_play.setText(s["resume"])
        else:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                self.player.setMedia(QMediaContent(QUrl(RECITERS[self.cmb_reciter.currentText()].format(self.cur_num))))
            self.player.play(); self.btn_play.setText(s["pause"])

    def stop_audio(self):
        self.player.stop(); self.player.setMedia(QMediaContent())
        self.btn_play.setText(STRINGS.get(self.lang, STRINGS["en"])["play"])
