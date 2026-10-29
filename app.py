# MEHAR MART V57 - STOCK & EXPIRY FULL FIX - FINAL - NOTHING MISS
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

st.set_page_config(page_title="MEHAR MART V57 STOCK FIX", layout="wide")

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

PAYMENT_METHODS = ["Cash on Delivery (COD)","JazzCash","Easypaisa","Bank Transfer"]

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
    cart_detail = {"visitor_id": st.session_state.visitor_id,"visitor_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"product": product['name'],"category": product['category'],"price": product['final'],"action": action,"delivery": "Karachi","status": "Added to Cart"}
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

st.sidebar.title("ADMIN LOGIN")
if not st.session_state.is_admin:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == get_password() and pwd != "": st.session_state.is_admin=True; st.rerun()
else: pwd = get_password()

if st.session_state.is_admin:
    st.sidebar.success(f"✅ ADMIN LOGIN - {st.session_state.visitor_id}")
    st.sidebar.button(f"👀 Visits: {total_visits} - Click Details", use_container_width=True, key="v_btn")
    st.sidebar.button(f"🛒 Cart: {len(load_json(CART_LOG_FILE, []))}", use_container_width=True)
    st.sidebar.button(f"📦 Products: {len(st.session_state.products)}", use_container_width=True)
    if st.sidebar.button("🔍 VISITOR DETAILS - Kaun Aya?", use_container_width=True, type="primary"):
        st.session_state.menu_override = "7. ORDERS TRACKING"; st.rerun()
    if st.sidebar.button("🛒 CART TRACKING - Kisne Add Kiya?", use_container_width=True):
        st.session_state.menu_override = "7. ORDERS TRACKING"; st.rerun()
    st.sidebar.divider()
    st.sidebar.code(f"{STORE_LINK}?admin={get_password()}")
    st.sidebar.divider()
    if 'menu_override' in st.session_state:
        menu = st.session_state.menu_override
        del st.session_state.menu_override
    else:
        menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"], label_visibility="collapsed")
    if st.sidebar.button("Logout", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else: menu = "6. DARAZ STORE"

# 1. PRODUCT SYSTEM
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V57")
    c1,c2,c3 = st.columns([2,1,1])
    with c1: category = st.selectbox("Category *", st.session_state.categories)
    with c2: new_cat = st.text_input("Nayi Category")
    with c3:
        st.write(""); st.write("")
        if st.button("➕ Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper())
                save_json(CAT_FILE, st.session_state.categories)
                st.rerun()
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
    highlights = st.text_area("Highlights *", value="100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested", height=100)
    full_desc = st.text_area("Full Description *", value="MEHAR MART - Aapki Sehat Ka Sathi\nCash on Delivery All Pakistan", height=100)
    specs = st.text_area("Specifications *", value="Weight: 500gm\nType: Beri Honey\nBrand: MEHAR MART\nExpiry: 2 Years", height=100)
    img_file = st.file_uploader("Photo", type=["jpg","png","jpeg"])
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
            st.success(f"✅ Save! Expiry: {expiry_date}"); st.balloons()
    st.divider()
    if st.session_state.products:
        st.subheader(f"✅ Saved Products ({len(st.session_state.products)}) - Ek Ek Delete")
        for idx, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1,col2,col3 = st.columns([2,1,1])
                with col1: st.markdown(f"**{idx+1}. {p['name']}**"); st.caption(f"🏷️ {p['category']} | Rs.{p['final']} | Stock {p['stock']}")
                with col2: st.caption(f"Expiry: {p.get('expiry','')}")
                with col3:
                    if st.button("❌ Delete", key=f"del_p_{idx}"): 
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()

# ★★★ 2. STOCK & EXPIRY - FULL FIX - BHAI KI DEMAND ★★★
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - FULL FIX - DARAZ + SHOPIFY STYLE")
    
    if not st.session_state.products:
        st.warning("Koi product nahi - 1. PRODUCT SYSTEM me add karo")
    else:
        # SUMMARY CARDS - SHOPIFY STYLE
        total_stock = sum([p.get('stock',0) for p in st.session_state.products])
        low_stock = len([p for p in st.session_state.products if p.get('stock',0) <= 10 and p.get('stock',0) > 0])
        out_stock = len([p for p in st.session_state.products if p.get('stock',0) == 0])
        
        # Check expiry
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
        
        # FILTERS
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            stock_filter = st.selectbox("🔍 Filter by Stock", ["ALL","In Stock (>10)","Low Stock (1-10)","Out of Stock (0)"])
        with col_f2:
            expiry_filter = st.selectbox("⏰ Filter by Expiry", ["ALL","Good (>30 days)","Expiring Soon (≤30 days)","Expired"])
        
        st.divider()
        
        # PRODUCT LIST WITH FULL EDITABLE CONTROLS
        for idx, p in enumerate(st.session_state.products):
            # Apply filters
            stock_val = p.get('stock',0)
            if stock_filter == "In Stock (>10)" and stock_val <= 10: continue
            if stock_filter == "Low Stock (1-10)" and not (1 <= stock_val <= 10): continue
            if stock_filter == "Out of Stock (0)" and stock_val != 0: continue
            
            try:
                exp_date = datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d")
                days_left = (exp_date - today).days
                if expiry_filter == "Good (>30 days)" and days_left <= 30: continue
                if expiry_filter == "Expiring Soon (≤30 days)" and not (0 <= days_left <= 30): continue
                if expiry_filter == "Expired" and days_left >= 0: continue
            except:
                days_left = 180
                exp_date = today + timedelta(days=180)
            
            # STATUS
            if stock_val == 0:
                stock_status = "❌ OUT OF STOCK"
                stock_color = "error"
            elif stock_val <= 10:
                stock_status = f"⚠️ LOW STOCK - {stock_val} left"
                stock_color = "warning"
            else:
                stock_status = f"✅ IN STOCK - {stock_val}"
                stock_color = "success"
            
            if days_left < 0:
                expiry_status = f"💀 EXPIRED - {abs(days_left)} days ago"
                expiry_color = "error"
            elif days_left <= 30:
                expiry_status = f"⏰ EXPIRING SOON - {days_left} days left"
                expiry_color = "warning"
            else:
                expiry_status = f"✅ GOOD - {days_left} days left"
                expiry_color = "success"
            
            with st.container(border=True):
                col_img, col_info, col_action = st.columns([1,2,2])
                
                with col_img:
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: st.write("No Image")
                    else: st.write("No Image")
                    st.caption(f"🏷️ {p['category']}")
                
                with col_info:
                    st.markdown(f"**{p['name']}**")
                    st.caption(f"Rs.{p['final']} (Was Rs.{p['sell']}) | Profit Rs.{p.get('profit',0)}")
                    
                    # Stock status
                    if stock_color == "error": st.error(stock_status)
                    elif stock_color == "warning": st.warning(stock_status)
                    else: st.success(stock_status)
                    
                    # Expiry status
                    if expiry_color == "error": st.error(expiry_status)
                    elif expiry_color == "warning": st.warning(expiry_status)
                    else: st.success(expiry_status)
                    
                    st.caption(f"📅 Expiry: {p.get('expiry','')} | 💰 Value: Rs.{p['final']*stock_val}")
                
                with col_action:
                    st.markdown("**⚙️ Stock Control:**")
                    col_minus, col_plus = st.columns(2)
                    with col_minus:
                        if st.button("➖ Minus 1", key=f"minus_{idx}", use_container_width=True):
                            if st.session_state.products[idx]['stock'] > 0:
                                st.session_state.products[idx]['stock'] -= 1
                                save_json(PRODUCT_FILE, st.session_state.products)
                                st.rerun()
                    with col_plus:
                        if st.button("➕ Plus 1", key=f"plus_{idx}", use_container_width=True):
                            st.session_state.products[idx]['stock'] += 1
                            save_json(PRODUCT_FILE, st.session_state.products)
                            st.rerun()
                    
                    # Direct stock edit
                    new_stock = st.number_input(f"Set Stock", value=stock_val, min_value=0, max_value=10000, key=f"stock_edit_{idx}")
                    if st.button("💾 Update Stock", key=f"update_stock_{idx}", use_container_width=True):
                        st.session_state.products[idx]['stock'] = new_stock
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.success(f"Stock updated to {new_stock}"); st.rerun()
                    
                    st.divider()
                    st.markdown("**📅 Expiry Edit:**")
                    try:
                        curr_exp = datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d").date()
                    except: curr_exp = (datetime.now()+timedelta(days=180)).date()
                    new_exp = st.date_input("New Expiry", value=curr_exp, key=f"exp_edit_{idx}")
                    if st.button("💾 Update Expiry", key=f"update_exp_{idx}", use_container_width=True):
                        st.session_state.products[idx]['expiry'] = new_exp.strftime("%Y-%m-%d")
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.success(f"Expiry updated"); st.rerun()
                    
                    st.divider()
                    if st.button(f"❌ Delete Product", key=f"del_stock_{idx}", use_container_width=True, type="primary"):
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.toast("Deleted"); st.rerun()
        
        st.divider()
        st.subheader("📊 Stock & Expiry Full Report")
        report_data = []
        for p in st.session_state.products:
            try:
                exp_date = datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d")
                days_left = (exp_date - datetime.now()).days
            except: days_left = 0
            report_data.append({
                "Product": p['name'][:30],
                "Category": p['category'],
                "Stock": p.get('stock',0),
                "Expiry": p.get('expiry',''),
                "Days Left": days_left,
                "Status": "Expired" if days_left<0 else "Expiring Soon" if days_left<=30 else "Good",
                "Value Rs.": p['final']*p.get('stock',0)
            })
        if report_data:
            st.dataframe(pd.DataFrame(report_data), use_container_width=True)

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART STORE - V57")
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
            delivery_choice = st.selectbox("🚚 Delivery City (10)", list(DELIVERY_OPTIONS.keys()), index=0)
            delivery_charge = DELIVERY_OPTIONS[delivery_choice]
        with col_d2:
            payment_choice = st.selectbox("💳 Payment", PAYMENT_METHODS, index=0)
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
                # Stock check
                try:
                    days_left = (datetime.strptime(p.get('expiry','2026-12-31'), "%Y-%m-%d") - datetime.now()).days
                    expiry_msg = f"✅ {days_left} days left" if days_left>30 else f"⚠️ {days_left} days left" if days_left>=0 else "❌ Expired"
                except: expiry_msg = ""
                stock_msg = "✅ In Stock" if p.get('stock',0)>10 else "⚠️ Low Stock" if p.get('stock',0)>0 else "❌ Out"
                st.markdown(f"### {p['name']}")
                st.markdown(f"🏷️ {p['category']} | Rs.{p['final']} ({p['discount']}% OFF) | {stock_msg} ({p.get('stock',0)}) | {expiry_msg}")
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
                            st.session_state.products[idx]['stock'] -= 1
                            save_json(PRODUCT_FILE, st.session_state.products)
                            st.toast("Added + Stock -1"); st.rerun()
                with col_btn2:
                    wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']}\n{STORE_LINK}")}"
                    st.link_button("💬 BUY NOW", wa, use_container_width=True)

# 7. TRACKING
elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING - CLICKABLE")
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

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    cart_logs = load_json(CART_LOG_FILE, [])
    if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.products:
        total_profit = sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        st.metric("Total Profit", f"Rs.{total_profit}")
        st.dataframe(pd.DataFrame(st.session_state.products), use_container_width=True)
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    visit_logs = load_json(VISIT_LOG_FILE, [])
    cart_logs = load_json(CART_LOG_FILE, [])
    if visit_logs: st.subheader("Visitors"); st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
    if cart_logs: st.subheader("Cart Clients"); st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
