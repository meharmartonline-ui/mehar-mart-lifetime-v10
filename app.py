# MEHAR MART V44 - V17 PROFIT + V20 3 BOX + 7 SYSTEMS - FINAL
import streamlit as st, os, urllib.parse, pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V44 COMPLETE", layout="wide")

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

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE,"r") as f: return int(f.read().strip())
        except: return 0
    return 0

def add_visit_once():
    if 'visit_counted' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE,"w") as f: f.write(str(v))
        st.session_state.visit_counted = True
        return v
    return get_visits()

total_visits = add_visit_once()

if os.path.exists(ORDER_FILE) and 'orders_loaded' not in st.session_state:
    try:
        st.session_state.orders = pd.read_csv(ORDER_FILE).to_dict('records')
        st.session_state.orders_loaded = True
    except: pass

def get_password():
    if os.path.exists("admin_password.txt"):
        with open("admin_password.txt","r") as f: return f.read().strip()
    return "mehar123"

st.sidebar.title("🔐 ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
if pwd == get_password() and pwd != "": st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    menu = st.sidebar.radio("System Select Karo:", 
        ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"],
        label_visibility="collapsed"
    )
    st.sidebar.text_input("Store Link:", value=STORE_LINK)
else:
    menu = "6. DARAZ STORE"

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Live Profit Wala")
    cat = st.selectbox("Category", ["PURE HONEY","SIDR HONEY","BERI HONEY","OTHER"])
    name = st.text_input("Product Name *", placeholder="PURE HONEY - Beri Flowers honey")
    c1,c2 = st.columns(2)
    with c1: kharid = st.number_input("Kharid Rate *", 0, 100000, 2000)
    with c2: bechna = st.number_input("Bechne Rate *", 0, 100000, 2500)
    discount = st.number_input("Discount %", 0, 90, 15)
    
    # LIVE HISAB
    customer_pay = int(bechna * (1 - discount/100))
    profit = customer_pay - kharid
    
    st.divider()
    st.subheader("💰 LIVE HISAAB - Box Me")
    b1,b2,b3,b4 = st.columns(4)
    with b1: st.info(f"Kharid\nRs.{kharid}")
    with b2: st.warning(f"Bechna\nRs.{bechna}")
    with b3: st.success(f"Customer Pay\nRs.{customer_pay}")
    with b4: st.success(f"PROFIT\nRs.{profit}")
    st.divider()

    stock = st.number_input("Stock", 0, 10000, 50)
    brand = st.text_input("Brand", value="MEHAR MART")

    # ★★★ YE 3 BOX - V20 WALE - AAPKI SCREENSHOT WALE - AB BILKUL WAISAY HI ★★★
    st.subheader("📝 Product Detail Boxes - V20 Wale")
    highlights = st.text_area("Highlights (Khali Hai)", placeholder="100% Pure\nNo Sugar", height=100)
    full_desc = st.text_area("Full Description (Khali Hai)", placeholder="Full detail...\nShahad k faide...", height=120)
    specs = st.text_area("Specifications (Khali Hai)", placeholder="Weight: 500gm\nOrigin: Karachi", height=100)
    
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    if st.button("💾 SAVE PRODUCT", use_container_width=True, type="primary"):
        if name:
            img_bytes = img_file.getvalue() if img_file else None
            exp_date = datetime.now() + timedelta(days=180)
            st.session_state.products.append({
                "name":name,"category":cat,"sell":bechna,"kharid":kharid,"discount":discount,
                "final":customer_pay,"buy":kharid,"stock":stock,"expiry":exp_date.strftime("%Y-%m-%d"),
                "profit":profit,"brand":brand,"highlights":highlights,"full_desc":full_desc,"specs":specs,
                "image_bytes":img_bytes
            })
            st.success(f"✅ Save! Customer Pay Rs.{customer_pay} | Profit Rs.{profit}")
        else:
            st.error("Name likho!")

# BAKI SYSTEMS - SHORT
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    for p in st.session_state.products:
        st.write(f"**{p['name']}** - Stock {p['stock']} - Profit Rs.{p.get('profit',0)}")
        st.caption(f"Highlights: {p.get('highlights','')} | Desc: {p.get('full_desc','')[:50]} | Specs: {p.get('specs','')}")
        st.divider()

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("sale"):
        prod_names = [p['name'] for p in st.session_state.products]
        sel_prod = st.selectbox("Product", prod_names) if prod_names else st.text_input("Product")
        qty=st.number_input("Qty",1,1000,1); client=st.text_input("Client"); sub=st.form_submit_button("Sale Add")
        if sub:
            price=0
            for p in st.session_state.products:
                if p['name']==sel_prod: price=p['final']
            st.session_state.sales.append({"date":datetime.now().strftime("%Y-%m-%d"),"product":sel_prod,"qty":qty,"price":price,"total":qty*price,"client":client})
            st.success("Added!")
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales),use_container_width=True)

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales); st.dataframe(df,use_container_width=True)

elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    if st.session_state.clients: st.dataframe(pd.DataFrame(st.session_state.clients),use_container_width=True)

elif menu == "6. DARAZ STORE":
    st.header("🛒 MEHAR MART STORE")
    st.code(STORE_LINK)
    if not st.session_state.products: st.warning("No products - 1. PRODUCT SYSTEM me add karo")
    else:
        cols=st.columns(2)
        for idx,p in enumerate(st.session_state.products):
            with cols[idx%2]:
                with st.container(border=True):
                    if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])),use_column_width=True)
                    st.markdown(f"**{p['name']}**"); st.markdown(f"**Rs.{p['final']}** ({p['discount']}% OFF)")
                    st.caption(f"{p.get('highlights','')} | {p.get('specs','')}")
                    if st.button(f"Add to Cart",key=f"add{idx}",use_container_width=True):
                        st.session_state.cart.append(p); st.rerun()

elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    st.metric("Visits", total_visits)
    if os.path.exists(ORDER_FILE):
        df=pd.read_csv(ORDER_FILE); st.dataframe(df,use_container_width=True)
