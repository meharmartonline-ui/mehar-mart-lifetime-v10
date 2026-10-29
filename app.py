# MEHAR MART V59 FINAL - PASSWORD RESET VISIBLE FIX - 8 SYSTEMS
import streamlit as st
import os
import urllib.parse
import pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta
import base64
import json
import random

st.set_page_config(page_title="MEHAR MART V59 PASS FIX", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

VISIT_FILE = "visits.txt"
PASS_FILE = "admin_password.txt"
PRODUCT_FILE = "products.json"
CAT_FILE = "categories.json"
VISIT_LOG_FILE = "visit_logs.json"
CART_LOG_FILE = "cart_logs.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SARSON OIL","DRY FRUITS","DATES - KHAJOOR","SPICES - MASALAY","HERBAL PRODUCTS","OTHER"]

DELIVERY_OPTIONS = {
    "Karachi - Rs.150 (Same Day)": 150,
    "Lahore - Rs.200 (1-2 Days)": 200,
    "Islamabad - Rs.200 (1-2 Days)": 200,
    "Rawalpindi - Rs.200 (1-2 Days)": 200,
    "Faisalabad - Rs.250 (2-3 Days)": 250,
    "Multan - Rs.250 (2-3 Days)": 250,
    "Peshawar - Rs.300 (2-3 Days)": 300,
    "Quetta - Rs.350 (3-4 Days)": 350,
    "Sialkot - Rs.250 (2 Days)": 250,
    "Gujranwala - Rs.250 (2 Days)": 250
}

PAYMENT_METHODS = ["Cash on Delivery (COD)","JazzCash","Easypaisa","Bank Transfer - MEHAR MART"]

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return default
    return default

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

if 'products' not in st.session_state: st.session_state.products = load_json(PRODUCT_FILE, [])
if 'categories' not in st.session_state: st.session_state.categories = load_json(CAT_FILE, DEFAULT_CATS)
if 'cart' not in st.session_state: st.session_state.cart = []
if 'visit_logs' not in st.session_state: st.session_state.visit_logs = load_json(VISIT_LOG_FILE, [])
if 'cart_logs' not in st.session_state: st.session_state.cart_logs = load_json(CART_LOG_FILE, [])
if 'visitor_id' not in st.session_state: st.session_state.visitor_id = f"VISITOR-{random.randint(1000,9999)}-{datetime.now().strftime('%d%m%H%M')}"

if 'is_admin' not in st.session_state: st.session_state.is_admin = False

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE, "r") as f: return int(f.read().strip())
        except: return 0
    return 0

def log_visit():
    if 'visit_logged' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE, "w") as f: f.write(str(v))
        visit_detail = {"id": st.session_state.visitor_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"date": datetime.now().strftime("%d-%m-%Y"),"page": "STORE","city_guess": "Pakistan","device": "Mobile","status": "Visited"}
        logs = load_json(VISIT_LOG_FILE, [])
        logs.append(visit_detail)
        save_json(VISIT_LOG_FILE, logs)
        st.session_state.visit_logs = logs
        st.session_state.visit_logged = True
        return v
    return get_visits()

def log_cart_action(product, action):
    cart_detail = {"visitor_id": st.session_state.visitor_id,"visitor_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"product": product['name'],"category": product['category'],"price": product['final'],"profit": product.get('profit',0),"action": action,"delivery": st.session_state.delivery_city if 'delivery_city' in st.session_state else "Karachi","payment": st.session_state.payment_method if 'payment_method' in st.session_state else "COD","status": "Added to Cart"}
    logs = load_json(CART_LOG_FILE, [])
    logs.append(cart_detail)
    save_json(CART_LOG_FILE, logs)
    st.session_state.cart_logs = logs

total_visits = log_visit()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return "mehar123"

def save_password(new_pass):
    with open(PASS_FILE, "w") as f: f.write(new_pass)

if st.query_params.get("admin") == get_password():
    st.session_state.is_admin = True

# SIDEBAR - PASSWORD RESET VISIBLE FIX
st.sidebar.title("ADMIN LOGIN")
if not st.session_state.is_admin:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == get_password() and pwd != "": st.session_state.is_admin=True; st.rerun()
else: pwd = get_password()

if st.session_state.is_admin:
    st.sidebar.success(f"✅ ADMIN LOGIN - {st.session_state.visitor_id}")
    
    # ★★★ PASSWORD RESET - AB BILKUL UPAR VISIBLE - BHAI KI DEMAND ★★★
    st.sidebar.divider()
    st.sidebar.markdown("### 🔑 PASSWORD RESET - YAHAN HAI BHAI")
    st.sidebar.caption(f"Current Password: {get_password()}")
    
    with st.sidebar.container(border=True):
        st.sidebar.markdown("**Change Password**")
        old_p = st.sidebar.text_input("Purana Password *", type="password", key="old_pass")
        new_p = st.sidebar.text_input("Naya Password *", type="password", key="new_pass")
        new_p2 = st.sidebar.text_input("Naya Dobara *", type="password", key="new_pass2")
        if st.sidebar.button("🔑 PASSWORD BADLO", use_container_width=True, type="primary"):
            if old_p != get_password(): st.sidebar.error("❌ Purana galat!")
            elif new_p != new_p2: st.sidebar.error("❌ Naye match nahi!")
            elif new_p == "": st.sidebar.error("❌ Naya likho!")
            elif len(new_p) < 4: st.sidebar.error("❌ 4 se zyada likho!")
            else: 
                save_password(new_p)
                st.sidebar.success(f"✅ Password Badal Gaya! Naya: {new_p}")
                st.sidebar.balloons()
    
    st.sidebar.divider()
    st.sidebar.button(f"👀 Visits: {total_visits} - Click Details", use_container_width=True)
    st.sidebar.button(f"🛒 Cart: {len(load_json(CART_LOG_FILE, []))}", use_container_width=True)
    st.sidebar.button(f"📦 Products: {len(st.session_state.products)}", use_container_width=True)
    if st.sidebar.button("🔍 VISITOR DETAILS DEKHO - Kaun Aya?", use_container_width=True, type="primary"):
        st.session_state.menu_override = "7. ORDERS TRACKING"; st.rerun()
    if st.sidebar.button("🛒 CART TRACKING - Kisne Add Kiya?", use_container_width=True):
        st.session_state.menu_override = "7. ORDERS TRACKING"; st.rerun()
    st.sidebar.divider()
    st.sidebar.code(f"{STORE_LINK}?admin={get_password()}")
    st.sidebar.caption("Ye link se direct login hoga")
    st.sidebar.divider()
    st.sidebar.markdown("♾️ **8 LIFETIME SYSTEMS**")
    if 'menu_override' in st.session_state:
        menu = st.session_state.menu_override
        del st.session_state.menu_override
    else:
        menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - PASSWORD RESET"], label_visibility="collapsed")
    if st.sidebar.button("Logout", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else: menu = "6. DARAZ STORE"

# 1. PRODUCT SYSTEM
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V59")
    c1,c2,c3 = st.columns([2,1,1])
    with c1: category = st.selectbox("Category * (Multiple)", st.session_state.categories)
    with c2: new_cat = st.text_input("Nayi Category")
    with c3:
        st.write(""); st.write("")
        if st.button("➕ Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper())
                save_json(CAT_FILE, st.session_state.categories)
                st.rerun()
    st.caption(f"Available: {', '.join(st.session_state.categories)}")
    st.divider()
    name = st.text_input("Product Name *", value="Pure Beri Flowers Honey 500gm - 100% Pure")
    col_a,col_b = st.columns(2)
    with col_a: kharid = st.number_input("Kharid Rate *", 0, 100000, 2000)
    with col_b: bechna = st.number_input("Bechne Rate *", 0, 100000, 3500)
    col_c,col_d = st.columns(2)
    with col_c: discount = st.number_input("Discount %", 0, 90, 15)
    with col_d: stock = st.number_input("Stock Qty *", 0, 10000, 50)
    expiry_date = st.date_input("Expiry Date *", value=datetime.now()+timedelta(days=180))
    customer_pay = int(bechna * (1 - discount/100))
    profit = customer_pay - kharid
    b1,b2,b3,b4 = st.columns(4)
    with b1: st.info(f"Kharid Rs.{kharid}")
    with b2: st.warning(f"Bechna Rs.{bechna}")
    with b3: st.success(f"Pay Rs.{customer_pay}")
    with b4: st.success(f"PROFIT Rs.{profit}")
    highlights = st.text_area("Highlights *", value="100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested\nFor Health, Energy & Immunity", height=120)
    full_desc = st.text_area("Full Description *", value="MEHAR MART - Aapki Sehat Ka Sathi\nCash on Delivery All Pakistan", height=120)
    specs = st.text_area("Specifications *", value="Weight: 500gm\nType: Beri Honey\nBrand: MEHAR MART\nExpiry: 2 Years", height=120)
    img_file = st.file_uploader("Photo *", type=["jpg","png","jpeg"])
    if st.button("💾 SAVE PRODUCT", use_container_width=True, type="primary"):
        if name:
            img_b64 = None
            if img_file:
                try:
                    img = Image.open(img_file)
                    img.thumbnail((600, 600))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=70)
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                except: pass
            new_prod = {"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":customer_pay,"buy":kharid,"stock":stock,"expiry":expiry_date.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64,"rating":5,"reviews":12}
            st.session_state.products.append(new_prod)
            save_json(PRODUCT_FILE, st.session_state.products)
            st.success(f"✅ Save! Profit Rs.{profit}"); st.balloons()
    st.divider()
    if st.session_state.products:
        st.subheader(f"✅ Saved Products ({len(st.session_state.products)}) - Ek Ek Delete")
        for idx, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1,col2,col3 = st.columns([2,1,1])
                with col1: st.markdown(f"**{idx+1}. {p['name']}**"); st.caption(f"🏷️ {p['category']} | Rs.{p['final']} | Stock {p['stock']} | Profit Rs.{p.get('profit',0)}")
                with col2: st.caption(f"Expiry: {p.get('expiry','')}")
                with col3:
                    if st.button("❌ Delete", key=f"del_p_{idx}"): 
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()

# 2. STOCK & EXPIRY
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - FULL FIX")
    if not st.session_state.products:
        st.warning("Koi product nahi")
    else:
        total_stock = sum([p.get('stock',0) for p in st.session_state.products])
        low_stock = len([p for p in st.session_state.products if 0 < p.get('stock',0) <= 10])
        out_stock = len([p for p in st.session_state.products if p.get('stock',0) == 0])
        today = datetime.now()
        expiring_soon = 0
        expired = 0
        for p in st.session_state.products:
            try:
                exp_date = datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d")
                days_left = (exp_date - today).days
                if days_left < 0: expired += 1
                elif days_left <= 30: expiring_soon += 1
            except: pass
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: st.metric("📦 Total Stock", total_stock)
        with c2: st.metric("⚠️ Low Stock", low_stock)
        with c3: st.metric("❌ Out Stock", out_stock)
        with c4: st.metric("⏰ Expiring Soon", expiring_soon)
        with c5: st.metric("💀 Expired", expired)
        st.divider()
        for idx, p in enumerate(st.session_state.products):
            try: days_left = (datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d") - today).days
            except: days_left = 180
            stock_val = p.get('stock',0)
            with st.container(border=True):
                col1,col2,col3 = st.columns([1,2,2])
                with col1:
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: pass
                with col2:
                    st.markdown(f"**{p['name']}**")
                    st.caption(f"Stock {stock_val} | Expiry {p.get('expiry','')} | {days_left} days left")
                    st.caption(f"Rs.{p['final']} | Profit Rs.{p.get('profit',0)}")
                with col3:
                    col_minus, col_plus = st.columns(2)
                    with col_minus:
                        if st.button("➖ Minus", key=f"minus_{idx}"):
                            if st.session_state.products[idx]['stock'] > 0:
                                st.session_state.products[idx]['stock'] -= 1
                                save_json(PRODUCT_FILE, st.session_state.products)
                                st.rerun()
                    with col_plus:
                        if st.button("➕ Plus", key=f"plus_{idx}"):
                            st.session_state.products[idx]['stock'] += 1
                            save_json(PRODUCT_FILE, st.session_state.products)
                            st.rerun()
                    new_stock = st.number_input("Set Stock", value=stock_val, min_value=0, key=f"se_{idx}")
                    if st.button("💾 Update Stock", key=f"us_{idx}"):
                        st.session_state.products[idx]['stock'] = new_stock
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()
                    try: curr_exp = datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d").date()
                    except: curr_exp = (datetime.now()+timedelta(days=180)).date()
                    new_exp = st.date_input("New Expiry", value=curr_exp, key=f"ee_{idx}")
                    if st.button("💾 Update Expiry", key=f"ue_{idx}"):
                        st.session_state.products[idx]['expiry'] = new_exp.strftime("%Y-%m-%d")
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()
                    if st.button("❌ Delete", key=f"del_s_{idx}", type="primary"):
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()

# 3. SALES & ORDERS
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    cart_logs = load_json(CART_LOG_FILE, [])
    if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    else: st.info("No cart data")

# 4. MONEY SYSTEM - FIXED
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - FIXED V59")
    if not st.session_state.products:
        st.warning("No products")
    else:
        cart_logs = load_json(CART_LOG_FILE, [])
        potential_profit = sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        potential_value = sum([p.get('final',0)*p.get('stock',0) for p in st.session_state.products])
        invested = sum([p.get('kharid',0)*p.get('stock',0) for p in st.session_state.products])
        actual_sales = len(cart_logs)
        actual_profit = sum([log.get('profit',0) for log in cart_logs]) if cart_logs else 0
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.metric("💰 Potential Profit", f"Rs.{potential_profit}")
        with c2: st.metric("✅ Actual Profit (Real)", f"Rs.{actual_profit}")
        with c3: st.metric("📦 Stock Value", f"Rs.{potential_value}")
        with c4: st.metric("💸 Invested", f"Rs.{invested}")
        st.divider()
        if actual_sales == 0:
            st.info(f"Abhi tak sale nahi - Actual Rs.0 - Potential Rs.{potential_profit} = Stock bikne pe")
        else:
            st.success(f"{actual_sales} Add to Cart - Actual Profit Rs.{actual_profit}")
        st.divider()
        report = []
        for p in st.session_state.products:
            report.append({"Product": p['name'][:25],"Stock": p.get('stock',0),"Kharid": p.get('kharid',0),"Bechna": p.get('final',0),"Profit/1": p.get('profit',0),"Potential": p.get('profit',0)*p.get('stock',0),"Expiry": p.get('expiry','')})
        st.dataframe(pd.DataFrame(report), use_container_width=True)

# 5. CLIENT SYSTEM
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    visit_logs = load_json(VISIT_LOG_FILE, [])
    cart_logs = load_json(CART_LOG_FILE, [])
    if visit_logs: st.subheader("Visitors"); st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
    if cart_logs: st.subheader("Cart Clients"); st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    if not visit_logs and not cart_logs: st.info("No data")

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART STORE - V59")
    search_q = st.text_input("🔍 Search Product", placeholder="Beri Honey search...")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if st.session_state.products:
            filter_cat = st.selectbox("Category Filter", ["ALL"] + st.session_state.categories)
        else: filter_cat = "ALL"
    with col_f2:
        sort_by = st.selectbox("Sort By", ["Default","Price Low to High","Price High to Low"])
    if len(st.session_state.cart) > 0:
        st.divider()
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            delivery_choice = st.selectbox("🚚 Delivery (10)", list(DELIVERY_OPTIONS.keys()), index=0)
            delivery_charge = DELIVERY_OPTIONS[delivery_choice]
            st.session_state.delivery_city = delivery_choice
        with col_d2:
            payment_choice = st.selectbox("💳 Payment", PAYMENT_METHODS, index=0)
            st.session_state.payment_method = payment_choice
        coupon = st.text_input("🏷️ Coupon MEHAR10", placeholder="MEHAR10")
        discount_coupon = 10 if coupon.upper() == "MEHAR10" else 0
        total_bill = sum([i['final'] for i in st.session_state.cart])
        if discount_coupon>0: total_bill = int(total_bill*0.9)
        final_total = total_bill + delivery_charge
        st.error(f"🛒 CART {len(st.session_state.cart)} = Rs.{total_bill} + Delivery Rs.{delivery_charge} = TOTAL Rs.{final_total}")
        for i,item in enumerate(st.session_state.cart):
            ca,cb = st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("❌ X", key=f"r{i}"): st.session_state.cart.pop(i); st.rerun()
        cart_txt = f"Salam! Order:\n" + "\n".join([f"{x['name']} Rs.{x['final']}" for x in st.session_state.cart]) + f"\nTotal Rs.{final_total}\nID: {st.session_state.visitor_id}\n{STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{final_total}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_txt)}", type="primary", use_container_width=True)
        st.divider()
    if not st.session_state.products:
        st.warning("No products")
    else:
        products_to_show = st.session_state.products
        if filter_cat != "ALL": products_to_show = [p for p in products_to_show if p['category']==filter_cat]
        if search_q: products_to_show = [p for p in products_to_show if search_q.lower() in p['name'].lower()]
        if sort_by == "Price Low to High": products_to_show = sorted(products_to_show, key=lambda x: x['final'])
        elif sort_by == "Price High to Low": products_to_show = sorted(products_to_show, key=lambda x: x['final'], reverse=True)
        st.success(f"{len(products_to_show)} Products")
        for idx,p in enumerate(products_to_show):
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: pass
                try: days_left = (datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d") - datetime.now()).days
                except: days_left = 180
                stock_msg = "✅ In Stock" if p.get('stock',0)>10 else "⚠️ Low Stock" if p.get('stock',0)>0 else "❌ Out"
                st.markdown(f"### {p['name']}")
                st.markdown(f"🏷️ {p['category']} | Rs.{p['final']} ({p['discount']}% OFF) | {stock_msg} ({p.get('stock',0)}) | {days_left} days left")
                if p.get('highlights'): st.info(p['highlights'])
                if p.get('full_desc'): st.success(p['full_desc'])
                if p.get('specs'):
                    with st.expander("📋 Specifications"): st.write(p['specs'])
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if p.get('stock',0) == 0:
                        st.button("❌ OUT OF STOCK", disabled=True, use_container_width=True)
                    else:
                        if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=f"add{idx}", use_container_width=True, type="primary"):
                            st.session_state.cart.append(p)
                            log_cart_action(p, "ADD TO CART")
                            for orig_idx, orig_p in enumerate(st.session_state.products):
                                if orig_p['name'] == p['name']:
                                    if st.session_state.products[orig_idx]['stock'] > 0:
                                        st.session_state.products[orig_idx]['stock'] -= 1
                                        save_json(PRODUCT_FILE, st.session_state.products)
                                    break
                            st.toast("Added!"); st.rerun()
                with col_btn2:
                    wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']}\n{STORE_LINK}")}"
                    st.link_button("💬 BUY NOW", wa, use_container_width=True)

# 7. ORDERS TRACKING
elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    visit_logs = load_json(VISIT_LOG_FILE, [])
    cart_logs = load_json(CART_LOG_FILE, [])
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("👀 Visits", total_visits)
    with c2: st.metric("🛒 Cart Clicks", len(cart_logs))
    with c3: st.metric("📦 Products", len(st.session_state.products))
    tab1, tab2 = st.tabs(["👀 Visits Details","🛒 Cart Tracking"])
    with tab1:
        if visit_logs: st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
        else: st.info("No visits")
    with tab2:
        if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
        else: st.info("No cart clicks")

# 8. SETTINGS - PASSWORD RESET - ★★★ BHAI KI DEMAND - AB CLEAR ★★★
elif menu == "8. SETTINGS - PASSWORD RESET":
    st.header("8. SETTINGS - PASSWORD RESET - V59 FINAL")
    st.divider()
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.subheader("🔑 Current Password Info")
        with st.container(border=True):
            st.info(f"Current Password: **{get_password()}**")
            st.code(f"{STORE_LINK}?admin={get_password()}")
            st.caption("Is link se direct admin login hoga")
    
    with col2:
        st.subheader("🔑 Change Password - Yahan Se Badlo")
        with st.container(border=True):
            st.markdown("**Bhai yahan se password change karo - Bilkul clear**")
            old_p_main = st.text_input("Purana Password *", type="password", key="old_main")
            new_p_main = st.text_input("Naya Password * (Naya jo rakhna hai)", type="password", key="new_main")
            new_p2_main = st.text_input("Naya Password Dobara *", type="password", key="new2_main")
            
            if st.button("🔑 PASSWORD BADLO - CLICK KARO", use_container_width=True, type="primary"):
                if old_p_main != get_password():
                    st.error(f"❌ Purana password galat hai! Current: {get_password()}")
                elif new_p_main != new_p2_main:
                    st.error("❌ Naye password match nahi kar rahe!")
                elif new_p_main == "":
                    st.error("❌ Naya password likho!")
                elif len(new_p_main) < 4:
                    st.error("❌ Password 4 characters se zyada rakho!")
                else:
                    save_password(new_p_main)
                    st.success(f"✅ Password Badal Gaya!")
                    st.success(f"✅ Naya Password: {new_p_main}")
                    st.balloons()
                    st.info(f"Ab se login: {STORE_LINK}?admin={new_p_main}")
    
    st.divider()
    st.subheader("📋 Full System Info")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Visits", total_visits)
        st.metric("Products", len(st.session_state.products))
    with col_b:
        st.metric("Cart Logs", len(load_json(CART_LOG_FILE, [])))
        st.metric("Visit Logs", len(load_json(VISIT_LOG_FILE, [])))
    with col_c:
        st.metric("Categories", len(st.session_state.categories))
        st.metric("Delivery Cities", len(DELIVERY_OPTIONS))
    
    st.divider()
    st.subheader("🗑️ Data Management")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        if st.button("🗑️ Clear Visit Logs", use_container_width=True):
            save_json(VISIT_LOG_FILE, [])
            st.success("Visit logs clear")
    with col_d2:
        if st.button("🗑️ Clear Cart Logs", use_container_width=True):
            save_json(CART_LOG_FILE, [])
            st.success("Cart logs clear")
    with col_d3:
        if st.button("🗑️ Clear All Products", use_container_width=True):
            save_json(PRODUCT_FILE, [])
            st.session_state.products = []
            st.success("All products cleared")
