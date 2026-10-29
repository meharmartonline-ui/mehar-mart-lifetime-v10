# MEHAR MART V22 - CLIENT PROFESSIONAL - NO PROFIT SHOW - FINAL HADH FIX
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART FINAL", layout="wide")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []

menu = st.sidebar.radio("MEHAR MART MENU", [
    "1. PRODUCT ADD KARO", "2. DARAZ STORE - CLIENT DEKHEGA", "3. MONEY SYSTEM - AAPKA MUNAFA"
])

# 1. PRODUCT ADD
if menu == "1. PRODUCT ADD KARO":
    st.title("Product Add Karo - Aap Ke Liye")
    c1,c2 = st.columns(2)
    with c1:
        name = st.text_input("Product Name *", placeholder="Pure Honey 500gm - Beri Honey - MEHAR MART")
        buy = st.number_input("Kharid Rate (Sirf Aap Dekho Ge)", 0, 100000, 1500)
        sell = st.number_input("Selling Price * (Client Dekhega)", 0, 100000, 2500)
        disc = st.number_input("Discount %", 0, 90, 15)
        stock = st.number_input("Stock", 0, 10000, 50)
    with c2:
        delivery = st.selectbox("Delivery", ["🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi","💵 Cash on Delivery Karachi","💵 Cash on Delivery - Rs.150 Charge"])
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","100% PURE","LIMITED STOCK"])
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
    
    highlights = st.text_area("Highlights", placeholder="100% Pure\nNo Sugar\nLaboratory Tested")
    desc = st.text_area("Full Description - Client Dekhega", placeholder="Pure honey, beri flowers se hasil, immunity ke liye best...")
    specs = st.text_area("Specifications", placeholder="Weight: 500gm\nPurity: 100%")
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    final_price = int(sell * (1-disc/100)) if disc>0 else sell
    profit = final_price - buy
    
    st.info(f"Aapka Private Hisaab: Kharid Rs.{buy} | Selling Rs.{final_price} | Munafa Rs.{profit} - Ye client nahi dekhega")
    
    if st.button("SAVE KARO", use_container_width=True):
        if not name: st.error("Name Likho")
        else:
            img_bytes = img_file.getvalue() if img_file else None
            st.session_state.products.append({"name":name,"buy":buy,"sell":sell,"final":final_price,"discount":disc,"stock":stock,"delivery":delivery,"badge":badge,"highlights":highlights,"description":desc,"specs":specs,"image_bytes":img_bytes,"profit":profit,"expiry":str(expiry)})
            st.success("Save Ho Gaya!"); st.balloons()

# 2. DARAZ STORE - CLIENT VIEW - NO PROFIT EVER
elif menu == "2. DARAZ STORE - CLIENT DEKHEGA":
    st.title("MEHAR MART STORE - Client View")
    if not st.session_state.products:
        st.warning("Abhi koi product nahi")
    else:
        for p in st.session_state.products:
            col1,col2 = st.columns([1,2])
            with col1:
                if p.get('image_bytes'):
                    st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name'])
                st.caption(f"{p['badge']} | {p['delivery']} | Stock: {p['stock']}")
                st.markdown(f"### ~~Rs.{p['sell']}~~  Rs.{p['final']}  ({p['discount']}% OFF)")
                if p['highlights']: st.success(p['highlights'])
                if p['description']: st.write(p['description'])
                if p['specs']: st.caption(p['specs'])
                st.button(f"Order Now - {p['name']}", key=p['name'])
            st.divider()

# 3. MONEY - ONLY YOU SEE PROFIT
else:
    st.title("Money System - Sirf Aap Dekho Ge Profit")
    if not st.session_state.products:
        st.info("Koi product nahi")
    else:
        df = pd.DataFrame([{k:v for k,v in x.items() if k!='image_bytes'} for x in st.session_state.products])
        st.dataframe(df[["name","buy","final","profit","stock"]], use_container_width=True)
        st.metric("TOTAL POTENTIAL MUNAFA (Agar Sab Bik Gaya)", f"Rs. {sum([x['profit']*x['stock'] for x in st.session_state.products])}")
