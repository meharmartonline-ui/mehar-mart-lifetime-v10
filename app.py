import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="MEHAR MART LIFETIME V10.2", layout="wide")
st.title("MEHAR MART LIFETIME SYSTEM V10.2")
st.markdown("### Category System Add Ho Gaya Bhai!")

if 'products' not in st.session_state:
    st.session_state.products = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'clients' not in st.session_state:
    st.session_state.clients = []

menu = st.sidebar.selectbox("LIFETIME SYSTEMS", ["1. PRODUCT SYSTEM", "2. STOCK & EXPIRY SYSTEM", "3. SALES & ORDERS", "4. MONEY SYSTEM", "5. CLIENT SYSTEM"])

# 1. PRODUCT SYSTEM WITH CATEGORY
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Add Lifetime Product")
    with st.form("product_form"):
        category = st.selectbox("Category Select Karo", ["PURE HONEY", "MASALA", "DRY FRUIT", "GADGET", "ATTA", "OTHER"])
        name = st.text_input("Product Name", "")
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
            full_name = f"{category} - {name}"
            st.session_state.products.append({"category":category,"name":full_name,"buy":buy,"sell":sell,"stock":stock,"expiry":str(expiry),"image":path})
            st.success(f"{full_name} Lifetime me Save Ho Gaya Bhai!")

    st.subheader("Aapke Sare Products")
    if st.session_state.products:
        for p in st.session_state.products:
            st.write(f"✅ {p['name']} | Category: {p['category']} | Stock: {p['stock']} | Rs.{p['sell']}")
            if p['image'] and os.path.exists(p['image']):
                st.image(p['image'], width=200)
    else:
        st.info("Abhi koi product nahi - Naya product add karo")

# 2. STOCK
elif menu == "2. STOCK & EXPIRY SYSTEM":
    st.header("2. STOCK & EXPIRY SYSTEM")
    if not st.session_state.products:
        st.warning("Abhi koi product nahi hai Bhai!")
    else:
        df = pd.DataFrame(st.session_state.products)
        st.dataframe(df)
        st.subheader("Category Filter")
        cat_filter = st.selectbox("Category Dekho", ["ALL"] + list(df['category'].unique()))
        if cat_filter != "ALL":
            st.dataframe(df[df['category']==cat_filter])

# 3. SALES
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("sale_form"):
        cname = st.text_input("Customer Name")
        city = st.text_input("City")
        pname = st.selectbox("Product", [p['name'] for p in st.session_state.products] if st.session_state.products else ["No Product"])
        qty = st.number_input("Qty", 1)
        s_submit = st.form_submit_button("MASHALLAH Sale")
        if s_submit:
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

# 4. MONEY
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales:
        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df)
        st.metric("Total Sale", f"Rs. {df['total'].sum()}")
        st.metric("Total Munafa", f"Rs. {df['profit'].sum()}")
    else:
        st.info("Abhi koi sale nahi Bhai")

# 5. CLIENT
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    if st.session_state.clients:
        df = pd.DataFrame(st.session_state.clients)
        st.dataframe(df)
    else:
        st.info("Abhi koi client nahi")
