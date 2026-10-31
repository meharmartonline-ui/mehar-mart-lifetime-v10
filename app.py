# MEHAR MART V74 - 100% CLEAN - NO EXTRA TEXT FOR CLIENT OR ADMIN
import streamlit as st, os, urllib.parse, json
from datetime import datetime, timedelta
from PIL import Image
import io, base64
import pandas as pd

st.set_page_config(page_title="Mehar Mart", layout="wide", initial_sidebar_state="expanded")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"

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
if 'categories' not in st.session_state: st.session_state.categories=load_json(CAT_FILE, ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","DRY FRUITS","DATES","SPICES","OTHER"])
if 'is_admin' not in st.session_state: st.session_state.is_admin=False
if 'admin_menu' not in st.session_state: st.session_state.admin_menu="PRODUCT SYSTEM"
if 'logo_b64' not in st.session_state: st.session_state.logo_b64=load_json(LOGO_FILE, None)

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"
def save_password(p):
    with open(PASS_FILE,"w") as f: f.write(p)

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True

if not st.session_state.is_admin:
    st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

if st.session_state.is_admin:
    menu = st.selectbox("", ["PRODUCT SYSTEM","STOCK","SALES","MONEY","CLIENTS","STORE VIEW","TRACKING","SETTINGS"], index=["PRODUCT SYSTEM","STOCK","SALES","MONEY","CLIENTS","STORE VIEW","TRACKING","SETTINGS"].index(st.session_state.admin_menu) if st.session_state.admin_menu in ["PRODUCT SYSTEM","STOCK","SALES","MONEY","CLIENTS","STORE VIEW","TRACKING","SETTINGS"] else 0)
    st.session_state.admin_menu=menu
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("STORE", use_container_width=True): st.session_state.admin_menu="STORE VIEW"; st.rerun()
    with c2:
        if st.button("ADD PRODUCT", use_container_width=True, type="primary"): st.session_state.admin_menu="PRODUCT SYSTEM"; st.rerun()
    with c3:
        if st.button("LOGOUT", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
    st.divider()
    with st.sidebar:
        st.title("ADMIN")
        sb = st.radio("", ["PRODUCT SYSTEM","STOCK","SALES","MONEY","CLIENTS","STORE VIEW","TRACKING","SETTINGS"], index=["PRODUCT SYSTEM","STOCK","SALES","MONEY","CLIENTS","STORE VIEW","TRACKING","SETTINGS"].index(menu))
        if sb!=menu: st.session_state.admin_menu=sb; st.rerun()
        if st.button("Logout"): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else:
    menu="STORE VIEW"

if menu=="PRODUCT SYSTEM":
    category=st.selectbox("Category", st.session_state.categories)
    new_cat=st.text_input("New Category")
    if st.button("Add Category"):
        if new_cat and new_cat.upper() not in st.session_state.categories:
            st.session_state.categories.append(new_cat.upper()); save_json(CAT_FILE, st.session_state.categories); st.rerun()
    name=st.text_input("Product Name")
    a,b=st.columns(2)
    with a: kharid=st.number_input("Kharid Rate", 0, 100000, 2000)
    with b: bechna=st.number_input("Bechne Rate", 0, 100000, 3500)
    c,d=st.columns(2)
    with c: discount=st.number_input("Discount %", 0, 90, 15)
    with d: stock=st.number_input("Stock", 0, 10000, 10)
    expiry=st.date_input("Expiry", value=datetime.now()+timedelta(days=180))
    pay=int(bechna * (1 - discount/100))
    img_file=st.file_uploader("Photo", type=["jpg","png","jpeg"])
    if st.button("SAVE", type="primary", use_container_width=True):
        if name:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((600,600)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=70); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":pay,"stock":stock,"expiry":expiry.strftime("%Y-%m-%d"),"image_b64":img_b64}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success("Saved")
    st.divider()
    for idx,p in enumerate(st.session_state.products):
        col1,col2=st.columns([4,1])
        with col1: st.write(f"{p['name']} - Rs.{p['final']}")
        with col2:
            if st.button("Delete", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="SETTINGS":
    st.subheader("Logo")
    logo_file=st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])
    if logo_file:
        try: img=Image.open(logo_file); img.thumbnail((200,200)); buf=io.BytesIO(); img.save(buf, format="PNG"); lb64=base64.b64encode(buf.getvalue()).decode(); st.session_state.logo_b64=lb64; save_json(LOGO_FILE, lb64); st.success("Logo Saved"); st.image(Image.open(io.BytesIO(base64.b64decode(lb64))), width=100)
        except: pass
    if st.session_state.logo_b64:
        if st.button("Remove Logo"): st.session_state.logo_b64=None; save_json(LOGO_FILE, None); st.rerun()
    st.divider()
    st.subheader("Password")
    old_p=st.text_input("Old Password", type="password")
    new_p=st.text_input("New Password", type="password")
    new_p2=st.text_input("Confirm New", type="password")
    if st.button("Change Password", type="primary"):
        if old_p!=get_password(): st.error("Wrong old")
        elif new_p!=new_p2: st.error("Not match")
        elif not new_p: st.error("Empty")
        else: save_password(new_p); st.success("Changed")
    st.divider()
    if st.button("DELETE ALL PRODUCTS", type="primary"):
        st.session_state.products=[]; save_json(PRODUCT_FILE, []); st.success("Deleted")

elif menu=="STOCK":
    for idx,p in enumerate(st.session_state.products):
        st.write(f"{p['name']} - Stock {p['stock']}")
        if st.button(f"Add Stock {idx}"): st.session_state.products[idx]['stock']+=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu in ["SALES","MONEY","CLIENTS","TRACKING"]:
    st.write(f"Products: {len(st.session_state.products)}")

else:
    cart_count=len(st.session_state.cart)
    cart_total=sum([p['final'] for p in st.session_state.cart])
    logo_html=""
    if st.session_state.logo_b64:
        try: logo_html=f"<img src='data:image/png;base64,{st.session_state.logo_b64}' style='height:28px; margin-right:8px; background:white; border-radius:4px; padding:2px; vertical-align:middle;'>"
        except: pass
    st.markdown(f"""
    <div style="background:#f85606; padding:10px 15px; margin:-1rem -1rem 0 -1rem; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; color:white; font-size:18px; font-weight:bold;">{logo_html}MEHAR MART</div>
    <div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">{cart_count}</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    search=st.text_input("", placeholder="Search...", label_visibility="collapsed")
    if cart_count>0:
        with st.container(border=True):
            for i,item in enumerate(st.session_state.cart):
                ca,cb=st.columns([3,1])
                with ca: st.write(f"{item['name'][:30]} - Rs.{item['final']}")
                with cb:
                    if st.button("X", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
            txt=f"Asalam O Alaikum\nOrder Karna Hai\n\n"
            for x in st.session_state.cart: txt+=f"Product: {x['name']}\nPrice: Rs.{x['final']}\n\n"
            txt+=f"Total: Rs.{cart_total}"
            st.link_button(f"Checkout Rs.{cart_total}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(txt)}", type="primary", use_container_width=True)
    prods=st.session_state.products
    if search.strip(): prods=[p for p in prods if search.lower() in p['name'].lower()]
    if len(prods)==0:
        st.markdown("<br><br><div style='text-align:center;'><p>Products coming soon</p></div>", unsafe_allow_html=True)
    else:
        c1,c2=st.columns(2)
        for idx,p in enumerate(prods):
            col=c1 if idx%2==0 else c2
            with col:
                with st.container(border=True):
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: st.write("No Image")
                    st.write(f"**{p['name'][:35]}**")
                    st.write(f"Rs.{p['final']}")
                    if st.button("Add to Cart", key=f"add_{idx}", use_container_width=True, type="primary"): st.session_state.cart.append(p); st.rerun()
                    single=f"Asalam O Alaikum\nOrder Karna Hai\n\nProduct: {p['name']}\nPrice: Rs.{p['final']}\nTotal: Rs.{p['final']}"
                    st.link_button("Buy Now", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(single)}", use_container_width=True)
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
