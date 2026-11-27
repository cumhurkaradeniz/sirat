import os, json, uuid
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
                             QComboBox, QProgressBar, QDialog, QLineEdit, QSpinBox, QFormLayout)
from modules.i18n import STRINGS, get_bundle

CFG = os.path.expanduser("~/.sirat_config.json")

DHIKR_UI = {
    "tr": ("+ Ekle", "Okunuş:", "Meal:", "Aşama {s} ({r})", "Özel Zikir Ekle", "Zikir Adı *:", "Arapça:", "Okunuş:", "Meal:", "Hedef:", "Kaydet", "İptal",
           ["Namaz Tesbihatı (33×3)", "Sübhanallahi ve bihamdihi", "Estağfirullah el-Azîm", "Salavat-ı Şerife", "Kelime-i Tevhid", "Kelime-i Temcid", "Hasbünallahu ve ni'mel vekîl", "Bâkıyât-ı Sâlihât", "Hz. Yunus Duası"],
           ["Allah'ı tüm noksanlıklardan tenzih ederim.", "Hamd yalnız Allah'a mahsustur.", "Allah en büyüktür.", "Allah'ı hamd ile tüm noksanlıklardan tenzih ederim.", "Yüce Allah'tan bağışlanma dilerim.", "Allah'ım! Efendimiz Muhammed'e salât ve selâm eyle.", "Allah'tan başka ilah yoktur, Muhammed Allah'ın elçisidir.", "Güç ve kuvvet yalnızca yüce Allah'ın yardımıyladır.", "Allah bize yeter, O ne güzel vekildir.", "Allah münezzehtir, hamd Allah'adır, O'ndan başka ilah yoktur ve O en büyüktür.", "Senden başka ilah yoktur. Seni tenzih ederim. Gerçekten ben zalimlerden oldum."]),
    "en": ("+ Add", "Transliteration:", "Meaning:", "Stage {s} ({r})", "Add Custom Dhikr", "Name *:", "Arabic:", "Reading:", "Meaning:", "Target:", "Save", "Cancel",
           ["Post-Prayer Tasbih (33×3)", "SubhanAllahi wa bihamdihi", "Astaghfirullah al-Azim", "Salawat upon the Prophet ﷺ", "Kalima Tayyibah", "Hawqala", "HasbunAllahu wa ni'mal Wakil", "Al-Baqiyat as-Salihat", "Dua of Prophet Yunus (AS)"],
           ["Glory be to Allah.", "All praise is due to Allah.", "Allah is the Greatest.", "Glory and praise be to Allah.", "I seek forgiveness from Allah, the Almighty.", "O Allah, send blessings upon our Master Muhammad.", "There is no deity except Allah, and Muhammad is His Messenger.", "There is no power and no strength except with Allah.", "Allah is sufficient for us, and He is the best Disposer of affairs.", "Glory be to Allah, all praise is for Allah, there is no god but Allah, and Allah is the Greatest.", "There is no deity except You; exalted are You. Indeed, I have been of the wrongdoers."]),
    "fr": ("+ Ajouter", "Translittération :", "Signification :", "Étape {s} ({r})", "Ajouter un Dhikr", "Nom * :", "Arabe :", "Lecture :", "Sens :", "Objectif :", "Enregistrer", "Annuler",
           ["Tasbih après la prière (33×3)", "SubhanAllahi wa bihamdihi", "Astaghfirullah al-Azim", "Salawat sur le Prophète ﷺ", "Kalima Tayyibah", "Hawqala", "HasbunAllahu wa ni'mal Wakil", "Al-Baqiyat as-Salihat", "Invocation de Yunus (AS)"],
           ["Gloire à Allah.", "Louange à Allah.", "Allah est le Plus Grand.", "Gloire et louange à Allah.", "Je demande pardon à Allah, le Tout-Puissant.", "Ô Allah, bénis notre Maître Muhammad.", "Il n'y a de divinité qu'Allah et Muhammad est Son Messager.", "Il n'y a de force ni de puissance qu'en Allah.", "Allah nous suffit, Il est notre meilleur Garant.", "Gloire à Allah, louange à Allah, il n'y a de dieu qu'Allah et Allah est le Plus Grand.", "Pas de divinité à part Toi ! Pureté à Toi ! J'ai été vraiment du nombre des injustes."]),
    "es": ("+ Añadir", "Transliteración:", "Significado:", "Etapa {s} ({r})", "Añadir Dhikr", "Nombre *:", "Árabe:", "Lectura:", "Significado:", "Meta:", "Guardar", "Cancelar",
           ["Tasbih tras la oración (33×3)", "SubhanAllahi wa bihamdihi", "Astaghfirullah al-Azim", "Salawat sobre el Profeta ﷺ", "Kalima Tayyibah", "Hawqala", "HasbunAllahu wa ni'mal Wakil", "Al-Baqiyat as-Salihat", "Súplica de Yunus (AS)"],
           ["Gloria a Allah.", "Toda alabanza pertenece a Allah.", "Allah es el Más Grande.", "Gloria y alabanza a Allah.", "Pido perdón a Allah, el Todopoderoso.", "Oh Allah, bendice a nuestro Maestro Muhammad.", "No hay más divinidad que Allah y Muhammad es Su Mensajero.", "No hay poder ni fuerza sino en Allah.", "Allah nos basta y es el mejor Protector.", "Gloria a Allah, alabanza a Allah, no hay dios sino Allah y Allah es el Más Grande.", "No hay más divinidad que Tú. ¡Gloria a Ti! Ciertamente he sido de los injustos."]),
    "pt": ("+ Adicionar", "Transliteração:", "Significado:", "Etapa {s} ({r})", "Adicionar Dhikr", "Nome *:", "Árabe:", "Leitura:", "Significado:", "Meta:", "Salvar", "Cancelar",
           ["Tasbih após a oração (33×3)", "SubhanAllahi wa bihamdihi", "Astaghfirullah al-Azim", "Salawat sobre o Profeta ﷺ", "Kalima Tayyibah", "Hawqala", "HasbunAllahu wa ni'mal Wakil", "Al-Baqiyat as-Salihat", "Súplica de Yunus (AS)"],
           ["Glória a Allah.", "Todo louvor pertence a Allah.", "Allah é o Maior.", "Glória e louvor a Allah.", "Peço perdão a Allah, o Todo-Poderoso.", "Ó Allah, abençoa nosso Mestre Muhammad.", "Não há divindade além de Allah e Muhammad é Seu Mensageiro.", "Não há poder nem força senão em Allah.", "Allah nos basta e é o melhor Protetor.", "Glória a Allah, louvor a Allah, não há deus além de Allah e Allah é o Maior.", "Não há divindade além de Ti! Glória a Ti! De fato, fui dos injustos."]),
    "id": ("+ Tambah", "Bacaan:", "Arti:", "Tahap {s} ({r})", "Tambah Dzikir", "Nama *:", "Arab:", "Bacaan:", "Arti:", "Target:", "Simpan", "Batal",
           ["Tasbih Setelah Shalat (33×3)", "Subhanallahi wa bihamdihi", "Astaghfirullah al-Azim", "Shalawat Nabi ﷺ", "Kalimat Tayyibah", "Hauqalah", "Hasbunallahu wa ni'mal Wakil", "Al-Baqiyat as-Salihat", "Doa Nabi Yunus (AS)"],
           ["Maha Suci Allah.", "Segala puji bagi Allah.", "Allah Maha Besar.", "Maha Suci Allah dan segala puji bagi-Nya.", "Aku memohon ampun kepada Allah Yang Maha Agung.", "Ya Allah, limpahkan shalawat kepada Nabi Muhammad.", "Tiada tuhan selain Allah, Muhammad utusan Allah.", "Tiada daya dan upaya kecuali dengan pertolongan Allah.", "Cukuplah Allah bagi kami dan Dia sebaik-baik Pelindung.", "Maha Suci Allah, segala puji bagi Allah, tiada tuhan selain Allah, Allah Maha Besar.", "Tiada tuhan selain Engkau, Maha Suci Engkau, sungguh aku termasuk orang yang zalim."]),
    "ru": ("+ Добавить", "Транскрипция:", "Перевод:", "Этап {s} ({r})", "Добавить зикр", "Название *:", "Арабский:", "Чтение:", "Значение:", "Цель:", "Сохранить", "Отмена",
           ["Тасбих после намаза (33×3)", "Субханаллахи ва бихамдихи", "Астагфируллах аль-Азым", "Салават Пророку ﷺ", "Калима Таййиба", "Хавкала", "Хасбуналлаху ва ни'маль Вакиль", "Аль-Бакият ас-Салихат", "Дуа пророка Юнуса (мир ему)"],
           ["Слава Аллаху.", "Хвала Аллаху.", "Аллах Велик.", "Слава и хвала Аллаху.", "Прошу прощения у Великого Аллаха.", "О Аллах, благослови нашего господина Мухаммада.", "Нет божества, кроме Аллаха, и Мухаммад — Посланник Аллаха.", "Нет мощи и силы ни у кого, кроме Аллаха.", "Достаточно нам Аллаха, и Он прекрасный Покровитель.", "Слава Аллаху, хвала Аллаху, нет бога, кроме Аллаха, и Аллах Велик.", "Нет божества, кроме Тебя! Пречист Ты! Воистину, я был одним из беззаконников."]),
    "zh": ("+ 添加", "音译：", "含义：", "第 {s} 阶段 ({r})", "添加自定义赞词", "名称 *：", "阿拉伯语：", "读音：", "含义：", "目标：", "保存", "取消",
           ["礼拜后赞念 (33×3)", "SubhanAllahi wa bihamdihi", "Astaghfirullah al-Azim", "赞圣词 ﷺ", "清真言", "豪格莱", "HasbunAllahu wa ni'mal Wakil", "四大赞词", "尤努斯先知祈祷词"],
           ["赞美真主超绝万物。", "一切赞颂全归真主。", "真主至大。", "赞美真主超绝万物，一切赞颂全归真主。", "我向伟大的真主求饶。", "真主啊！求你赐福我们的领袖穆罕默德。", "万物非主，唯有真主；穆罕默德是真主的使者。", "无法无力，唯凭真主。", "真主是使我们满足的，他是最好的监护者。", "赞主超绝，赞颂归主，万物非主唯有真主，真主至大。", "除你之外绝无应受崇拜的，赞你超绝，我确是不义者。"]),
    "ar": ("+ إضافة", "النطق:", "المعنى:", "المرحلة {s} ({r})", "إضافة ذكر خاص", "اسم الذكر *:", "العربية:", "النطق:", "المعنى:", "الهدف:", "حفظ", "إلغاء",
           ["تسبيح بعد الصلاة (33×3)", "سبحان الله وبحمده", "أستغفر الله العظيم", "الصلاة على النبي ﷺ", "كلمة التوحيد", "الحوقلة", "حسبنا الله ونعم الوكيل", "الباقيات الصالحات", "دعاء يونس عليه السلام"],
           ["سبحان الله وتنزيهاً له عن كل نقص.", "الحمد والثناء لله وحده.", "الله أكبر من كل شيء.", "سبحان الله وبحمده عدد خلقه.", "أستغفر الله العظيم وأتوب إليه.", "اللهم صلِّ وسلم على سيدنا محمد.", "لا إله إلا الله محمد رسول الله.", "لا حول ولا قوة إلا بالله العلي العظيم.", "حسبنا الله ونعم الوكيل.", "سبحان الله والحمد لله ولا إله إلا الله والله أكبر.", "لا إله إلا أنت سبحانك إني كنت من الظالمين."]),
    "ur": ("+ شامل کریں", "تلفظ:", "ترجمہ:", "مرحلہ {s} ({r})", "نیا ذکر شامل کریں", "ذکر کا نام *:", "عربی:", "تلفظ:", "ترجمہ:", "ہدف:", "محفوظ کریں", "منسوخ",
           ["نماز کے بعد تسبیح (33×3)", "سبحان اللہ وبحمدہ", "استغفر اللہ العظیم", "درودِ پاک ﷺ", "کلمہ طیبہ", "حوقلہ", "حسبنا اللہ ونعم الوکیل", "باقیاتِ صالحات", "دعائے یونس علیہ السلام"],
           ["اللہ ہر عیب سے پاک ہے۔", "تمام تعریفیں اللہ ہی کے لیے ہیں۔", "اللہ سب سے بڑا ہے۔", "اللہ پاک ہے اور تمام تعریفیں اسی کے لیے ہیں۔", "میں عظمت والے اللہ سے بخشش مانگتا ہوں۔", "اے اللہ! ہمارے سردار محمد ﷺ پر رحمت نازل فرما۔", "اللہ کے سوا کوئی معبود نہیں، محمد ﷺ اللہ کے رسول ہیں۔", "نیکی کرنے کی طاقت اور برائی سے بچنے کی قوت صرف اللہ کی توفیق سے ہے۔", "ہمیں اللہ ہی کافی ہے اور وہ بہترین کارساز ہے۔", "اللہ پاک ہے، سب تعریف اللہ کے لیے ہے، اللہ کے سوا کوئی معبود نہیں اور اللہ سب سے بڑا ہے۔", "تیرے سوا کوئی معبود نہیں، تو پاک ہے، بے شک میں قصورواروں میں سے ہوں۔"])
}

TASBIH_AR = ["سُبْحَانَ اللّٰهِ", "اَلْحَمْدُ لِلّٰهِ", "اَللّٰهُ اَكْبَرُ"]
TASBIH_READ = ["SubhanAllah", "Alhamdulillah", "Allahu Akbar"]

DEFAULT_DHIKRS = [
    {"id": "tasbih", "ar": "", "r": "", "target": 99},
    {"id": "subhan", "ar": "سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ", "r": "SubhanAllahi wa bihamdihi", "target": 100},
    {"id": "istighfar", "ar": "اَسْتَغْفِرُ اللّٰهَ الْعَظِيمَ", "r": "Astaghfirullah al-Azim", "target": 100},
    {"id": "salawat", "ar": "اَللّٰهُمَّ صَلِّ عَلٰى سَيِّدِنَا مُحَمَّدٍ", "r": "Allahumma salli ala sayyidina Muhammad", "target": 100},
    {"id": "tahlil", "ar": "لَا اِلٰهَ اِلَّا اللّٰهُ مُحَمَّدٌ رَسُولُ اللّٰهِ", "r": "La ilaha illallah Muhammadur rasulullah", "target": 100},
    {"id": "hawqala", "ar": "لَا حَوْلَ وَلَا قُوَّةَ اِلَّا بِاللّٰهِ", "r": "La hawla wa la quwwata illa billah", "target": 100},
    {"id": "hasbunallah", "ar": "حَسْبُنَا اللّٰهُ وَنِعْمَ الْوَكِيلُ", "r": "HasbunAllahu wa ni'mal Wakil", "target": 100},
    {"id": "baqiyat", "ar": "سُبْحَانَ اللّٰهِ وَالْحَمْدُ لِلّٰهِ وَلَا اِلٰهَ اِلَّا اللّٰهُ وَاللّٰهُ اَكْبَرُ", "r": "SubhanAllah walhamdulillah wa la ilaha illallah wallahu Akbar", "target": 100},
    {"id": "yunus", "ar": "لَا اِلٰهَ اِلَّا اَنْتَ سُبْحَانَكَ اِنِّي كُنْتُ مِنَ الظَّالِمِينَ", "r": "La ilaha illa anta subhanaka inni kuntu minaz-zalimin", "target": 100}
]

class AddDhikrDialog(QDialog):
    def __init__(self, lang="tr", parent=None):
        super().__init__(parent)
        ui = get_bundle(lang)["dhikr"]
        self.setWindowTitle(ui[4])
        self.setFixedWidth(400)
        lay = QVBoxLayout(self); form = QFormLayout(); form.setSpacing(10)
        self.in_name = QLineEdit(); self.in_ar = QLineEdit()
        self.in_read = QLineEdit(); self.in_mean = QLineEdit()
        self.in_tgt = QSpinBox(); self.in_tgt.setRange(1, 100000); self.in_tgt.setValue(100)
        form.addRow(ui[5], self.in_name); form.addRow(ui[6], self.in_ar)
        form.addRow(ui[7], self.in_read); form.addRow(ui[8], self.in_mean); form.addRow(ui[9], self.in_tgt)
        lay.addLayout(form)
        btns = QHBoxLayout()
        b_ok = QPushButton(ui[10]); b_ok.setObjectName("ActionBtn"); b_ok.clicked.connect(self.accept)
        b_no = QPushButton(ui[11]); b_no.setObjectName("MiniBtn"); b_no.clicked.connect(self.reject)
        btns.addStretch(); btns.addWidget(b_no); btns.addWidget(b_ok); lay.addLayout(btns)

class DhikrWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.lang, self.fsize = lang, fsize
        self.cfg = json.load(open(CFG)) if os.path.exists(CFG) else {}
        self.counts = self.cfg.get("dhikr_counts", {})
        self.total = self.cfg.get("dhikr_total", 0)
        self.custom_dhikrs = self.cfg.get("custom_dhikrs", [])
        self.init_ui(); self.set_prefs(lang, fsize)

    def all_dhikrs(self): return DEFAULT_DHIKRS + self.custom_dhikrs

    def save_state(self):
        c = json.load(open(CFG)) if os.path.exists(CFG) else {}
        c["dhikr_counts"] = self.counts; c["dhikr_total"] = self.total; c["custom_dhikrs"] = self.custom_dhikrs
        json.dump(c, open(CFG, "w"))

    def init_ui(self):
        root = QVBoxLayout(self); root.setContentsMargins(28,12,28,24); root.setSpacing(16)
        top = QHBoxLayout(); top.setSpacing(8)
        self.cmb = QComboBox(); self.cmb.currentIndexChanged.connect(self.refresh)
        self.btn_add = QPushButton(); self.btn_add.setObjectName("MiniBtn"); self.btn_add.clicked.connect(self.add_custom)
        self.btn_del = QPushButton("🗑"); self.btn_del.setObjectName("MiniBtn"); self.btn_del.setFixedWidth(36); self.btn_del.clicked.connect(self.del_custom)
        self.btn_rst = QPushButton(); self.btn_rst.setObjectName("MiniBtn"); self.btn_rst.clicked.connect(self.reset_cur)
        top.addWidget(self.cmb, 1); top.addWidget(self.btn_add); top.addWidget(self.btn_del); top.addWidget(self.btn_rst); root.addLayout(top)

        info = QFrame(); info.setObjectName("Card"); il = QVBoxLayout(info); il.setContentsMargins(20,18,20,18); il.setSpacing(8)
        self.lbl_ar = QLabel(); self.lbl_ar.setAlignment(Qt.AlignCenter); self.lbl_ar.setWordWrap(True)
        self.lbl_lat = QLabel(); self.lbl_lat.setAlignment(Qt.AlignCenter); self.lbl_lat.setWordWrap(True)
        self.lbl_tr = QLabel(); self.lbl_tr.setAlignment(Qt.AlignCenter); self.lbl_tr.setWordWrap(True)
        il.addWidget(self.lbl_ar); il.addWidget(self.lbl_lat); il.addWidget(self.lbl_tr); root.addWidget(info)

        hero = QFrame(); hero.setObjectName("HeroCard"); hl = QVBoxLayout(hero); hl.setContentsMargins(24,24,24,24); hl.setSpacing(12)
        self.lbl_stage = QLabel(); self.lbl_stage.setAlignment(Qt.AlignCenter); self.lbl_stage.setStyleSheet("color:#10B981; font-weight:bold; background:transparent;")
        self.lbl_cnt = QLabel("0"); self.lbl_cnt.setAlignment(Qt.AlignCenter); self.lbl_cnt.setStyleSheet("font-size:56px; font-family:'JetBrains Mono','Ubuntu Mono',monospace; font-weight:bold; background:transparent;")
        self.pbar = QProgressBar(); self.pbar.setTextVisible(False); self.pbar.setFixedHeight(8)
        self.pbar.setStyleSheet("QProgressBar{background:rgba(128,128,128,0.2);border-radius:4px;} QProgressBar::chunk{background:#10B981;border-radius:4px;}")
        sub_row = QHBoxLayout(); sub_row.setSpacing(8)
        self.lbl_sub = QLabel(); self.lbl_sub.setStyleSheet("opacity:0.75; background:transparent;")
        self.btn_rst_tot = QPushButton("↺"); self.btn_rst_tot.setObjectName("MiniBtn")
        self.btn_rst_tot.setFixedSize(26, 22)
        self.btn_rst_tot.setStyleSheet("padding:0px; font-size:13px; border-radius:6px;")
        self.btn_rst_tot.clicked.connect(self.reset_total)
        sub_row.addStretch(); sub_row.addWidget(self.lbl_sub); sub_row.addWidget(self.btn_rst_tot); sub_row.addStretch()
        hl.addWidget(self.lbl_stage); hl.addWidget(self.lbl_cnt); hl.addWidget(self.pbar); hl.addLayout(sub_row)
        root.addWidget(hero, 1)

        self.btn_tap = QPushButton(); self.btn_tap.setObjectName("ActionBtn"); self.btn_tap.setMinimumHeight(54)
        self.btn_tap.setStyleSheet("font-size:18px; border-radius:14px;")
        self.btn_tap.clicked.connect(self.increment); root.addWidget(self.btn_tap)

    def reload_combo(self, sel_idx=0):
        self.cmb.blockSignals(True); self.cmb.clear()
        ui = get_bundle(self.lang)["dhikr"]
        for i, d in enumerate(self.all_dhikrs()):
            if d.get("custom"):
                self.cmb.addItem("★ " + d["tr_n"])
            else:
                self.cmb.addItem(ui[12][i])
        self.cmb.setCurrentIndex(max(0, min(self.cmb.count() - 1, sel_idx)))
        self.cmb.blockSignals(False)

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        s = STRINGS.get(lang, STRINGS["en"])
        ui = get_bundle(lang)["dhikr"]
        self.reload_combo(max(0, self.cmb.currentIndex()))
        self.btn_add.setText(ui[0])
        self.btn_rst.setText(s["dhikr_rst"])
        self.btn_tap.setText(s["dhikr_tap"])
        self.lbl_ar.setStyleSheet(f"font-size:{fsize+12}px; color:#10B981; font-weight:bold; font-family:'Amiri','Scheherazade New','Noto Naskh Arabic',serif; background:transparent;")
        self.lbl_lat.setStyleSheet(f"font-size:{fsize+1}px; background:transparent;")
        self.lbl_tr.setStyleSheet(f"font-size:{fsize}px; opacity:0.85; background:transparent;")
        self.refresh()

    def add_custom(self):
        dlg = AddDhikrDialog(self.lang, self)
        if dlg.exec_() == QDialog.Accepted and dlg.in_name.text().strip():
            nm = dlg.in_name.text().strip()
            rd = dlg.in_read.text().strip() or nm
            mn = dlg.in_mean.text().strip() or "-"
            item = {"id": "c_" + uuid.uuid4().hex[:8], "custom": True, "ar": dlg.in_ar.text().strip(),
                    "tr_n": nm, "r": rd, "m": mn, "target": dlg.in_tgt.value()}
            self.custom_dhikrs.append(item); self.save_state()
            self.reload_combo(len(self.all_dhikrs()) - 1); self.refresh()

    def del_custom(self):
        d = self.all_dhikrs()[max(0, self.cmb.currentIndex())]
        if not d.get("custom"): return
        self.custom_dhikrs = [x for x in self.custom_dhikrs if x["id"] != d["id"]]
        self.counts.pop(d["id"], None); self.save_state()
        self.reload_combo(0); self.refresh()

    def refresh(self):
        idx = max(0, self.cmb.currentIndex())
        d = self.all_dhikrs()[idx]
        self.btn_del.setVisible(bool(d.get("custom")))
        c = self.counts.get(d["id"], 0); tgt = d["target"]
        s = STRINGS.get(self.lang, STRINGS["en"])
        ui = get_bundle(self.lang)["dhikr"]
        if d["id"] == "tasbih":
            st_idx = (c // 33) % 3
            ar_txt = TASBIH_AR[st_idx]
            read_txt = TASBIH_READ[st_idx]
            mean_txt = ui[13][st_idx]
            ranges = ["1–33", "34–66", "67–99"]
            self.lbl_stage.setText(ui[3].format(s=st_idx+1, r=ranges[st_idx]))
        elif d.get("custom"):
            ar_txt = d.get("ar", ""); read_txt = d["r"]; mean_txt = d["m"]
            self.lbl_stage.setText(d["tr_n"])
        else:
            ar_txt = d.get("ar", ""); read_txt = d["r"]; mean_txt = ui[13][idx + 2]
            self.lbl_stage.setText(ui[12][idx])

        self.lbl_ar.setVisible(bool(ar_txt)); self.lbl_ar.setText(ar_txt)
        self.lbl_lat.setText(f"<b>{ui[1]}</b> <i>{read_txt}</i>")
        self.lbl_tr.setText(f"<b>{ui[2]}</b> {mean_txt}")
        self.lbl_cnt.setText(str(c))
        self.pbar.setMaximum(tgt); self.pbar.setValue(c % tgt if c % tgt != 0 or c == 0 else tgt)
        self.lbl_sub.setText(s["dhikr_stat"].format(cur=c, tgt=tgt, tot=self.total))

    def increment(self):
        d = self.all_dhikrs()[max(0, self.cmb.currentIndex())]
        self.counts[d["id"]] = self.counts.get(d["id"], 0) + 1
        self.total += 1; self.save_state(); self.refresh()

    def reset_cur(self):
        d = self.all_dhikrs()[max(0, self.cmb.currentIndex())]
        self.counts[d["id"]] = 0; self.save_state(); self.refresh()

    def reset_total(self):
        self.total = 0; self.save_state(); self.refresh()
