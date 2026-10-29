# MEHAR MART V23 - CATEGORY WAPAS + CLIENT FIX - FINAL
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V23", layout="wide")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []

menu = st.sidebar.radio("MEHAR MART MENU", [
    "1. PRODUCT ADD KARO", "2. DARAZ STORE - CLIENT DEKHEGA", "3. MONEY SYSTEM"
])

if menu == "1. PRODUCT ADD KARO":
    st.title("Product Add Karo")
    c1,c2 = st.columns(2)
    with c1:
        # CATEGORY WAPAS BHAI - YAHAN HAI
        cat = st.selectbox("Category * - Wapas Add Kiya", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER","OIL","SHAMPOO","SOAP"])
        name = st.text_input("Product Name *", placeholder="Pure Honey 500gm - Beri Honey - MEHAR MART")
        buy = st.number_input("Kharid Rate (Sirf Aap)", 0, 100000, 1500)
        sell = st.number_input("Selling Price * (Client Dekhega)", 0, 100000, 2500)
        disc = st.number_input("Discount %", 0, 90, 15)
        stock = st.number_input("Stock", 0, 10000, 50)
    with c2:
        brand = st.text_input("Brand", "MEHAR MART")
        weight = st.text_input("Weight", "500gm")
        delivery = st.selectbox("Delivery", ["🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi","💵 Cash on Delivery Karachi","💵 Cash on Delivery - Rs.150 Charge","🚚 Free Delivery Lahore / Karachi / Islamabad"])
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","100% PURE","LIMITED STOCK","SALE"])
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
    
    highlights = st.text_area("Highlights", placeholder="100% Pure\nNo Sugar")
    desc = st.text_area("Full Description - Client Dekhega", placeholder="Pure honey, beri flowers se hasil...")
    specs = st.text_area("Specifications", placeholder="Weight: 500gm\nPurity: 100%")
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    final_price = int(sell * (1-disc/100)) if disc>0 else sell
    profit = final_price - buy
    st.info(f"Aapka Private: Kharid Rs.{buy} | Selling Rs.{final_price} | Munafa Rs.{profit} - Client Nahi Dekhega")
    
    if st.button("SAVE KARO", use_container_width=True):
        if not name: st.error("Name Likho Bhai!")
        else:
            img_bytes = img_file.getvalue() if img_file else None
            st.session_state.products.append({
                "category":cat,"name":name,"brand":brand,"buy":buy,"sell":sell,"final":final_price,
                "discount":disc,"stock":stock,"weight":weight,"delivery":delivery,"badge":badge,
                "highlights":highlights,"description":desc,"specs":specs,
                "image_bytes":img_bytes,"profit":profit,"expiry":str(expiry)
            })
            st.success(f"Save Ho Gaya! Category: {cat}"); st.balloons()
    
    # SAVED - CLIENT VIEW - NO PROFIT
    st.divider()
    st.subheader("Saved Products - Client Ko Ye Dikhega (No Profit)")
    if st.session_state.products:
        for p in st.session_state.products:
            st.markdown(f"**{p['category']} | {p['name']} | Rs.{p['final']} | {p['delivery']}**")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=250)
                except: pass
            if p.get('description'): st.write(p['description'])
            with st.expander("🔒 Private Munafa (Sirf Aap)"): st.write(f"Buy Rs.{p['buy']} Profit Rs.{p['profit']}")
            st.divider()

elif menu == "2. DARAZ STORE - CLIENT DEKHEGA":
    st.title("MEHAR MART STORE - Client View - No Profit")
    if not st.session_state.products:
        st.warning("Koi Product Nahi")
    else:
        # Category Filter - Client ke liye
        all_cats = ["All"] + list(set([x['category'] for x in st.session_state.products]))
        sel_cat = st.selectbox("Category Filter Karo", all_cats)
        
        for p in st.session_state.products:
            if sel_cat!="All" and p['category']!=sel_cat: continue
            col1,col2 = st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name'])
                st.caption(f"{p['category']} | {p['badge']} | {p['delivery']} | {p['brand']} - {p['weight']}")
                st.markdown(f"### ~~Rs.{p['sell']}~~  Rs.{p['final']}  ({p['discount']}% OFF)")
                if p['highlights']: st.success(p['highlights'])
                if p['description']: st.write(p['description'])
            st.divider()

else:
    st.title("Money System - Sirf Aap Dekho Ge")
    if st.session_state.products:
        df = pd.DataFrame([{k:v for k,v in x.items() if k!='image_bytes'} for x in st.session_state.products])
        st.dataframe(df[["category","name","buy","final","profit","stock"]], use_container_width=True)
        # Category wise profit
        st.bar_chart(df.groupby("category")["profit"].sum())
