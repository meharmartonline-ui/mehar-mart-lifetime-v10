# MEHAR MART V65 - NO DEFAULT PRODUCT - AAPKI MARZI
import streamlit as st, os, urllib.parse, json, random
from datetime import datetime, timedelta
from PIL import Image
import io, base64
import pandas as pd

st.set_page_config(page_title="MEHAR MART V65 NO DEFAULT", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SPICES - MASALAY","OTHER"]

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f)

# ★★★ AB KOI DEFAULT PRODUCT NAHI - KHALI START ★★★
if 'products' not in st.session_state: 
    st.session_state.products = load_json(PRODUCT_FILE, [])
if 'cart' not in st.session_state: st.session_state.cart=[]
if 'categories' not in st.session_state: st.session_state.categories=load_json(CAT_FILE, DEFAULT_CATS)
if 'is_admin' not in st.session_state: st.session_state.is_admin=False

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True

# SIDEBAR
st.sidebar.text_input("🔗 Store Link", value=STORE_LINK)
st.sidebar.title("ADMIN LOGIN")
if not st.session_state.is_admin:
    pwd=st.sidebar.text_input("Password",type="password")
    if pwd==get_password() and pwd!="": st.session_state.is_admin=True; st.rerun()
else:
    st.sidebar.success("✅ ADMIN")
    menu=st.sidebar.radio("System", ["6. DARAZ STORE","1. PRODUCT SYSTEM","2. STOCK","8. SETTINGS"], label_visibility="collapsed")
    if st.sidebar.button("Logout"): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
    # ★★★ DELETE ALL PRODUCTS BUTTON - SIDEBAR ME ★★★
    st.sidebar.divider()
    if st.sidebar.button("🗑️ SAARE PRODUCTS DELETE KARO", use_container_width=True, type="primary"):
        st.session_state.products=[]
        save_json(PRODUCT_FILE, [])
        st.sidebar.success("✅ Saare products delete!")
        st.balloons()
        st.rerun()

if not st.session_state.is_admin: menu="6. DARAZ STORE"

# PRODUCT SYSTEM
if menu=="1. PRODUCT SYSTEM":
    st.header("📦 Product System - V65")
    st.caption("Ab koi auto Beri Honey nahi - aap jo add karoge wahi dikhega!")
    
    name=st.text_input("Product Name *", value="")
    c1,c2=st.columns(2)
    with c1: bechna=st.number_input("Bechne Rate",0,100000,3000)
    with c2: stock=st.number_input("Stock",0,10000,10)
    cat=st.selectbox("Category", st.session_state.categories)
    highlights=st.text_area("Highlights", value="100% Pure")
    img_file=st.file_uploader("Photo", type=["jpg","png","jpeg"])
    
    if st.button("💾 SAVE PRODUCT", use_container_width=True, type="primary"):
        if name=="": st.error("Naam likho!")
        else:
            img_b64=None
            if img_file:
                try:
                    img=Image.open(img_file); img.thumbnail((600,600)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=70); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":cat,"final":bechna,"discount":0,"stock":stock,"profit":500,"kharid":2000,"sell":bechna,"expiry":(datetime.now()+timedelta(days=180)).strftime("%Y-%m-%d"),"highlights":highlights,"full_desc":"MEHAR MART","specs":"500gm","image_b64":img_b64}
            st.session_state.products.append(prod)
            save_json(PRODUCT_FILE, st.session_state.products)
            st.success(f"✅ {name} Save!"); st.balloons()
    
    st.divider()
    st.subheader(f"Saved Products ({len(st.session_state.products)})")
    if len(st.session_state.products)==0:
        st.info("Koi product nahi - Upar se naya add karo!")
    else:
        for idx,p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1,col2=st.columns([3,1])
                with col1: st.write(f"**{idx+1}. {p['name']}** - Rs.{p['final']} Stock {p['stock']}")
                with col2:
                    if st.button("❌ Delete", key=f"del_{idx}"):
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.success("Delete ho gaya!")
                        st.rerun()

# STORE
else:
    st.success("🏪 MEHAR MART STORE - V65 - NO DEFAULT")
    st.text_input("Store Link", value=STORE_LINK, key="top")
    
    if len(st.session_state.cart)>0:
        total=sum([i['final'] for i in st.session_state.cart])
        st.error(f"🛒 CART {len(st.session_state.cart)} = Rs.{total}")
        for i,item in enumerate(st.session_state.cart):
            ca,cb=st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("❌", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
        # WhatsApp Simple - No Link
        simple_txt = f"Asalam O Alaikum\nOrder Karna Hai\n\n"
        for x in st.session_state.cart:
            simple_txt += f"Product: {x['name']}\nPrice: Rs.{x['final']}\nCategory: {x['category']}\n\n"
        simple_txt += f"Total: Rs.{total}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{total}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(simple_txt)}", type="primary", use_container_width=True)
        st.divider()
    
    search=st.text_input("🔍 Search", placeholder="Search")
    prods=st.session_state.products
    if search.strip()!="": prods=[p for p in prods if search.lower() in p['name'].lower()]
    
    if len(prods)==0:
        st.warning("⚠️ Koi product nahi hai - Admin se product add karwao!")
        st.info("Aapne Beri Honey delete kar diya hai - Ab store khali hai - Yehi aap chahte the!")
        if st.session_state.is_admin:
            st.write("Upar PRODUCT SYSTEM me jaake naya product add karo!")
    else:
        st.write(f"**{len(prods)} Products**")
        for idx,p in enumerate(prods):
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: st.markdown("<div style='font-size:70px; text-align:center;'>🍯</div>", unsafe_allow_html=True)
                else: st.markdown("<div style='font-size:70px; text-align:center;'>🍯</div>", unsafe_allow_html=True)
                
                st.subheader(p['name'])
                st.write(f"🏷️ {p['category']} | Rs.{p['final']} | Stock {p.get('stock',0)}")
                if p.get('highlights'): st.info(p['highlights'])
                
                # ADD TO CART - STABLE KEY
                if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=f"add_{idx}", use_container_width=True, type="primary"):
                    st.session_state.cart.append(p)
                    st.toast("✅ Cart me add!"); st.rerun()
                
                # BUY NOW SIMPLE - NO LINK
                simple_single = f"Asalam O Alaikum\nOrder Karna Hai\n\nProduct: {p['name']}\nPrice: Rs.{p['final']}\nCategory: {p['category']}\nStock: {p.get('stock',0)}\n\nTotal: Rs.{p['final']}"
                st.link_button(f"💬 BUY NOW", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(simple_single)}", use_container_width=True)
                st.write(""); st.write("")
    
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
