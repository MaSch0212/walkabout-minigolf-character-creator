# Build data/bundle.js (+ textures) for the web character creator from the game's asset bundles. Needs UnityPy, numpy, Pillow.
# Usage: python tools/build_data.py "<Walkabout Mini Golf install folder>"
import UnityPy, json, base64, os, re, struct, sys, glob, numpy as np
from UnityPy.helpers.MeshHelper import MeshHandler
from PIL import Image
if len(sys.argv)!=2: sys.exit('usage: python tools/build_data.py "<Walkabout Mini Golf install folder>"')
hits=glob.glob(os.path.join(glob.escape(sys.argv[1]),"**","avatarsandputters_assets_all.bundle"),recursive=True)
if not hits: sys.exit("avatarsandputters_assets_all.bundle not found under "+sys.argv[1])
A=os.path.dirname(hits[0])
if not os.path.isfile(os.path.join(A,"common_assets_all.bundle")): sys.exit("common_assets_all.bundle not found in "+A)
print("reading",A)
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(OUT,"data"),exist_ok=True)
env=UnityPy.load(os.path.join(A,"avatarsandputters_assets_all.bundle"))
bypath={o.path_id:o for o in env.objects}
CAT={1:"head",2:"beard",3:"eyebrows",4:"eyelashes",5:"eyes",6:"glasses",7:"hair",8:"hat",9:"outfit",10:"accessories",17:"makeup",18:"mouth"}

def qrot(q,v):
    x,y,z,w=q; u=np.array([x,y,z]); return v+2*np.cross(u,np.cross(u,v)+w*v)
def xf(v,t):  # apply Transform (scale, rot, pos)
    s=t.m_LocalScale; r=t.m_LocalRotation; p=t.m_LocalPosition
    v=np.asarray(v,float)[:,:3]*[s.x,s.y,s.z]; v=qrot((r.x,r.y,r.z,r.w),v); return v+[p.x,p.y,p.z]
def xfn(n,t):
    r=t.m_LocalRotation; return qrot((r.x,r.y,r.z,r.w),np.asarray(n,float)[:,:3])
def rh(v): v=np.array(v,float); v[:,0]*=-1; return v      # left-handed Unity -> right-handed

blob=bytearray(); _cache={}
def put(arr,dtype):
    global blob
    a=np.ascontiguousarray(np.asarray(arr,dtype=dtype)); b=a.tobytes()
    if b in _cache: return _cache[b]
    while len(blob)%4: blob.append(0)
    off=len(blob); blob+=b; _cache[b]=[off,a.size]; return _cache[b]
def mesh_entry(P,N,UV,T):
    T=np.asarray(T,np.int64).reshape(-1,3)[:,::-1]    # flip winding with the mirror
    big=T.max()>=65536
    e={"p":put(P,np.float32),"uv":put(UV,np.float32),"i":put(T.reshape(-1),np.uint32 if big else np.uint16),"i32":bool(big)}
    return e   # normals omitted: the viewer uses flat shading, exports don't need them

# ---------- avatar parts ----------
lib=[o for o in env.objects if o.type.name=="GameObject" and o.peek_name()=="Library"][0].read()
models=[]; parts=[]
for ch in lib.m_Transform.read().m_Children:
    mt=ch.read(); mg=mt.m_GameObject.read()
    minfo={"key":mg.m_Name}
    for c in mg.m_Component:
        if c.component.type.name=="MonoBehaviour":
            tt=c.component.read_typetree()
            if "parts" in tt and "id" in tt: minfo.update(id=tt["id"],tag=tt.get("tagName",""))
            if "infoAssetName" in tt: minfo.update(pack=tt["infoAssetName"],iap=tt["iapKey"])
    if "id" not in minfo: continue
    models.append(minfo)
    for k in mt.m_Children:
        kt=k.read(); kg=kt.m_GameObject.read(); comp=None; info={}
        for c in kg.m_Component:
            if c.component.type.name=="MonoBehaviour":
                tt=c.component.read_typetree()
                if "submesh" in tt: comp=tt
                elif "infoAssetName" in tt: info=tt
        if not comp: continue
        m=bypath[comp["filter"]["m_PathID"]].read().m_Mesh.read(); h=MeshHandler(m); h.process()
        V=[(v["x"],v["y"],v["z"]) for v in comp["basis"]["vertices"]] or list(h.m_Vertices)
        N=[(v["x"],v["y"],v["z"]) for v in comp["basis"]["normals"]] or (list(h.m_Normals) if h.m_Normals else None)
        UV=[(u["x"],u["y"]) for u in comp["submesh"]["uvs"]] or [tuple(u[:2]) for u in h.m_UV0]
        T=comp["submesh"]["triangles"] or list(h.m_IndexBuffer)
        e=mesh_entry(rh(xf(V,kt)), rh(xfn(N,kt)) if N else None, UV, T)
        shapes={}
        for s in comp["shapes"]:
            sv=[(v["x"],v["y"],v["z"]) for v in s["vertices"]]
            if len(sv)==len(V): shapes[s["name"]]=put(rh(xf(sv,kt)),np.float32)
        parts.append(dict(model=mg.m_Name,name=kg.m_Name,cat=CAT.get(comp["type"],"other"),type=comp["type"],id=comp["id"],
            color=comp["color"],colors=comp["colors"],blend=comp["blend"],pack=info.get("infoAssetName",""),mesh=e,shapes=shapes))
print(len(models),"models",len(parts),"parts")

# ---------- presets ----------
presets=[]
for path,o in env.container.items():
    if "/Presets/" in path:
        tt=o.read_typetree(); presets.append({"id":tt["id"],"label":tt.get("label",""),"options":[[x["t"],x["i"],x["v"]] for x in tt["options"]]})
presets.sort(key=lambda p:p["id"])

# ---------- putters ----------
def collect_children(rootname):
    g=[o for o in env.objects if o.type.name=="GameObject" and o.peek_name()==rootname][0].read()
    out={}
    for ch in g.m_Transform.read().m_Children:
        t=ch.read(); cg=t.m_GameObject.read()
        for c in cg.m_Component:
            if c.component.type.name=="MeshFilter":
                m=c.component.read().m_Mesh.read(); h=MeshHandler(m); h.process()
                if not h.m_Vertices or not h.m_UV0: print("skip empty",cg.m_Name); continue
                uv=h.m_UV1 if (rootname=="Balls" and h.m_UV1) else h.m_UV0      # balls: UV1 selects the ball's cell in BallsTexture
                uv0=[tuple(u[:2]) for u in h.m_UV0]                           # balls: UV0 is the sphere unwrap used by the dimple normal map
                out[cg.m_Name]=(t,list(h.m_Vertices),list(h.m_Normals) if h.m_Normals else None,[tuple(u[:2]) for u in uv],list(h.m_IndexBuffer),uv0)
    return out
pc=collect_children("Putters")
# normalise: whole putter (club_0 + shaft_0 + hand_0) -> 0.9 m tall, club sole at y=0
ref=np.vstack([xf(pc[n][1],pc[n][0]) for n in ("club_0","shaft_0","hand_0")])
PS=0.9/(ref[:,1].max()-ref[:,1].min()); PY=ref[:,1].min()
pparts={}
for name,(t,V,N,UV,T,_) in pc.items():
    P=(xf(V,t)-[0,PY,0])*PS
    pparts[name]=mesh_entry(rh(P), rh(xfn(N,t)) if N else None, UV, T)
ids=sorted({re.match(r"(?:club|shaft|hand)_(.+)",n).group(1) for n in pc if re.match(r"(club|shaft|hand)_",n)}, key=lambda s:(len(s),s))
putters=[]
for i in ids:
    pl=[f"club_{i}",f"shaft_{i}",f"hand_{i}"]+([f"handle_{i}"] if f"handle_{i}" in pc else [])
    putters.append({"id":i,"parts":[p for p in pl if p in pc]})
addons=[n for n in pc if "Addon" in n]
print(len(putters),"putters; addons",addons)

# ---------- balls ----------
bc=collect_children("Balls")
balls=[]
for name,(t,V,N,UV,T,UV0) in sorted(bc.items(), key=lambda kv:(not kv[0][4:].isdigit(), int(kv[0][4:]) if kv[0][4:].isdigit() else 0, kv[0])):
    s=t.m_LocalScale; r=t.m_LocalRotation
    P=qrot((r.x,r.y,r.z,r.w),np.array(V,float)[:,:3]*[s.x,s.y,s.z]); P-=P.mean(0)
    d=(P.max(0)-P.min(0)).max(); P*=0.0427/d                 # regulation ball: 42.7 mm
    e=mesh_entry(rh(P), rh(xfn(N,t)) if N else None, UV, T); e["uv0"]=put(UV0,np.float32)
    balls.append({"name":name,"mesh":e})
print(len(balls),"balls")

# ---------- textures ----------
atlas=[o for o in env.objects if o.type.name=="Texture2D" and o.peek_name()=="avatar_texture_4096_brian_putters"][0].read().image.convert("RGB")
atlas.save(os.path.join(OUT,"data","avatar_atlas.png"))
env2=UnityPy.load(os.path.join(A,"common_assets_all.bundle"))
bt=[o for o in env2.objects if o.type.name=="Texture2D" and o.peek_name()=="BallsTexture"][0].read().image.convert("RGB")
bt.save(os.path.join(OUT,"data","balls_texture.png"))

# ---------- material maps ----------
# Avatar parts + putters use Avatar_Putter_Combined (Amplify "Putter" shader, _USEMETALLICALPHA_ON):
#   metallic = metal map R * _Metalness(1), smoothness = metal map A * _Smoothness(1), emission = emission map RGB.
# Balls use Ball_Material (Shader Graph): same metal/smoothness packing, emission map, dimple normal map on UV0.
# three.js reads metalness from B and roughness from G, so the metal maps are repacked (R unused = 255).
def tex(e, name): return [o for o in e.objects if o.type.name=="Texture2D" and o.peek_name()==name][0].read().image
def save_mr(img, fn):
    a=np.asarray(img.convert("RGBA")).astype(np.uint8)
    out=np.stack([np.full(a.shape[:2],255,np.uint8), 255-a[...,3], a[...,0]],-1)
    Image.fromarray(out,"RGB").save(os.path.join(OUT,"data",fn), optimize=True)
save_mr(tex(env,"avatar_texture_4096_brian_putters_metal"),"avatar_mr.png")
tex(env,"avatar_texture_4096_brian_putters_emissive").convert("RGB").save(os.path.join(OUT,"data","avatar_emissive.png"))
save_mr(tex(env2,"BallsTexture_Metalness"),"balls_mr.png")
tex(env2,"BallsTexture_Emission").convert("RGB").save(os.path.join(OUT,"data","balls_emissive.png"), optimize=True)
n=np.asarray(tex(env2,"BallNormalMap_Temp").convert("RGBA")).astype(np.float32)/255*2-1   # DXT5nm: X in A, Y in G
nx,ny=n[...,3],n[...,1]; nz=np.sqrt(np.clip(1-nx*nx-ny*ny,0,1))
Image.fromarray(((np.stack([nx,ny,nz],-1)+1)/2*255).round().astype(np.uint8),"RGB").save(os.path.join(OUT,"data","ball_normal.png"))
materials={"avatar":{"metalness":1.0,"smoothness":1.0,"emissiveIntensity":1.0},
           "ball":{"emissiveIntensity":1.5,"normalScale":2.0}}

meta={"models":models,"parts":parts,"presets":presets,"putters":putters,"putterParts":pparts,"addons":addons,"balls":balls,"atlasSize":4096,"variantStep":16,"materials":materials}
json.dump(meta,open(os.path.join(OUT,"data","meta.json"),"w"))
open(os.path.join(OUT,"data","geometry.bin"),"wb").write(blob)
# file:// friendly copies (browsers block fetch() from file://): everything as JS globals
def b64file(p): return base64.b64encode(open(p,"rb").read()).decode()
with open(os.path.join(OUT,"data","bundle.js"),"w") as f:
    f.write("window.WMG_META="+json.dumps(meta)+";\n")
    f.write("window.WMG_GEOMETRY_B64='"+base64.b64encode(bytes(blob)).decode()+"';\n")
    f.write("window.WMG_ATLAS='data:image/png;base64,"+b64file(os.path.join(OUT,"data","avatar_atlas.png"))+"';\n")
    f.write("window.WMG_BALLTEX='data:image/png;base64,"+b64file(os.path.join(OUT,"data","balls_texture.png"))+"';\n")
    for var,fn in [("WMG_ATLAS_MR","avatar_mr.png"),("WMG_ATLAS_EMISSIVE","avatar_emissive.png"),("WMG_BALL_MR","balls_mr.png"),
                   ("WMG_BALL_EMISSIVE","balls_emissive.png"),("WMG_BALL_NORMAL","ball_normal.png")]:
        f.write(f"window.{var}='data:image/png;base64,"+b64file(os.path.join(OUT,"data",fn))+"';\n")
print("geometry bytes",len(blob), "bundle.js MB", os.path.getsize(os.path.join(OUT,"data","bundle.js"))/1e6)
