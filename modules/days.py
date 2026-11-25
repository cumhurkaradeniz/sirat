from datetime import date
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextBrowser
from modules.i18n import STRINGS

DAYS = {
    "tr": [
        ("2026-12-10", "Üç Ayların Başlangıcı (1 Recep)", "<h3>Üç Ayların Başlangıcı</h3><p>Recep, Şaban ve Ramazan aylarını kapsayan manevi arınma mevsimidir.</p><b>Önerilen İbadetler:</b><ul><li>Kaza ve nafile namazlara ağırlık vermek</li><li>Kur'an-ı Kerim tilavetini artırmak</li><li>Pazartesi ve Perşembe günleri oruç tutmak</li><li>Bolca istiğfar (Estağfirullah) ve salavat getirmek</li></ul>"),
        ("2026-12-17", "Regaip Kandili", "<h3>Regaip Kandili</h3><p>Recep ayının ilk Cuma gecesidir; rahmet ve bereket gecesidir.</p><b>Önerilen İbadetler:</b><ul><li>Tesbih ve teheccüd namazı kılmak</li><li>Günahların affı için tövbe ve dua etmek</li><li>Sadaka vermek</li></ul>"),
        ("2027-01-05", "Miraç Kandili", "<h3>Miraç Kandili</h3><p>Beş vakit namazın farz kılındığı mübarek gecedir.</p><b>Önerilen İbadetler:</b><ul><li>Beş vakit namazı huşu ile kılmak</li><li>Bakara Suresi son iki ayetini (Âmenerrasûlü) okumak</li></ul>"),
        ("2027-01-24", "Berat Kandili", "<h3>Berat Kandili</h3><p>Şaban ayının 15. gecesi, günahlardan arınma ve af gecesidir.</p><b>Önerilen İbadetler:</b><ul><li>Geceyi namaz, zikir ve Kur'an ile ihya etmek</li><li>Ertesi gün (Şaban'ın 15. günü) nafile oruç tutmak</li></ul>"),
        ("2027-02-08", "Ramazan-ı Şerif Başlangıcı", "<h3>On Bir Ayın Sultanı Ramazan</h3><p>Oruç, teravih ve Kur'an ayıdır.</p><b>Önerilen İbadetler:</b><ul><li>Sahura kalkıp oruç tutmak</li><li>Teravih namazı kılmak ve mukabele okumak</li><li>Fitre ve zekat ibadetlerini yerine getirmek</li></ul>"),
        ("2027-03-05", "Kadir Gecesi", "<h3>Kadir Gecesi</h3><p>Bin aydan daha hayırlı olduğu müjdelenen gecedir.</p><b>Önerilen İbadetler:</b><ul><li>“Allahümme inneke afüvvün tuhibbü'l-afve fa'fü annî” duasını okumak</li><li>Kur'an-ı Kerim okuyup tefekkür etmek</li></ul>"),
        ("2027-03-08", "Ramazan Bayramı Arifesi", "<h3>Ramazan Bayramı Arifesi</h3><p>Ramazan ayının son günüdür; bayrama hazırlık ve kabir ziyareti günüdür.</p><b>Önerilen İbadetler:</b><ul><li>Fitre sadakasını bayram namazından önce vermek</li><li>Bolca İhlâs Suresi ve istiğfar okumak</li></ul>"),
        ("2027-03-09", "Ramazan Bayramı (3 Gün)", "<h3>Ramazan Bayramı (9–11 Mart 2027)</h3><p>Bir aylık oruç ibadetinin ardından erişilen sevinç ve kardeşlik günleridir.</p><b>Önerilen İbadetler:</b><ul><li>Bayram namazını cemaatle kılmak</li><li>Anne-baba, akraba ve komşuları ziyaret etmek</li></ul>"),
        ("2027-05-15", "Kurban Bayramı Arifesi", "<h3>Kurban Bayramı Arifesi (Teşrik Tekbirleri Başlangıcı)</h3><p>Hacıların Arafat'ta vakfeye durduğu, duaların kabul edildiği çok faziletli bir gündür.</p><b>Önerilen İbadetler:</b><ul><li>Sabah namazından itibaren farz namazların ardından Teşrik Tekbiri getirmek</li><li>Hacda olmayanlar için Arife günü orucu tutmak</li></ul>"),
        ("2027-05-16", "Kurban Bayramı (4 Gün)", "<h3>Kurban Bayramı (16–19 Mayıs 2027)</h3><p>Allah'a yakınlaşma, kurban ibadeti ve paylaşma günleridir.</p><b>Önerilen İbadetler:</b><ul><li>Bayram namazını cemaatle kılmak</li><li>Vacip olan kurbanı kesmek ve etini ihtiyaç sahipleriyle paylaşmak</li><li>Bayramın 4. günü ikindi namazına kadar Teşrik Tekbirlerine devam etmek</li></ul>"),
        ("2027-06-06", "Hicri Yılbaşı (1 Muharrem 1449)", "<h3>Hicri Yılbaşı</h3><p>Peygamber Efendimiz'in Mekke'den Medine'ye hicretini esas alan Hicri takvimin ilk günüdür.</p><b>Önerilen İbadetler:</b><ul><li>Muharrem ayında nafile oruç tutmak</li><li>Yeni yılın hayırlara vesile olması için dua etmek</li></ul>"),
        ("2027-06-15", "Aşure Günü (10 Muharrem)", "<h3>Aşure Günü</h3><p>Muharrem ayının 10. günüdür; birlik, bereket ve şükür günüdür.</p><b>Önerilen İbadetler:</b><ul><li>9-10. veya 10-11. günlerde oruç tutmak</li><li>Aileye ve komşulara ikramda bulunmak, sadaka vermek</li></ul>"),
        ("2027-08-14", "Mevlid Kandili", "<h3>Mevlid Kandili</h3><p>Âlemlere rahmet olarak gönderilen Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) dünyayı teşrif ettiği gecedir.</p><b>Önerilen İbadetler:</b><ul><li>Bolca Salât-ü Selâm getirmek</li><li>Peygamber Efendimiz'in hayatını (Siyer) ve ahlakını okumak</li></ul>")
    ],
    "en": [
        ("2026-12-10", "Start of Three Holy Months", "<h3>Beginning of Rajab</h3><p>Season of spiritual renewal.</p><b>Recommended Worship:</b><ul><li>Voluntary (Nafl) prayers and Quran recitation</li><li>Fasting on Mondays and Thursdays</li></ul>"),
        ("2026-12-17", "Laylat al-Raghaib", "<h3>Laylat al-Raghaib</h3><p>First Friday night of Rajab.</p><b>Recommended Worship:</b><ul><li>Night prayers (Tahajjud), repentance, and charity</li></ul>"),
        ("2027-01-05", "Isra and Mi'raj", "<h3>Night of Isra and Mi'raj</h3><p>The night five daily prayers were ordained.</p>"),
        ("2027-01-24", "Laylat al-Bara'ah", "<h3>Night of Forgiveness (Mid-Sha'ban)</h3><p>Night of seeking mercy and fasting the next day.</p>"),
        ("2027-02-08", "Start of Ramadan", "<h3>Blessed Month of Ramadan</h3><p>Month of fasting, Taraweeh prayers, and Zakat.</p>"),
        ("2027-03-05", "Laylat al-Qadr", "<h3>Night of Decree</h3><p>Better than a thousand months.</p>"),
        ("2027-03-09", "Eid al-Fitr (3 Days)", "<h3>Eid al-Fitr (March 9–11, 2027)</h3><p>Eid prayer, Zakat al-Fitr, and family visits.</p>"),
        ("2027-05-15", "Day of Arafah", "<h3>Day of Arafah</h3><p>Fasting on the Day of Arafah and beginning Takbir al-Tashreeq after Fajr.</p>"),
        ("2027-05-16", "Eid al-Adha (4 Days)", "<h3>Eid al-Adha (May 16–19, 2027)</h3><p>Eid prayer, Qurbani (Udhiyah) sacrifice, sharing with the needy, and Takbir al-Tashreeq.</p>"),
        ("2027-06-06", "Islamic New Year (1 Muharram)", "<h3>Islamic New Year 1449 AH</h3><p>Commemorating the Hijrah; voluntary fasting in Muharram.</p>"),
        ("2027-06-15", "Day of Ashura (10 Muharram)", "<h3>Day of Ashura</h3><p>Fasting on the 9th–10th or 10th–11th of Muharram and giving charity.</p>"),
        ("2027-08-14", "Mawlid al-Nabi", "<h3>Mawlid al-Nabi</h3><p>Sending abundant Salawat upon Prophet Muhammad (peace be upon him) and studying his Seerah.</p>")
    ]
}

class DaysWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        l = QHBoxLayout(self); l.setContentsMargins(16,16,16,16); l.setSpacing(14)
        self.lst = QListWidget(); self.lst.itemClicked.connect(lambda it: self.view.setHtml(self.wrap(it.data(Qt.UserRole)))); l.addWidget(self.lst, 1)
        self.view = QTextBrowser(); self.view.setStyleSheet("border:none;"); l.addWidget(self.view, 2)
        self.set_prefs(lang, fsize)

    def wrap(self, html): return f"<div style='font-size:{self.fsize}px; line-height:1.6;'>{html}</div>"

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        self.lst.clear(); today = date.today(); s = STRINGS.get(lang, STRINGS["en"])
        for dt_str, title, desc in DAYS.get(lang, DAYS["en"]):
            diff = (date.fromisoformat(dt_str) - today).days
            tag = s["days_left"].format(d=diff) if diff > 0 else (s["today"] if diff == 0 else s["passed"])
            it = QListWidgetItem(f"{dt_str} • {title}\n{tag}"); it.setData(Qt.UserRole, desc); self.lst.addItem(it)
        self.lst.setCurrentRow(0); self.view.setHtml(self.wrap(self.lst.item(0).data(Qt.UserRole)))
