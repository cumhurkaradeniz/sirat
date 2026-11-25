import os, json, math, urllib.request, urllib.parse
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Sirat/1.0"}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode())

def detect_location():
    try:
        d = fetch_json("http://ip-api.com")
        if d.get("status") == "success":
            return d.get("city", "Sungurlu"), d.get("country", "Turkey")
    except Exception:
        pass
    return "Sungurlu", "Turkey"

def get_coords(city, country):
    try:
        q = urllib.parse.urlencode({"q": f"{city}, {country}", "format": "json", "limit": 1})
        res = fetch_json("https://openstreetmap.org?" + q)
        first = next(iter(res), None)
        if first: return float(first["lat"]), float(first["lon"])
    except Exception:
        pass
    return 40.1675, 34.3739
def fmt_time(hours):
    hours = (hours + 24) % 24
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60: h = (h + 1) % 24; m = 0
    return f"{h:02d}:{m:02d}"

def get_today_times(city, country):
    lat, lon = get_coords(city, country)
    now = datetime.now()
    tz = round((datetime.now() - datetime.utcnow()).total_seconds() / 3600)
    jd = now.toordinal() + 1721424.5 - lon / 360.0
    d = jd - 2451545.0
    g = math.radians((357.529 + 0.98560028 * d) % 360)
    q = (280.459 + 0.98564736 * d) % 360
    L = math.radians((q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360)
    e = math.radians(23.439 - 0.00000036 * d)
    ra = math.degrees(math.atan2(math.cos(e) * math.sin(L), math.cos(L))) / 15.0
    eqt = q / 15.0 - ((ra + 24) % 24)
    if eqt > 12: eqt -= 24
    if eqt < -12: eqt += 24
    decl = math.asin(math.sin(e) * math.sin(L))
    noon = 12 + tz - lon / 15.0 - eqt

    def sun_angle(ang):
        cos_h = (-math.sin(math.radians(ang)) - math.sin(math.radians(lat)) * math.sin(decl)) / (math.cos(math.radians(lat)) * math.cos(decl))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos_h)))) / 15.0

    asr_alt = math.degrees(math.atan(1.0 / (1.0 + math.tan(abs(math.radians(lat) - decl)))))
    return {
        "İmsak": fmt_time(noon - sun_angle(18.0)),
        "Güneş": fmt_time(noon - sun_angle(0.833) - 0.08),
        "Öğle": fmt_time(noon + 0.08),
        "İkindi": fmt_time(noon + sun_angle(-asr_alt) + 0.05),
        "Akşam": fmt_time(noon + sun_angle(0.833) + 0.12),
        "Yatsı": fmt_time(noon + sun_angle(17.0) + 0.03)
    }
