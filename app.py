# MEHAR MART V49 - PASSWORD RESET + 7 SYSTEMS + VISITS + ORDERS + ADD TO CART
import streamlit as st
import os
import urllib.parse
import pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V49 PASSWORD RESET", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

if 'products' not in st.session_state: st.session_state.products = []
if 'cart' not in st.session_state: st.session_state.cart = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'clients' not in st.session_state: st.session_state.clients = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"
PASS_FILE = "admin_password.txt"

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

# SIDEBAR
st.sidebar.title("ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
if pwd == get_password() and pwd != "":
    st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    
    # VISITS + ORDERS - V42 WALA BOX
    col_v, col_o = st.sidebar.columns(2)
    with col_v: st.metric("👀 Visits", total_visits)
    with col_o: st.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.divider()
    
    # ★★★ PASSWORD RESET OPTION - NEW ★★★
    st.sidebar.markdown("🔑 **Password Reset**")
    with st.sidebar.expander("Change Password"):
        old_p = st.text_input("Purana Password", type="password", key="old")
        new_p = st.text_input("Naya Password", type="password", key="new")
        new_p2 = st.text_input("Naya Dobara", type="password", key="new2")
        if st.button("Password Badlo", use_container_width=True):
            if old_p != get_password():
                st.sidebar.error("Purana galat hai!")
            elif new_p == "":
                st.sidebar.error("Naya likho!")
            elif new_p != new_p2:
                st.sidebar.error("Dono naye same nahi!")
            else:
                save_password(new_p)
                st.sidebar.success(f"Ho gaya! Naya: {new_p}")
                st.balloons()
    
    st.sidebar.divider()
    st.sidebar.markdown("♾️ **LIFETIME SYSTEMS - 7 SYSTEMS**")
    menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"], label_visibility="collapsed")
    st.sidebar.text_input("Store Link", value=STORE_LINK)
    
    # LOGOUT
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.is_admin = False
        st.rerun()
else:
    menu = "6. DARAZ STORE"

# 1. PRODUCT SYSTEM
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - LIVE PROFIT")
    cat = st.selectbox("Category", ["PURE HONEY","SIDR HONEY","BERI HONEY","OTHER"])
    name = st.text_input("Product Name *")
    c1,c2 = st.columns(2)
    with c1: kharid = st.number_input("Kharid Rate *", 0, 100000, 2000)
    with c2: bechna = st.number_input("Bechne Rate *", 0, 100000, 2500)
    discount = st.number_input("Discount %", 0, 90, 15)
    stock = st.number_input("Stock", 0, 10000, 50)
    customer_pay = int(bechna * (1 - discount/100))
    profit = customer_pay - kharid
    st.divider()
    b1,b2,b3,b4 = st.columns(4)
    with b1: st.info(f"Kharid\nRs.{kharid}")
    with b2: st.warning(f"Bechna\nRs.{bechna}")
    with b3: st.success(f"Customer Pay\nRs.{customer_pay}")
    with b4: st.success(f"PROFIT\nRs.{profit}")
    st.divider()
    highlights = st.text_area("Highlights (Khali Hai)", height=100)
    full_desc = st.text_area("Full Description (Khali Hai)", height=120)
    specs = st.text_area("Specifications (Khali Hai)", height=100)
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])
    if st.button("SAVE PRODUCT", use_container_width=True, type="primary"):
        if name:
            img_bytes = img_file.getvalue() if img_file else None
            exp = datetime.now() + timedelta(days=180)
            st.session_state.products.append({
                "name":name,"category":cat,"sell":bechna,"kharid":kharid,"discount":discount,
                "final":customer_pay,"buy":kharid,"stock":stock,"expiry":exp.strftime("%Y-%m-%d"),
                "profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_bytes":img_bytes
            })
            st.success("Save Ho Gaya!")
            st.balloons()

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART OFFICIAL STORE")
    st.code(STORE_LINK)
    st.caption(f"👀 {total_visits} visits | 📦 {len(st.session_state.orders)} orders")
    if len(st.session_state.cart)>0:
        total_bill = sum([i['final'] for i in st.session_state.cart])
        st.error(f"🛒 CART: {len(st.session_state.cart)} items - Rs.{total_bill}")
        for i,item in enumerate(st.session_state.cart):
            ca,cb = st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("Remove", key=f"r{i}"): st.session_state.cart.pop(i); st.rerun()
        cart_txt = "Salam! Order:\n" + "\n".join([f"{x['name']} Rs.{x['final']}" for x in st.session_state.cart]) + f"\nTotal Rs.{total_bill}\n{STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{total_bill}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_txt)}", type="primary", use_container_width=True)
        if st.button("Cart Khali Karo", use_container_width=True): st.session_state.cart=[]; st.rerun()
        st.divider()
    if not st.session_state.products:
        st.warning("No products - 1. PRODUCT SYSTEM me add karo")
    else:
        for idx,p in enumerate(st.session_state.products):
            with st.container(border=True):
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
                st.markdown(f"**{p['name']}** - Rs.{p['final']} ({p['discount']}% OFF)")
                st.caption(p.get('highlights',''))
                if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=f"add{idx}", use_container_width=True, type="primary"):
                    st.session_state.cart.append(p); st.rerun()
                wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']} - {STORE_LINK}")}"
                st.link_button("💬 BUY NOW", wa, use_container_width=True)

# BAKI SYSTEMS
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    for p in st.session_state.products: st.write(f"{p['name']} - Stock {p['stock']}"); st.divider()
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
    st.divider()
    st.subheader("🔑 Password Status")
    st.info(f"Current Password: {get_password()} - Isko change kar sakte ho sidebar se")
    if os.path.exists(ORDER_FILE):
        st.dataframe(pd.read_csv(ORDER_FILE), use_container_width=True)
