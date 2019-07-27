import pandas as pd
from PIL import Image
from fpdf import FPDF
import os

froot = "../P1_2018_09_15/"
platename = "Plate1Map.txt"

pmap = pd.read_csv(froot+platename,sep="\t")
pmap["fname"] = [fn.split(".jpg")[0] for fn in pmap.ImageName]
pmap["id"] = [fn[0:13] for fn in pmap.fname]
pmap["type"] = [fn[13:] for fn in pmap.fname]
pmap["path"] = [froot+imname.split("_")[0]+"/"+imname for imname in pmap.ImageName]

ids = list(set(pmap.id))
#types = list(set(pmap.type))
types = ["c1","c2","c1-2"]
ids.sort()

pdf = FPDF('L', 'mm', 'A4')
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(255, 255, 255)

for i,ident in enumerate(ids):
    print(ident)
    dat = pmap[pmap.id == ident]
    lab = "{} {} {}".format(dat.id.values[0],dat.Drug.values[0],dat.Concentration.values[0])
    paths = [dat.path[dat.type == t].values[0] for t in types]
    ims = [Image.open(p) for p in paths]
    w,h = ims[0].size
    pageh = int(round(h*297.0/(3*w)))
    new_im = Image.new('RGB', (w*3,h))
    for j,im in enumerate(ims):
        new_im.paste(im,(j*w,0))
    new_im.save(lab+"tmp.jpg", quality=60, optimize=True, progressive=True)
    if i%2==0:
        pdf.add_page()
        start = 0
    else:
        start = 210 - pageh
    pdf.image(lab+"tmp.jpg",0,start,297,pageh)
    os.remove(lab+"tmp.jpg")
    pdf.set_xy(0,start)
    pdf.write(10,lab)
pdf.output("Report.pdf","F")
        
    
