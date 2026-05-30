#!/usr/bin/env python3
"""
MorForm screenshot caption badges - LIQUID GLASS (LOCKED, fully wired)
Zilla Slab Bold + plum frosted glass + edge refraction + beveled 3D rim + drop shadow.
Output flattened (NO alpha), original dimensions preserved. JPG and WebP.

Self-contained: extracts working.zip from uploads, resolves the font, runs all JOBS.
Run:  python3 morform_glass.py
"""
import os, zipfile, urllib.request
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------- CONFIG ----------------
OUT_FORMATS = ["jpg", "webp"]            # any of "jpg","webp"
OUT_DIR  = "/mnt/user-data/outputs"
UPLOADS  = "/mnt/user-data/uploads"      # where working.zip and the font land
SRC_DIR  = "/home/claude/mf_sources"     # extraction target (writable)
ZIP_NAME = "working.zip"

# naming: {app}-{platform}-{feature}.  app: mf=Supervisor mm=Manager mo=Office
JOBS = [
  # ---- Supervisor / Android (1080x2340) ----
  {"src":"Screenshot_20260523_184412_MorForm.jpg","caption":"Time Tracking","out":"mf-android-time"},
  {"src":"Screenshot_20260523_184422_MorForm.jpg","caption":"Job Sites","out":"mf-android-jobs"},
  {"src":"Screenshot_20260523_184433_MorForm.jpg","caption":"Track Expenses","out":"mf-android-expenses"},
  {"src":"Screenshot_20260523_184448_MorForm.jpg","caption":"OH&S Safety Forms","out":"mf-android-safety"},
  {"src":"Screenshot_20260523_184502_MorForm.jpg","caption":"Timesheets & Reports","out":"mf-android-reports"},
  {"src":"Screenshot_20260523_184546_MorForm.jpg","caption":"Hazard Assessments","out":"mf-android-flha"},
  {"src":"Screenshot_20260523_184605_MorForm.jpg","caption":"Digital Sign-Off","out":"mf-android-signoff"},
  # ---- Manager / Android (1080x2340) ----
  {"src":"Screenshot_20260523_184748_MorForm Manager.jpg","caption":"Build Quotes","out":"mm-android-estimate"},
  {"src":"Screenshot_20260523_185144_MorForm Manager.jpg","caption":"Aggregated Reports","out":"mm-android-reports"},
  {"src":"Screenshot_20260523_185017_MorForm Manager.jpg","caption":"Aggregated Reports","out":"mm-android-reports-2"},  # near-dup of above; pick one
  {"src":"Screenshot_20260523_185100_MorForm Manager.jpg","caption":"Manage Jobs","out":"mm-android-jobs"},
  {"src":"Screenshot_20260523_185110_MorForm Manager.jpg","caption":"Field Report Inbox","out":"mm-android-inbox"},
  {"src":"Screenshot_20260523_185124_MorForm Manager.jpg","caption":"Job Overview","out":"mm-android-overview"},
  {"src":"Screenshot_20260523_185134_MorForm Manager.jpg","caption":"Budget Tracking","out":"mm-android-budget"},
  # ---- Supervisor / iOS (1242x2688) ----
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 18.03.10.png","caption":"Time Tracking","out":"mf-ios-time"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 18.03.26.png","caption":"Job Sites","out":"mf-ios-jobs"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 18.04.57.png","caption":"Track Expenses","out":"mf-ios-expenses"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 18.19.26.png","caption":"OH&S Safety Forms","out":"mf-ios-safety"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 18.21.38.png","caption":"Timesheets & Reports","out":"mf-ios-reports"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.57.37.png","caption":"Province-Aware OH&S","out":"mf-ios-compliance"},
  # ---- Manager / iOS (1242x2688) ----
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 09.26.53.png","caption":"Project Oversight","out":"mm-ios-welcome"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.10.35.png","caption":"Subtrades & Markup","out":"mm-ios-subtrades"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.13.45.png","caption":"CSI Cost Codes","out":"mm-ios-costcodes"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.16.14.png","caption":"Optional Extras","out":"mm-ios-extras"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.20.35.png","caption":"Job Estimates","out":"mm-ios-estimates"},
  {"src":"Simulator Screenshot - iPhone 16 Plus - 2026-05-23 at 17.21.41.png","caption":"Tasks & Notes","out":"mm-ios-tasks"},
  # ---- Office / Windows (1920x1080, landscape -> smaller badge) ----
  {"src":"Office screenshot 1.PNG","caption":"Desktop Estimating","out":"mo-windows-estimate","fsize":58,"pill_y":30},
  {"src":"office screenshot 2.PNG","caption":"Project Dashboard","out":"mo-windows-overview","fsize":58,"pill_y":30},
  {"src":"office screenshot 3.PNG","caption":"Contacts & Vendors","out":"mo-windows-contacts","fsize":58,"pill_y":30},
  {"src":"office screenshot 4.PNG","caption":"Settings & Import","out":"mo-windows-settings","fsize":58,"pill_y":30},
]

# -------- LOCKED LOOK (reference geometry: 1080x2340, font 58) --------
W0, H0, F0 = 1080, 2340, 58
TINT = (88, 30, 78); TINT_A_DEFAULT = 0.52
# ---------------------------------------------------------------------

def ensure_sources():
    if os.path.isdir(SRC_DIR) and any(os.scandir(SRC_DIR)): return
    os.makedirs(SRC_DIR, exist_ok=True)
    zp = os.path.join(UPLOADS, ZIP_NAME)
    if os.path.exists(zp):
        with zipfile.ZipFile(zp) as z: z.extractall(SRC_DIR)
        print("extracted", ZIP_NAME, "->", SRC_DIR)
    else:
        print("NOTE: %s not found; expecting sources already in %s" % (ZIP_NAME, SRC_DIR))

def find_src(name):
    c = os.path.join(SRC_DIR, name)
    if os.path.exists(c): return c
    for root, _, files in os.walk(SRC_DIR):
        if name in files: return os.path.join(root, name)
    return None

def resolve_font():
    for c in ["fonts/ZillaSlab-Bold.ttf", os.path.join(UPLOADS,"ZillaSlab-Bold.ttf"), "ZillaSlab-Bold.ttf"]:
        if os.path.exists(c): return c
    os.makedirs("fonts", exist_ok=True); dst="fonts/ZillaSlab-Bold.ttf"
    urllib.request.urlretrieve("https://github.com/google/fonts/raw/main/ofl/zillaslab/ZillaSlab-Bold.ttf", dst)
    return dst
FONT_PATH = resolve_font()

def tw_of(d,t,f,tr): return sum(d.textlength(c,font=f) for c in t)+tr*(len(t)-1)
def draw_tracked(d,x,yc,t,f,fill,tr):
    for c in t:
        d.text((x,yc),c,font=f,fill=fill,anchor='lm'); x+=d.textlength(c,font=f)+tr

def make(src, caption, out_base, pill_y=None, fsize=None, tint_a=TINT_A_DEFAULT):
    img = Image.open(src).convert('RGB'); W,H = img.size
    if fsize is None: fsize=max(10,round(W*F0/W0))
    if pill_y is None: pill_y=round(H*88/H0)
    font=ImageFont.truetype(FONT_PATH,fsize); s=fsize/F0; track=max(1,round(s*1))
    dmm=ImageDraw.Draw(Image.new('RGB',(10,10)))
    tw=tw_of(dmm,caption,font,track); asc,desc=font.getmetrics()
    pill_w=int(tw)+round(s*150); pill_h=(asc+desc)+round(s*58)
    pill_x=(W-pill_w)//2; rad=pill_h//2
    box=[pill_x,pill_y,pill_x+pill_w,pill_y+pill_h]; cx,cyc=pill_x+pill_w/2,pill_y+pill_h/2
    mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).rounded_rectangle(box,radius=rad,fill=255)
    mnp=np.asarray(mask).astype(np.float32)/255.0
    sh=Image.new('L',(W,H),0)
    ImageDraw.Draw(sh).rounded_rectangle([box[0],box[1]+round(s*8),box[2],box[3]+round(s*8)],radius=rad,fill=120)
    sh=sh.filter(ImageFilter.GaussianBlur(s*20)); img=Image.composite(Image.new('RGB',(W,H),(0,0,0)),img,sh)
    arr=np.asarray(img).astype(np.float32)
    S=cv2.GaussianBlur(mnp,(0,0),pill_h*0.20); gy,gx=np.gradient(S); st=pill_h*1.5
    Xc=np.arange(W)[None,:].repeat(H,0).astype(np.float32); Yc=np.arange(H)[:,None].repeat(W,1).astype(np.float32)
    refr=cv2.remap(arr,Xc-st*gx,Yc-st*gy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    frost=np.clip(cv2.GaussianBlur(refr,(0,0),s*4.5)*1.05+6,0,255)
    glass=frost*(1-tint_a)+np.array(TINT,np.float32)*tint_a
    img=Image.composite(Image.fromarray(glass.astype('uint8')),img,mask)
    sd=np.zeros((H,W),np.float32)
    for yy in range(pill_y,pill_y+pill_h//2): sd[yy,:]=(1-(yy-pill_y)/(pill_h/2))*58
    sheen=Image.composite(Image.fromarray(sd.astype('uint8')),Image.new('L',(W,H),0),mask)
    img=Image.composite(Image.new('RGB',(W,H),(255,255,255)),img,sheen)
    arr2=np.asarray(img).astype(np.float32)
    Sb=cv2.GaussianBlur(mnp,(0,0),max(3.0,pill_h*0.09)); gby,gbx=np.gradient(Sb)
    mag=np.sqrt(gbx**2+gby**2); eps=1e-6; nx,ny=gbx/(mag+eps),gby/(mag+eps)
    light=nx*(-0.45)+ny*(-0.89); rim=mag/(mag.max()+eps)
    hi=np.clip(light,0,1)*rim; lo=np.clip(-light,0,1)*rim
    near=cv2.GaussianBlur(mnp,(0,0),max(2.0,s*3)); hi*=near; lo*=near
    arr2+=(hi*150)[...,None]; arr2-=(lo*95)[...,None]; img=Image.fromarray(np.clip(arr2,0,255).astype('uint8'))
    ov=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle(box,radius=rad,outline=(255,255,255,70),width=max(1,round(s*1)))
    img=Image.alpha_composite(img.convert('RGBA'),ov).convert('RGB')
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); td=ImageDraw.Draw(txt); tx=cx-tw/2
    draw_tracked(td,tx,cyc+round(s*2),caption,font,(0,0,0,120),track)
    txt=txt.filter(ImageFilter.GaussianBlur(s*2.5))
    draw_tracked(ImageDraw.Draw(txt),tx,cyc,caption,font,(255,255,255,255),track)
    img=Image.alpha_composite(img.convert('RGBA'),txt).convert('RGB')
    os.makedirs(OUT_DIR,exist_ok=True); saved=[]
    for fmt in OUT_FORMATS:
        p=os.path.join(OUT_DIR,out_base+"."+fmt)
        img.save(p,"WEBP",quality=90,method=6) if fmt=="webp" else img.save(p,quality=92); saved.append(p)
    return saved

def main():
    ensure_sources()
    ok=miss=0
    for j in JOBS:
        src=find_src(j["src"])
        if not src: print("SKIP missing:",j["src"]); miss+=1; continue
        make(src,j["caption"],j["out"],j.get("pill_y"),j.get("fsize"),j.get("tint_a",TINT_A_DEFAULT))
        print("  ok:",j["out"]); ok+=1
    print("done. %d created, %d missing." % (ok,miss))

if __name__=="__main__": main()
