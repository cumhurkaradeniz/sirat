import os
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont, QPen
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextBrowser

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

from PyQt5.QtGui import QLinearGradient, QRadialGradient

def draw_figure(p, cx, step, female=False):
    skin = QColor("#F1C6A7")
    skin_s = QColor("#D49E7A")
    robe1 = QColor("#8B5CF6") if female else QColor("#14B8A6")
    robe2 = QColor("#4C1D95") if female else QColor("#0F766E")
    hijab = QColor("#F8FAFC") if female else QColor("#FFFFFF")
    rug1 = QColor("#EDE9FE") if female else QColor("#CCFBF1")
    rug2 = QColor("#C4B5FD") if female else QColor("#5EEAD4")

    # Perspektifli Seccade
    rug_path = QPainterPath()
    rug_path.moveTo(cx - 52, 248); rug_path.lineTo(cx + 52, 248)
    rug_path.lineTo(cx + 62, 266); rug_path.lineTo(cx - 62, 266); rug_path.closeSubpath()
    rg = QLinearGradient(cx, 248, cx, 266); rg.setColorAt(0, rug1); rg.setColorAt(1, rug2)
    p.setPen(QPen(robe2, 1.2)); p.setBrush(rg); p.drawPath(rug_path)

    p.setPen(QPen(QColor("#1E293B"), 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    def head(hx, hy, tilt=0):
        p.save(); p.translate(hx, hy); p.rotate(tilt)
        if female:
            sh = QPainterPath()
            sh.moveTo(-18, -8); sh.cubicTo(-18, -28, 18, -28, 18, -8)
            sh.cubicTo(22, 18, 18, 42, 0, 46); sh.cubicTo(-18, 42, -22, 18, -18, -8)
            p.setBrush(hijab); p.drawPath(sh)
            p.setBrush(skin); p.drawEllipse(QRectF(-10, -10, 20, 24))
        else:
            p.setBrush(skin); p.drawEllipse(QRectF(-10, -10, 20, 24))
            cap = QPainterPath(); cap.moveTo(-10, -3); cap.quadTo(0, -18, 10, -3); cap.closeSubpath()
            p.setBrush(hijab); p.drawPath(cap)
        p.restore()

    bg_grad = QLinearGradient(cx - 30, 50, cx + 30, 250)
    bg_grad.setColorAt(0, robe1); bg_grad.setColorAt(1, robe2)

    if step in (0, 1):
        head(cx, 48)
        body = QPainterPath()
        wb = 34 if female else 24
        body.moveTo(cx - 22, 74); body.quadTo(cx, 66, cx + 22, 74)
        body.cubicTo(cx + wb, 140, cx + wb + 4, 210, cx + wb + 4, 252)
        body.lineTo(cx - wb - 4, 252)
        body.cubicTo(cx - wb - 4, 210, cx - wb, 140, cx - 22, 74)
        p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(skin_s)
        p.drawRoundedRect(QRectF(cx - 15, 252, 11, 7), 3, 3); p.drawRoundedRect(QRectF(cx + 4, 252, 11, 7), 3, 3)
        if step == 0:
            hy = 76 if female else 42
            for sgn in (-1, 1):
                arm = QPainterPath()
                arm.moveTo(cx + sgn*20, 76); arm.quadTo(cx + sgn*38, 100, cx + sgn*28, hy)
                arm.lineTo(cx + sgn*19, hy); arm.quadTo(cx + sgn*26, 92, cx + sgn*16, 90); arm.closeSubpath()
                p.setBrush(robe2); p.drawPath(arm)
                p.setBrush(skin); p.drawEllipse(QRectF(cx + sgn*23 - 5, hy - 8, 10, 14))
        else:
            hy = 98 if female else 128
            p.setBrush(robe2)
            p.drawRoundedRect(QRectF(cx - 25, 76, 10, hy - 66), 5, 5)
            p.drawRoundedRect(QRectF(cx + 15, 76, 10, hy - 66), 5, 5)
            p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 17, hy, 34, 12), 6, 6)
    elif step == 2:
        hx, hy = (cx - 38, 86) if female else (cx - 50, 116)
        head(hx, hy, -45 if female else -82)
        body = QPainterPath()
        if female:
            body.moveTo(cx - 24, 92); body.quadTo(cx + 6, 98, cx + 26, 120)
            body.lineTo(cx + 30, 252); body.lineTo(cx + 8, 252); body.lineTo(cx + 2, 144); body.lineTo(cx - 24, 116)
        else:
            body.moveTo(cx - 36, 108); body.lineTo(cx + 26, 108); body.lineTo(cx + 28, 252)
            body.lineTo(cx + 8, 252); body.lineTo(cx + 6, 136); body.lineTo(cx - 36, 132)
        body.closeSubpath(); p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(robe2)
        arm = QPainterPath()
        arm.moveTo(cx - 22, 116); arm.lineTo(cx - (4 if female else 10), 184); arm.lineTo(cx + (6 if female else 0), 184); arm.lineTo(cx - 12, 116)
        arm.closeSubpath(); p.drawPath(arm)
        p.setBrush(skin); p.drawEllipse(QRectF(cx - (6 if female else 12), 182, 11, 11))
    elif step == 3:
        head(cx - 48, 236, -75)
        body = QPainterPath()
        if female:
            body.moveTo(cx - 36, 244); body.cubicTo(cx - 10, 188, cx + 26, 198, cx + 40, 218)
            body.lineTo(cx + 48, 252); body.lineTo(cx - 16, 252)
        else:
            body.moveTo(cx - 36, 244); body.cubicTo(cx - 12, 152, cx + 24, 168, cx + 38, 204)
            body.lineTo(cx + 48, 252); body.lineTo(cx + 20, 252); body.lineTo(cx - 2, 206); body.lineTo(cx - 18, 252)
        body.closeSubpath(); p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 34, 245, 17, 7), 3, 3)
    elif step == 4:
        head(cx - 4, 94)
        body = QPainterPath()
        body.moveTo(cx - 18, 120); body.quadTo(cx + 2, 114, cx + 18, 122)
        body.lineTo(cx + 26, 224); body.lineTo(cx - 36, 224); body.quadTo(cx - 46, 238, cx - 34, 252)
        body.lineTo(cx + 34, 252); body.lineTo(cx + 28, 224); body.closeSubpath()
        p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(robe2); p.drawRoundedRect(QRectF(cx - 15, 128, 11, 58), 5, 5)
        p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 28, 184, 17, 9), 4, 4)

def ensure_imgs():
    m_path = os.path.join(DATA_DIR, "postures_m.png")
    f_path = os.path.join(DATA_DIR, "postures_f.png")
    for path, is_f in [(m_path, False), (f_path, True)]:
        if os.path.exists(path): continue
        pix = QPixmap(1000, 320); pix.fill(Qt.transparent)
        p = QPainter(pix); p.setRenderHint(QPainter.Antialiasing)
        titles = ["1. İftitah Tekbiri", "2. Kıyam", "3. Rükû", "4. Secde", "5. Oturuş (Ka'de)"]
        accent = QColor("#7C3AED") if is_f else QColor("#0D9488")
        bg_c = QColor(124, 58, 237, 16) if is_f else QColor(13, 148, 136, 16)
        for i, t in enumerate(titles):
            x = i * 200 + 6
            p.setBrush(bg_c); p.setPen(QPen(accent, 1.8))
            p.drawRoundedRect(QRectF(x, 6, 188, 308), 16, 16)
            # Mihrap kemeri
            arch = QPainterPath(); arch.moveTo(x + 24, 266); arch.lineTo(x + 24, 54); arch.quadTo(x + 94, 14, x + 164, 54); arch.lineTo(x + 164, 266)
            p.setBrush(Qt.NoBrush); p.setPen(QPen(QColor(accent.red(), accent.green(), accent.blue(), 60), 1.5)); p.drawPath(arch)
            p.setPen(accent); p.setFont(QFont("Sans", 11, QFont.Bold))
            p.drawText(QRectF(x, 276, 188, 28), Qt.AlignCenter, t)
            draw_figure(p, x + 94, i, is_f)
        p.end(); pix.save(path)
    return m_path, f_path

def get_topics():
    mp, fp = ensure_imgs()
    m_img = f"<div style='margin:12px 0; text-align:center;'><img src='file://{mp}' width='640' style='border-radius:12px;'/></div>"
    f_img = f"<div style='margin:12px 0; text-align:center;'><img src='file://{fp}' width='640' style='border-radius:12px;'/></div>"
    return {
        "tr": [
            ("1. Erkekler İçin Namaz Rükünleri", "<h3>Erkeklerde Namazın Kılınışı ve Rükünleri</h3>" + m_img + "<ol><li><b>Niyet ve İftitah Tekbiri:</b> Kıbleye dönülür, niyet edilir. Eller kulak hizasına kaldırılarak 'Allahu Ekber' denir.</li><li><b>Kıyam:</b> Sağ elin baş ve serçe parmakları sol el bileğini kavrar, eller göbek altında bağlanır. Sübhaneke, Fâtiha ve zamm-ı sure okunur.</li><li><b>Rükû:</b> 'Allahu Ekber' diyerek sırt tam düz (90 derece) olacak şekilde eğilinir, dizler kavranır ve 3 kez 'Sübhâne Rabbiye'l-Azîm' denir.</li><li><b>Secde:</b> Dirsekler yanlara açık, karın uyluklardan uzak şekilde alın, burun, eller, dizler ve ayak parmakları yere konularak 3 kez 'Sübhâne Rabbiye'l-A'lâ' denir.</li><li><b>Oturuş (Ka'de) ve Selam:</b> Sol ayak yayılır, sağ ayak dik tutulur. Ettehiyyâtü, Salli-Bârik ve Rabbenâ okunduktan sonra sağa ve sola selam verilir.</li></ol>"),
            ("2. Hanımlar İçin Namaz Rükünleri", "<h3>Hanımlarda Namazın Kılınışı ve Rükünleri</h3>" + f_img + "<ol><li><b>Niyet ve İftitah Tekbiri:</b> Kıbleye dönülür, niyet edilir. Eller omuz hizasına kaldırılarak 'Allahu Ekber' denir.</li><li><b>Kıyam:</b> Sağ el sol elin üzerine (halka yapmadan) göğüs üzerinde konulur; ayaklar birbirine yakın tutulur.</li><li><b>Rükû:</b> Sırt tam düz yapılmaz, dizler hafif kırık şekilde eller dizlerin üzerine konulur ve parmaklar açılmaz.</li><li><b>Secde:</b> Kollar yanlara yapışık, karın uyluklara bitişik şekilde mümkün olduğunca toplu halde 3 kez 'Sübhâne Rabbiye'l-A'lâ' denir.</li><li><b>Oturuş (Tevverük) ve Selam:</b> Ayaklar sağa yatırılarak sol kalça üzerine oturulur. Dualar okunduktan sonra sağa ve sola selam verilir.</li></ol>"),
            ("3. Abdest Nasıl Alınır?", "<h3>Adım Adım Abdest</h3><ol><li><b>Niyet ve Besmele:</b> 'Niyet ettim Allah rızası için abdest almaya' denir ve Eûzü-Besmele çekilir.</li><li><b>Eller:</b> Bileklere kadar 3 kez yıkanır, parmak araları hilallenir.</li><li><b>Ağız ve Burun:</b> Sağ avuçla 3 kez ağza su verilir (mazmaza), 3 kez buruna su çekilir (istinşak).</li><li><b>Yüz:</b> Alın saç bitiminden çene altına ve kulaklara kadar 3 kez yıkanır.</li><li><b>Kollar:</b> Önce sağ, sonra sol kol dirseklerle beraber 3 kez yıkanır.</li><li><b>Baş, Kulak ve Boyun:</b> Islak elle başın dörtte biri, kulaklar ve boyun meshedilir.</li><li><b>Ayaklar:</b> Önce sağ, sonra sol ayak topuklarla beraber 3 kez yıkanır.</li></ol>"),
            ("4. Beş Vakit Namaz Özeti", "<h3>Vakit Namazları Rekatları</h3><ul><li><b>Sabah Namazı:</b> 2 Sünnet + 2 Farz</li><li><b>Öğle Namazı:</b> 4 İlk Sünnet + 4 Farz + 2 Son Sünnet</li><li><b>İkindi Namazı:</b> 4 Sünnet + 4 Farz</li><li><b>Akşam Namazı:</b> 3 Farz + 2 Sünnet</li><li><b>Yatsı Namazı:</b> 4 İlk Sünnet + 4 Farz + 2 Son Sünnet + 3 Vitir</li></ul>"),
            ("5. Cuma Namazı Kılınışı", "<h3>Cuma Namazı (16 Rekat)</h3><p>Cuma namazı cemaatle kılınır ve farzı 2 rekattır:</p><ol><li><b>4 Rekat İlk Sünnet:</b> Öğle namazının ilk sünneti gibi kılınır.</li><li><b>Hutbe ve 2 Rekat Farz:</b> İmam minberde hutbe okur (sessizce dinlenir). Ardından kamet getirilir ve imama uyularak 2 rekat farz kılınır.</li><li><b>4 Rekat Son Sünnet:</b> Öğle namazının ilk sünneti gibi kılınır.</li><li><b>4 Rekat Zuhr-i Âhir & 2 Rekat Vaktin Sünneti:</b> İhtiyaten kılınan 4 rekat namazın ardından 2 rekat sabah namazı sünneti gibi kılınarak tamamlanır.</li></ol>"),
            ("6. Bayram Namazları Kılınışı", "<h3>Ramazan ve Kurban Bayramı Namazı (2 Rekat)</h3><p>Bayram namazları cemaatle kılınan vacip namazlardır ve her rekatta <b>3 Zevâid Tekbiri</b> vardır:</p><ol><li><b>1. Rekat:</b> Niyet edilir, İftitah tekbiri alınıp eller bağlanır ve <b>Sübhaneke</b> okunur. Ardından imamla birlikte eller kulak hizasına kaldırılarak <b>3 kez tekbir</b> alınır: İlk ikisinde eller yanlara salınır, <b>3. tekbirden sonra eller bağlanır</b>. İmam Fâtiha ve sure okur, rükû ve secdeler yapılır.</li><li><b>2. Rekat:</b> İmam önce Fâtiha ve sureyi okur. Rükûya gitmeden önce imamla birlikte <b>3 kez daha tekbir</b> alınır: Üçünde de eller yanlara salınır, <b>4. tekbir ile rükûya eğilinir</b>. Secdeler ve oturuşun ardından selam verilir.</li></ol>"),
            ("7. Namaz Duaları", "<h3>Sübhaneke</h3><p><i>Sübhânekellâhümme ve bi hamdik ve tebârakesmük ve teâlâ ceddük (ve celle senâük) ve lâ ilâhe ğayruk.</i></p><h3>Ettehiyyâtü</h3><p><i>Ettehiyyâtü lillâhi vessalevâtü vettayyibât. Esselâmü aleyke eyyühen-nebiyyü ve rahmetullâhi ve berekâtüh. Esselâmü aleynâ ve alâ ibâdillâhis-sâlihîn. Eşhedü en lâ ilâhe illallâh ve eşhedü enne Muhammeden abdühû ve resûlüh.</i></p><h3>Allahümme Salli & Bârik</h3><p><i>Allâhümme salli alâ Muhammedin ve alâ âli Muhammed, kemâ salleyte alâ İbrâhîme ve alâ âli İbrâhîm, inneke hamîdün mecîd.</i></p>"),
            ("8. Kısa Zikirler ve Anlamları", "<h3>Günlük Tesbihat ve Faziletli Zikirler</h3><ul><li><b>Sübhânallâh (33 kez):</b> <i>Allah'ı her türlü eksiklikten tenzih ederim.</i></li><li><b>Elhamdülillâh (33 kez):</b> <i>Bütün hamd ve övgüler Allah'a mahsustur.</i></li><li><b>Allâhu Ekber (33 kez):</b> <i>Allah en büyüktür.</i></li><li><b>Lâ ilâhe illallâh:</b> <i>Allah'tan başka ilah yoktur. (Zikirlerin en faziletlisidir.)</i></li><li><b>Estağfirullâh el-Azîm:</b> <i>Yüce Allah'tan bağışlanma dilerim.</i></li><li><b>Lâ havle velâ kuvvete illâ billâh:</b> <i>Güç ve kuvvet yalnızca Allah'ın yardımıyladır. (Cennet hazinelerinden bir sözdür.)</i></li><li><b>Sübhânallâhi ve bihamdihî, sübhânallâhi'l-Azîm:</b> <i>Allah'ı hamd ile tesbih ederim, Yüce Allah'ı tenzih ederim. (Dilde hafif, mizanda ağır gelen zikirdir.)</i></li><li><b>Allâhümme salli alâ Seyyidinâ Muhammed:</b> <i>Allah'ım! Efendimiz Muhammed'e salât ve selam eyle.</i></li></ul>")
        ],
        "en": [
            ("1. Prayer Postures (Men)", "<h3>Prayer Postures for Men</h3>" + m_img + "<ol><li><b>Takbir:</b> Raise hands up to earlobes.</li><li><b>Qiyam:</b> Clasp hands below the navel.</li><li><b>Ruku:</b> Bow with back completely flat (90 degrees).</li><li><b>Sujood:</b> Keep elbows away from sides and stomach away from thighs.</li><li><b>Sitting:</b> Sit on left foot with right foot upright.</li></ol>"),
            ("2. Prayer Postures (Women)", "<h3>Prayer Postures for Women</h3>" + f_img + "<ol><li><b>Takbir:</b> Raise hands up to shoulder level.</li><li><b>Qiyam:</b> Place right hand over left on the chest.</li><li><b>Ruku:</b> Bow slightly without making back completely flat.</li><li><b>Sujood:</b> Keep arms close to sides and body compact.</li><li><b>Sitting:</b> Sit on left hip with both feet extended to the right.</li></ol>"),
            ("3. How to Perform Wudu", "<h3>Step-by-Step Wudu</h3><ol><li>Make intention and say Bismillah.</li><li>Wash hands, mouth, nose, face, and arms 3 times.</li><li>Wipe head and ears once, then wash feet 3 times.</li></ol>"),
            ("4. Daily Prayer Rakahs", "<h3>Summary of Daily Rakahs</h3><ul><li><b>Fajr:</b> 2 Sunnah + 2 Fard</li><li><b>Dhuhr:</b> 4 Sunnah + 4 Fard + 2 Sunnah</li><li><b>Asr:</b> 4 Sunnah + 4 Fard</li><li><b>Maghrib:</b> 3 Fard + 2 Sunnah</li><li><b>Isha:</b> 4 Sunnah + 4 Fard + 2 Sunnah + 3 Witr</li></ul>"),
            ("5. Jumu'ah (Friday) Prayer", "<h3>Jumu'ah Prayer</h3><p>Performed in congregation on Friday instead of Dhuhr: 4 Rakah Sunnah, listening to the Khutbah, 2 Rakah Fard in congregation, followed by 4 Rakah Sunnah.</p>"),
            ("6. Eid Prayers (Fitr & Adha)", "<h3>Eid Prayer (2 Rakahs)</h3><p>Includes 3 extra Takbirs in each Rakah: In the 1st Rakah, after Subhanaka, raise hands 3 times (drop sides on first two, fold on the 3rd). In the 2nd Rakah, after recitation, raise hands 3 times before bowing on the 4th Takbir.</p>"),
            ("7. Short Dhikr & Meanings", "<h3>Daily Remembrance (Dhikr)</h3><ul><li><b>SubhanAllah (33x):</b> <i>Glory be to Allah.</i></li><li><b>Alhamdulillah (33x):</b> <i>All praise is due to Allah.</i></li><li><b>Allahu Akbar (33x):</b> <i>Allah is the Greatest.</i></li><li><b>La ilaha illallah:</b> <i>There is no deity worthy of worship except Allah.</i></li><li><b>Astaghfirullah:</b> <i>I seek forgiveness from Allah.</i></li><li><b>La hawla wa la quwwata illa billah:</b> <i>There is no power nor strength except with Allah.</i></li><li><b>SubhanAllahi wa bihamdihi, SubhanAllahil-Adheem:</b> <i>Glory and praise be to Allah, Glory be to Allah the Supreme.</i></li></ul>")
        ]
    }

class GuideWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.topics = get_topics()
        l = QHBoxLayout(self); l.setContentsMargins(16,16,16,16); l.setSpacing(14)
        self.lst = QListWidget(); self.lst.itemClicked.connect(lambda it: self.view.setHtml(self.wrap(it.data(Qt.UserRole)))); l.addWidget(self.lst, 1)
        self.view = QTextBrowser(); self.view.setStyleSheet("border:none;"); l.addWidget(self.view, 2)
        self.set_prefs(lang, fsize)

    def wrap(self, html): return f"<div style='font-size:{self.fsize}px; line-height:1.6;'>{html}</div>"

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize; self.lst.clear()
        for title, body in self.topics.get(lang, self.topics["en"]):
            it = QListWidgetItem(title); it.setData(Qt.UserRole, body); self.lst.addItem(it)
        self.lst.setCurrentRow(0); self.view.setHtml(self.wrap(self.lst.item(0).data(Qt.UserRole)))
