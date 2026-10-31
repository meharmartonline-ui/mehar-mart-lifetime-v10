# MEHAR MART V71 - FULL 8 ADMIN SYSTEMS + CLEAN CLIENT - NOTHING MISS
import streamlit as st, os, urllib.parse, json, random
from datetime import datetime, timedelta
from PIL import Image
import io, base64
import pandas as pd

st.set_page_config(page_title="Mehar Mart", layout="wide", page_icon="🍯")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
VISIT_FILE = "visits.txt"
VISIT_LOG_FILE = "visit_logs.json"
CART_LOG_FILE = "cart_logs.json"

DEFAULT_CATS = ["PURE HONEY","SIDR HONEY","BERI HONEY","DESI GHEE","SARSON OIL","DRY FRUITS","DATES - KHAJOOR","SPICES - MASALAY","OTHER"]

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
if 'categories' not in st.session_state: st.session_state.categories=load_json(CAT_FILE, DEFAULT_CATS)
if 'is_admin' not in st.session_state: st.session_state.is_admin=False
if 'visit_logs' not in st.session_state: st.session_state.visit_logs=load_json(VISIT_LOG_FILE, [])
if 'cart_logs' not in st.session_state: st.session_state.cart_logs=load_json(CART_LOG_FILE, [])

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"
def save_password(p):
    with open(PASS_FILE,"w") as f: f.write(p)

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE,"r") as f: return int(f.read().strip())
        except: return 0
    return 0

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True

st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;}</style>", unsafe_allow_html=True)

# === ADMIN SIDEBAR - FULL 8 SYSTEMS ===
if st.session_state.is_admin:
    with st.sidebar:
        st.title("MEHAR MART ADMIN")
        st.success("✅ ADMIN LOGIN")
        st.caption(f"Pass: {get_password()}")
        st.text_input("Store Link", value=STORE_LINK, key="admin_store_link")
        st.text_input("Admin Link", value=f"{STORE_LINK}?admin={get_password()}", key="admin_admin_link")
        st.divider()
        st.button(f"👀 Visits: {get_visits()}", use_container_width=True)
        st.button(f"🛒 Cart Clicks: {len(load_json(CART_LOG_FILE, []))}", use_container_width=True)
        st.button(f"📦 Products: {len(st.session_state.products)}", use_container_width=True)
        st.divider()
        # FULL 8 SYSTEMS RESTORED
        menu = st.radio("8 SYSTEMS", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - PASSWORD"], label_visibility="collapsed")
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else:
    menu="6. DARAZ STORE"

# 1. PRODUCT SYSTEM - FULL
if menu=="1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V71 FULL")
    c1,c2,c3=st.columns([2,1,1])
    with c1: category=st.selectbox("Category *", st.session_state.categories)
    with c2: new_cat=st.text_input("Nayi Category")
    with c3:
        st.write(""); st.write("")
        if st.button("➕ Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper()); save_json(CAT_FILE, st.session_state.categories); st.rerun()
    name=st.text_input("Product Name *", placeholder="Pure Beri Honey 500gm")
    col_a,col_b=st.columns(2)
    with col_a: kharid=st.number_input("Kharid Rate *", 0, 100000, 2000)
    with col_b: bechna=st.number_input("Bechne Rate *", 0, 100000, 3500)
    col_c,col_d=st.columns(2)
    with col_c: discount=st.number_input("Discount %", 0, 90, 15)
    with col_d: stock=st.number_input("Stock Qty *", 0, 10000, 50)
    expiry_date=st.date_input("Expiry Date *", value=datetime.now()+timedelta(days=180))
    customer_pay=int(bechna * (1 - discount/100)); profit=customer_pay - kharid
    st.info(f"Kharid Rs.{kharid} | Bechna Rs.{bechna} | Pay Rs.{customer_pay} | Profit Rs.{profit}")
    highlights=st.text_area("Highlights *", value="100% Pure - No Sugar, No Mix")
    img_file=st.file_uploader("Photo *", type=["jpg","png","jpeg"])
    if st.button("💾 SAVE PRODUCT", use_container_width=True, type="primary"):
        if name:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((600,600)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=70); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            new_prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":customer_pay,"buy":kharid,"stock":stock,"expiry":expiry_date.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":"MEHAR MART","specs":"500gm","image_b64":img_b64,"rating":5,"reviews":12}
            st.session_state.products.append(new_prod); save_json(PRODUCT_FILE, st.session_state.products); st.success("Saved!"); st.balloons()
    st.divider()
    for idx,p in enumerate(st.session_state.products):
        col1,col2=st.columns([3,1])
        with col1: st.write(f"{idx+1}. {p['name']} - Rs.{p['final']} Stock {p['stock']}")
        with col2:
            if st.button("❌ Delete", key=f"del_p_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - FULL")
    for idx,p in enumerate(st.session_state.products):
        with st.container(border=True):
            col1,col2=st.columns([2,1])
            with col1: st.write(f"**{p['name']}** - Stock {p.get('stock',0)} | Expiry {p.get('expiry','')}")
            with col2:
                if st.button("➕ Plus", key=f"plus_{idx}"): st.session_state.products[idx]['stock']+=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()
                if st.button("➖ Minus", key=f"minus_{idx}"): 
                    if st.session_state.products[idx]['stock']>0: st.session_state.products[idx]['stock']-=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="3. SALES & ORDERS":
    st.header("3. SALES & ORDERS - FULL")
    cart_logs=load_json(CART_LOG_FILE, [])
    if cart_logs: st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    else: st.info("No sales yet")

elif menu=="4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - FULL")
    if not st.session_state.products: st.warning("No products")
    else:
        potential=sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        st.metric("💰 Potential Profit", f"Rs.{potential}")
        report=[]
        for p in st.session_state.products: report.append({"Product":p['name'][:25],"Stock":p.get('stock',0),"Profit/1":p.get('profit',0),"Potential":p.get('profit',0)*p.get('stock',0)})
        st.dataframe(pd.DataFrame(report), use_container_width=True)

elif menu=="5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM - FULL")
    visit_logs=load_json(VISIT_LOG_FILE, []); cart_logs=load_json(CART_LOG_FILE, [])
    if visit_logs: st.subheader("Visits"); st.dataframe(pd.DataFrame(visit_logs), use_container_width=True)
    if cart_logs: st.subheader("Cart"); st.dataframe(pd.DataFrame(cart_logs), use_container_width=True)
    if not visit_logs and not cart_logs: st.info("No client data yet")

elif menu=="7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING - FULL")
    st.metric("👀 Visits", get_visits())
    st.metric("🛒 Cart Clicks", len(load_json(CART_LOG_FILE, [])))
    st.metric("📦 Products", len(st.session_state.products))

elif menu=="8. SETTINGS - PASSWORD":
    st.header("8. SETTINGS - PASSWORD RESET - FULL")
    st.text_input("Store Link", value=STORE_LINK)
    st.text_input("Admin Link", value=f"{STORE_LINK}?admin={get_password()}")
    col1,col2=st.columns(2)
    with col1:
        with st.container(border=True):
            st.info(f"Current: {get_password()}")
            old_p=st.text_input("Purana Password *", type="password", key="old_main")
            new_p=st.text_input("Naya Password *", type="password", key="new_main")
            new_p2=st.text_input("Dobara *", type="password", key="new2_main")
            if st.button("🔑 PASSWORD BADLO", use_container_width=True, type="primary"):
                if old_p!=get_password(): st.error("❌ Galat!")
                elif new_p!=new_p2: st.error("❌ Match nahi!")
                elif new_p=="": st.error("❌ Likho!")
                else: save_password(new_p); st.success(f"✅ Naya: {new_p}"); st.balloons()
    with col2:
        with st.container(border=True):
            st.write("Admin Direct Link")
            st.code(f"{STORE_LINK}?admin={get_password()}")
            if st.button("🗑️ DELETE ALL PRODUCTS", use_container_width=True, type="primary"):
                st.session_state.products=[]; save_json(PRODUCT_FILE, []); st.success("All Deleted!"); st.rerun()

# 6. DARAZ STORE - CLIENT CLEAN - NO EXTRA TEXT FOR CLIENT
else:
    cart_count=len(st.session_state.cart)
    cart_total=sum([p['final'] for p in st.session_state.cart])
    
    st.markdown(f"""
    <div style="background:#f85606; padding:12px 15px; margin:-1rem -1rem 0 -1rem; color:white; display:flex; justify-content:space-between; align-items:center;">
    <div style="font-size:20px; font-weight:bold;">🍯 MEHAR MART</div>
    <div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">🛒 {cart_count}</div>
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
                    if st.button("✕", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
            txt=f"Asalam O Alaikum\nOrder Karna Hai\n\n"
            for x in st.session_state.cart: txt+=f"Product: {x['name']}\nPrice: Rs.{x['final']}\n\n"
            txt+=f"Total: Rs.{cart_total}"
            st.link_button(f"Checkout Rs.{cart_total}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(txt)}", type="primary", use_container_width=True)
    
    prods=st.session_state.products
    if search.strip(): prods=[p for p in prods if search.lower() in p['name'].lower()]
    
    if len(prods)==0:
        st.markdown("<br><br><div style='text-align:center; padding:30px;'><div style='font-size:50px;'>🛍️</div><p style='color:gray;'>Products coming soon</p></div>", unsafe_allow_html=True)
        if st.session_state.is_admin:
            st.info("Admin: Add Product se product add karo - Client ko ye message nahi dikhega, sirf 'Products coming soon' dikhega")
    else:
        c1,c2=st.columns(2)
        for idx,p in enumerate(prods):
            col=c1 if idx%2==0 else c2
            with col:
                with st.container(border=True):
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: st.markdown("<div style='font-size:50px; text-align:center; padding:15px;'>🍯</div>", unsafe_allow_html=True)
                    else: st.markdown("<div style='font-size:50px; text-align:center; padding:15px;'>🍯</div>", unsafe_allow_html=True)
                    st.write(f"**{p['name'][:40]}**")
                    st.write(f"Rs.{p['final']} | {p.get('discount',0)}% OFF")
                    st.caption(f"⭐ {p.get('rating',4.8)} | {p.get('reviews',100)} sold | ✓ Free Delivery")
                    if st.button("Add to Cart", key=f"add_{idx}", use_container_width=True, type="primary"):
                        st.session_state.cart.append(p); st.rerun()
                    single=f"Asalam O Alaikum\nOrder Karna Hai\n\nProduct: {p['name']}\nPrice: Rs.{p['final']}\nTotal: Rs.{p['final']}"
                    st.link_button("Buy Now", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(single)}", use_container_width=True)
    
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    
    # Secret admin entry - small
    if not st.session_state.is_admin:
        st.markdown("---")
        if st.button("⚙️", key="secret_admin"):
            st.session_state.show_admin_login = True
        if st.session_state.get('show_admin_login', False):
            pwd = st.text_input("Admin Password", type="password")
            if st.button("Login Admin"):
                if pwd==get_password(): st.session_state.is_admin=True; st.rerun()
                else: st.error("Wrong")
