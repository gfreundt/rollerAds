import filetype
import os

p = r"C:\pythonCode\rollerAds\player\media"

x = os.listdir(p)

print(x)

for n in x:
    if os.path.isfile(os.path.join(p, n)):
        q, r = filetype.guess(os.path.join(p, n)).mime.split("/")
        print(f"file={n}  family={q} type={r}")
