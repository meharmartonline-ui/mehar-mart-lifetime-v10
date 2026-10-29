# MEHAR MART V55 FINAL - ALL FEATURES - NOTHING MISS - SHOPIFY + DARAZ + DELIVERY + DESC + DELETE
import streamlit as st
import os
import urllib.parse
import pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta
import base64
import json

st.set_page_config(page_title="MEHAR MART V55 FINAL ALL", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"
PASS_FILE = "admin_password.txt"
PRODUCT_FILE = "products.json"
CAT_FILE = "categories.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SARSON OIL","DRY FRUITS","DATES - KHAJOOR","SPICES - MASALAY","HERBAL PRODUCTS","OTHER"]

# ★ 10 DELIVERY OPTIONS - BHAI KA MISS WALA BOX - V52 SE ★
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

# ★ SHOPIFY + DARAZ PAYMENT METHODS ★
PAYMENT_METHODS = ["Cash on Delivery (COD)","JazzCash - 0300-XXXXXXX","Easypaisa - 0300-XXXXXXX","Bank Transfer - MEHAR MART"]

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
if 'sales' not in st.session_state: st.session_state.sales = []
if 'clients' not in st.session_state: st.session_state.clients = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'delivery_city' not in st.session_state: st.session_state.delivery_city = "Karachi - Rs.150 (Same Day)"
if 'payment_method' not in st.session_state: st.session_state.payment_method = "Cash on Delivery (COD)"

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

query_params = st.query_params
if query_params.get("admin") == get_password():
    st.session_state.is_admin = True

st.sidebar.title("ADMIN LOGIN")
if not st.session_state.is_admin:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == get_password() and pwd != "": st.session_state.is_admin=True; st.rerun()
else: pwd = get_password()

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    col_v,col_o = st.sidebar.columns(2)
    with col_v: st.metric("👀 Visits", total_visits)
    with col_o: st.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.metric("📦 Products", len(st.session_state.products))
    st.sidebar.divider()
    st.sidebar.markdown("🔑 Password Reset")
    with st.sidebar.expander("Change Password"):
        old_p = st.text_input("Purana", type="password", key="old")
        new_p = st.text_input("Naya", type="password", key="new")
        new_p2 = st.text_input("Dobara", type="password", key="new2")
        if st.button("Badlo", use_container_width=True):
            if old_p != get_password(): st.sidebar.error("Galat!")
            elif new_p != new_p2: st.sidebar.error("Match nahi!")
            elif new_p=="": st.sidebar.error("Likho!")
            else: save_password(new_p); st.sidebar.success(f"New: {new_p}")
    st.sidebar.divider()
    st.sidebar.code(f"{STORE_LINK}?admin={get_password()}")
    st.sidebar.divider()
    st.sidebar.markdown("♾️ **7 LIFETIME SYSTEMS + SHOPIFY**")
    menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"], label_visibility="collapsed")
    st.sidebar.text_input("Store Link", value=STORE_LINK)
    if st.sidebar.button("Logout", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else: menu = "6. DARAZ STORE"

# =================================================================
# 1. PRODUCT SYSTEM - ALL FEATURES - NOTHING MISS
# =================================================================
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V55 FINAL ALL FEATURES")
    
    # CATEGORY SYSTEM - MULTIPLE
    c1,c2,c3 = st.columns([2,1,1])
    with c1: category = st.selectbox("Category * (Multiple System)", st.session_state.categories)
    with c2: new_cat = st.text_input("Nayi Category", placeholder="DESI GHEE")
    with c3:
        st.write(""); st.write("")
        if st.button("➕ Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper())
                save_json(CAT_FILE, st.session_state.categories)
                st.success(f"{new_cat.upper()} Add!")
                st.rerun()
    st.caption(f"Available Categories: {', '.join(st.session_state.categories)}")
    st.divider()
    
    # DELIVERY BOX SHOW - ADMIN
    st.subheader("🚚 Delivery Settings (10 Cities) - Customer ko dikhega")
    cols = st.columns(2)
    for i, (city, charge) in enumerate(DELIVERY_OPTIONS.items()):
        cols[i%2].write(f"• {city}")
    st.divider()
    
    # PRODUCT FIELDS - KHARID / BECHNA / DISCOUNT / STOCK / PROFIT
    name = st.text_input("Product Name *", value="Pure Beri Flowers Honey 500gm - 100% Pure")
    col_a,col_b = st.columns(2)
    with col_a: kharid = st.number_input("Kharid Rate * (Aapka Cost)", 0, 100000, 2000)
    with col_b: bechna = st.number_input("Bechne Rate * (Original Price)", 0, 100000, 3500)
    col_c,col_d = st.columns(2)
    with col_c: discount = st.number_input("Discount %", 0, 90, 15)
    with col_d: stock = st.number_input("Stock Qty *", 0, 10000, 50)
    customer_pay = int(bechna * (1 - discount/100))
    profit = customer_pay - kharid
    b1,b2,b3,b4 = st.columns(4)
    with b1: st.info(f"Kharid\nRs.{kharid}")
    with b2: st.warning(f"Bechna\nRs.{bechna}")
    with b3: st.success(f"Customer Pay\nRs.{customer_pay}")
    with b4: st.success(f"PROFIT\nRs.{profit}")
    st.divider()
    
    # DESCRIPTION FIELDS - HIGHLIGHTS / FULL DESC / SPECS
    highlights = st.text_area("Highlights * (Checkmark ke sath dikhega)", value="100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested\nFor Health, Energy & Immunity\nDirect From Bees - MEHAR MART", height=120)
    full_desc = st.text_area("Full Description * (Hare box me dikhega)", value="MEHAR MART - Aapki Sehat Ka Sathi\nOrder Now: Cash on Delivery All Pakistan\nPure Beri Flowers Honey 500gm - 100% Pure & Natural\nManda, Khansi, Kamzori ke liye behtareen", height=120)
    specs = st.text_area("Specifications * (Dropdown me dikhega)", value="Weight: 500gm\nType: Beri Flowers Honey\nBest For: Manda, Khansi, Kamzori\nBrand: MEHAR MART\nExpiry: 2 Years\nStock: Fresh", height=120)
    img_file = st.file_uploader("Product Photo * (2.4MB auto compress hoga)", type=["jpg","png","jpeg"])
    
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
                except: img_b64 = None
            exp = datetime.now() + timedelta(days=180)
            new_prod = {"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":customer_pay,"buy":kharid,"stock":stock,"expiry":exp.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64,"rating":5,"reviews":12}
            st.session_state.products.append(new_prod)
            save_json(PRODUCT_FILE, st.session_state.products)
            st.success(f"✅ {name} Save! Category: {category} | Final Rs.{customer_pay}")
            st.balloons()
        else:
            st.error("Name likho!")
    
    # ★ SINGLE DELETE - EK EK KARKE - BHAI KI DEMAND ★
    st.divider()
    if st.session_state.products:
        st.subheader(f"✅ Saved Products ({len(st.session_state.products)}) - Ek Ek Delete")
        st.caption("Har product ke saath alag Delete button - Ek dabao ek delete")
        for idx, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col_img, col_det, col_del = st.columns([1,2,1])
                with col_img:
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: st.write("No Image")
                with col_det:
                    st.markdown(f"**{idx+1}. {p['name']}**")
                    st.caption(f"🏷️ {p['category']} | Rs.{p['final']} | Stock {p['stock']} | Profit Rs.{p.get('profit',0)}")
                    st.caption(f"{p.get('highlights','')[:60]}...")
                with col_del:
                    st.write("")
                    if st.button(f"❌ Delete", key=f"single_del_{idx}", use_container_width=True, type="primary"):
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.toast(f"Deleted")
                        st.rerun()
    else:
        st.info("Koi product nahi - Upar SAVE dabao")

# =================================================================
# 6. DARAZ STORE - SHOPIFY + DARAZ FEATURES + ALL OLD FEATURES
# =================================================================
elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART STORE - DARAZ + SHOPIFY - FINAL V55")
    
    # ★ DARAZ FEATURE 1: SEARCH BAR ★
    search_q = st.text_input("🔍 Search Product (Daraz jaisa)", placeholder="Beri Honey search karo...")
    
    # ★ DARAZ FEATURE 2: CATEGORY FILTER + SORT ★
    col_f1, col_f2, col_f3 = st.columns([2,1,1])
    with col_f1:
        if st.session_state.products:
            filter_cat = st.selectbox("🔍 Category Filter", ["ALL"] + st.session_state.categories)
        else: filter_cat = "ALL"
    with col_f2:
        sort_by = st.selectbox("Sort By", ["Default","Price Low to High","Price High to Low","Discount Zyada"])
    with col_f3:
        st.metric("Products", len(st.session_state.products))
    
    # ★ SHOPIFY FEATURE 1: CART + DELIVERY 10 OPTIONS + PAYMENT + COUPON ★
    if len(st.session_state.cart) > 0:
        st.divider()
        st.subheader("🛒 CART + DELIVERY + PAYMENT (Shopify Checkout jaisa)")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("**🚚 Delivery City (10 Options)**")
            delivery_choice = st.selectbox("📦 Delivery City *", list(DELIVERY_OPTIONS.keys()), index=0, label_visibility="collapsed")
            st.session_state.delivery_city = delivery_choice
            delivery_charge = DELIVERY_OPTIONS[delivery_choice]
        with col_d2:
            st.markdown("**💳 Payment Method (Shopify jaisa)**")
            payment_choice = st.selectbox("Payment", PAYMENT_METHODS, index=0, label_visibility="collapsed")
            st.session_state.payment_method = payment_choice
        
        # COUPON CODE - DARAZ FEATURE
        coupon = st.text_input("🏷️ Coupon Code (Daraz jaisa) - MEHAR10 likho 10% OFF", placeholder="MEHAR10")
        discount_coupon = 0
        if coupon.upper() == "MEHAR10":
            discount_coupon = 10
            st.success("✅ Coupon Applied 10% OFF!")
        
        total_bill = sum([i['final'] for i in st.session_state.cart])
        if discount_coupon > 0:
            total_bill = int(total_bill * (1 - discount_coupon/100))
        
        final_total = total_bill + delivery_charge
        
        st.error(f"🛒 CART {len(st.session_state.cart)} items = Rs.{total_bill} + Delivery Rs.{delivery_charge} = **TOTAL Rs.{final_total}** | Payment: {payment_choice}")
        
        for i,item in enumerate(st.session_state.cart):
            ca,cb,cc = st.columns([3,1,1])
            with ca: st.write(f"{item['name']} ({item['category']}) - Rs.{item['final']}")
            with cb: st.caption(f"Stock {item.get('stock',0)}")
            with cc:
                if st.button("❌ X", key=f"r{i}"): st.session_state.cart.pop(i); st.rerun()
        
        # WHATSAPP MESSAGE WITH ALL DETAILS - SHOPIFY + DARAZ
        cart_txt = f"Salam MEHAR MART! Mera Order:\n"
        for x in st.session_state.cart:
            cart_txt += f"• {x['name']} Rs.{x['final']}\n"
        cart_txt += f"\nSubtotal: Rs.{total_bill}\nDelivery: {delivery_choice} Rs.{delivery_charge}\nPayment: {payment_choice}\n"
        if discount_coupon>0: cart_txt += f"Coupon MEHAR10 -10%\n"
        cart_txt += f"TOTAL: Rs.{final_total}\n{STORE_LINK}\nJazakAllah!"
        
        st.link_button(f"✅ WHATSAPP ORDER Rs.{final_total} - {payment_choice}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_txt)}", type="primary", use_container_width=True)
        
        col_clr1, col_clr2 = st.columns(2)
        with col_clr1:
            if st.button("🗑️ Cart Khali Karo (Ek ek X se bhi)", use_container_width=True): st.session_state.cart=[]; st.rerun()
        with col_clr2:
            if st.button("🛍️ Shopping Continue", use_container_width=True): st.rerun()
        st.divider()
    
    # PRODUCT DISPLAY
    if not st.session_state.products:
        st.warning("No products - 1. PRODUCT SYSTEM me add karo")
    else:
        # FILTER + SEARCH + SORT LOGIC
        products_to_show = st.session_state.products
        
        # Category Filter
        if filter_cat != "ALL":
            products_to_show = [p for p in products_to_show if p['category']==filter_cat]
        
        # Search Filter - DARAZ
        if search_q:
            products_to_show = [p for p in products_to_show if search_q.lower() in p['name'].lower() or search_q.lower() in p.get('highlights','').lower() or search_q.lower() in p.get('full_desc','').lower()]
        
        # Sort - SHOPIFY
        if sort_by == "Price Low to High":
            products_to_show = sorted(products_to_show, key=lambda x: x['final'])
        elif sort_by == "Price High to Low":
            products_to_show = sorted(products_to_show, key=lambda x: x['final'], reverse=True)
        elif sort_by == "Discount Zyada":
            products_to_show = sorted(products_to_show, key=lambda x: x['discount'], reverse=True)
        
        st.success(f"🔍 {len(products_to_show)} Products Found - {filter_cat} - Sort: {sort_by}")
        
        for idx,p in enumerate(products_to_show):
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: pass
                
                # ★ STOCK STATUS - DARAZ FEATURE ★
                stock_status = "✅ In Stock" if p.get('stock',0) > 10 else "⚠️ Low Stock" if p.get('stock',0) > 0 else "❌ Out of Stock"
                
                # ★ RATING - SHOPIFY FEATURE ★
                rating = p.get('rating',5)
                reviews = p.get('reviews',12)
                
                st.markdown(f"### {p['name']}")
                st.markdown(f"🏷️ **{p['category']}** | ~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF) | {stock_status} ({p.get('stock',0)}) | ⭐ {rating}/5 ({reviews} Reviews)")
                
                # ★ DESCRIPTION SHOW - V54 FEATURE - NOT MISS ★
                if p.get('highlights'):
                    st.markdown("**✅ Highlights:**")
                    st.info(p['highlights'])
                
                if p.get('full_desc'):
                    st.markdown("**📝 Description:**")
                    st.success(p['full_desc'])
                
                if p.get('specs'):
                    with st.expander("📋 Specifications - Click to View (Daraz jaisa)"):
                        st.write(p['specs'])
                        st.caption(f"Profit: Rs.{p.get('profit',0)} | Expiry: {p.get('expiry','')}")
                
                st.divider()
                
                # ★ ADD TO CART + BUY NOW - SHOPIFY + DARAZ ★
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=f"add{idx}", use_container_width=True, type="primary"):
                        st.session_state.cart.append(p); st.toast(f"{p['name']} Add Ho Gaya!"); st.rerun()
                with col_btn2:
                    wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']}\nCategory: {p['category']}\n{p.get('highlights','')}\nPayment: {st.session_state.payment_method}\n{STORE_LINK}")}"
                    st.link_button("💬 BUY NOW WHATSAPP", wa, use_container_width=True)

# OTHER SYSTEMS
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - Ek Ek Delete")
    for idx, p in enumerate(st.session_state.products):
        with st.container(border=True):
            col1,col2,col3 = st.columns([3,1,1])
            with col1: 
                status = "✅" if p.get('stock',0)>10 else "⚠️ Low"
                st.write(f"{status} {p['name']} | {p['category']} | Stock {p['stock']} | Profit Rs.{p.get('profit',0)}")
            with col2: st.caption(f"Rs.{p['final']}")
            with col3:
                if st.button("❌ Delete", key=f"stock_del_{idx}"):
                    st.session_state.products.pop(idx)
                    save_json(PRODUCT_FILE, st.session_state.products)
                    st.rerun()
        st.divider()
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)
    else: st.info("No sales yet")
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - PROFIT")
    if st.session_state.products:
        total_profit = sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        st.metric("Total Potential Profit", f"Rs.{total_profit}")
        st.dataframe(pd.DataFrame(st.session_state.products), use_container_width=True)
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    if st.session_state.clients: st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)
    else: st.info("No clients")
elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING + SHOPIFY DASHBOARD")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Visits", total_visits)
    with c2: st.metric("Orders", len(st.session_state.orders))
    with c3: st.metric("Products", len(st.session_state.products))
    with c4: 
        total_val = sum([p['final']*p['stock'] for p in st.session_state.products])
        st.metric("Stock Value", f"Rs.{total_val}")
    st.divider()
    st.subheader("🚚 Delivery Charges (10 Cities) - V52 Feature")
    st.dataframe(pd.DataFrame(list(DELIVERY_OPTIONS.items()), columns=["City","Charge"]), use_container_width=True)
    st.divider()
    st.subheader("💳 Payment Methods (Shopify Feature)")
    st.dataframe(pd.DataFrame(PAYMENT_METHODS, columns=["Payment Method"]), use_container_width=True)
    st.write(f"Categories: {', '.join(st.session_state.categories)}")
