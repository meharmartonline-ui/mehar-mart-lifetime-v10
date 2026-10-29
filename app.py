# MEHAR MART V24 - FINAL - 7 MENU WAPAS + ALL FIX
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V24 FINAL", layout="wide")
st.title("MEHAR MART V24 - FINAL - SAB KUCH WAPAS")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []

menu = st.sidebar.radio("MEHAR MART MENU - 7 MENU", [
    "1. PRODUCT SYSTEM", "2. STOCK & EXPIRY", "3. SALES & ORDERS", 
    "4. MONEY SYSTEM", "5. CLIENT SYSTEM - EXCEL", "6. DARAZ STORE", "7. MARKETING KING"
])

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - Sab Wapas")
    c1,c2 = st.columns(2)
    with c1:
        cat = st.selectbox("Category *", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER","OIL"])
        name = st.text_input("Product Name *", "", placeholder="Pure Honey 500gm - MEHAR MART")
        buy = st.number_input("Kharid Rate (Sirf Aap Dekho Ge)", 0, 100000, 1500, step=100)
        sell = st.number_input("Selling Price * (Client Dekhega)", 0, 100000, 2500, step=100)
        disc = st.number_input("Discount %", 0, 90, 15)
        stock = st.number_input("Stock *", 0, 10000, 50)
    with c2:
        brand = st.text_input("Brand", "MEHAR MART")
        weight = st.text_input("Weight", "500gm")
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
        delivery = st.selectbox("Delivery Option * - 10 Options", [
            "🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi",
            "💵 Cash on Delivery Karachi","🚚 Free Delivery - Karachi + Hyderabad",
            "💵 Cash on Delivery + Free Delivery Karachi","🚚 Free Delivery on Orders Above Rs.2000",
            "💵 Cash on Delivery - Rs.150 Delivery Charge","🚚 Free Delivery Lahore / Karachi / Islamabad",
            "💵 Cash on Delivery + Free Return"
        ])
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
    
    highlights = st.text_area("Highlights (Khali Hai)", "", placeholder="100% Pure\nNo Sugar\nLab Tested", height=80)
    desc = st.text_area("Full Description (Khali Hai)", "", placeholder="Full detail jo client dekhega...", height=120)
    specs = st.text_area("Specifications (Khali Hai)", "", placeholder="Weight: 500gm\nPurity: 100%", height=80)
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    # PROFIT BOX - LAST ME - JAISA 17 ME THA - BHAI KI DEMAND
    final_price = int(sell * (1-disc/100)) if disc>0 else sell
    profit = final_price - buy
    st.divider()
    st.markdown("### 💰 LIVE HISAAB - LAST ME (Sirf Aap Ke Liye)")
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.metric("Kharid", f"Rs.{buy}")
    with m2: st.metric("Bechna", f"Rs.{sell}")
    with m3: st.metric("Customer Pay", f"Rs.{final_price}", f"-{disc}%")
    with m4: st.metric("💰 MUNAFA", f"Rs.{profit}", "Per Piece")
    if profit>0: st.success(f"✅ MASHALLAH! Profit Rs.{profit} - Client ko nahi dikhega")

    if st.button("♾️ LIFETIME SAVE", use_container_width=True):
        if not name: st.error("Name Likho Bhai!")
        else:
            img_bytes = img_file.getvalue() if img_file else None
            st.session_state.products.append({
                "date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,"buy":buy,"sell":sell,
                "discount":disc,"final":final_price,"stock":stock,"weight":weight,"expiry":str(expiry),
                "delivery":delivery,"badge":badge,"highlights":highlights,"description":desc,"specs":specs,
                "image_bytes":img_bytes,"profit":profit
            })
            st.success(f"{name} Save! Category: {cat}"); st.balloons()

    st.divider()
    st.subheader("Saved Products - Client Price Dikhega, Profit Nahi")
    if st.session_state.products:
        for p in st.session_state.products:
            st.markdown(f"### ✅ {p['category']} | {p['name']} | Price Rs.{p['final']} (was Rs.{p['sell']}) | {p['delivery']}")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=250)
                except: pass
            if p.get('highlights'): st.info(f"Highlights: {p['highlights']}")
            if p.get('description'): st.write(f"Description: {p['description']}")
            if p.get('specs'): st.caption(f"Specs: {p['specs']}")
            with st.expander("🔒 Private Profit Dekho (Sirf Aap)"): st.write(f"Buy Rs.{p['buy']} | Profit Rs.{p['profit']}")
            st.divider()

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - Category Ke Sath")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["category","name","stock","expiry","final","profit"]], use_container_width=True)

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
                    st.session_state.sales.append({"date":str(datetime.now().date()),"customer":cname,"city":city,"category":p['category'],"product":pname,"qty":qty,"total":p['final']*qty,"profit":profit_total,"delivery":p['delivery']})
                    st.success(f"Sale! Profit Rs.{profit_total}"); st.balloons()
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - Aapka Private Munafa")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA", f"Rs. {df['profit'].sum()}", delta="MASHALLAH - Private")

elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 EXCEL DOWNLOAD", df.to_csv(index=False).encode('utf-8'), "clients.csv", "text/csv")

elif menu == "6. DARAZ STORE":
    st.header("6. DARAZ STORE - Client Dekhega - No Profit")
    if st.session_state.products:
        cats = ["All"] + list(set([x['category'] for x in st.session_state.products]))
        sel = st.selectbox("Category Filter", cats)
        for p in st.session_state.products:
            if sel!="All" and p['category']!=sel: continue
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name'])
                st.caption(f"{p['category']} | {p['badge']} | {p['delivery']} | {p['brand']} - {p['weight']}")
                st.markdown(f"~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF)")
                if p.get('highlights'): st.success(p['highlights'])
                if p.get('description'): st.write(p['description'])
            st.divider()

elif menu == "7. MARKETING KING":
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - {prod['category']}\nPrice Rs.{prod['final']} (was {prod['sell']})\n{prod['delivery']}\n{prod['description']}\n\nOrder Now - MEHAR MART"
        st.text_area("WhatsApp Caption - Client Ko Bhejo - No Profit", wa, height=200)
        st.download_button("Copy Text", wa, file_name="caption.txt")
