# MEHAR MART V51 - PERSISTENT - LOGIN + PRODUCTS SAVE - FINAL FIX
import streamlit as st
import os
import urllib.parse
import pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta
import base64
import json

st.set_page_config(page_title="MEHAR MART V51 PERSISTENT", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"
PASS_FILE = "admin_password.txt"
PRODUCT_FILE = "products.json"
CAT_FILE = "categories.json"

# DEFAULTS
DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SARSON OIL","DRY FRUITS","DATES - KHAJOOR","SPICES - MASALAY","HERBAL PRODUCTS","OTHER"]

# LOAD PERSISTENT DATA
def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Init session from files (ONLY FIRST TIME)
if 'products' not in st.session_state:
    st.session_state.products = load_json(PRODUCT_FILE, [])
if 'categories' not in st.session_state:
    st.session_state.categories = load_json(CAT_FILE, DEFAULT_CATS)
if 'cart' not in st.session_state: st.session_state.cart = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'clients' not in st.session_state: st.session_state.clients = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE, "r") as f: return int(f.read().strip())
        except: return 0
    return 0

def add_visit_once():
    if 'visit_counted' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE, "w") as f: f.write(str(v))
        st.session_state.visit_counted = True
        return v
    return get_visits()

total_visits = add_visit_once()

if os.path.exists(ORDER_FILE):
    if 'orders_loaded' not in st.session_state:
        try:
            st.session_state.orders = pd.read_csv(ORDER_FILE).to_dict('records')
            st.session_state.orders_loaded = True
        except: pass

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return "mehar123"

def save_password(new_pass):
    with open(PASS_FILE, "w") as f: f.write(new_pass)

# ★★★ AUTO LOGIN FIX - BAR BAR LOGIN KA HAL ★★★
# URL me ?admin=mehar123 lagao to login nahi mangega
query_params = st.query_params
if query_params.get("admin") == get_password():
    st.session_state.is_admin = True

# SIDEBAR LOGIN
st.sidebar.title("ADMIN LOGIN")

# Agar already admin hai to password mat mango
if not st.session_state.is_admin:
    pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
    if pwd == get_password() and pwd != "":
        st.session_state.is_admin = True
        st.rerun()
else:
    pwd = get_password()

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    col_v, col_o = st.sidebar.columns(2)
    with col_v: st.metric("👀 Visits", total_visits)
    with col_o: st.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.divider()
    
    st.sidebar.markdown("🔑 Password Reset")
    with st.sidebar.expander("Change Password"):
        old_p = st.text_input("Purana", type="password", key="old")
        new_p = st.text_input("Naya", type="password", key="new")
        new_p2 = st.text_input("Naya Dobara", type="password", key="new2")
        if st.button("Badlo", use_container_width=True):
            if old_p != get_password(): st.sidebar.error("Purana galat!")
            elif new_p != new_p2: st.sidebar.error("Match nahi!")
            elif new_p=="": st.sidebar.error("Likho!")
            else: save_password(new_p); st.sidebar.success(f"New: {new_p} - Ab is se login karo")
    
    st.sidebar.divider()
    # ★★★ AUTO LOGIN LINK ★★★
    st.sidebar.markdown("🔗 **Bar Bar Login Se Bachne Ke Liye**")
    auto_link = f"{STORE_LINK}?admin={get_password()}"
    st.sidebar.code(auto_link)
    st.sidebar.caption("Is link ko bookmark karo - Direct admin khulega - Password nahi mangega!")
    
    st.sidebar.divider()
    st.sidebar.markdown("♾️ **7 LIFETIME SYSTEMS**")
    menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"], label_visibility="collapsed")
    st.sidebar.text_input("Store Link", value=STORE_LINK)
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.is_admin = False
        st.query_params.clear()
        st.rerun()
else:
    menu = "6. DARAZ STORE"

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - PERSISTENT")
    st.info("Ab product save hoga - Reboot pe bhi nahi jayega!")
    
    c1,c2,c3 = st.columns([2,1,1])
    with c1:
        category = st.selectbox("Category * (Multiple)", st.session_state.categories)
    with c2:
        new_cat = st.text_input("Nayi Category", placeholder="DESI GHEE")
    with c3:
        st.write(""); st.write("")
        if st.button("➕ Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper())
                save_json(CAT_FILE, st.session_state.categories)
                st.success(f"{new_cat.upper()} Save!")
                st.rerun()
    
    st.caption(f"Available: {', '.join(st.session_state.categories)}")
    st.divider()
    
    name = st.text_input("Product Name *")
    col_a,col_b = st.columns(2)
    with col_a: kharid = st.number_input("Kharid Rate *", 0, 100000, 2000)
    with col_b: bechna = st.number_input("Bechne Rate *", 0, 100000, 2500)
    discount = st.number_input("Discount %", 0, 90, 15)
    stock = st.number_input("Stock", 0, 10000, 50)
    
    customer_pay = int(bechna * (1 - discount/100))
    profit = customer_pay - kharid
    
    b1,b2,b3,b4 = st.columns(4)
    with b1: st.info(f"Kharid\nRs.{kharid}")
    with b2: st.warning(f"Bechna\nRs.{bechna}")
    with b3: st.success(f"Pay\nRs.{customer_pay}")
    with b4: st.success(f"PROFIT\nRs.{profit}")
    st.divider()
    
    highlights = st.text_area("Highlights", height=80)
    full_desc = st.text_area("Full Description", height=80)
    specs = st.text_area("Specifications", height=80)
    img_file = st.file_uploader("Photo", type=["jpg","png","jpeg"])
    
    if st.button("💾 SAVE PRODUCT - PERSISTENT", use_container_width=True, type="primary"):
        if name:
            # Image ko base64 me save karo taki file me rahe
            img_b64 = None
            if img_file:
                img_b64 = base64.b64encode(img_file.getvalue()).decode()
            exp = datetime.now() + timedelta(days=180)
            new_prod = {
                "name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,
                "final":customer_pay,"buy":kharid,"stock":stock,"expiry":exp.strftime("%Y-%m-%d"),
                "profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64
            }
            st.session_state.products.append(new_prod)
            save_json(PRODUCT_FILE, st.session_state.products)
            st.success(f"{name} Save Ho Gaya! Ab reboot pe bhi rahega!")
            st.balloons()
        else:
            st.error("Name likho!")

elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART STORE - MULTI CATEGORY")
    if st.session_state.products:
        filter_cat = st.selectbox("🔍 Category Filter", ["ALL"] + st.session_state.categories)
    else:
        filter_cat = "ALL"
    
    if len(st.session_state.cart)>0:
        total_bill = sum([i['final'] for i in st.session_state.cart])
        st.error(f"🛒 CART {len(st.session_state.cart)} - Rs.{total_bill}")
        for i,item in enumerate(st.session_state.cart):
            ca,cb = st.columns([3,1])
            with ca: st.write(f"{item['name']} ({item['category']}) - Rs.{item['final']}")
            with cb:
                if st.button("X", key=f"r{i}"): st.session_state.cart.pop(i); st.rerun()
        cart_txt = "Salam! Order:\n" + "\n".join([f"{x['name']} Rs.{x['final']}" for x in st.session_state.cart]) + f"\nTotal Rs.{total_bill}\n{STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{total_bill}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_txt)}", type="primary", use_container_width=True)
        if st.button("Khali Karo", use_container_width=True): st.session_state.cart=[]; st.rerun()
        st.divider()
    
    if not st.session_state.products:
        st.warning("No products - 1. PRODUCT SYSTEM me add karo - Ab save rahega!")
    else:
        products_to_show = st.session_state.products if filter_cat=="ALL" else [p for p in st.session_state.products if p['category']==filter_cat]
        for idx,p in enumerate(products_to_show):
            with st.container(border=True):
                if p.get('image_b64'):
                    try:
                        img_data = base64.b64decode(p['image_b64'])
                        st.image(Image.open(io.BytesIO(img_data)), use_column_width=True)
                    except: pass
                st.markdown(f"**{p['name']}**")
                st.caption(f"🏷️ {p['category']} | Rs.{p['final']} ({p['discount']}% OFF)")
                if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=f"add{idx}", use_container_width=True, type="primary"):
                    st.session_state.cart.append(p); st.rerun()
                wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']} - {STORE_LINK}")}"
                st.link_button("💬 BUY NOW", wa, use_container_width=True)

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if not st.session_state.products: st.warning("No products")
    for p in st.session_state.products:
        col1,col2 = st.columns([4,1])
        with col1: st.write(f"{p['name']} | {p['category']} | Stock {p['stock']} | Profit Rs.{p.get('profit',0)}")
        with col2:
            if st.button("Delete", key=f"del_{p['name']}"):
                st.session_state.products = [x for x in st.session_state.products if x['name']!=p['name']]
                save_json(PRODUCT_FILE, st.session_state.products)
                st.rerun()
        st.divider()
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    if st.session_state.clients: st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)
elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    c1,c2 = st.columns(2)
    with c1: st.metric("Visits", total_visits)
    with c2: st.metric("Orders", len(st.session_state.orders))
    st.write(f"Total Products Saved: {len(st.session_state.products)}")
    st.write(f"Categories: {', '.join(st.session_state.categories)}")
    if os.path.exists(ORDER_FILE): st.dataframe(pd.read_csv(ORDER_FILE), use_container_width=True)
