# MEHAR MART V63 - FULL 8 SYSTEMS + LINK FIX + IMAGE + CART - NOTHING MISSING
import streamlit as st, os, urllib.parse, pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta
import base64, json, random

st.set_page_config(page_title="MEHAR MART V63 FULL RESTORED", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

VISIT_FILE = "visits.txt"
PASS_FILE = "admin_password.txt"
PRODUCT_FILE = "products.json"
CAT_FILE = "categories.json"
VISIT_LOG_FILE = "visit_logs.json"
CART_LOG_FILE = "cart_logs.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SARSON OIL","DRY FRUITS","DATES - KHAJOOR","SPICES - MASALAY","HERBAL PRODUCTS","OTHER"]

# LIFETIME DEFAULT - TAQREEBAN NO PRODUCTS KABHI NAHI
DEFAULT_PRODUCT = {
    "name": "Pure Beri Flowers Honey 500gm - 100% Pure",
    "category": "BERI HONEY",
    "sell": 3500, "kharid": 2000, "discount": 15, "final": 2975, "buy": 2000, "stock": 50,
    "expiry": (datetime.now()+timedelta(days=730)).strftime("%Y-%m-%d"),
    "profit": 975,
    "highlights": "100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested",
    "full_desc": "MEHAR MART - Aapki Sehat Ka Sathi\nCash on Delivery All Pakistan",
    "specs": "Weight: 500gm\nType: Beri Honey\nBrand: MEHAR MART\nExpiry: 2 Years",
    "image_b64": None, "rating": 5, "reviews": 12
}

DELIVERY_OPTIONS = {
    "Karachi - Rs.150 (Same Day)": 150, "Lahore - Rs.200 (1-2 Days)": 200,
    "Islamabad - Rs.200 (1-2 Days)": 200, "Rawalpindi - Rs.200 (1-2 Days)": 200,
    "Faisalabad - Rs.250 (2-3 Days)": 250, "Multan - Rs.250 (2-3 Days)": 250,
    "Peshawar - Rs.300 (2-3 Days)": 300, "Quetta - Rs.350 (3-4 Days)": 350,
}
PAYMENT_METHODS = ["Cash on Delivery (COD)","JazzCash","Easypaisa","Bank Transfer - MEHAR MART"]

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                if file == PRODUCT_FILE and len(data) == 0:
                    return [DEFAULT_PRODUCT]
                return data
        except:
            return [DEFAULT_PRODUCT] if file == PRODUCT_FILE else default
    return [DEFAULT_PRODUCT] if file == PRODUCT_FILE else default

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f)

if 'products' not in st.session_state: st.session_state.products = load_json(PRODUCT_FILE, [DEFAULT_PRODUCT])
if 'categories' not in st.session_state: st.session_state.categories = load_json(CAT_FILE, DEFAULT_CATS)
if 'cart' not in st.session_state: st.session_state.cart = []
if 'visit_logs' not in st.session_state: st.session_state.visit_logs = load_json(VISIT_LOG_FILE, [])
if 'cart_logs' not in st.session_state: st.session_state.cart_logs = load_json(CART_LOG_FILE, [])
if 'visitor_id' not in st.session_state: st.session_state.visitor_id = f"VISITOR-{random.randint(1000,9999)}-{datetime.now().strftime('%d%m%H%M')}"
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

if len(st.session_state.products) == 0:
    st.session_state.products = [DEFAULT_PRODUCT]
    save_json(PRODUCT_FILE, st.session_state.products)

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
        logs = load_json(VISIT_LOG_FILE, [])
        logs.append({"id": st.session_state.visitor_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"date": datetime.now().strftime("%d-%m-%Y"),"page": "STORE"})
        save_json(VISIT_LOG_FILE, logs)
        st.session_state.visit_logs = logs
        st.session_state.visit_logged = True
        return v
    return get_visits()

def log_cart_action(product, action):
    cart_detail = {"visitor_id": st.session_state.visitor_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"product": product['name'],"category": product['category'],"price": product['final'],"profit": product.get('profit',0),"action": action}
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

# === SIDEBAR - FULL FIX - LINK VISIBLE WITH TEXT_INPUT (NOT CODE) ===
st.sidebar.title("MEHAR MART")

st.sidebar.markdown("### 🔗 STORE LINK")
# FIX: st.code ki jagah st.text_input - mobile pe khali nahi hoga
with st.sidebar.container(border=True):
    st.sidebar.text_input("Store Link - Copy Karo", value=STORE_LINK, key="store_link_sidebar")
    st.sidebar.link_button("🏪 STORE KHOLO", STORE_LINK, use_container_width=True)
    st.sidebar.caption("Customer ko ye bhejo!")

st.sidebar.divider()
st.sidebar.title("ADMIN LOGIN")
if not st.session_state.is_admin:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == get_password() and pwd != "": st.session_state.is_admin=True; st.rerun()
else: pwd = get_password()

if st.session_state.is_admin:
    st.sidebar.success(f"✅ ADMIN LOGIN - {st.session_state.visitor_id}")
    st.sidebar.divider()
    st.sidebar.markdown("### 🔑 PASSWORD RESET - YAHAN HAI BHAI")
    st.sidebar.caption(f"Current: {get_password()}")
    with st.sidebar.container(border=True):
        old_p = st.sidebar.text_input("Purana Password *", type="password", key="old_pass")
        new_p = st.sidebar.text_input("Naya Password *", type="password", key="new_pass")
        new_p2 = st.sidebar.text_input("Naya Dobara *", type="password", key="new_pass2")
        if st.sidebar.button("🔑 PASSWORD BADLO", use_container_width=True, type="primary"):
            if old_p != get_password(): st.sidebar.error("❌ Purana galat!")
            elif new_p != new_p2: st.sidebar.error("❌ Match nahi!")
            elif new_p == "": st.sidebar.error("❌ Likho!")
            elif len(new_p) < 4: st.sidebar.error("❌ 4+ chars!")
            else: save_password(new_p); st.sidebar.success(f"✅ Naya: {new_p}"); st.sidebar.balloons()
    
    st.sidebar.divider()
    # Admin Direct Link - FIX with text_input
    st.sidebar.markdown("**Admin Direct Link**")
    admin_link_val = f"{STORE_LINK}?admin={get_password()}"
    st.sidebar.text_input("Admin Link", value=admin_link_val, key="admin_link_sidebar")
    st.sidebar.link_button("🔑 Direct Admin Login", admin_link_val, use_container_width=True)
    
    st.sidebar.divider()
    st.sidebar.button(f"👀 Visits: {total_visits}", use_container_width=True)
    st.sidebar.button(f"🛒 Cart: {len(load_json(CART_LOG_FILE, []))}", use_container_width=True)
    st.sidebar.button(f"📦 Products: {len(st.session_state.products)}", use_container_width=True)
    st.sidebar.divider()
    st.sidebar.markdown("♾️ **8 LIFETIME SYSTEMS**")
    if 'menu_override' in st.session_state:
        menu = st.session_state.menu_override
        del st.session_state.menu_override
    else:
        menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - PASSWORD RESET"], label_visibility="collapsed")
    if st.sidebar.button("Logout", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else: menu = "6. DARAZ STORE"

# 1. PRODUCT SYSTEM - FULL
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V63")
    st.info(f"🏪 Store Link: {STORE_LINK}")
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
    highlights = st.text_area("Highlights *", value="100% Pure - No Sugar, No Mix")
    full_desc = st.text_area("Full Description *", value="MEHAR MART - Aapki Sehat Ka Sathi")
    specs = st.text_area("Specifications *", value="Weight: 500gm")
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
        for idx, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1,col2,col3 = st.columns([2,1,1])
                with col1: st.markdown(f"**{idx+1}. {p['name']}**"); st.caption(f"{p['category']} | Rs.{p['final']} | Stock {p['stock']}")
                with col2: st.caption(f"Expiry: {p.get('expiry','')}")
                with col3:
                    if st.button("❌ Delete", key=f"del_p_{idx}"): 
                        st.session_state.products.pop(idx)
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()

# 2. STOCK & EXPIRY
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if not st.session_state.products:
        st.warning("Koi product nahi")
    else:
        for idx, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1,col2 = st.columns([2,1])
                with col1: st.markdown(f"**{p['name']}**"); st.caption(f"Stock {p.get('stock',0)} | Expiry {p.get('expiry','')}")
                with col2:
                    if st.button("➖ Minus", key=f"minus_{idx}"):
                        if st.session_state.products[idx]['stock'] > 0:
                            st.session_state.products[idx]['stock'] -= 1
                            save_json(PRODUCT_FILE, st.session_state.products)
                            st.rerun()
                    if st.button("➕ Plus", key=f"plus_{idx}"):
                        st.session_state.products[idx]['stock'] += 1
                        save_json(PRODUCT_FILE, st.session_state.products)
                        st.rerun()

# 3. SALES & ORDERS
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    cart_logs = load_json(CART_LOG_FILE, [])
    if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    else: st.info("No cart data")

# 4. MONEY SYSTEM
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - V63")
    if not st.session_state.products: st.warning("No products")
    else:
        cart_logs = load_json(CART_LOG_FILE, [])
        potential_profit = sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        actual_profit = sum([log.get('profit',0) for log in cart_logs]) if cart_logs else 0
        c1,c2 = st.columns(2)
        with c1: st.metric("💰 Potential Profit", f"Rs.{potential_profit}")
        with c2: st.metric("✅ Actual Profit", f"Rs.{actual_profit}")
        report=[]
        for p in st.session_state.products:
            report.append({"Product":p['name'][:25],"Stock":p.get('stock',0),"Profit/1":p.get('profit',0),"Potential":p.get('profit',0)*p.get('stock',0)})
        st.dataframe(pd.DataFrame(report), use_container_width=True)

# 5. CLIENT SYSTEM
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    visit_logs = load_json(VISIT_LOG_FILE, [])
    cart_logs = load_json(CART_LOG_FILE, [])
    if visit_logs: st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
    if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    if not visit_logs and not cart_logs: st.info("No data")

# 6. DARAZ STORE - FULL WITH LINK + IMAGE + CART FIX
elif menu == "6. DARAZ STORE":
    # STORE LINK TOP - FIXED WITH TEXT_INPUT
    st.success("🏪 MEHAR MART STORE - V63 FULL")
    with st.container(border=True):
        st.text_input("🔗 Official Store Link - Copy Karo", value=STORE_LINK, key="store_link_top")
        c1,c2 = st.columns(2)
        with c1: st.link_button("🏪 STORE KHOLO", STORE_LINK, use_container_width=True, type="primary")
        with c2:
            wa_share = f"https://wa.me/?text=Mehar Mart: {STORE_LINK}"
            st.link_button("💬 WhatsApp Share", wa_share, use_container_width=True)
    
    # CART TOP
    if len(st.session_state.cart) > 0:
        total_bill = sum([i['final'] for i in st.session_state.cart])
        st.error(f"🛒 CART {len(st.session_state.cart)} = Rs.{total_bill}")
        for i,item in enumerate(st.session_state.cart):
            ca,cb = st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("❌ X", key=f"r_{i}_{random.randint(1,9999)}"): st.session_state.cart.pop(i); st.rerun()
        cart_txt = f"Salam! Order:\n" + "\n".join([f"{x['name']} Rs.{x['final']}" for x in st.session_state.cart]) + f"\nTotal Rs.{total_bill}\n{STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{total_bill}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_txt)}", type="primary", use_container_width=True)
        st.divider()
    
    search_q = st.text_input("🔍 Search Product", placeholder="Beri Honey search...")
    filter_cat = st.selectbox("Category Filter", ["ALL"] + st.session_state.categories)
    sort_by = st.selectbox("Sort By", ["Default","Price Low to High","Price High to Low"])
    
    products_to_show = st.session_state.products
    if filter_cat != "ALL": products_to_show = [p for p in products_to_show if p['category']==filter_cat]
    if search_q.strip() != "": products_to_show = [p for p in products_to_show if search_q.lower() in p['name'].lower()]
    if sort_by == "Price Low to High": products_to_show = sorted(products_to_show, key=lambda x: x['final'])
    elif sort_by == "Price High to Low": products_to_show = sorted(products_to_show, key=lambda x: x['final'], reverse=True)
    
    st.success(f"{len(products_to_show)} Products - LIFETIME GUARANTEED")
    
    for idx,p in enumerate(products_to_show):
        with st.container(border=True):
            # IMAGE FIX - AGAR IMAGE HAI TO DIKHAO WARNA HONEY EMOJI
            if p.get('image_b64'):
                try:
                    st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                except:
                    st.markdown("<div style='font-size:70px; text-align:center;'>🍯</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='font-size:70px; text-align:center;'>🍯</div>", unsafe_allow_html=True)
            
            st.subheader(p['name'])
            st.write(f"🏷️ {p['category']} | Rs.{p['final']} ({p['discount']}% OFF) | Stock {p.get('stock',0)}")
            if p.get('highlights'): st.info(p['highlights'])
            if p.get('full_desc'): st.success(p['full_desc'])
            
            # CART BUTTON - UNIQUE KEY FIX
            btn_key = f"add_{idx}_{random.randint(1000,9999)}_{p['name'][:3]}"
            if p.get('stock',0) == 0:
                st.button("❌ OUT OF STOCK", disabled=True, use_container_width=True, key=f"out_{btn_key}")
            else:
                if st.button(f"🛒 ADD TO CART - Rs.{p['final']}", key=btn_key, use_container_width=True, type="primary"):
                    st.session_state.cart.append(p)
                    log_cart_action(p, "ADD TO CART")
                    for orig_idx, orig_p in enumerate(st.session_state.products):
                        if orig_p['name'] == p['name'] and st.session_state.products[orig_idx]['stock'] > 0:
                            st.session_state.products[orig_idx]['stock'] -= 1
                            save_json(PRODUCT_FILE, st.session_state.products)
                            break
                    st.toast("✅ Added!"); st.balloons(); st.rerun()
            
            wa = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(f"Salam! {p['name']} Rs.{p['final']}\n{STORE_LINK}")}"
            st.link_button("💬 BUY NOW", wa, use_container_width=True)
    
    st.divider()
    st.text_input("🔗 Mehar Mart Official Store - Lifetime", value=STORE_LINK, key="store_link_footer")
    st.caption("Ye link save kar lo - Lifetime chalega!")

# 7. ORDERS TRACKING
elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    visit_logs = load_json(VISIT_LOG_FILE, [])
    cart_logs = load_json(CART_LOG_FILE, [])
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("👀 Visits", total_visits)
    with c2: st.metric("🛒 Cart Clicks", len(cart_logs))
    with c3: st.metric("📦 Products", len(st.session_state.products))
    tab1, tab2 = st.tabs(["👀 Visits","🛒 Cart"])
    with tab1:
        if visit_logs: st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
        else: st.info("No visits")
    with tab2:
        if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
        else: st.info("No cart clicks")

# 8. SETTINGS - PASSWORD RESET
elif menu == "8. SETTINGS - PASSWORD RESET":
    st.header("8. SETTINGS - PASSWORD RESET - V63 FINAL")
    st.text_input("Store Link", value=STORE_LINK, key="settings_store_link")
    st.text_input("Admin Link", value=f"{STORE_LINK}?admin={get_password()}", key="settings_admin_link")
    col1, col2 = st.columns([1,1])
    with col1:
        with st.container(border=True):
            st.info(f"Current Password: **{get_password()}**")
            st.text_input("Direct Admin Link", value=f"{STORE_LINK}?admin={get_password()}", key="direct_admin")
    with col2:
        with st.container(border=True):
            old_p_main = st.text_input("Purana Password *", type="password", key="old_main")
            new_p_main = st.text_input("Naya Password *", type="password", key="new_main")
            new_p2_main = st.text_input("Dobara *", type="password", key="new2_main")
            if st.button("🔑 PASSWORD BADLO", use_container_width=True, type="primary"):
                if old_p_main != get_password(): st.error("❌ Galat!")
                elif new_p_main != new_p2_main: st.error("❌ Match nahi!")
                elif new_p_main == "": st.error("❌ Likho!")
                else: save_password(new_p_main); st.success(f"✅ Naya: {new_p_main}"); st.balloons()
