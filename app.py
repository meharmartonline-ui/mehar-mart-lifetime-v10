# MEHAR MART V17 - PROFIT LIVE + PHOTO FIX - FINAL SOCH KE
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V17 PROFIT LIVE", layout="wide")
st.title("MEHAR MART V17 - PROFIT LIVE FIX")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []

menu = st.sidebar.radio("MENU - FINAL 7", [
    "1. PRODUCT SYSTEM", 
    "2. STOCK & EXPIRY", 
    "3. SALES & ORDERS", 
    "4. MONEY SYSTEM", 
    "5. CLIENT SYSTEM - EXCEL", 
    "6. DARAZ STORE",
    "7. MARKETING KING"
])

# 1. PRODUCT - NO FORM - LIVE PROFIT
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Live Profit Wala")
    
    c1,c2 = st.columns(2)
    with c1:
        cat = st.selectbox("Category", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER"])
        name = st.text_input("Product Name *", "", placeholder="PURE HONEY - Beri Flowers honey")
        buy = st.number_input("Kharid Rate *", 0, 100000, 2000, step=100)
        sell = st.number_input("Bechne Rate *", 0, 100000, 2500, step=100)
        disc = st.number_input("Discount %", 0, 100, 15)
        stock = st.number_input("Stock *", 0, 10000, 50)
    with c2:
        brand = st.text_input("Brand", "MEHAR MART")
        weight = st.text_input("Weight", "500gm")
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
        delivery = st.text_input("Delivery", "Free Delivery Karachi")
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
    
    highlights = st.text_area("Highlights (Khali Hai)", "", placeholder="100% Pure\nNo Sugar", height=80)
    desc = st.text_area("Full Description (Khali Hai)", "", placeholder="Full detail likho...", height=120)
    specs = st.text_area("Specifications (Khali Hai)", "", placeholder="Weight: 500gm", height=80)
    img_file = st.file_uploader("Photo Upload Karo", type=["jpg","png","jpeg"])

    # *** PROFIT LIVE FIX - HAMESHA SHOW HOGA ***
    final_price = int(sell * (1-disc/100)) if disc>0 else sell
    profit_one = sell - buy
    profit_after_disc = final_price - buy
    
    st.divider()
    col1,col2,col3,col4 = st.columns(4)
    with col1: st.metric("Kharid", f"Rs.{buy}")
    with col2: st.metric("Bechna", f"Rs.{sell}")
    with col3: st.metric("Customer Pay", f"Rs.{final_price}", delta=f"-{disc}%")
    with col4: st.metric("💰 AAPKA MUNAFA", f"Rs.{profit_after_disc}", delta=f"Per Piece")
    
    if profit_one > 0:
        st.success(f"✅ MASHALLAH! Is Product Pe Aapka Munafa: Rs.{profit_after_disc} Per Piece | Discount Ke Baad Bhi Rs.{profit_after_disc} Profit Hai!")
    elif buy==0 or sell==0:
        st.warning("⚠️ Bhai Kharid aur Bechne Rate Likho - Profit Khud Show Hoga Jaise Upar Hai")
    else:
        st.error("❌ Loss Ho Raha Hai Bhai! Bechne Rate Badhao")

    if st.button("♾️ LIFETIME SAVE - PHOTO KE SATH"):
        if not name:
            st.error("Product Name Likho Bhai!")
        else:
            img_bytes = img_file.getvalue() if img_file else None
            st.session_state.products.append({
                "date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,
                "buy":buy,"sell":sell,"discount":disc,"final":final_price,"stock":stock,
                "weight":weight,"expiry":str(expiry),"delivery":delivery,"badge":badge,
                "highlights":highlights,"description":desc,"specs":specs,
                "image_bytes":img_bytes,"profit":profit_after_disc,"profit_one":profit_one
            })
            st.success(f"✅ {name} Save Ho Gaya! Munafa Rs.{profit_after_disc}"); st.balloons()

    # LIST - JAISA AAPKE PEHLE SCREENSHOT ME THA
    st.divider()
    st.subheader("Aapke Sare Products - Aise Show Honge Jaise Pehle Hote The")
    if not st.session_state.products:
        st.info("Abhi koi product nahi")
    else:
        for p in st.session_state.products:
            st.markdown(f"### ✅ {p['name']}")
            c1,c2 = st.columns([1,3])
            with c1:
                if p.get('image_bytes'):
                    st.image(Image.open(io.BytesIO(p['image_bytes'])), width=250)
            with c2:
                st.write(f"Category: {p['category']} | Stock: {p['stock']} | Rs.{p['final']}")
                st.markdown(f"**Brand: {p['brand']} | {p['weight']} | {p['delivery']}**")
                st.success(f"💰 Munafa: Rs.{p['profit']} per piece | Kharid: Rs.{p['buy']} | Bechna: Rs.{p['final']}")
                st.write(f"📝 {p['description']}")
            st.divider()

# 2. STOCK
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["name","stock","expiry","buy","final","profit"]], use_container_width=True)

# 3. SALES
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS - Profit Show")
    with st.container():
        cname=st.text_input("Customer Name", "", placeholder="Ali")
        city=st.text_input("City", "", placeholder="Karachi")
        if st.session_state.products:
            pname=st.selectbox("Product", [p['name'] for p in st.session_state.products])
            qty=st.number_input("Qty",1,100,1)
            if st.button("MASHALLAH SALE KARO"):
                for p in st.session_state.products:
                    if p['name']==pname:
                        profit_total = (p['final'] - p['buy']) * qty
                        p['stock'] -= qty
                        st.session_state.sales.append({"date":str(datetime.now().date()),"customer":cname,"city":city,"product":pname,"qty":qty,"buy":p['buy'],"sell":p['final'],"total":p['final']*qty,"profit":profit_total})
                        st.success(f"✅ Sale! Total: Rs.{p['final']*qty} | 💰 PROFIT: Rs.{profit_total}"); st.balloons()
        else: st.warning("Pehle product add karo")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA", f"Rs. {df['profit'].sum()}")

# 4. MONEY
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - Profit Fix")
    if not st.session_state.sales: st.warning("No sale yet")
    else:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("Total Sale", f"Rs. {df['total'].sum()}")
        with c2: st.metric("Total Cost", f"Rs. {(df['buy']*df['qty']).sum()}")
        with c3: st.metric("TOTAL MUNAFA", f"Rs. {df['profit'].sum()}", delta="MASHALLAH")

# 5. CLIENT EXCEL
elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL")
    if not st.session_state.sales: st.warning("Pehle Sale Karo")
    else:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 SALES EXCEL DOWNLOAD", df.to_csv(index=False).encode('utf-8'), "sales.csv", "text/csv")

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    st.header("6. DARAZ STORE - Photo Fix")
    if not st.session_state.products: st.warning("No Product")
    else:
        for p in st.session_state.products:
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name']); st.write(f"Stock {p['stock']} | {p['weight']}"); st.markdown(f"~~Rs.{p['sell']}~~ -> **Rs.{p['final']}**"); st.success(f"💰 Munafa Rs.{p['profit']}")
            st.divider()

# 7. MARKETING
elif menu == "7. MARKETING KING":
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']} (was {prod['sell']})\n{prod['description']}\nMunafa aapka Rs.{prod['profit']}"
        st.text_area("WhatsApp Caption", wa, height=200)
