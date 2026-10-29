import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V16 FINAL IMAGE", layout="wide")
st.title("MEHAR MART V16 - IMAGE FIX FINAL")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'coupons' not in st.session_state: st.session_state.coupons = []

menu = st.sidebar.radio("LIFETIME SYSTEMS - FIXED 7", [
    "1. PRODUCT SYSTEM", 
    "2. STOCK & EXPIRY", 
    "3. SALES & ORDERS", 
    "4. MONEY SYSTEM", 
    "5. CLIENT SYSTEM - EXCEL", 
    "6. DARAZ STORE",
    "7. MARKETING KING"
])

# 1. PRODUCT - IMAGE BYTES FIX
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Photo Ab Show Hogi")
    with st.form("p_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Category", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER"])
            name = st.text_input("Product Name *", "", placeholder="PURE HONEY - Beri Flowers honey")
            buy = st.number_input("Kharid Rate *", 0, step=100)
            sell = st.number_input("Bechne Rate *", 0, step=100)
            disc = st.number_input("Discount %", 0, 100, 0)
            stock = st.number_input("Stock *", 50)
        with c2:
            brand = st.text_input("Brand", "", placeholder="MEHAR MART")
            weight = st.text_input("Weight", "", placeholder="500gm")
            badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
            delivery = st.text_input("Delivery", "", placeholder="Free Delivery Karachi")
            expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
        highlights = st.text_area("Highlights (Khali Hai)", "", placeholder="100% Pure\nNo Sugar", height=80)
        desc = st.text_area("Full Description (Khali Hai)", "", placeholder="Full detail likho...", height=150)
        specs = st.text_area("Specifications (Khali Hai)", "", placeholder="Weight: 500gm", height=80)
        img_file = st.file_uploader("Photo Upload Karo - Jaise Screenshot Me", type=["jpg","png","jpeg"])
        if buy and sell:
            st.info(f"💰 Profit: Rs.{sell-buy} | Customer Pay: Rs.{int(sell*(1-disc/100)) if disc else sell}")
        save = st.form_submit_button("♾️ SAVE - PHOTO KE SATH")
        if save:
            if not name: st.error("Name likho!")
            else:
                img_bytes = img_file.getvalue() if img_file else None
                final = int(sell*(1-disc/100)) if disc else sell
                st.session_state.products.append({
                    "date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,
                    "buy":buy,"sell":sell,"discount":disc,"final":final,"stock":stock,
                    "weight":weight,"expiry":str(expiry),"delivery":delivery,"badge":badge,
                    "highlights":highlights,"description":desc,"specs":specs,
                    "image_bytes":img_bytes,"profit":sell-buy
                })
                st.success(f"{name} Photo Ke Sath Save Ho Gaya!"); st.balloons()

    # AAPKE SARE PRODUCTS - PHOTO KE SATH - JAISA SCREENSHOT ME HAI
    st.divider()
    st.subheader("Aapke Sare Products - Photo Ke Sath")
    if not st.session_state.products: st.info("Koi product nahi")
    else:
        for p in st.session_state.products:
            st.write(f"✅ {p['name']} | Category: {p['category']} | Stock: {p['stock']} | Rs.{p['final']}")
            st.success(f"💰 Munafa: Rs.{p['profit']}")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=300)
                except: st.error("Photo load error")
            if p['description']: st.info(f"📝 {p['description']}")
            st.divider()

# 2. STOCK
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY"); 
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df, use_container_width=True)

# 3. SALES
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("s_form"):
        cname=st.text_input("Customer Name", "", placeholder="Ali")
        city=st.text_input("City", "", placeholder="Karachi")
        if st.session_state.products:
            pname=st.selectbox("Product", [p['name'] for p in st.session_state.products])
            qty=st.number_input("Qty",1,100,1)
        else: pname="No"; qty=1
        go=st.form_submit_button("SALE KARO")
        if go and st.session_state.products:
            for p in st.session_state.products:
                if p['name']==pname:
                    profit=(p['final']-p['buy'])*qty
                    p['stock']-=qty
                    st.session_state.sales.append({"date":str(datetime.now().date()),"customer":cname,"product":pname,"qty":qty,"total":p['final']*qty,"profit":profit})
                    st.success(f"Sale! Profit Rs.{profit}"); st.balloons()
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

# 4. MONEY
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA", f"Rs. {df['profit'].sum()}", delta="MASHALLAH")

# 5. CLIENT EXCEL
elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL")
    if not st.session_state.sales: st.warning("Pehle Sale Karo")
    else:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        c1,c2=st.columns(2)
        with c1: st.download_button("📥 SALES EXCEL", df.to_csv(index=False).encode('utf-8'), "sales.csv", "text/csv")
        with c2: 
            client_df=df.groupby(["customer"]).agg(orders=("product","count"), total=("total","sum")).reset_index()
            st.download_button("📥 CLIENT EXCEL", client_df.to_csv(index=False).encode('utf-8'), "clients.csv", "text/csv")

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    st.header("6. DARAZ STORE - Photo Ke Sath")
    if not st.session_state.products: st.warning("No Product")
    else:
        for p in st.session_state.products:
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name']); st.write(f"Stock {p['stock']} | Rs.{p['final']}"); st.success(f"💰 Munafa Rs.{p['profit']}")
                if p['description']: st.write(p['description'])
            st.divider()

# 7. MARKETING
elif menu == "7. MARKETING KING":
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']}\n{prod['description']}\nOrder Now!"
        st.text_area("WhatsApp Caption", wa, height=200)
