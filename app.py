# MEHAR MART V75 - V60 FULL RESTORED - HIGHLIGHTS+DESCRIPTION+SPECIFICATIONS+VISITORS+PROFIT ALL BACK + CLIENT CLEAN
import streamlit as st, os, urllib.parse, json, random
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
if 'admin_menu' not in st.session_state: st.session_state.admin_menu="1. PRODUCT SYSTEM"
if 'logo_b64' not in st.session_state: st.session_state.logo_b64=load_json(LOGO_FILE, None)
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
def add_visit_log():
    try:
        logs=load_json(VISIT_LOG_FILE, [])
        logs.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M"), "ip":"client"})
        save_json(VISIT_LOG_FILE, logs[-100:])
        count=get_visits()+1
        with open(VISIT_FILE,"w") as f: f.write(str(count))
    except: pass

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True

if not st.session_state.is_admin:
    st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;}</style>", unsafe_allow_html=True)
    add_visit_log()
else:
    st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

if st.session_state.is_admin:
    menu_top = st.selectbox("", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - LOGO & PASSWORD"], index=0)
    st.session_state.admin_menu=menu_top
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("STORE VIEW", use_container_width=True): st.session_state.admin_menu="6. DARAZ STORE"; st.rerun()
    with c2:
        if st.button("ADD PRODUCT", use_container_width=True, type="primary"): st.session_state.admin_menu="1. PRODUCT SYSTEM"; st.rerun()
    with c3:
        if st.button("LOGOUT", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
    st.divider()
    menu = st.session_state.admin_menu
    with st.sidebar:
        st.title("ADMIN")
        st.success("Login OK")
        st.text_input("Store Link", value=STORE_LINK)
        st.text_input("Admin Link", value=f"{STORE_LINK}?admin={get_password()}")
        st.divider()
        v=get_visits()
        cart_logs=load_json(CART_LOG_FILE, [])
        st.button(f"👀 Visitors: {v}", use_container_width=True)
        st.button(f"🛒 Add to Cart Clicks: {len(cart_logs)}", use_container_width=True)
        st.button(f"📦 Total Products: {len(st.session_state.products)}", use_container_width=True)
        st.divider()
        sb = st.radio("Menu", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - LOGO & PASSWORD"], index=["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - LOGO & PASSWORD"].index(menu) if menu in ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING","8. SETTINGS - LOGO & PASSWORD"] else 0)
        if sb!=menu: st.session_state.admin_menu=sb; st.rerun()
        if st.button("Logout"): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
else:
    menu="6. DARAZ STORE"

if menu=="1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - V60 FULL")
    c1,c2,c3=st.columns([2,1,1])
    with c1: category=st.selectbox("Category *", st.session_state.categories)
    with c2: new_cat=st.text_input("New Category")
    with c3:
        st.write(""); st.write("")
        if st.button("Add Category", use_container_width=True):
            if new_cat and new_cat.upper() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.upper()); save_json(CAT_FILE, st.session_state.categories); st.rerun()
    name=st.text_input("Product Name *", placeholder="Beri Honey 500gm")
    ca,cb=st.columns(2)
    with ca: kharid=st.number_input("Kharid Rate *", 0, 100000, 2000)
    with cb: bechna=st.number_input("Bechne Rate *", 0, 100000, 3500)
    cc,cd=st.columns(2)
    with cc: discount=st.number_input("Discount %", 0, 90, 15)
    with cd: stock=st.number_input("Stock *", 0, 10000, 10)
    expiry=st.date_input("Expiry *", value=datetime.now()+timedelta(days=180))
    pay=int(bechna * (1 - discount/100)); profit=pay - kharid
    st.info(f"Client Pay Kare Ga: Rs.{pay} | Aapka Profit: Rs.{profit}")
    highlights=st.text_area("Highlights *", value="100% Pure - No Sugar, No Mix\nOriginal Beri Flowers Honey\nLaboratory Tested\nFor Health, Energy & Immunity", height=120)
    full_desc=st.text_area("Full Description *", value="MEHAR MART - Aapki Sehat Ka Sathi\nCash on Delivery All Pakistan\n100% Pure & Natural", height=100)
    specs=st.text_area("Specifications *", value="Weight: 500gm\nType: Beri Honey\nBrand: MEHAR MART\nExpiry: 2 Years", height=100)
    img_file=st.file_uploader("Photo *", type=["jpg","png","jpeg"])
    if st.button("SAVE PRODUCT", type="primary", use_container_width=True):
        if name and highlights and full_desc and specs:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((800,800)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=75); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":pay,"buy":kharid,"stock":stock,"expiry":expiry.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64,"rating":5,"reviews":10}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success(f"{name} Saved!"); st.balloons()
        else:
            st.error("Product Name, Highlights, Description, Specifications zaroori hain!")
    st.divider()
    st.subheader(f"Saved Products: {len(st.session_state.products)}")
    for idx,p in enumerate(st.session_state.products):
        with st.container(border=True):
            c1,c2=st.columns([3,1])
            with c1: st.write(f"**{idx+1}. {p['name']}** - Rs.{p['final']} | Stock {p['stock']} | Profit Rs.{p.get('profit',0)}")
            with c2:
                if st.button("Delete", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - V60 FULL")
    for idx,p in enumerate(st.session_state.products):
        with st.container(border=True):
            col1,col2,col3=st.columns([2,1,1])
            with col1: st.write(f"**{p['name']}**"); st.caption(f"Stock: {p['stock']} | Expiry: {p.get('expiry','')} | Profit: Rs.{p.get('profit',0)}")
            with col2:
                if st.button("Plus Stock", key=f"plus_{idx}"): st.session_state.products[idx]['stock']+=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()
            with col3:
                if st.button("Minus Stock", key=f"minus_{idx}"): 
                    if st.session_state.products[idx]['stock']>0: st.session_state.products[idx]['stock']-=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="3. SALES & ORDERS":
    st.header("3. SALES & ORDERS - V60 FULL")
    cart_logs=load_json(CART_LOG_FILE, [])
    if cart_logs:
        df=pd.DataFrame(cart_logs)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Add to Cart Clicks", len(cart_logs))
    else: st.info("Abhi tak koi Add to Cart nahi hua")

elif menu=="4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - V60 FULL")
    if not st.session_state.products: st.warning("No products")
    else:
        potential=sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])
        total_kharid=sum([p.get('kharid',0)*p.get('stock',0) for p in st.session_state.products])
        total_sell=sum([p.get('final',0)*p.get('stock',0) for p in st.session_state.products])
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Kharid Total", f"Rs.{total_kharid}")
        with c2: st.metric("Sell Total", f"Rs.{total_sell}")
        with c3: st.metric("Potential Profit", f"Rs.{potential}")
        data=[]
        for p in st.session_state.products: data.append({"Product":p['name'][:20],"Stock":p['stock'],"Kharid":p['kharid'],"Sell":p['final'],"Profit/1":p.get('profit',0),"Potential Profit":p.get('profit',0)*p['stock']})
        st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu=="5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM - V60 FULL")
    visit_logs=load_json(VISIT_LOG_FILE, [])
    cart_logs=load_json(CART_LOG_FILE, [])
    st.metric("Total Visitors", get_visits())
    st.metric("Add to Cart Clicks", len(cart_logs))
    if visit_logs:
        st.subheader("Visit Logs")
        st.dataframe(pd.DataFrame(visit_logs[-50:]), use_container_width=True)
    if cart_logs:
        st.subheader("Add to Cart Logs")
        st.dataframe(pd.DataFrame(cart_logs[-50:]), use_container_width=True)

elif menu=="7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING - V60 FULL")
    st.metric("👀 Visitors", get_visits())
    st.metric("🛒 Add to Cart", len(load_json(CART_LOG_FILE, [])))
    st.metric("📦 Products", len(st.session_state.products))
    st.metric("💰 Potential Profit", f"Rs.{sum([p.get('profit',0)*p.get('stock',0) for p in st.session_state.products])}")

elif menu=="8. SETTINGS - LOGO & PASSWORD":
    st.header("8. SETTINGS - LOGO & PASSWORD - V60 FULL")
    st.subheader("Logo Upload")
    logo_file=st.file_uploader("Logo (200x200 PNG)", type=["png","jpg","jpeg"])
    if logo_file:
        try: img=Image.open(logo_file); img.thumbnail((200,200)); buf=io.BytesIO(); img.save(buf, format="PNG"); lb64=base64.b64encode(buf.getvalue()).decode(); st.session_state.logo_b64=lb64; save_json(LOGO_FILE, lb64); st.success("Logo Saved")
        except: pass
    if st.session_state.logo_b64:
        try: st.image(Image.open(io.BytesIO(base64.b64decode(st.session_state.logo_b64))), width=100)
        except: pass
        if st.button("Remove Logo"): st.session_state.logo_b64=None; save_json(LOGO_FILE, None); st.rerun()
    st.divider()
    st.subheader("Password Reset")
    st.text_input("Store Link", value=STORE_LINK)
    st.text_input("Admin Link", value=f"{STORE_LINK}?admin={get_password()}")
    old_p=st.text_input("Old Password", type="password", key="old_pass")
    new_p=st.text_input("New Password", type="password", key="new_pass")
    new_p2=st.text_input("Confirm New", type="password", key="new_pass2")
    if st.button("Change Password", type="primary", use_container_width=True):
        if old_p!=get_password(): st.error("Wrong old")
        elif new_p!=new_p2: st.error("Not match")
        elif not new_p: st.error("Empty")
        else: save_password(new_p); st.success(f"New: {new_p}"); st.balloons()
    if st.button("DELETE ALL PRODUCTS", type="primary", use_container_width=True):
        st.session_state.products=[]; save_json(PRODUCT_FILE, []); st.success("All Deleted")

else:
    # 6. DARAZ STORE - CLIENT - CLEAN - NO ADMIN BOX
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
    search=st.text_input("", placeholder="Search products...", label_visibility="collapsed")
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
        st.markdown("<br><br><div style='text-align:center;'><p style='color:gray;'>Products coming soon</p></div>", unsafe_allow_html=True)
    else:
        c1,c2=st.columns(2)
        for idx,p in enumerate(prods):
            col=c1 if idx%2==0 else c2
            with col:
                with st.container(border=True):
                    if p.get('image_b64'):
                        try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                        except: st.write("🍯")
                    st.write(f"**{p['name'][:35]}**")
                    st.write(f"Rs.{p['final']} | {p.get('discount',0)}% OFF")
                    st.caption(f"⭐ {p.get('rating',5)} | Free Delivery")
                    if st.button("Add to Cart", key=f"add_{idx}", use_container_width=True, type="primary"):
                        logs=load_json(CART_LOG_FILE, []); logs.append({"product":p['name'],"price":p['final'],"time":datetime.now().strftime("%Y-%m-%d %H:%M")}); save_json(CART_LOG_FILE, logs); st.session_state.cart.append(p); st.rerun()
                    single=f"Asalam O Alaikum\nOrder Karna Hai\n\nProduct: {p['name']}\nPrice: Rs.{p['final']}\nTotal: Rs.{p['final']}"
                    st.link_button("Buy Now", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(single)}", use_container_width=True)
    st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
