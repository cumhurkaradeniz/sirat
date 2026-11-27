import os
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QColor, QFont, QPen, QLinearGradient
from modules.i18n import get_bundle
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextBrowser

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def draw_figure(p, cx, step, female=False):
    skin = QColor("#F1C6A7"); skin_s = QColor("#D49E7A")
    robe1 = QColor("#8B5CF6") if female else QColor("#14B8A6")
    robe2 = QColor("#4C1D95") if female else QColor("#0F766E")
    hijab = QColor("#F8FAFC") if female else QColor("#FFFFFF")
    rug1 = QColor("#EDE9FE") if female else QColor("#CCFBF1")
    rug2 = QColor("#C4B5FD") if female else QColor("#5EEAD4")

    rug = QPainterPath()
    rug.moveTo(cx - 52, 248); rug.lineTo(cx + 52, 248)
    rug.lineTo(cx + 62, 266); rug.lineTo(cx - 62, 266); rug.closeSubpath()
    rg = QLinearGradient(cx, 248, cx, 266); rg.setColorAt(0, rug1); rg.setColorAt(1, rug2)
    p.setPen(QPen(robe2, 1.2)); p.setBrush(rg); p.drawPath(rug)
    p.setPen(QPen(QColor("#1E293B"), 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    def head(hx, hy, tilt=0):
        p.save(); p.translate(hx, hy); p.rotate(tilt)
        if female:
            sh = QPainterPath()
            sh.moveTo(-17, -8); sh.cubicTo(-17, -26, 17, -26, 17, -8)
            sh.cubicTo(20, 16, 16, 38, 0, 42); sh.cubicTo(-16, 38, -20, 16, -17, -8)
            p.setBrush(hijab); p.drawPath(sh)
            p.setBrush(skin); p.drawEllipse(QRectF(-9, -9, 18, 22))
        else:
            p.setBrush(skin); p.drawEllipse(QRectF(-9, -9, 18, 22))
            cap = QPainterPath(); cap.moveTo(-9, -3); cap.quadTo(0, -17, 9, -3); cap.closeSubpath()
            p.setBrush(hijab); p.drawPath(cap)
        p.restore()

    bg_grad = QLinearGradient(cx - 30, 50, cx + 30, 250)
    bg_grad.setColorAt(0, robe1); bg_grad.setColorAt(1, robe2)

    if step in (0, 1):
        head(cx, 48)
        body = QPainterPath()
        wb = 32 if female else 23
        body.moveTo(cx - 21, 74); body.quadTo(cx, 66, cx + 21, 74)
        body.cubicTo(cx + wb, 140, cx + wb + 3, 210, cx + wb + 3, 250)
        body.lineTo(cx - wb - 3, 250)
        body.cubicTo(cx - wb - 3, 210, cx - wb, 140, cx - 21, 74)
        p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(skin_s)
        p.drawRoundedRect(QRectF(cx - 14, 250, 10, 6), 3, 3); p.drawRoundedRect(QRectF(cx + 4, 250, 10, 6), 3, 3)
        if step == 0:
            # Erkek: kulak hizasi (y=54), Kadin: omuz hizasi (y=80)
            hy = 80 if female else 54
            for sgn in (-1, 1):
                arm = QPainterPath()
                arm.moveTo(cx + sgn*20, 78); arm.quadTo(cx + sgn*40, 105, cx + sgn*28, hy)
                arm.lineTo(cx + sgn*19, hy); arm.quadTo(cx + sgn*26, 95, cx + sgn*16, 92); arm.closeSubpath()
                p.setBrush(robe2); p.drawPath(arm)
                p.setBrush(skin); p.drawEllipse(QRectF(cx + sgn*23 - 5, hy - 7, 10, 14))
        else:
            # Erkek: gobek alti (y=138), Kadin: gogus ustu (y=98)
            hy = 98 if female else 138
            p.setBrush(robe2)
            p.drawRoundedRect(QRectF(cx - 24, 76, 9, hy - 66), 4, 4)
            p.drawRoundedRect(QRectF(cx + 15, 76, 9, hy - 66), 4, 4)
            p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 16, hy, 32, 11), 5, 5)
    elif step == 2:
        hx, hy = (cx - 34, 88) if female else (cx - 48, 122)
        head(hx, hy, -42 if female else -85)
        body = QPainterPath()
        if female:
            # Kadin: sirt hafif egik, dizler hafif kirik, eller dizde
            body.moveTo(cx - 22, 92); body.quadTo(cx + 8, 100, cx + 26, 128)
            body.lineTo(cx + 18, 188); body.lineTo(cx + 28, 250); body.lineTo(cx + 8, 250)
            body.lineTo(cx - 2, 188); body.lineTo(cx + 4, 142); body.lineTo(cx - 22, 114)
        else:
            # Erkek: sirt 90 derece duz, bacaklar dik, eller dizde
            body.moveTo(cx - 36, 114); body.lineTo(cx + 26, 114); body.lineTo(cx + 28, 250)
            body.lineTo(cx + 8, 250); body.lineTo(cx + 6, 140); body.lineTo(cx - 36, 136)
        body.closeSubpath(); p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(robe2)
        kx = cx + 2 if female else cx + 10
        arm = QPainterPath()
        arm.moveTo(cx - 20, 118); arm.lineTo(kx, 182); arm.lineTo(kx + 10, 182); arm.lineTo(cx - 10, 118)
        arm.closeSubpath(); p.setBrush(robe2); p.drawPath(arm)
        p.setBrush(skin); p.drawEllipse(QRectF(kx - 1, 179, 11, 11))
    elif step == 3:
        head(cx - 46, 236, -78)
        body = QPainterPath()
        if female:
            # Kadin: yere yakin toplu secde
            body.moveTo(cx - 36, 245); body.cubicTo(cx - 14, 204, cx + 24, 210, cx + 42, 226)
            body.lineTo(cx + 48, 250); body.lineTo(cx - 18, 250)
        else:
            # Erkek: dirsekler yerden kalkik, karin uyluktan acik
            body.moveTo(cx - 36, 245); body.cubicTo(cx - 12, 166, cx + 24, 178, cx + 38, 210)
            body.lineTo(cx + 48, 250); body.lineTo(cx + 22, 250); body.lineTo(cx - 2, 212); body.lineTo(cx - 18, 250)
        body.closeSubpath(); p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 32, 244, 16, 6), 3, 3)
    elif step == 4:
        head(cx - 4, 96)
        body = QPainterPath()
        body.moveTo(cx - 18, 122); body.quadTo(cx + 2, 116, cx + 18, 124)
        body.lineTo(cx + 26, 224); body.lineTo(cx - 36, 224); body.quadTo(cx - 46, 238, cx - 34, 250)
        body.lineTo(cx + 34, 250); body.lineTo(cx + 28, 224); body.closeSubpath()
        p.setBrush(bg_grad); p.drawPath(body)
        p.setBrush(robe2); p.drawRoundedRect(QRectF(cx - 15, 130, 11, 56), 5, 5)
        p.setBrush(skin); p.drawRoundedRect(QRectF(cx - 28, 184, 17, 9), 4, 4)

def ensure_imgs():
    out_dir = DATA_DIR if os.access(DATA_DIR, os.W_OK) else os.path.expanduser("~/.cache/sirat")
    os.makedirs(out_dir, exist_ok=True)
    m_path = os.path.join(out_dir, "postures_m.png")
    f_path = os.path.join(out_dir, "postures_f.png")
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
            arch = QPainterPath(); arch.moveTo(x + 24, 266); arch.lineTo(x + 24, 54); arch.quadTo(x + 94, 14, x + 164, 54); arch.lineTo(x + 164, 266)
            p.setBrush(Qt.NoBrush); p.setPen(QPen(QColor(accent.red(), accent.green(), accent.blue(), 60), 1.5)); p.drawPath(arch)
            p.setPen(accent); p.setFont(QFont("Sans", 11, QFont.Bold))
            p.drawText(QRectF(x, 276, 188, 28), Qt.AlignCenter, t)
            draw_figure(p, x + 94, i, is_f)
        p.end(); pix.save(path)
    return m_path, f_path

def get_topics():
    mp, fp = ensure_imgs()
    m_img = f"<div style='margin:12px 0; text-align:center;'><img src='file://{mp}' width='__IMGW__' style='border-radius:12px;'/></div>"
    f_img = f"<div style='margin:12px 0; text-align:center;'><img src='file://{fp}' width='__IMGW__' style='border-radius:12px;'/></div>"
    return {
        "tr": [
            ("1. Erkekler İçin Namaz Rükünleri", "<h3>Erkeklerde Namazın Kılınışı ve Rükünleri</h3>" + m_img + "<ol><li><b>Niyet ve İftitah Tekbiri:</b> Kıbleye dönülür, niyet edilir. Başparmaklar kulak yumuşağı hizasına gelecek şekilde eller kaldırılarak 'Allahu Ekber' denir.</li><li><b>Kıyam:</b> Sağ elin baş ve serçe parmakları sol el bileğini kavrar, eller göbek altında bağlanır. Sübhaneke, Fâtiha ve zamm-ı sure okunur.</li><li><b>Rükû:</b> 'Allahu Ekber' diyerek sırt tam düz (90 derece) olacak şekilde eğilinir, dizler kavranır ve 3 kez 'Sübhâne Rabbiye'l-Azîm' denir.</li><li><b>Secde:</b> Dirsekler yerden kalkık ve yanlara açık, karın uyluklardan uzak şekilde alın, burun, eller, dizler ve ayak parmakları yere konularak 3 kez 'Sübhâne Rabbiye'l-A'lâ' denir.</li><li><b>Oturuş (Ka'de) ve Selam:</b> Sol ayak yayılır, sağ ayak dik tutulur. Ettehiyyâtü, Salli-Bârik ve Rabbenâ okunduktan sonra sağa ve sola selam verilir.</li></ol>"),
            ("2. Hanımlar İçin Namaz Rükünleri", "<h3>Hanımlarda Namazın Kılınışı ve Rükünleri</h3>" + f_img + "<ol><li><b>Niyet ve İftitah Tekbiri:</b> Kıbleye dönülür, niyet edilir. Eller omuz hizasına kaldırılarak 'Allahu Ekber' denir.</li><li><b>Kıyam:</b> Sağ el sol elin üzerine (halka yapmadan) göğüs üzerinde konulur; ayaklar birbirine yakın tutulur.</li><li><b>Rükû:</b> Sırt tam düz yapılmaz, dizler hafif kırık şekilde eller dizlerin üzerine konulur ve parmaklar açılmaz.</li><li><b>Secde:</b> Kollar yanlara ve yere yapışık, karın uyluklara bitişik şekilde mümkün olduğunca toplu halde 3 kez 'Sübhâne Rabbiye'l-A'lâ' denir.</li><li><b>Oturuş (Tevverrük) ve Selam:</b> Ayaklar sağa yatırılarak sol kalça üzerine oturulur. Dualar okunduktan sonra sağa ve sola selam verilir.</li></ol>"),
            ("3. Abdest Nasıl Alınır?", "<h3>Adım Adım Abdest</h3><ol><li><b>Niyet ve Besmele:</b> 'Niyet ettim Allah rızası için abdest almaya' denir ve Eûzü-Besmele çekilir.</li><li><b>Eller:</b> Bileklere kadar 3 kez yıkanır, parmak araları hilallenir.</li><li><b>Ağız ve Burun:</b> Sağ avuçla 3 kez ağza su verilir (mazmaza), 3 kez buruna su çekilir (istinşak).</li><li><b>Yüz:</b> Alın saç bitiminden çene altına ve kulaklara kadar 3 kez yıkanır.</li><li><b>Kollar:</b> Önce sağ, sonra sol kol dirseklerle beraber 3 kez yıkanır.</li><li><b>Baş, Kulak ve Boyun:</b> Islak elle başın dörtte biri, kulaklar ve boyun meshedilir.</li><li><b>Ayaklar:</b> Önce sağ, sonra sol ayak topuklarla beraber 3 kez yıkanır.</li></ol>"),
            ("4. Beş Vakit Namaz Özeti", "<h3>Vakit Namazları Rekatları</h3><ul><li><b>Sabah Namazı:</b> 2 Sünnet + 2 Farz</li><li><b>Öğle Namazı:</b> 4 İlk Sünnet + 4 Farz + 2 Son Sünnet</li><li><b>İkindi Namazı:</b> 4 Sünnet + 4 Farz</li><li><b>Akşam Namazı:</b> 3 Farz + 2 Sünnet</li><li><b>Yatsı Namazı:</b> 4 İlk Sünnet + 4 Farz + 2 Son Sünnet + 3 Vitir</li></ul>"),
            ("5. Cuma Namazı Kılınışı", "<h3>Cuma Namazı (16 Rekat)</h3><p>Cuma namazı cemaatle kılınır ve farzı 2 rekattır:</p><ol><li><b>4 Rekat İlk Sünnet:</b> Öğle namazının ilk sünneti gibi kılınır.</li><li><b>Hutbe ve 2 Rekat Farz:</b> İmam minberde hutbe okur (sessizce dinlenir). Ardından kamet getirilir ve imama uyularak 2 rekat farz kılınır.</li><li><b>4 Rekat Son Sünnet:</b> Öğle namazının ilk sünneti gibi kılınır.</li><li><b>4 Rekat Zuhr-i Âhir & 2 Rekat Vaktin Sünneti:</b> İhtiyaten kılınan 4 rekat namazın ardından 2 rekat sabah namazı sünneti gibi kılınarak tamamlanır.</li></ol>"),
            ("6. Bayram Namazları Kılınışı", "<h3>Ramazan ve Kurban Bayramı Namazı (2 Rekat)</h3><p>Bayram namazları cemaatle kılınan vacip namazlardır ve her rekatta <b>3 Zevâid Tekbiri</b> vardır:</p><ol><li><b>1. Rekat:</b> Niyet edilir, İftitah tekbiri alınıp eller bağlanır ve <b>Sübhaneke</b> okunur. Ardından imamla birlikte eller kulak hizasına kaldırılarak <b>3 kez tekbir</b> alınır: İlk ikisinde eller yanlara salınır, <b>3. tekbirden sonra eller bağlanır</b>. İmam Fâtiha ve sure okur, rükû ve secdeler yapılır.</li><li><b>2. Rekat:</b> İmam önce Fâtiha ve sureyi okur. Rükûya gitmeden önce imamla birlikte <b>3 kez daha tekbir</b> alınır: Üçünde de eller yanlara salınır, <b>4. tekbir ile rükûya eğilinir</b>. Secdeler ve oturuşun ardından selam verilir.</li></ol>"),
            ("7. Namaz Duaları", "<h3>Sübhaneke</h3><p><i>Sübhânekellâhümme ve bi hamdik ve tebârakesmük ve teâlâ ceddük (ve celle senâük) ve lâ ilâhe ğayruk.</i></p><h3>Ettehiyyâtü</h3><p><i>Ettehiyyâtü lillâhi vessalevâtü vettayyibât. Esselâmü aleyke eyyühen-nebiyyü ve rahmetullâhi ve berekâtüh. Esselâmü aleynâ ve alâ ibâdillâhis-sâlihîn. Eşhedü en lâ ilâhe illallâh ve eşhedü enne Muhammeden abdühû ve resûlüh.</i></p><h3>Allahümme Salli & Bârik</h3><p><i>Allâhümme salli alâ Muhammedin ve alâ âli Muhammed, kemâ salleyte alâ İbrâhîme ve alâ âli İbrâhîm, inneke hamîdün mecîd.</i></p>"),
            ("8. Kısa Zikirler ve Anlamları", "<h3>Günlük Tesbihat ve Faziletli Zikirler</h3><ul><li><b>Sübhânallâh (33 kez):</b> <i>Allah'ı her türlü eksiklikten tenzih ederim.</i></li><li><b>Elhamdülillâh (33 kez):</b> <i>Bütün hamd ve övgüler Allah'a mahsustur.</i></li><li><b>Allâhu Ekber (33 kez):</b> <i>Allah en büyüktür.</i></li><li><b>Lâ ilâhe illallâh:</b> <i>Allah'tan başka ilah yoktur.</i></li><li><b>Estağfirullâh el-Azîm:</b> <i>Yüce Allah'tan bağışlanma dilerim.</i></li></ul>")
        ],
        "fr": [
            ("1. Postures de Prière (Hommes)", "<h3>Postures de Prière pour les Hommes</h3>" + m_img + "<ol><li><b>Takbir :</b> Lever les mains au niveau des lobes d'oreilles.</li><li><b>Qiyam :</b> Joindre les mains sous le nombril.</li><li><b>Ruku :</b> S'incliner le dos droit à 90 degrés.</li><li><b>Sujood :</b> Garder les coudes levés du sol.</li><li><b>Assise :</b> S'asseoir sur le pied gauche, le pied droit dressé.</li></ol>"),
            ("2. Postures de Prière (Femmes)", "<h3>Postures de Prière pour les Femmes</h3>" + f_img + "<ol><li><b>Takbir :</b> Lever les mains au niveau des épaules.</li><li><b>Qiyam :</b> Poser la main droite sur la gauche sur la poitrine.</li><li><b>Ruku :</b> S'incliner légèrement, mains sur les genoux.</li><li><b>Sujood :</b> Garder les bras proches du corps.</li><li><b>Assise :</b> S'asseoir sur la hanche gauche, pieds vers la droite.</li></ol>"),
            ("3. Comment faire les Ablutions (Wudu)", "<h3>Étapes des Ablutions</h3><ol><li>Formuler l'intention et dire Bismillah.</li><li>Laver les mains, la bouche, le nez, le visage et les bras 3 fois.</li><li>Essuyer la tête et les oreilles, puis laver les pieds 3 fois.</li></ol>"),
            ("4. Nombre de Rak'ahs Quotidiennes", "<h3>Résumé des Prières</h3><ul><li><b>Fajr :</b> 2 Sunnah + 2 Fard</li><li><b>Dhuhr :</b> 4 Sunnah + 4 Fard + 2 Sunnah</li><li><b>Asr :</b> 4 Sunnah + 4 Fard</li><li><b>Maghrib :</b> 3 Fard + 2 Sunnah</li><li><b>Isha :</b> 4 Sunnah + 4 Fard + 2 Sunnah + 3 Witr</li></ul>"),
            ("5. Prière du Vendredi (Jumu'ah)", "<h3>Prière de Jumu'ah</h3><p>Accomplie en congrégation le vendredi : 4 Rak'ahs Sunnah, écoute du sermon (Khutbah), 2 Rak'ahs Fard, puis 4 Rak'ahs Sunnah.</p>"),
            ("6. Prières de l'Aïd", "<h3>Prière de l'Aïd (2 Rak'ahs)</h3><p>Comprend 3 Takbirs supplémentaires dans chaque Rak'ah (avant la récitation dans la 1ère, avant le Ruku dans la 2ème).</p>"),
            ("7. Invocations et Dhikr", "<h3>Dhikr Quotidien</h3><ul><li><b>SubhanAllah (33x) :</b> Gloire à Allah.</li><li><b>Alhamdulillah (33x) :</b> Louange à Allah.</li><li><b>Allahu Akbar (33x) :</b> Allah est le Plus Grand.</li></ul>")
        ],
        "es": [
            ("1. Posturas de Oración (Hombres)", "<h3>Posturas para Hombres</h3>" + m_img + "<ol><li><b>Takbir:</b> Levantar las manos hasta los lóbulos de las orejas.</li><li><b>Qiyam:</b> Cruzar las manos debajo del ombligo.</li><li><b>Ruku:</b> Inclinarse con la espalda recta a 90 grados.</li><li><b>Sujood:</b> Mantener los codos levantados del suelo.</li><li><b>Sentado:</b> Sentarse sobre el pie izquierdo con el derecho erguido.</li></ol>"),
            ("2. Posturas de Oración (Mujeres)", "<h3>Posturas para Mujeres</h3>" + f_img + "<ol><li><b>Takbir:</b> Levantar las manos a la altura de los hombros.</li><li><b>Qiyam:</b> Colocar la mano derecha sobre la izquierda en el pecho.</li><li><b>Ruku:</b> Inclinarse ligeramente con las manos en las rodillas.</li><li><b>Sujood:</b> Mantener los brazos pegados al cuerpo.</li><li><b>Sentado:</b> Sentarse sobre la cadera izquierda con ambos pies a la derecha.</li></ol>"),
            ("3. Cómo hacer la Ablución (Wudu)", "<h3>Pasos del Wudu</h3><ol><li>Hacer la intención y decir Bismillah.</li><li>Lavar manos, boca, nariz, rostro y brazos 3 veces.</li><li>Pasar manos húmedas por cabeza y orejas, y lavar los pies 3 veces.</li></ol>"),
            ("4. Rak'ahs Diarias", "<h3>Resumen de Oraciones</h3><ul><li><b>Fajr:</b> 2 Sunnah + 2 Fard</li><li><b>Dhuhr:</b> 4 Sunnah + 4 Fard + 2 Sunnah</li><li><b>Asr:</b> 4 Sunnah + 4 Fard</li><li><b>Maghrib:</b> 3 Fard + 2 Sunnah</li><li><b>Isha:</b> 4 Sunnah + 4 Fard + 2 Sunnah + 3 Witr</li></ul>"),
            ("5. Oración del Viernes (Yumu'ah)", "<h3>Oración de Yumu'ah</h3><p>En congregación el viernes: 4 Sunnah, escuchar la Jutbah, 2 Fard y 4 Sunnah.</p>"),
            ("6. Oraciones del Eid", "<h3>Oración del Eid (2 Rak'ahs)</h3><p>Incluye 3 Takbires adicionales en cada Rak'ah.</p>"),
            ("7. Dhikr y Significados", "<h3>Recuerdo Diario</h3><ul><li><b>SubhanAllah (33x):</b> Gloria a Allah.</li><li><b>Alhamdulillah (33x):</b> Alabanza a Allah.</li><li><b>Allahu Akbar (33x):</b> Allah es el Más Grande.</li></ul>")
        ],
        "pt": [
            ("1. Posturas de Oração (Homens)", "<h3>Posturas para Homens</h3>" + m_img + "<ol><li><b>Takbir:</b> Erguer as mãos até os lóbulos das orelhas.</li><li><b>Qiyam:</b> Unir as mãos abaixo do umbigo.</li><li><b>Ruku:</b> Inclinar-se com as costas retas a 90 graus.</li><li><b>Sujood:</b> Manter os cotovelos afastados do chão.</li><li><b>Sentado:</b> Sentar sobre o pé esquerdo com o direito erguido.</li></ol>"),
            ("2. Posturas de Oração (Mulheres)", "<h3>Posturas para Mulheres</h3>" + f_img + "<ol><li><b>Takbir:</b> Erguer as mãos na altura dos ombros.</li><li><b>Qiyam:</b> Colocar a mão direita sobre a esquerda no peito.</li><li><b>Ruku:</b> Inclinar-se levemente com as mãos nos joelhos.</li><li><b>Sujood:</b> Manter os braços juntos ao corpo.</li><li><b>Sentado:</b> Sentar sobre o quadril esquerdo com os pés à direita.</li></ol>"),
            ("3. Como fazer a Ablução (Wudu)", "<h3>Passo a Passo do Wudu</h3><ol><li>Fazer a intenção e dizer Bismillah.</li><li>Lavar mãos, boca, nariz, rosto e braços 3 vezes.</li><li>Passar as mãos úmidas na cabeça e orelhas, e lavar os pés 3 vezes.</li></ol>"),
            ("4. Rak'ahs Diárias", "<h3>Resumo das Orações</h3><ul><li><b>Fajr:</b> 2 Sunnah + 2 Fard</li><li><b>Dhuhr:</b> 4 Sunnah + 4 Fard + 2 Sunnah</li><li><b>Asr:</b> 4 Sunnah + 4 Fard</li><li><b>Maghrib:</b> 3 Fard + 2 Sunnah</li><li><b>Isha:</b> 4 Sunnah + 4 Fard + 2 Sunnah + 3 Witr</li></ul>"),
            ("5. Oração de Sexta-feira (Jumu'ah)", "<h3>Oração de Jumu'ah</h3><p>Em congregação na sexta: 4 Sunnah, ouvir a Khutbah, 2 Fard e 4 Sunnah.</p>"),
            ("6. Orações do Eid", "<h3>Oração do Eid (2 Rak'ahs)</h3><p>Inclui 3 Takbires extras em cada Rak'ah.</p>"),
            ("7. Dhikr e Significados", "<h3>Lembrança Diária</h3><ul><li><b>SubhanAllah (33x):</b> Glória a Allah.</li><li><b>Alhamdulillah (33x):</b> Louvor a Allah.</li><li><b>Allahu Akbar (33x):</b> Allah é o Maior.</li></ul>")
        ],
        "id": [
            ("1. Gerakan Shalat (Pria)", "<h3>Tata Cara Shalat Pria</h3>" + m_img + "<ol><li><b>Takbir:</b> Mengangkat tangan sejajar daun telinga.</li><li><b>Qiyam:</b> Bersedekap di bawah pusar.</li><li><b>Rukuk:</b> Membungkuk punggung lurus 90 derajat.</li><li><b>Sujud:</b> Siku diangkat dari lantai dan perut jauh dari paha.</li><li><b>Duduk:</b> Duduk iftirasy di atas kaki kiri.</li></ol>"),
            ("2. Gerakan Shalat (Wanita)", "<h3>Tata Cara Shalat Wanita</h3>" + f_img + "<ol><li><b>Takbir:</b> Mengangkat tangan sejajar bahu.</li><li><b>Qiyam:</b> Meletakkan tangan kanan di atas kiri di dada.</li><li><b>Rukuk:</b> Membungkuk ringan, tangan di lutut.</li><li><b>Sujud:</b> Merapatkan lengan ke sisi tubuh.</li><li><b>Duduk:</b> Duduk tawarruk di pinggul kiri.</li></ol>"),
            ("3. Tata Cara Wudhu", "<h3>Langkah-Langkah Wudhu</h3><ol><li>Niat dan membaca Bismillah.</li><li>Membasuh tangan, mulut, hidung, wajah, dan lengan 3 kali.</li><li>Mengusap kepala dan telinga, lalu membasuh kaki 3 kali.</li></ol>"),
            ("4. Jumlah Rakaat Shalat", "<h3>Ringkasan Shalat Wajib</h3><ul><li><b>Subuh:</b> 2 Sunnah + 2 Fardhu</li><li><b>Dzuhur:</b> 4 Sunnah + 4 Fardhu + 2 Sunnah</li><li><b>Ashar:</b> 4 Sunnah + 4 Fardhu</li><li><b>Maghrib:</b> 3 Fardhu + 2 Sunnah</li><li><b>Isya:</b> 4 Sunnah + 4 Fardhu + 2 Sunnah + 3 Witir</li></ul>"),
            ("5. Shalat Jumat", "<h3>Shalat Jumat</h3><p>Dilaksanakan berjamaah pada hari Jumat: 4 Sunnah, mendengarkan Khutbah, 2 Fardhu, dan 4 Sunnah.</p>"),
            ("6. Shalat Idul Fitri & Adha", "<h3>Shalat Id (2 Rakaat)</h3><p>Disertai 3 kali takbir tambahan pada setiap rakaat.</p>"),
            ("7. Dzikir Harian", "<h3>Bacaan Dzikir</h3><ul><li><b>SubhanAllah (33x):</b> Maha Suci Allah.</li><li><b>Alhamdulillah (33x):</b> Segala puji bagi Allah.</li><li><b>Allahu Akbar (33x):</b> Allah Maha Besar.</li></ul>")
        ],
        "ru": [
            ("1. Порядок намаза (Мужчины)", "<h3>Положения в намазе для мужчин</h3>" + m_img + "<ol><li><b>Такбир:</b> Поднять руки до мочек ушей.</li><li><b>Кыям:</b> Сложить руки ниже пупка.</li><li><b>Руку:</b> Поясной поклон с прямой спиной (90 градусов).</li><li><b>Суджуд:</b> Земной поклон, локти приподняты от пола.</li><li><b>Сидение:</b> Сидеть на левой ступне, правая вертикально.</li></ol>"),
            ("2. Порядок намаза (Женщины)", "<h3>Положения в намазе для женщин</h3>" + f_img + "<ol><li><b>Такбир:</b> Поднять руки на уровень плеч.</li><li><b>Кыям:</b> Положить правую руку на левую на груди.</li><li><b>Руку:</b> Лёгкий наклон, руки на коленях.</li><li><b>Суджуд:</b> Локти прижаты к телу и полу.</li><li><b>Сидение:</b> Сидеть на левом бедре, стопы вправо.</li></ol>"),
            ("3. Как совершать омовение (Вуду)", "<h3>Пошаговое омовение</h3><ol><li>Сделать намерение и сказать Бисмиллях.</li><li>Вымыть кисти рук, рот, нос, лицо и руки до локтей по 3 раза.</li><li>Протереть голову и уши, затем вымыть ноги по 3 раза.</li></ol>"),
            ("4. Ракааты ежедневных намазов", "<h3>Таблица ракаатов</h3><ul><li><b>Фаджр:</b> 2 Сунна + 2 Фард</li><li><b>Зухр:</b> 4 Сунна + 4 Фард + 2 Сунна</li><li><b>Аср:</b> 4 Сунна + 4 Фард</li><li><b>Магриб:</b> 3 Фард + 2 Сунна</li><li><b>Иша:</b> 4 Сунна + 4 Фард + 2 Сунна + 3 Витр</li></ul>"),
            ("5. Пятничный намаз (Джума)", "<h3>Джума-намаз</h3><p>Совершается в джамаате в пятницу: 4 Сунна, слушание хутбы, 2 Фард и 4 Сунна.</p>"),
            ("6. Праздничные намазы (Ид)", "<h3>Праздничный намаз (2 ракаата)</h3><p>Включает по 3 дополнительных такбира в каждом ракаате.</p>"),
            ("7. Краткие зикры", "<h3>Ежедневное поминание Аллаха</h3><ul><li><b>Субханаллах (33 раза):</b> Слава Аллаху.</li><li><b>Альхамдулиллях (33 раза):</b> Хвала Аллаху.</li><li><b>Аллаху Акбар (33 раза):</b> Аллах Велик.</li></ul>")
        ],
        "zh": [
            ("1. 礼拜姿势（男性）", "<h3>男性礼拜步骤</h3>" + m_img + "<ol><li><b>抬手大赞：</b>双手抬至耳垂高度。</li><li><b>站立（格亚姆）：</b>双手交握于肚脐下方。</li><li><b>鞠躬（鲁库）：</b>背部平直成90度，双手扶膝。</li><li><b>叩头（苏朱德）：</b>双肘离地，腹部不贴大腿。</li><li><b>跪坐：</b>左脚平铺坐于其上，右脚立起。</li></ol>"),
            ("2. 礼拜姿势（女性）", "<h3>女性礼拜步骤</h3>" + f_img + "<ol><li><b>抬手大赞：</b>双手抬至肩膀高度。</li><li><b>站立：</b>右手叠放于左手之上置于胸前。</li><li><b>鞠躬：</b>身体微倾，双手放于膝盖上。</li><li><b>叩头：</b>双臂贴近身体两侧及地面。</li><li><b>跪坐：</b>左臀着地，双脚向右侧伸出。</li></ol>"),
            ("3. 如何做小净（乌都）", "<h3>小净步骤</h3><ol><li>举意并念泰斯米（奉真主之名）。</li><li>依次洗双手、漱口、呛鼻、洗脸及洗双臂至肘部各3次。</li><li>抹头与双耳1次，最后洗双脚至踝部各3次。</li></ol>"),
            ("4. 每日五番拜拜数", "<h3>拜数总览</h3><ul><li><b>晨礼：</b>2拜圣行 + 2拜主命</li><li><b>晌礼：</b>4拜前圣行 + 4拜主命 + 2拜后圣行</li><li><b>晡礼：</b>4拜圣行 + 4拜主命</li><li><b>昏礼：</b>3拜主命 + 2拜圣行</li><li><b>宵礼：</b>4拜前圣行 + 4拜主命 + 2拜后圣行 + 3拜奇数拜</li></ul>"),
            ("5. 主麻聚礼", "<h3>主麻拜</h3><p>周五集体礼拜：4拜圣行、聆听呼图白演讲、2拜集体主命拜，随后4拜圣行。</p>"),
            ("6. 会礼（开斋节与古尔邦节）", "<h3>节日会礼（2拜）</h3><p>每拜中包含3次额外的大赞词。</p>"),
            ("7. 日常赞念词", "<h3>日常记念真主</h3><ul><li><b>赞主超绝 (33遍)：</b>SubhanAllah</li><li><b>一切赞颂全归真主 (33遍)：</b>Alhamdulillah</li><li><b>真主至大 (33遍)：</b>Allahu Akbar</li></ul>")
        ],
        "ar": [
            ("١. صفة الصلاة للرجال", "<h3>أركان وصفة الصلاة للرجال</h3>" + m_img + "<ol><li><b>تكبيرة الإحرام:</b> رفع اليدين حذو شحمتي الأذنين وقول الله أكبر.</li><li><b>القيام:</b> وضع اليد اليمنى على اليسرى تحت السرة وقراءة الفاتحة.</li><li><b>الركوع:</b> انحناء الظهر مستوياً بمقدار ٩٠ درجة ووضع اليدين على الركبتين.</li><li><b>السجود:</b> مجافاة المرفقين عن الأرض والبطن عن الفخذين.</li><li><b>الجلوس والتسليم:</b> افتراش القدم اليسرى ونصب اليمنى وقراءة التشهد ثم التسليم.</li></ol>"),
            ("٢. صفة الصلاة للنساء", "<h3>أركان وصفة الصلاة للنساء</h3>" + f_img + "<ol><li><b>تكبيرة الإحرام:</b> رفع اليدين حذو المنكبين.</li><li><b>القيام:</b> وضع اليد اليمنى على اليسرى على الصدر.</li><li><b>الركوع:</b> انحناء يسير بالظهر مع ثني الركبتين قليلاً.</li><li><b>السجود:</b> ضم الذراعين إلى الجنبين والأرض والتجمع في السجود.</li><li><b>الجلوس (التورك):</b> الجلوس على الورك الأيسر وإخراج القدمين من جهة اليمين.</li></ol>"),
            ("٣. كيفية الوضوء", "<h3>خطوات الوضوء</h3><ol><li>النية والتسمية (بسم الله).</li><li>غسل الكفين، والمضمضة، والاستنشاق، وغسل الوجه واليدين إلى المرفقين ثلاث مرات.</li><li>مسح الرأس والأذنين مرة واحدة، ثم غسل الرجلين إلى الكعبين ثلاث مرات.</li></ol>"),
            ("٤. عدد ركعات الصلوات الخمس", "<h3>جدول الركعات اليومية</h3><ul><li><b>الفجر:</b> ٢ سنة + ٢ فرض</li><li><b>الظهر:</b> ٤ سنة قبلية + ٤ فرض + ٢ سنة بعدية</li><li><b>العصر:</b> ٤ سنة + ٤ فرض</li><li><b>المغرب:</b> ٣ فرض + ٢ سنة</li><li><b>العشاء:</b> ٤ سنة قبلية + ٤ فرض + ٢ سنة بعدية + ٣ وتر</li></ul>"),
            ("٥. صلاة الجمعة", "<h3>صلاة الجمعة</h3><p>تُصلى جماعة يوم الجمعة: ٤ ركعات سنة، ثم الاستماع للخطبة، ثم ركعتان فرضاً مع الإمام، ثم ٤ ركعات سنة.</p>"),
            ("٦. صلاة العيدين", "<h3>صلاة عيد الفطر والأضحى (ركعتان)</h3><p>تتضمن ٣ تكبيرات زوائد في كل ركعة قبل القراءة في الأولى وقبل الركوع في الثانية.</p>"),
            ("٧. أذكار قصيرة", "<h3>التسبيح اليومي</h3><ul><li><b>سبحان الله (٣٣ مرة)</b></li><li><b>الحمد لله (٣٣ مرة)</b></li><li><b>الله أكبر (٣٣ مرة)</b></li><li><b>لا إله إلا الله</b></li></ul>")
        ],
        "ur": [
            ("1. مردوں کی نماز کا طریقہ", "<h3>مردوں کے لیے نماز کے ارکان</h3>" + m_img + "<ol><li><b>تکبیرِ تحریمہ:</b> ہاتھ کانوں کی لو تک اٹھا کر اللہ اکبر کہنا۔</li><li><b>قیام:</b> ناف کے نیچے ہاتھ باندھنا اور ثناء، سورہ فاتحہ و سورت پڑھنا۔</li><li><b>رکوع:</b> کمر کو بالکل سیدھا (90 ڈگری) جھکانا اور گھٹنوں کو پکڑنا۔</li><li><b>سجدہ:</b> کہنیوں کو زمین سے اور پیٹ کو رانوں سے جدا رکھنا۔</li><li><b>قعدہ اور سلام:</b> بایاں پاؤں بچھا کر اس پر بیٹھنا اور دایاں پاؤں کھڑا رکھنا۔</li></ol>"),
            ("2. خواتین کی نماز کا طریقہ", "<h3>خواتین کے لیے نماز کے ارکان</h3>" + f_img + "<ol><li><b>تکبیرِ تحریمہ:</b> ہاتھ کندھوں تک اٹھانا۔</li><li><b>قیام:</b> سینے پر دایاں ہاتھ بائیں ہاتھ پر رکھنا۔</li><li><b>رکوع:</b> قدرے جھکنا اور ہاتھ گھٹنوں پر رکھنا۔</li><li><b>سجدہ:</b> بازو پہلوؤں اور زمین سے ملا کر سمٹ کر سجدہ کرنا۔</li><li><b>قعدہ (تورک):</b> بائیں سرین پر بیٹھنا اور دونوں پاؤں دائیں جانب نکالنا۔</li></ol>"),
            ("3. وضو کا طریقہ", "<h3>وضو کے مراحل</h3><ol><li>نیت کرنا اور بسم اللہ پڑھنا۔</li><li>ہاتھ، کلی، ناک، چہرہ اور کہنیوں سمیت بازو تین تین بار دھونا۔</li><li>سر اور کانوں کا مسح کرنا، پھر ٹخنوں سمیت پاؤں تین بار دھونا۔</li></ol>"),
            ("4. پنجگانہ نمازوں کی رکعتیں", "<h3>روزانہ کی رکعتوں کا خلاصہ</h3><ul><li><b>فجر:</b> 2 سنت + 2 فرض</li><li><b>ظہر:</b> 4 سنت + 4 فرض + 2 سنت</li><li><b>عصر:</b> 4 سنت + 4 فرض</li><li><b>مغرب:</b> 3 فرض + 2 سنت</li><li><b>عشاء:</b> 4 سنت + 4 فرض + 2 سنت + 3 وتر</li></ul>"),
            ("5. نمازِ جمعہ", "<h3>نمازِ جمعہ</h3><p>جمعہ کے دن باجماعت ادا کی جاتی ہے: 4 سنت، خطبہ سننا، 2 فرض باجماعت اور 4 سنت۔</p>"),
            ("6. عیدین کی نماز", "<h3>نمازِ عید الفطر و عید الاضحیٰ (2 رکعت)</h3><p>ہر رکعت میں 3 زائد تکبیرات کہی جاتی ہیں۔</p>"),
            ("7. مختصر اذکار", "<h3>روزانہ کی تسبیحات</h3><ul><li><b>سبحان اللہ (33 مرتبہ)</b></li><li><b>الحمد للہ (33 مرتبہ)</b></li><li><b>اللہ اکبر (33 مرتبہ)</b></li></ul>")
        ],
        "en": [
            ("1. Prayer Postures (Men)", "<h3>Prayer Postures for Men</h3>" + m_img + "<ol><li><b>Takbir:</b> Raise hands up to earlobes.</li><li><b>Qiyam:</b> Clasp hands below the navel.</li><li><b>Ruku:</b> Bow with back completely flat (90 degrees).</li><li><b>Sujood:</b> Keep elbows lifted from the ground and stomach away from thighs.</li><li><b>Sitting:</b> Sit on left foot with right foot upright.</li></ol>"),
            ("2. Prayer Postures (Women)", "<h3>Prayer Postures for Women</h3>" + f_img + "<ol><li><b>Takbir:</b> Raise hands up to shoulder level.</li><li><b>Qiyam:</b> Place right hand over left on the chest.</li><li><b>Ruku:</b> Bow slightly with knees slightly bent and hands on knees.</li><li><b>Sujood:</b> Keep arms close to sides and body compact.</li><li><b>Sitting:</b> Sit on left hip with both feet extended to the right.</li></ol>"),
            ("3. How to Perform Wudu", "<h3>Step-by-Step Wudu</h3><ol><li>Make intention and say Bismillah.</li><li>Wash hands, mouth, nose, face, and arms 3 times.</li><li>Wipe head and ears once, then wash feet 3 times.</li></ol>"),
            ("4. Daily Prayer Rakahs", "<h3>Summary of Daily Rakahs</h3><ul><li><b>Fajr:</b> 2 Sunnah + 2 Fard</li><li><b>Dhuhr:</b> 4 Sunnah + 4 Fard + 2 Sunnah</li><li><b>Asr:</b> 4 Sunnah + 4 Fard</li><li><b>Maghrib:</b> 3 Fard + 2 Sunnah</li><li><b>Isha:</b> 4 Sunnah + 4 Fard + 2 Sunnah + 3 Witr</li></ul>"),
            ("5. Jumu'ah (Friday) Prayer", "<h3>Jumu'ah Prayer</h3><p>Performed in congregation on Friday instead of Dhuhr: 4 Rakah Sunnah, listening to the Khutbah, 2 Rakah Fard in congregation, followed by 4 Rakah Sunnah.</p>"),
            ("6. Eid Prayers (Fitr & Adha)", "<h3>Eid Prayer (2 Rakahs)</h3><p>Includes 3 extra Takbirs in each Rakah: In the 1st Rakah, after Subhanaka, raise hands 3 times (drop sides on first two, fold on the 3rd). In the 2nd Rakah, after recitation, raise hands 3 times before bowing on the 4th Takbir.</p>"),
            ("7. Short Dhikr & Meanings", "<h3>Daily Remembrance (Dhikr)</h3><ul><li><b>SubhanAllah (33x):</b> <i>Glory be to Allah.</i></li><li><b>Alhamdulillah (33x):</b> <i>All praise is due to Allah.</i></li><li><b>Allahu Akbar (33x):</b> <i>Allah is the Greatest.</i></li><li><b>La ilaha illallah:</b> <i>There is no deity worthy of worship except Allah.</i></li><li><b>Astaghfirullah:</b> <i>I seek forgiveness from Allah.</i></li></ul>")
        ]
    }

class GuideWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        self.mp, self.fp = ensure_imgs()
        l = QHBoxLayout(self); l.setContentsMargins(28,12,28,24); l.setSpacing(14)
        self.lst = QListWidget(); self.lst.itemClicked.connect(self.render_current); l.addWidget(self.lst, 1)
        self.view = QTextBrowser(); self.view.setStyleSheet("border:none;"); l.addWidget(self.view, 2)
        self.set_prefs(lang, fsize)

    def render_current(self, it=None):
        it = it or self.lst.currentItem()
        if not it: return
        vw = self.view.viewport().width()
        w = max(260, min(860, vw - 24)) if vw > 100 else 380
        html = it.data(Qt.UserRole).replace("__MIMG__", f"file://{self.mp}").replace("__FIMG__", f"file://{self.fp}").replace("__IMGW__", str(w))
        d = "rtl" if self.lang in ("ar", "ur") else "ltr"
        al = "right" if d == "rtl" else "left"
        self.view.setHtml(f"<div dir='{d}' align='{al}' style='font-size:{self.fsize}px; line-height:1.6; text-align:{al};'>{html}</div>")

    def showEvent(self, e):
        super().showEvent(e)
        self.render_current()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.render_current()

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        row = max(0, self.lst.currentRow())
        self.lst.clear()
        for title, body in get_bundle(lang)["guide"]:
            it = QListWidgetItem(title); it.setData(Qt.UserRole, body); self.lst.addItem(it)
        self.lst.setCurrentRow(row if row < self.lst.count() else 0)
        self.render_current()
