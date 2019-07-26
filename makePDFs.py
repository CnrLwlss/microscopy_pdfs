import pandas as pd
from PIL import Image

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

for ident in ids:
    dat = pmap[pmap.id == ident]
    ims = [Image.open(dat.path[dat.type == t].values[0]) for t in types]
    w,h = ims[0].size
    new_im = Image.new('RGB', (w*3,h))
    
