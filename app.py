# MEHAR MART V18 - PRICE KE SATH PROFIT BOX - FINAL
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V18", layout="wide")
st.title("MEHAR MART V18 - PRICE KE SATH PROFIT BOX")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []

menu = st.sidebar.radio("MENU - FINAL", [
    "1. PRODUCT SYSTEM", "2. STOCK & EXPIRY", "3. SALES & ORDERS", 
    "4. MONEY SYSTEM", "5. CLIENT SYSTEM - EXCEL", "6. DARAZ STORE", "7. MARKETING KING"
])

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM")
    
    # --- PRICE INPUTS + PROFIT BOX EK SATH ---
    col_a, col_b = st.columns(2)
    with col_a:
        cat = st.selectbox("Category", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER"])
        name = st.text_input("Product Name *", "", placeholder="PURE HONEY - Beri Flowers honey")
        buy = st.number_input("Kharid Rate *", 0, 100000, 2000, step=100)
        sell = st.number_input("Bechne Rate *", 0, 100000, 2500, step=100)
        disc = st.number_input("Discount %", 0, 100, 15)
        stock = st.number_input("Stock *", 0, 10000, 50)
        
        # *** YAHAN PROFIT BOX - PRICE KE SATH HI ***
        final_price = int(sell * (1-disc/100)) if disc>0 else sell
        profit = final_price - buy
        
        st.markdown("---")
        st.markdown("### 💰 LIVE HISAAB - Price Ke Sath")
        m1,m2,m3,m4 = st.columns(4)
        with m1: st.metric("Kharid", f"Rs.{buy}")
        with m2: st.metric("Bechna", f"Rs.{sell}")
        with m3: st.metric("Customer Pay", f"Rs.{final_price}", f"-{disc}%")
        with m4: st.metric("💰 MUNAFA", f"Rs.{profit}", "Per Piece")
        
        if profit>0:
            st.success(f"✅ MASHALLAH! Profit Rs.{profit} | Customer Pay Rs.{final_price}")
        elif buy==0 or sell==0:
            st.warning("Kharid/Bechna Likho - Profit Yahi Ayega")
        else:
            st.error(f"Loss Rs.{profit} - Rate Badhao")

    with col_b:
        brand = st.text_input("Brand", "MEHAR MART")
        weight = st.text_input("Weight", "500gm")
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
        delivery = st.text_input("Delivery", "Free Delivery Karachi")
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
        highlights = st.text_area("Highlights (Khali Hai)", "", placeholder="100% Pure\nNo Sugar", height=80)
        desc = st.text_area("Full Description (Khali Hai)", "", placeholder="Full detail...", height=120)
        specs = st.text_area("Specifications (Khali Hai)", "", placeholder="Weight: 500gm", height=80)
        img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    if st.button("♾️ LIFETIME SAVE - PHOTO KE SATH", use_container_width=True):
        if not name: st.error("Name Likho Bhai!")
        else:
            img_bytes = img_file.getvalue() if img_file else None
            st.session_state.products.append({
                "date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,
                "buy":buy,"sell":sell,"discount":disc,"final":final_price,"stock":stock,
                "weight":weight,"expiry":str(expiry),"delivery":delivery,"badge":badge,
                "highlights":highlights,"description":desc,"specs":specs,
                "image_bytes":img_bytes,"profit":profit
            })
            st.success(f"{name} Save! Munafa Rs.{profit}"); st.balloons()

    st.divider()
    st.subheader("Saved Products - Photo Ke Sath")
    if not st.session_state.products: st.info("Koi product nahi")
    else:
        for p in st.session_state.products:
            st.write(f"✅ {p['name']} | Rs.{p['final']} | Profit Rs.{p['profit']}")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=200)
                except: pass
            st.divider()

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["name","stock","expiry","buy","final","profit"]], use_container_width=True)

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    cname=st.text_input("Customer Name", "", placeholder="Ali")
    city=st.text_input("City", "", placeholder="Karachi")
    if st.session_state.products:
        pname=st.selectbox("Product", [p['name'] for p in st.session_state.products])
        qty=st.number_input("Qty",1,100,1)
        if st.button("MASHALLAH SALE KARO"):
            for p in st.session_state.products:
                if p['name']==pname:
                    profit_total=(p['final']-p['buy'])*qty
                    p['stock']-=qty
                    st.session_state.sales.append({"date":str(datetime.now().date()),"customer":cname,"city":city,"product":pname,"qty":qty,"total":p['final']*qty,"profit":profit_total})
                    st.success(f"Sale! Profit Rs.{profit_total}"); st.balloons()
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA", f"Rs. {df['profit'].sum()}", delta="MASHALLAH")

elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 EXCEL DOWNLOAD", df.to_csv(index=False).encode('utf-8'), "sales.csv", "text/csv")

elif menu == "6. DARAZ STORE":
    st.header("6. DARAZ STORE")
    if st.session_state.products:
        for p in st.session_state.products:
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2: st.subheader(p['name']); st.write(f"Rs.{p['final']} | Profit Rs.{p['profit']}"); st.write(p['description'])
            st.divider()

elif menu == "7. MARKETING KING":
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']}\nProfit aapka Rs.{prod['profit']}\n{prod['description']}"
        st.text_area("WhatsApp Caption", wa, height=200)
