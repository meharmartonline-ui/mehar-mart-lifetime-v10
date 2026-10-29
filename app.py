import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import os

st.set_page_config(page_title="MEHAR MART LIFETIME V10", layout="wide")

st.title("MEHAR MART LIFETIME SYSTEM V10")
st.markdown("### Ek Baar Banao, Lifetime Chalao - Bhai ka Wada!")

# --- Session State for Data ---
if 'products' not in st.session_state:
    st.session_state.products = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'clients' not in st.session_state:
    st.session_state.clients = []

menu = st.sidebar.selectbox("LIFETIME SYSTEMS", ["1. PRODUCT SYSTEM", "2. STOCK & EXPIRY SYSTEM", "3. SALES & ORDERS", "4. MONEY SYSTEM", "5. CLIENT SYSTEM"])

# 1. PRODUCT SYSTEM
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Add Lifetime Product")
    with st.form("product_form"):
        name = st.text_input("Product Name", "PURE HONEY 100% Natural")
        buy = st.number_input("Kharid Rate", 0)
        sell = st.number_input("Bechne Rate", 0)
        stock = st.number_input("Stock Qty", 0)
        expiry = st.date_input("Expiry Date", datetime.now() + timedelta(days=365))
        img = st.file_uploader("Product Photo", type=["jpg","png","jpeg"])
        submit = st.form_submit_button("♾️ LIFETIME SAVE")
        if submit:
            path = ""
            if img:
                os.makedirs("images", exist_ok=True)
                path = f"images/{img.name}"
                with open(path, "wb") as f:
                    f.write(img.getbuffer())
            st.session_state.products.append({"name":name,"buy":buy,"sell":sell,"stock":stock,"expiry":str(expiry),"image":path})
            st.success("Lifetime me Save Ho Gaya Bhai!")

    if st.session_state.products:
        for p in st.session_state.products:
            st.write(f"✅ {p['name']} | Stock: {p['stock']} | Expiry: {p['expiry']}")
            if p['image'] and os.path.exists(p['image']):
                st.image(p['image'], width=200)

# 2. STOCK & EXPIRY SYSTEM - FIXED
elif menu == "2. STOCK & EXPIRY SYSTEM":
    st.header("2. STOCK & EXPIRY SYSTEM - Auto Alert")
    if not st.session_state.products:
        st.warning("Abhi koi product nahi hai Bhai!")
    else:
        df = pd.DataFrame(st.session_state.products)
        # FIXED: Simple dataframe without error parameter
        st.dataframe(df)
        
        # Expiry Alert
        st.subheader("⚠️ Expiry Alert (30 Din me expire)")
        today = datetime.now().date()
        for p in st.session_state.products:
            exp_date = datetime.strptime(p['expiry'], "%Y-%m-%d").date()
            diff = (exp_date - today).days
            if diff <= 30:
                st.error(f"{p['name']} - {diff} din me expire! Stock: {p['stock']}")

# 3. SALES & ORDERS
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("sale_form"):
        cname = st.text_input("Customer Name")
        city = st.text_input("City")
        pname = st.selectbox("Product", [p['name'] for p in st.session_state.products] if st.session_state.products else ["No Product"])
        qty = st.number_input("Qty", 1)
        s_submit = st.form_submit_button("MASHALLAH Sale")
        if s_submit:
            # Find product price
            price = 0
            buy_price = 0
            for p in st.session_state.products:
                if p['name'] == pname:
                    price = p['sell']
                    buy_price = p['buy']
                    p['stock'] -= qty
            profit = (price - buy_price) * qty
            st.session_state.sales.append({"customer":cname,"city":city,"product":pname,"qty":qty,"total":price*qty,"profit":profit,"date":str(datetime.now().date())})
            if cname not in [c['name'] for c in st.session_state.clients]:
                st.session_state.clients.append({"name":cname,"city":city})
            st.success(f"Sale Ho Gayi! Profit: {profit}")

    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales))

# 4. MONEY SYSTEM
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - Din ka Hisaab")
    if st.session_state.sales:
        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df)
        st.metric("Total Sale", f"Rs. {df['total'].sum()}")
        st.metric("Total Munafa", f"Rs. {df['profit'].sum()}")
    else:
        st.info("Abhi koi sale nahi Bhai")

# 5. CLIENT SYSTEM
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    if st.session_state.clients:
        df = pd.DataFrame(st.session_state.clients)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("CLIENT LIST DOWNLOAD", csv, "clients.csv", "text/csv")
    else:
        st.info("Abhi koi client nahi")
    
    st.info("1 Baar Product Add Karo Roz Sale Add Karo Hisaab Auto Hoga!")
