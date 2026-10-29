import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="MEHAR MART V10.4 DARAZ", layout="wide")
st.title("MEHAR MART - DARAZ STYLE V10.4")

if 'products' not in st.session_state:
    st.session_state.products = []
if 'sales' not in st.session_state:
    st.session_state.sales = []

menu = st.sidebar.selectbox("MENU", ["1. PRODUCT ADD", "2. DARAZ STYLE STORE"])

if menu == "1. PRODUCT ADD":
    st.header("Naya Product Add Karo - Daraz Style")
    with st.form("daraz_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["PURE HONEY", "MASALA", "DRY FRUIT", "GADGET", "MOBILE", "ATTA", "OTHER"])
            name = st.text_input("Product Title (Daraz Jaisa)", "PURE HONEY - Beri Flowers 🌼🌹 Honey - 1KG")
            buy = st.number_input("Kharid Rate", 0)
            sell = st.number_input("Bechne Rate (Price)", 2500)
            discount = st.number_input("Discount %", 0, 100, 15)
            stock = st.number_input("Stock Qty", 50)
        with col2:
            brand = st.text_input("Brand", "MEHAR MART")
            weight = st.text_input("Weight / Size", "1 KG")
            expiry = st.date_input("Expiry", datetime.now() + timedelta(days=365))
            delivery = st.selectbox("Delivery", ["Free Delivery Karachi", "All Pakistan Delivery", "Cash on Delivery"])
            warranty = st.text_input("Warranty", "100% Pure Guarantee")
        
        st.subheader("Daraz Jaisi Full Details")
        highlights = st.text_area("Highlights (Bullet Points) - 1 line me 1 point", "100% Pure & Natural\nNo Sugar Added\nKohistan Ka Asli Shehad\nEnergy Booster\nBachon Ke Liye Best", height=100)
        description = st.text_area("Full Description (Daraz Jaisi Lambi Detail)", "MEHAR MART ka Khaalis Beri Phool Ka Shehad. Ye shehad Kohistan ki pahadiyon se hasil kiya gaya hai. 100% natural hai, koi milawat nahi.\n\nFayde:\n- Quwwat e mudafiat barhata hai\n- Bachon ki sehat ke liye behtareen\n- Natural energy deta hai\n- Gala kharab me mufeed\n\nWeight 1KG Pure Packing me.", height=150)
        specs = st.text_area("Specifications / What is in Box", "Type: Beri Flowers Honey\nWeight: 1KG\nPacking: Glass Jar\nExpiry: 2 Years\nOrigin: Kohistan\nIn Box: 1x Honey Jar", height=100)
        
        img = st.file_uploader("Product Photo (Daraz Main Image)", type=["jpg","png","jpeg"])
        submit = st.form_submit_button("🛒 DARAZ STYLE SAVE")
        
        if submit:
            path = ""
            if img:
                os.makedirs("images", exist_ok=True)
                path = f"images/{img.name}"
                with open(path, "wb") as f:
                    f.write(img.getbuffer())
            st.session_state.products.append({
                "category":category,"name":name,"brand":brand,"buy":buy,"sell":sell,
                "discount":discount,"stock":stock,"weight":weight,"expiry":str(expiry),
                "delivery":delivery,"warranty":warranty,"highlights":highlights,
                "description":description,"specs":specs,"image":path
            })
            st.success("Daraz Style Product Save Ho Gaya Bhai!")

# DARAZ STYLE DISPLAY
elif menu == "2. DARAZ STYLE STORE":
    st.header("MEHAR MART STORE - Daraz Jaisa")
    if not st.session_state.products:
        st.warning("Abhi koi product nahi Bhai - Pehle Add Karo")
    else:
        for p in st.session_state.products:
            # Daraz Top Section
            col_img, col_detail = st.columns([1, 2])
            with col_img:
                if p['image'] and os.path.exists(p['image']):
                    st.image(p['image'], use_column_width=True)
                else:
                    st.image("https://via.placeholder.com/300?text=MEHAR+MART", use_column_width=True)
            with col_detail:
                st.subheader(p['name'])
                st.caption(f"Brand: {p['brand']} | Category: {p['category']}")
                old_price = int(p['sell'] / (1 - p['discount']/100)) if p['discount']>0 else p['sell']
                if p['discount']>0:
                    st.markdown(f"~~Rs. {old_price}~~  **-{p['discount']}%**")
                st.markdown(f"### Rs. {p['sell']}")
                st.write(f"✅ Stock: {p['stock']} | {p['weight']} | {p['delivery']}")
                st.write(f"🛡️ {p['warranty']}")
                st.button(f"Add to Cart - {p['name']}", key=p['name'])
            
            # Daraz Tabs
            tab1, tab2, tab3 = st.tabs(["Highlights", "Full Description", "Specifications"])
            with tab1:
                st.write("**Product Highlights:**")
                for line in p['highlights'].split('\n'):
                    st.write(f"• {line}")
            with tab2:
                st.write(p['description'])
            with tab3:
                st.code(p['specs'])
            st.divider()
