# MEHAR MART V62 - STORE LINK VISIBLE FIX
import streamlit as st, os, json, random
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V62 LINK FIX", layout="wide")

# ★★★ STORE LINK - AB HAR JAGAH VISIBLE ★★★
STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CART_LOG_FILE = "cart_logs.json"
CAT_FILE = "categories.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SPICES - MASALAY","OTHER"]

DEFAULT_PRODUCT = {
    "name": "Pure Beri Flowers Honey 500gm - 100% Pure",
    "category": "BERI HONEY",
    "final": 2975, "discount": 15, "stock": 50,
    "profit": 975, "kharid": 2000, "sell": 3500,
    "expiry": (datetime.now()+timedelta(days=730)).strftime("%Y-%m-%d"),
    "highlights": "100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested",
    "image_b64": None
}

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f:
                data=json.load(f)
                if file==PRODUCT_FILE and len(data)==0:
                    return [DEFAULT_PRODUCT]
                return data
        except:
            return [DEFAULT_PRODUCT] if file==PRODUCT_FILE else default
    return [DEFAULT_PRODUCT] if file==PRODUCT_FILE else default

def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f)

if 'products' not in st.session_state: st.session_state.products=load_json(PRODUCT_FILE,[DEFAULT_PRODUCT])
if 'cart' not in st.session_state: st.session_state.cart=[]
if 'categories' not in st.session_state: st.session_state.categories=load_json(CAT_FILE, DEFAULT_CATS)

if len(st.session_state.products)==0:
    st.session_state.products=[DEFAULT_PRODUCT]
    save_json(PRODUCT_FILE, st.session_state.products)

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True
if 'is_admin' not in st.session_state: st.session_state.is_admin=False

# === SIDEBAR - STORE LINK VISIBLE ===
st.sidebar.title("MEHAR MART")

# ★★★ STORE LINK - SIDEBAR ME BILKUL UPAR ★★★
st.sidebar.markdown("### 🔗 STORE LINK")
with st.sidebar.container(border=True):
    st.sidebar.code(STORE_LINK, language="text")
    st.sidebar.link_button("🏪 STORE KHOLO", STORE_LINK, use_container_width=True)
    st.sidebar.caption("Ye link customer ko bhejo!")

st.sidebar.divider()

# ADMIN LOGIN
if not st.session_state.is_admin:
    st.sidebar.subheader("ADMIN LOGIN")
    pwd=st.sidebar.text_input("Password",type="password")
    if pwd==get_password() and pwd!="":
        st.session_state.is_admin=True
        st.rerun()
else:
    st.sidebar.success("✅ ADMIN LOGIN")
    st.sidebar.write(f"Pass: {get_password()}")
    with st.sidebar.container(border=True):
        st.sidebar.markdown("**Admin Direct Link**")
        admin_link = f"{STORE_LINK}?admin={get_password()}"
        st.sidebar.code(admin_link)
        st.sidebar.link_button("🔑 Direct Admin Login", admin_link, use_container_width=True)

if st.session_state.is_admin:
    menu=st.sidebar.radio("Menu",["🏪 STORE (Customer View)","📦 PRODUCT","💰 MONEY","🔗 LINKS"])
else:
    menu="🏪 STORE (Customer View)"

# === LINKS PAGE - NAYA TAB ===
if menu=="🔗 LINKS":
    st.header("🔗 STORE LINKS - Sab Links Yahan")
    
    col1,col2=st.columns(2)
    with col1:
        st.subheader("🏪 Customer Store Link")
        with st.container(border=True):
            st.code(STORE_LINK)
            st.link_button("🏪 Store Kholo", STORE_LINK, use_container_width=True, type="primary")
            st.write("Customer ko ye bhejo:")
            st.code(f"Assalam! Mehar Mart se shopping karo:\n{STORE_LINK}")
    
    with col2:
        st.subheader("🔑 Admin Link (Password ke saath)")
        with st.container(border=True):
            admin_link = f"{STORE_LINK}?admin={get_password()}"
            st.code(admin_link)
            st.link_button("🔑 Admin Login", admin_link, use_container_width=True)
            st.caption("Sirf aap ke liye - password ke saath direct login")
    
    st.divider()
    st.subheader("📱 WhatsApp Share")
    wa_share = f"https://wa.me/?text={STORE_LINK}"
    st.link_button("💬 WhatsApp pe Store Share Karo", wa_share, use_container_width=True)
    
    st.divider()
    st.metric("Total Products", len(st.session_state.products))
    st.metric("Store Link", "Active ✅")

# PRODUCT
elif menu=="📦 PRODUCT":
    st.header("📦 Product Add")
    # Link yahan bhi dikhao
    st.info(f"🏪 Store Link: {STORE_LINK}")
    with st.form("add"):
        name=st.text_input("Name", "Beri Honey 500gm")
        price=st.number_input("Price",100,10000,2975)
        stock=st.number_input("Stock",1,1000,50)
        cat=st.selectbox("Category", st.session_state.categories)
        if st.form_submit_button("SAVE LIFETIME", type="primary", use_container_width=True):
            prod={"name":name,"category":cat,"final":price,"discount":15,"stock":stock,"profit":975,"kharid":2000,"sell":3500,"expiry":(datetime.now()+timedelta(days=730)).strftime("%Y-%m-%d"),"highlights":"100% Pure","image_b64":None}
            st.session_state.products.append(prod)
            save_json(PRODUCT_FILE, st.session_state.products)
            st.success("Saved!"); st.balloons()

# MONEY
elif menu=="💰 MONEY":
    st.header("💰 Money")
    st.info(f"Store: {STORE_LINK}")

# STORE
else:
    # ★★★ STORE LINK - STORE PAGE PE BHI BILKUL UPAR ★★★
    st.success(f"🔗 STORE LINK: {STORE_LINK} - Copy karke customer ko bhejo!")
    
    with st.container(border=True):
        c1,c2,c3=st.columns([2,1,1])
        with c1:
            st.code(STORE_LINK, language="text")
        with c2:
            st.link_button("🏪 Store Link Copy", STORE_LINK, use_container_width=True)
        with c3:
            wa = f"https://wa.me/?text=Mehar Mart Store: {STORE_LINK}"
            st.link_button("💬 WhatsApp Share", wa, use_container_width=True)
    
    st.title("MEHAR MART STORE - V62")
    st.caption(f"Official Store: {STORE_LINK}")
    
    if len(st.session_state.cart)>0:
        st.success(f"🛒 CART {len(st.session_state.cart)} = Rs.{sum([p['final'] for p in st.session_state.cart])}")
        for i, c in enumerate(st.session_state.cart):
            col1,col2=st.columns([3,1])
            with col1: st.write(f"{c['name']} - Rs.{c['final']}")
            with col2:
                if st.button("❌", key=f"rem_{i}"):
                    st.session_state.cart.pop(i); st.rerun()
        st.divider()
    
    search=st.text_input("🔍 Search", placeholder="Beri Honey")
    prods=st.session_state.products
    if search.strip()!="":
        prods=[p for p in prods if search.lower() in p['name'].lower()]
    
    st.write(f"**{len(prods)} Products - LIFETIME GUARANTEED**")
    
    for idx, p in enumerate(prods):
        with st.container(border=True):
            st.markdown("<div style='font-size:70px; text-align:center;'>🍯</div>", unsafe_allow_html=True)
            st.subheader(p['name'])
            st.write(f"🏷️ {p['category']} | Rs.{p['final']} | Stock {p['stock']}")
            if p.get('highlights'): st.info(p['highlights'])
            
            # Product ka apna link
            prod_link = f"{STORE_LINK}?product={p['name'].replace(' ','-')}"
            
            btn_key = f"add_cart_{idx}_{random.randint(100,9999)}"
            if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=btn_key, use_container_width=True, type="primary"):
                st.session_state.cart.append(p)
                for orig in st.session_state.products:
                    if orig['name']==p['name'] and orig['stock']>0:
                        orig['stock']-=1
                        break
                save_json(PRODUCT_FILE, st.session_state.products)
                st.toast("✅ Cart me add!"); st.balloons(); st.rerun()
            
            # Share this product
            wa_prod = f"https://wa.me/{WA_NUMBER}?text={p['name']} Rs.{p['final']} - {STORE_LINK}"
            st.link_button(f"💬 Share {p['name'][:15]}", wa_prod, use_container_width=True)
    
    st.divider()
    # FOOTER ME BHI LINK
    st.success(f"🏪 Mehar Mart Official Store: {STORE_LINK}")
    st.caption("Ye link save kar lo - Lifetime chalega!")
