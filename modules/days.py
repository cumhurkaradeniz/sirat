from datetime import date
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextBrowser
from modules.i18n import STRINGS, get_bundle

DAYS = {
    "tr": [
        ("2026-12-10", "Üç Ayların Başlangıcı (1 Recep)", "<h3>Üç Ayların Başlangıcı</h3><p>Recep, Şaban ve Ramazan aylarını kapsayan manevi arınma mevsimidir.</p><ul><li>Kaza ve nafile namazlar kılmak</li><li>Kur'an tilavetini artırmak</li><li>Pazartesi ve Perşembe oruç tutmak</li></ul>"),
        ("2026-12-17", "Regaip Kandili", "<h3>Regaip Kandili</h3><p>Recep ayının ilk Cuma gecesidir; rahmet ve bereket gecesidir.</p><ul><li>Teheccüd ve tesbih namazı kılmak</li><li>Tövbe, istiğfar ve sadaka vermek</li></ul>"),
        ("2027-01-05", "Miraç Kandili", "<h3>Miraç Kandili</h3><p>Beş vakit namazın farz kılındığı mübarek gecedir.</p><ul><li>Beş vakit namazı huşu ile kılmak</li><li>Bakara Suresi son iki ayetini okumak</li></ul>"),
        ("2027-01-24", "Berat Kandili", "<h3>Berat Kandili</h3><p>Şaban ayının 15. gecesi, günahlardan arınma ve af gecesidir.</p><ul><li>Geceyi ibadetle ihya etmek</li><li>Ertesi gün nafile oruç tutmak</li></ul>"),
        ("2027-02-08", "Ramazan-ı Şerif Başlangıcı", "<h3>Ramazan Ayı</h3><p>Oruç, teravih ve Kur'an ayıdır.</p><ul><li>Oruç tutmak ve teravih kılmak</li><li>Fitre ve zekat vermek</li></ul>"),
        ("2027-03-05", "Kadir Gecesi", "<h3>Kadir Gecesi</h3><p>Bin aydan daha hayırlı olduğu müjdelenen gecedir.</p><ul><li>Kur'an okuyup dua etmek</li></ul>"),
        ("2027-03-09", "Ramazan Bayramı (3 Gün)", "<h3>Ramazan Bayramı</h3><p>Bayram namazı, fitre sadakası ve akraba ziyareti günleridir.</p>"),
        ("2027-05-15", "Kurban Bayramı Arifesi", "<h3>Kurban Bayramı Arifesi</h3><p>Arafat günü orucu ve sabah namazından itibaren Teşrik Tekbirleri başlar.</p>"),
        ("2027-05-16", "Kurban Bayramı (4 Gün)", "<h3>Kurban Bayramı</h3><p>Bayram namazı, kurban ibadeti ve paylaşma günleridir.</p>"),
        ("2027-06-06", "Hicri Yılbaşı (1 Muharrem)", "<h3>Hicri Yılbaşı 1449</h3><p>Muharrem ayında nafile oruç tutmak ve dua etmek faziletlidir.</p>"),
        ("2027-06-15", "Aşure Günü (10 Muharrem)", "<h3>Aşure Günü</h3><p>Muharrem ayının 9-10 veya 10-11. günleri oruç tutmak ve ikramda bulunmak sünnettir.</p>"),
        ("2027-08-14", "Mevlid Kandili", "<h3>Mevlid Kandili</h3><p>Peygamber Efendimiz'e (s.a.v.) bolca salavat getirmek ve Siyer okumak tavsiye edilir.</p>")
    ],
    "en": [
        ("2026-12-10", "Start of Three Holy Months", "<h3>Beginning of Rajab</h3><p>Season of spiritual renewal: Nafl prayers, Quran recitation, and voluntary fasting.</p>"),
        ("2026-12-17", "Laylat al-Raghaib", "<h3>Laylat al-Raghaib</h3><p>First Friday night of Rajab: Night prayers, repentance, and charity.</p>"),
        ("2027-01-05", "Isra and Mi'raj", "<h3>Night of Isra and Mi'raj</h3><p>The night five daily prayers were ordained.</p>"),
        ("2027-01-24", "Laylat al-Bara'ah", "<h3>Night of Forgiveness (Mid-Sha'ban)</h3><p>Night of seeking mercy and fasting the next day.</p>"),
        ("2027-02-08", "Start of Ramadan", "<h3>Blessed Month of Ramadan</h3><p>Month of fasting, Taraweeh prayers, and Zakat.</p>"),
        ("2027-03-05", "Laylat al-Qadr", "<h3>Night of Decree</h3><p>Better than a thousand months.</p>"),
        ("2027-03-09", "Eid al-Fitr (3 Days)", "<h3>Eid al-Fitr</h3><p>Eid prayer, Zakat al-Fitr, and family visits.</p>"),
        ("2027-05-15", "Day of Arafah", "<h3>Day of Arafah</h3><p>Fasting on Arafah and beginning Takbir al-Tashreeq after Fajr.</p>"),
        ("2027-05-16", "Eid al-Adha (4 Days)", "<h3>Eid al-Adha</h3><p>Eid prayer, Qurbani sacrifice, sharing with the needy, and Takbir al-Tashreeq.</p>"),
        ("2027-06-06", "Islamic New Year (1 Muharram)", "<h3>Islamic New Year 1449 AH</h3><p>Commemorating the Hijrah; voluntary fasting in Muharram.</p>"),
        ("2027-06-15", "Day of Ashura (10 Muharram)", "<h3>Day of Ashura</h3><p>Fasting on the 9th–10th or 10th–11th of Muharram and giving charity.</p>"),
        ("2027-08-14", "Mawlid al-Nabi", "<h3>Mawlid al-Nabi</h3><p>Sending abundant Salawat upon Prophet Muhammad ﷺ and studying his Seerah.</p>")
    ],
    "fr": [
        ("2026-12-10", "Début des Trois Mois Sacrés", "<h3>Début de Rajab</h3><p>Saison de renouveau spirituel : prières surérogatoires, lecture du Coran et jeûne.</p>"),
        ("2026-12-17", "Nuit de Raghaïb", "<h3>Laylat al-Raghaïb</h3><p>Première nuit du vendredi de Rajab : prières nocturnes, repentir et aumône.</p>"),
        ("2027-01-05", "Isra et Mi'raj", "<h3>Nuit de l'Ascension</h3><p>La nuit où les cinq prières quotidiennes furent prescrites.</p>"),
        ("2027-01-24", "Nuit du Pardon (Bara'ah)", "<h3>Mi-Cha'bane</h3><p>Nuit de miséricorde, d'invocation et de jeûne le lendemain.</p>"),
        ("2027-02-08", "Début du Ramadan", "<h3>Mois Béni du Ramadan</h3><p>Mois du jeûne, des prières de Tarawih et de la Zakat.</p>"),
        ("2027-03-05", "Nuit du Destin (Al-Qadr)", "<h3>Laylat al-Qadr</h3><p>Meilleure que mille mois.</p>"),
        ("2027-03-09", "Aïd al-Fitr (3 Jours)", "<h3>Aïd al-Fitr</h3><p>Prière de l'Aïd, Zakat al-Fitr et visites familiales.</p>"),
        ("2027-05-15", "Jour d'Arafat", "<h3>Jour d'Arafat</h3><p>Jeûne d'Arafat et début des Takbirat al-Tachriq après le Fajr.</p>"),
        ("2027-05-16", "Aïd al-Adha (4 Jours)", "<h3>Aïd al-Adha</h3><p>Prière de l'Aïd, sacrifice (Qurbani) et partage avec les nécessiteux.</p>"),
        ("2027-06-06", "Nouvel An Hégirien (1 Muharram)", "<h3>Nouvel An Islamique 1449</h3><p>Commémoration de l'Hégire et jeûne recommandé en Muharram.</p>"),
        ("2027-06-15", "Jour d'Achoura (10 Muharram)", "<h3>Jour d'Achoura</h3><p>Jeûne des 9-10 ou 10-11 Muharram et aumône.</p>"),
        ("2027-08-14", "Mawlid al-Nabi", "<h3>Mawlid al-Nabi</h3><p>Multiplier les prières sur le Prophète ﷺ et étudier sa Sira.</p>")
    ],
    "es": [
        ("2026-12-10", "Inicio de los Tres Meses Sagrados", "<h3>Comienzo de Rayab</h3><p>Temporada de renovación espiritual: oración, lectura del Corán y ayuno voluntario.</p>"),
        ("2026-12-17", "Noche de Raghaib", "<h3>Laylat al-Raghaib</h3><p>Primera noche de viernes de Rayab: oración nocturna y caridad.</p>"),
        ("2027-01-05", "Isra y Mi'raj", "<h3>Noche de Isra y Mi'raj</h3><p>La noche en que se prescribieron las cinco oraciones diarias.</p>"),
        ("2027-01-24", "Noche del Perdón (Bara'ah)", "<h3>Mitad de Sha'ban</h3><p>Noche de súplica y ayuno al día siguiente.</p>"),
        ("2027-02-08", "Inicio de Ramadán", "<h3>Mes Bendito de Ramadán</h3><p>Mes de ayuno, oración de Tarawih y Zakat.</p>"),
        ("2027-03-05", "Noche del Destino (Al-Qadr)", "<h3>Laylat al-Qadr</h3><p>Mejor que mil meses.</p>"),
        ("2027-03-09", "Eid al-Fitr (3 Días)", "<h3>Eid al-Fitr</h3><p>Oración del Eid, Zakat al-Fitr y visitas familiares.</p>"),
        ("2027-05-15", "Día de Arafah", "<h3>Día de Arafah</h3><p>Ayuno de Arafah e inicio del Takbir al-Tashriq tras el Fajr.</p>"),
        ("2027-05-16", "Eid al-Adha (4 Días)", "<h3>Eid al-Adha</h3><p>Oración del Eid, sacrificio (Qurbani) y compartir con los necesitados.</p>"),
        ("2027-06-06", "Año Nuevo Islámico (1 Muharram)", "<h3>Año Nuevo Hégira 1449</h3><p>Conmemoración de la Hégira y ayuno en Muharram.</p>"),
        ("2027-06-15", "Día de Ashura (10 Muharram)", "<h3>Día de Ashura</h3><p>Ayuno los días 9-10 o 10-11 de Muharram y caridad.</p>"),
        ("2027-08-14", "Mawlid al-Nabi", "<h3>Mawlid al-Nabi</h3><p>Enviar bendiciones al Profeta ﷺ y estudiar su vida.</p>")
    ],
    "pt": [
        ("2026-12-10", "Início dos Três Meses Sagrados", "<h3>Começo de Rajab</h3><p>Época de renovação espiritual: orações, leitura do Alcorão e jejum voluntário.</p>"),
        ("2026-12-17", "Noite de Raghaib", "<h3>Laylat al-Raghaib</h3><p>Primeira noite de sexta-feira de Rajab: oração noturna e caridade.</p>"),
        ("2027-01-05", "Isra e Mi'raj", "<h3>Noite de Isra e Mi'raj</h3><p>A noite em que as cinco orações diárias foram instituídas.</p>"),
        ("2027-01-24", "Noite do Perdão (Bara'ah)", "<h3>Metade de Sha'ban</h3><p>Noite de misericórdia e jejum no dia seguinte.</p>"),
        ("2027-02-08", "Início do Ramadã", "<h3>Mês Abençoado do Ramadã</h3><p>Mês de jejum, orações Tarawih e Zakat.</p>"),
        ("2027-03-05", "Noite do Decreto (Al-Qadr)", "<h3>Laylat al-Qadr</h3><p>Melhor do que mil meses.</p>"),
        ("2027-03-09", "Eid al-Fitr (3 Dias)", "<h3>Eid al-Fitr</h3><p>Oração do Eid, Zakat al-Fitr e visitas familiares.</p>"),
        ("2027-05-15", "Dia de Arafah", "<h3>Dia de Arafah</h3><p>Jejum de Arafah e início do Takbir al-Tashriq após o Fajr.</p>"),
        ("2027-05-16", "Eid al-Adha (4 Dias)", "<h3>Eid al-Adha</h3><p>Oração do Eid, sacrifício (Qurbani) e partilha com os necessitados.</p>"),
        ("2027-06-06", "Ano Novo Islâmico (1 Muharram)", "<h3>Ano Novo Islâmico 1449</h3><p>Comemoração da Hégira e jejum voluntário em Muharram.</p>"),
        ("2027-06-15", "Dia de Ashura (10 Muharram)", "<h3>Dia de Ashura</h3><p>Jejum nos dias 9-10 ou 10-11 de Muharram e caridade.</p>"),
        ("2027-08-14", "Mawlid al-Nabi", "<h3>Mawlid al-Nabi</h3><p>Enviar bênçãos ao Profeta ﷺ e estudar a sua biografia.</p>")
    ]
}

DAYS.update({
    "id": [
        ("2026-12-10", "Awal Tiga Bulan Suci (1 Rajab)", "<h3>Awal Bulan Rajab</h3><p>Musim penyucian jiwa: memperbanyak shalat sunnah, tilawah Al-Qur'an, dan puasa sunnah.</p>"),
        ("2026-12-17", "Malam Raghaib", "<h3>Laylat al-Raghaib</h3><p>Malam Jumat pertama bulan Rajab: shalat malam, istighfar, dan sedekah.</p>"),
        ("2027-01-05", "Isra Mi'raj", "<h3>Malam Isra dan Mi'raj</h3><p>Malam diwajibkannya shalat lima waktu.</p>"),
        ("2027-01-24", "Malam Nisfu Sya'ban", "<h3>Malam Pengampunan</h3><p>Malam memohon ampunan dan berpuasa sunnah pada keesokan harinya.</p>"),
        ("2027-02-08", "Awal Ramadhan", "<h3>Bulan Suci Ramadhan</h3><p>Bulan puasa, shalat Tarawih, tadarus Al-Qur'an, dan zakat.</p>"),
        ("2027-03-05", "Lailatul Qadar", "<h3>Malam Kemuliaan</h3><p>Malam yang lebih baik dari seribu bulan.</p>"),
        ("2027-03-09", "Idul Fitri (3 Hari)", "<h3>Hari Raya Idul Fitri</h3><p>Shalat Id, menunaikan zakat fitrah, dan silaturahmi.</p>"),
        ("2027-05-15", "Hari Arafah", "<h3>Hari Arafah</h3><p>Puasa sunnah Arafah dan dimulainya Takbir Tasyrik setelah Subuh.</p>"),
        ("2027-05-16", "Idul Adha (4 Hari)", "<h3>Hari Raya Idul Adha</h3><p>Shalat Id, ibadah kurban, dan berbagi kepada sesama.</p>"),
        ("2027-06-06", "Tahun Baru Islam (1 Muharram)", "<h3>Tahun Baru Hijriah 1449</h3><p>Memperingati peristiwa Hijrah dan puasa sunnah bulan Muharram.</p>"),
        ("2027-06-15", "Hari Asyura (10 Muharram)", "<h3>Hari Asyura</h3><p>Puasa sunnah tanggal 9-10 atau 10-11 Muharram dan bersedekah.</p>"),
        ("2027-08-14", "Maulid Nabi Muhammad ﷺ", "<h3>Maulid Nabi</h3><p>Memperbanyak shalawat kepada Nabi ﷺ dan mempelajari sirah beliau.</p>")
    ],
    "ru": [
        ("2026-12-10", "Начало трёх священных месяцев", "<h3>Начало месяца Раджаб</h3><p>Время духовного очищения: дополнительные намазы, чтение Корана и пост.</p>"),
        ("2026-12-17", "Ночь Рагаиб", "<h3>Ляйлят аль-Рагаиб</h3><p>Первая пятничная ночь Раджаба: ночные молитвы, покаяние и милостыня.</p>"),
        ("2027-01-05", "Ночь Исра и Мирадж", "<h3>Ночь Вознесения</h3><p>Ночь, когда были предписаны пять ежедневных намазов.</p>"),
        ("2027-01-24", "Ночь Бараат (середина Шаабана)", "<h3>Ночь прощения</h3><p>Ночь молитв о прощении и добровольного поста на следующий день.</p>"),
        ("2027-02-08", "Начало месяца Рамадан", "<h3>Священный Рамадан</h3><p>Месяц обязательного поста, намазов Таравих и Закята.</p>"),
        ("2027-03-05", "Ночь Предопределения (Ляйлят аль-Кадр)", "<h3>Ночь Могущества</h3><p>Ночь, которая лучше тысячи месяцев.</p>"),
        ("2027-03-09", "Ураза-байрам (Ид аль-Фитр)", "<h3>Праздник Разговения</h3><p>Праздничный намаз, выплата Закят аль-Фитр и посещение родных.</p>"),
        ("2027-05-15", "День Арафа", "<h3>День Арафа</h3><p>Пост в день Арафа и начало такбиров Ташрик после утреннего намаза.</p>"),
        ("2027-05-16", "Курбан-байрам (Ид аль-Адха)", "<h3>Праздник Жертвоприношения</h3><p>Праздничный намаз, жертвоприношение и помощь нуждающимся.</p>"),
        ("2027-06-06", "Исламский Новый год (1 Мухаррам)", "<h3>1449 год по Хиджре</h3><p>Память о Хиджре и добровольный пост в месяц Мухаррам.</p>"),
        ("2027-06-15", "День Ашура (10 Мухаррам)", "<h3>День Ашура</h3><p>Пост 9-10 или 10-11 Мухаррама и раздача милостыни.</p>"),
        ("2027-08-14", "Мавлид ан-Наби", "<h3>Рождение Пророка ﷺ</h3><p>Чтение салаватов Пророку Мухаммаду ﷺ и изучение его жизнеописания.</p>")
    ],
    "zh": [
        ("2026-12-10", "三个圣月开始（莱哲卜月1日）", "<h3>莱哲卜月开始</h3><p>心灵净化的季节：多做副功拜、诵读古兰经与自愿斋戒。</p>"),
        ("2026-12-17", "莱加伊布之夜", "<h3>莱加伊布之夜</h3><p>莱哲卜月第一个主麻夜：夜间礼拜、忏悔与施舍。</p>"),
        ("2027-01-05", "登宵节（夜行与登宵）", "<h3>登宵之夜</h3><p>真主规定每日五次礼拜的神圣夜晚。</p>"),
        ("2027-01-24", "白拉阿特之夜（舍尔邦月15日）", "<h3>赦免之夜</h3><p>祈求真主宽恕并在次日封副功斋的夜晚。</p>"),
        ("2027-02-08", "斋月开始（莱麦丹月）", "<h3>尊贵的斋月</h3><p>斋戒、泰拉威哈礼拜、诵读古兰经与缴纳天课的月份。</p>"),
        ("2027-03-05", "盖德尔夜（高贵之夜）", "<h3>前定之夜</h3><p>胜过一千个月的神圣夜晚。</p>"),
        ("2027-03-09", "开斋节（3天）", "<h3>开斋节</h3><p>参加会礼、缴纳开斋捐并探望亲友。</p>"),
        ("2027-05-15", "阿拉法特日", "<h3>阿拉法特日</h3><p>阿拉法特日斋戒，晨礼后开始念泰什里格大赞词。</p>"),
        ("2027-05-16", "古尔邦节（宰牲节 4天）", "<h3>古尔邦节</h3><p>参加会礼、献牲并与穷人分享肉食。</p>"),
        ("2027-06-06", "伊斯兰新年（穆哈兰月1日）", "<h3>伊历1449年新年</h3><p>纪念迁徙（希吉来）并在穆哈兰月封副功斋。</p>"),
        ("2027-06-15", "阿舒拉日（穆哈兰月10日）", "<h3>阿舒拉日</h3><p>在穆哈兰月9-10日或10-11日封斋并行善施舍。</p>"),
        ("2027-08-14", "圣纪节（穆罕默德圣人诞辰）", "<h3>圣纪节</h3><p>多念赞圣词并学习先知穆罕默德 ﷺ 的生平事迹。</p>")
    ],
    "ar": [
        ("2026-12-10", "بداية الأشهر الحرم (1 رجب)", "<h3>غرة شهر رجب</h3><p>موسم الطاعات وتزكية النفس بالإكثار من النوافل وتلاوة القرآن والصيام.</p>"),
        ("2026-12-17", "ليلة الرغائب", "<h3>ليلة الرغائب</h3><p>أول ليلة جمعة من شهر رجب؛ يُستحب فيها قيام الليل والاستغفار والصدقة.</p>"),
        ("2027-01-05", "ليلة الإسراء والمعراج", "<h3>الإسراء والمعراج</h3><p>الليلة المباركة التي فُرضت فيها الصلوات الخمس.</p>"),
        ("2027-01-24", "ليلة النصف من شعبان", "<h3>ليلة البراءة والمغفرة</h3><p>ليلة الدعاء والاستغفار وصيام يوم الخامس عشر من شعبان.</p>"),
        ("2027-02-08", "بداية شهر رمضان المبارك", "<h3>شهر رمضان</h3><p>شهر الصيام والقيام والتراويح وتلاوة القرآن والزكاة.</p>"),
        ("2027-03-05", "ليلة القدر", "<h3>ليلة القدر</h3><p>ليلة خير من ألف شهر، يُستحب إحياؤها بالصلاة والقرآن والدعاء.</p>"),
        ("2027-03-09", "عيد الفطر المبارك (3 أيام)", "<h3>عيد الفطر</h3><p>صلاة العيد وإخراج زكاة الفطر وصلة الأرحام.</p>"),
        ("2027-05-15", "يوم عرفة", "<h3>يوم عرفة</h3><p>صيام يوم عرفة لغير الحاج وبدء تكبيرات التشريق بعد صلاة الفجر.</p>"),
        ("2027-05-16", "عيد الأضحى المبارك (4 أيام)", "<h3>عيد الأضحى</h3><p>صلاة العيد وذبح الأضحية ومشاركة اللحوم مع الفقراء والأقارب.</p>"),
        ("2027-06-06", "رأس السنة الهجرية (1 محرم)", "<h3>العام الهجري 1449</h3><p>ذكرى الهجرة النبوية الشريفة وصيام التطوع في شهر الله المحرم.</p>"),
        ("2027-06-15", "يوم عاشوراء (10 محرم)", "<h3>يوم عاشوراء</h3><p>صيام اليوم التاسع والعاشر أو العاشر والحادي عشر من محرم والصدقة.</p>"),
        ("2027-08-14", "المولد النبوي الشريف", "<h3>ذكرى المولد النبوي</h3><p>الإكثار من الصلاة والسلام على رسول الله ﷺ وقراءة سيرته العطرة.</p>")
    ],
    "ur": [
        ("2026-12-10", "تین بابرکت مہینوں کا آغاز (یکم رجب)", "<h3>ماہِ رجب کا آغاز</h3><p>روحانی تربیت کا موسم: نوافل، تلاوتِ قرآن اور نفلی روزوں کا اہتمام کریں۔</p>"),
        ("2026-12-17", "شبِ رغائب", "<h3>شبِ رغائب</h3><p>رجب کی پہلی شبِ جمعہ: تہجد، توبہ و استغفار اور صدقہ و خیرات کی رات۔</p>"),
        ("2027-01-05", "شبِ معراج", "<h3>شبِ اسراء و معراج</h3><p>وہ بابرکت رات جس میں پانچ وقت کی نمازیں فرض کی گئیں۔</p>"),
        ("2027-01-24", "شبِ برات (15 شعبان)", "<h3>مغفرت کی رات</h3><p>عبادت، دعا اور اگلے دن نفلی روزہ رکھنے کی فضیلت ہے۔</p>"),
        ("2027-02-08", "آغازِ رمضان المبارک", "<h3>ماہِ رمضان</h3><p>روزہ، تراویح، تلاوتِ قرآن اور زکوٰۃ کا بابرکت مہینہ۔</p>"),
        ("2027-03-05", "شبِ قدر", "<h3>لیلۃ القدر</h3><p>ہزار مہینوں سے بہتر رات؛ عبادت اور دعا میں گزاریں۔</p>"),
        ("2027-03-09", "عید الفطر (3 دن)", "<h3>عید الفطر</h3><p>نمازِ عید، صدقہ فطر کی ادائیگی اور صلہ رحمی کے دن۔</p>"),
        ("2027-05-15", "یومِ عرفہ", "<h3>یومِ عرفہ</h3><p>یومِ عرفہ کا روزہ اور نمازِ فجر کے بعد تکبیراتِ تشریق کا آغاز۔</p>"),
        ("2027-05-16", "عید الاضحیٰ (4 دن)", "<h3>عید الاضحیٰ</h3><p>نمازِ عید، قربانی اور مستحقین میں گوشت تقسیم کرنے کے ایام۔</p>"),
        ("2027-06-06", "اسلامی نیا سال (یکم محرم)", "<h3>نیا ہجری سال 1449</h3><p>ہجرتِ نبوی ﷺ کی یاد اور ماہِ محرم میں نفلی روزوں کی فضیلت۔</p>"),
        ("2027-06-15", "یومِ عاشورہ (10 محرم)", "<h3>یومِ عاشورہ</h3><p>9 اور 10 یا 10 اور 11 محرم کا روزہ رکھنا اور صدقہ دینا مسنون ہے۔</p>"),
        ("2027-08-14", "عید میلاد النبی ﷺ", "<h3>ولادتِ باسعادت ﷺ</h3><p>نبی کریم ﷺ پر کثرت سے درود و سلام بھیجیں اور سیرتِ طیبہ کا مطالعہ کریں۔</p>")
    ]
})

class DaysWidget(QWidget):
    def __init__(self, lang="tr", fsize=15):
        super().__init__()
        l = QHBoxLayout(self); l.setContentsMargins(28,12,28,24); l.setSpacing(14)
        self.lst = QListWidget(); self.lst.setWordWrap(True); self.lst.setHorizontalScrollBarPolicy(1)
        self.lst.itemClicked.connect(lambda it: self.view.setHtml(self.wrap(it.data(Qt.UserRole))))
        l.addWidget(self.lst, 1)
        self.view = QTextBrowser(); self.view.setStyleSheet("border:none;"); l.addWidget(self.view, 2)
        self.set_prefs(lang, fsize)

    def wrap(self, html):
        d = "rtl" if self.lang in ("ar", "ur") else "ltr"
        al = "right" if d == "rtl" else "left"
        return f"<div dir='{d}' align='{al}' style='font-size:{self.fsize}px; line-height:1.6; text-align:{al};'>{html}</div>"

    def set_prefs(self, lang, fsize):
        self.lang, self.fsize = lang, fsize
        self.lst.clear(); today = date.today(); s = STRINGS.get(lang, STRINGS["en"])
        m_names = get_bundle(lang)["calendar"][1]
        for dt_str, title, desc in get_bundle(lang)["days"]:
            d_obj = date.fromisoformat(dt_str)
            fmt_date = f"{d_obj.day} {m_names[d_obj.month - 1]} {d_obj.year}"
            diff = (d_obj - today).days
            tag = s["days_left"].format(d=diff) if diff > 0 else (s["today"] if diff == 0 else s["passed"])
            it = QListWidgetItem(f"{fmt_date} • {title}\n{tag}"); it.setData(Qt.UserRole, desc); self.lst.addItem(it)
        self.lst.setCurrentRow(0); self.view.setHtml(self.wrap(self.lst.item(0).data(Qt.UserRole)))
