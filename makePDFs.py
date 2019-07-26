import pandas as pd
from PIL import Image
from fpdf import FPDF

froot = "../P1_2018_09_15/"
pmap = pd.read_csv(froot+"Plate1Map.txt",sep="\t")
pmap["fname"] = [fn.split(".jpg")[0] for fn in pmap.ImageName]
pmap["id"] = [fn[0:13] for fn in pmap.fname]
pmap["type"] = [fn[13:] for fn in pmap.fname]
pmap["path"] = [froot+imname.split("_")[0]+"/"+imname for imname in pmap.ImageName]

ids = list(set(pmap.id))
#types = list(set(pmap.type))
types = ["c1","c2","c1-2"]
ids.sort()
types.sort()

pdf = FPDF('L', 'mm', 'A4')
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(255, 255, 255)

for i,ident in enumerate(ids[0:4]):
    print(ident)
    dat = pmap[pmap.id == ident]
    lab = "{} {} {}".format(dat.id.values[0],dat.Drug.values[0],dat.Concentration.values[0])
    ims = [Image.open(dat.path[dat.type == t].values[0]) for t in types]
    w,h = ims[0].size
    pageh = int(round(h*297.0/(3*w)))
    new_im = Image.new('RGB', (w*3,h))
    for j,im in enumerate(ims):
        new_im.paste(im,(j*w,0))
    new_im.save("tmp.png",dpi=(3000.0, 3000.0))
    if i%2==0:
        pdf.add_page()
    pdf.image("tmp.png",0,pageh*(i%2),297,pageh)
    pdf.cell(297, pageh, lab, 1)
pdf.output("Report.pdf","F")
        
    
