# MEHAR MART V69 - ULTRA CLEAN - CLIENT KO SIRF PRODUCT
import streamlit as st, os, urllib.parse, json, random
from datetime import datetime, timedelta
from PIL import Image
import io, base64

st.set_page_config(page_title="Mehar Mart", layout="wide")

WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f: return json.load(f)
        except: return default
    return default

def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f)

if 'products' not in st.session_state: st.session_state.products=load_json(PRODUCT_FILE, [])
if 'cart' not in st.session_state: st.session_state.cart=[]
if 'is_admin' not in st.session_state: st.session_state.is_admin=False

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True

st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;}</style>", unsafe_allow_html=True)

if st.session_state.is_admin:
    with st.sidebar:
        st.title("ADMIN")
        menu = st.radio("", ["Store", "Add Product"])
        if st.button("Logout"): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else:
    menu="Store"

if menu=="Add Product" and st.session_state.is_admin:
    st.header("Add Product")
    name=st.text_input("Name")
    price=st.number_input("Price", 100, 100000, 3000)
    stock=st.number_input("Stock", 0, 10000, 10)
    img_file=st.file_uploader("Image", type=["jpg","png","jpeg"])
    if st.button("SAVE", type="primary", use_container_width=True):
        if name:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((800,800)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=80); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"final":price,"stock":stock,"image_b64":img_b64}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success("Saved!")
    for idx,p in enumerate(st.session_state.products):
        if st.button(f"Delete {p['name']}", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()
    st.stop()

# === STORE - ULTRA CLEAN ===
# Header
st.markdown("""
<div style="background:#f85606; padding:12px 15px; margin:-1rem -1rem 0 -1rem; color:white; display:flex; justify-content:space-between;">
<div style="font-size:20px; font-weight:bold;">MEHAR MART</div>
<div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">🛒 """+str(len(st.session_state.cart))+"""</div>
</div>
""", unsafe_allow_html=True)

st.write("")
search=st.text_input("", placeholder="Search...", label_visibility="collapsed")

# Cart
if len(st.session_state.cart)>0:
    total=sum([i['final'] for i in st.session_state.cart])
    with st.container(border=True):
        for i,item in enumerate(st.session_state.cart):
            ca,cb=st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("✕", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
        txt=f"Asalam O Alaikum\nOrder Karna Hai\n\n"
        for x in st.session_state.cart: txt+=f"Product: {x['name']}\nPrice: Rs.{x['final']}\n\n"
        txt+=f"Total: Rs.{total}"
        st.link_button(f"Checkout Rs.{total}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(txt)}", type="primary", use_container_width=True)

prods=st.session_state.products
if search.strip(): prods=[p for p in prods if search.lower() in p['name'].lower()]

if len(prods)>0:
    c1,c2=st.columns(2)
    for idx,p in enumerate(prods):
        col=c1 if idx%2==0 else c2
        with col:
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: st.markdown("<div style='font-size:50px; text-align:center; padding:15px;'>🍯</div>", unsafe_allow_html=True)
                else: st.markdown("<div style='font-size:50px; text-align:center; padding:15px;'>🍯</div>", unsafe_allow_html=True)
                st.write(f"**{p['name']}**")
                st.write(f"Rs.{p['final']}")
                if st.button("Add to Cart", key=f"add_{idx}", use_container_width=True, type="primary"):
                    st.session_state.cart.append(p); st.rerun()
                single=f"Asalam O Alaikum\nOrder Karna Hai\n\nProduct: {p['name']}\nPrice: Rs.{p['final']}\nTotal: Rs.{p['final']}"
                st.link_button("Buy Now", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(single)}", use_container_width=True)

st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
