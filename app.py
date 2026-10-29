import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import random

st.set_page_config(page_title="MEHAR MART V12.1 KHALI BOX", layout="wide")
st.title("MEHAR MART V12.1 - KHALI DESCRIPTION")
st.markdown("### Ab Koi Pehle Se Likha Hua Nahi Ayega Bhai!")

if 'products' not in st.session_state:
    st.session_state.products = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'coupons' not in st.session_state:
    st.session_state.coupons = []

menu = st.sidebar.selectbox("MENU", ["1. PRODUCT ADD", "2. DARAZ STORE", "3. SALES & PROFIT", "4. MONEY", "5. MARKETING KING"])

# 1. PRODUCT ADD - KHALI BOXES
if menu == "1. PRODUCT ADD":
    st.header("Product Add Karo - Sab Khali Hai")
    with st.form("product_form"):
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("Category", ["PURE HONEY", "MASALA", "DRY FRUIT", "GADGET", "OTHER"])
            name = st.text_input("Product Name", "", placeholder="Jaise: MEHAR Beri Honey 500gm")
            buy = st.number_input("Kharid Rate", 0, placeholder="2000")
            sell = st.number_input("Bechne Rate", 0, placeholder="2500")
            discount = st.number_input("Discount %", 0, 100, 0)
            stock = st.number_input("Stock Qty", 0)
        with c2:
            brand = st.text_input("Brand", "", placeholder="MEHAR MART")
            weight = st.text_input("Weight / Size", "", placeholder="500gm ya 1KG")
            badge = st.selectbox("Badge", ["BEST SELLER", "NEW", "LIMITED STOCK", "100% PURE", "SALE"])
            delivery = st.text_input("Delivery", "", placeholder="Free Delivery Karachi")
            expiry = st.date_input("Expiry", datetime.now() + timedelta(days=365))
        
        # KHALI BOXES - KOI PEHLE SE LIKHA HUA NAHI
        highlights = st.text_area("Highlights Likho (Khali Hai)", "", placeholder="Yahan likho:\n100% Pure\nNo Sugar\nNatural", height=100)
        description = st.text_area("Full Description Likho (Khali Hai) - Daraz Jaisi", "", placeholder="Yahan apni marzi se full detail likho... Jaise: Ye Kohistan ka asli shehad hai, 100% pure...", height=150)
        specs = st.text_area("Specifications Likho (Khali Hai)", "", placeholder="Weight: 500gm\nType: Beri Honey\nPacking: Glass Jar", height=80)
        
        img = st.file_uploader("Product Photo", type=["jpg","png","jpeg"])
        
        # PROFIT LIVE
        profit = sell - buy
        if buy > 0 and sell > 0:
            final_price = int(sell * (1-discount/100)) if discount>0 else sell
            st.info(f"💰 LIVE PROFIT: Rs.{profit} | Customer Pay Karega: Rs.{final_price}")
        else:
            st.info("Kharid aur Bechne Rate Likho - Profit Khud Niklega")
        
        submit = st.form_submit_button("♾️ SAVE KARO")
        if submit:
            if name == "":
                st.error("Bhai Product Name to likho!")
            else:
                path = ""
                if img:
                    os.makedirs("images", exist_ok=True)
                    path = f"images/{img.name}"
                    with open(path, "wb") as f:
                        f.write(img.getbuffer())
                final_price = int(sell * (1-discount/100)) if discount>0 else sell
                st.session_state.products.append({
                    "category":category,"name":name,"brand":brand,"buy":buy,"sell":sell,
                    "discount":discount,"stock":stock,"weight":weight,"expiry":str(expiry),
                    "delivery":delivery,"badge":badge,"highlights":highlights,
                    "description":description,"specs":specs,"image":path,
                    "profit":profit,"final":final_price
                })
                st.success(f"✅ {name} Save Ho Gaya! Profit Rs.{profit}")
                st.balloons()

# 2. STORE
elif menu == "2. DARAZ STORE":
    st.header("Store")
    if not st.session_state.products:
        st.warning("Koi product nahi")
    else:
        for p in st.session_state.products:
            col1, col2 = st.columns([1,2])
            with col1:
                if p['image'] and os.path.exists(p['image']):
                    st.image(p['image'], use_column_width=True)
            with col2:
                st.markdown(f"**{p['badge']}**")
                st.subheader(p['name'])
                st.write(f"Stock: {p['stock']} | {p['weight']}")
                st.markdown(f"~~Rs.{p['sell']}~~ -> **Rs.{p['final']}** (-{p['discount']}%)")
                st.success(f"💰 Munafa: Rs.{p['profit']}")
            if p['description']:
                with st.expander("Full Description Dekho"):
                    st.write(p['description'])
            st.divider()

# 3. SALES
elif menu == "3. SALES & PROFIT":
    st.header("Sale Karo")
    with st.form("sale_form"):
        cname = st.text_input("Customer Name", "")
        city = st.text_input("City", "")
        if st.session_state.products:
            pname = st.selectbox("Product", [p['name'] for p in st.session_state.products])
            qty = st.number_input("Qty", 1, 100, 1)
        else:
            pname="No"; qty=1
        s_submit = st.form_submit_button("Sale Done")
        if s_submit and st.session_state.products:
            for p in st.session_state.products:
                if p['name']==pname:
                    disc = p['final']
                    profit_total = (disc - p['buy']) * qty
                    p['stock'] -= qty
                    st.session_state.sales.append({"date":str(datetime.now().date()),"customer":cname,"product":pname,"qty":qty,"total":disc*qty,"profit":profit_total})
                    st.success(f"Sale! Total Rs.{disc*qty} | PROFIT Rs.{profit_total}")
                    st.balloons()
    if st.session_state.sales:
        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Munafa", f"Rs. {df['profit'].sum()}")

# 4. MONEY
elif menu == "4. MONEY":
    st.header("MONEY DASHBOARD")
    if st.session_state.sales:
        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA (PROFIT)", f"Rs. {df['profit'].sum()}", delta="MASHALLAH")
    else:
        st.warning("No sale yet")

# 5. MARKETING
elif menu == "5. MARKETING KING":
    st.header("MARKETING KING")
    if st.session_state.products:
        p_name = st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod = [x for x in st.session_state.products if x['name']==p_name][0]
        wa_msg = f"🍯 {prod['name']} 🍯\nPrice: Rs.{prod['sell']} -> Rs.{prod['final']}\n{prod['description']}\nOrder Now!"
        st.text_area("WhatsApp Message (Khali description se banega)", wa_msg, height=200)
