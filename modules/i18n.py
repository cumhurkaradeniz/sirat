import os, json, locale

LOCALES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales")

BUNDLES = {}
SUPPORTED_LANGS = []

for fn in sorted(os.listdir(LOCALES_DIR)):
    if fn.endswith(".json"):
        code = fn[:-5]
        data = json.load(open(os.path.join(LOCALES_DIR, fn), encoding="utf-8"))
        BUNDLES[code] = data
        SUPPORTED_LANGS.append((code, data.get("label", code.upper())))

STRINGS = {code: data["ui"] for code, data in BUNDLES.items()}

def get_bundle(lang):
    return BUNDLES.get(lang, BUNDLES.get("en", {}))

def detect_os_lang():
    raw = os.environ.get("LANG", "") or (locale.getdefaultlocale()[0] or "")
    code = raw.split("_")[0].split(".")[0].lower()
    return code if code in BUNDLES else "en"
