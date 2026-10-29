# MEHAR MART V28 - ADMIN LOCK - CUSTOMER KO PROFIT/KHARID KABHI NAHI DIKHEGA
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io

st.set_page_config(page_title="MEHAR MART V28 LOCK", layout="wide")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# ADMIN LOCK SYSTEM
st.sidebar.title("🔐 LOGIN")
password = st.sidebar.text_input("Admin Password Likho", type="password", placeholder="Password")
if st.sidebar.button("Admin Login"):
    if password == "mehar123":  # <-- AAPKA PASSWORD - CHANGE KAR SAKTE HO BHAI
        st.session_state.is_admin = True
        st.sidebar.success("Admin Login Ho Gaya Bhai!")
    else:
        st.sidebar.error("Ghalat Password!")

if st.sidebar.button("Logout - Customer View"):
    st.session_state.is_admin = False
    st.sidebar.info("Customer View Pe Chale Gaye")

# MENU - ADMIN VS CUSTOMER
if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN MODE - Aapko sab dikhega")
    menu = st.sidebar.radio("ADMIN MENU - 7 SYSTEM", [
        "1. PRODUCT SYSTEM", "2. STOCK & EXPIRY", "3. SALES & ORDERS", 
        "4. MONEY SYSTEM", "5. CLIENT SYSTEM - EXCEL", "6. DARAZ STORE", "7. MARKETING KING"
    ])
else:
    st.sidebar.warning("👤 CUSTOMER VIEW - Sirf Store Dikhega - No Profit")
    menu = "6. DARAZ STORE"  # Customer ko sirf Daraz Store dikhega
    st.title("MEHAR MART STORE")
    st.info("👋 Welcome to MEHAR MART - Best Products, Best Price!")

# 1. PRODUCT SYSTEM - SIRF ADMIN DEKHEGA
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - ADMIN ONLY - Customer Nahi Dekhega")
    st.warning("🔒 Ye sirf aap dekh rahe ho - Customer kabhi nahi dekhega")
    c1,c2 = st.columns(2)
    with c1:
        cat = st.selectbox("Category *", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER","OIL"])
        name = st.text_input("Product Name *", "", placeholder="Pure Honey 500gm - MEHAR MART")
        disc = st.number_input("Discount % - Upar", 0, 90, 15)
        buy = st.number_input("Kharid Rate - ADMIN ONLY", 0, 100000, 2000, help="Ye sirf aap dekho ge, customer nahi")
        sell = st.number_input("Selling Price *", 0, 100000, 3500)

        final_price = int(sell * (1-disc/100)) if disc>0 else sell
        profit = final_price - buy

        st.number_input("Customer Pay Karega - BOX ME", value=final_price, disabled=True)
        st.number_input("💰 Aapka Munafa - BOX ME - ADMIN ONLY", value=profit, disabled=True)
        stock = st.number_input("Stock *", 0, 10000, 50)
    with c2:
        brand = st.text_input("Brand", "MEHAR MART")
        weight = st.text_input("Weight", "500gm")
        badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
        delivery = st.selectbox("Delivery Option *", ["🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi","💵 Cash on Delivery Karachi"])
        expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
    
    highlights = st.text_area("Highlights", "", height=80)
    desc = st.text_area("Full Description", "", height=120)
    specs = st.text_area("Specifications", "", height=80)
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])

    if st.button("♾️ LIFETIME SAVE", use_container_width=True):
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
            st.success(f"Save Ho Gaya!"); st.balloons()

    st.divider()
    st.subheader("✅ Our Products - Admin View")
    if st.session_state.products:
        for p in st.session_state.products:
            st.markdown(f"**{p['category']} | {p['name']} | Final Rs.{p['final']} | Buy Rs.{p['buy']} | Profit Rs.{p['profit']}** - ADMIN ONLY")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=250)
                except: pass
            st.divider()

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK - ADMIN ONLY")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["category","name","stock","final","buy","profit"]], use_container_width=True)

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES - ADMIN ONLY")
    cname=st.text_input("Customer Name", "")
    city=st.text_input("City", "")
    if st.session_state.products:
        pname=st.selectbox("Product", [p['name'] for p in st.session_state.products])
        qty=st.number_input("Qty",1,100,1)
        if st.button("MASHALLAH SALE KARO"):
            for p in st.session_state.products:
                if p['name']==pname:
                    p['stock']-=qty
                    st.session_state.sales.append({"customer":cname,"city":city,"product":pname,"qty":qty,"total":p['final']*qty,"profit":(p['final']-p['buy'])*qty})
                    st.success("Sale!")

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - ADMIN ONLY - PROFIT YAHAN HAI")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA - SIRF AAP", f"Rs. {df['profit'].sum()}")

elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. EXCEL - ADMIN ONLY")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.download_button("📥 EXCEL", df.to_csv(index=False).encode('utf-8'), "clients.csv", "text/csv")

# 6. DARAZ STORE - CUSTOMER + ADMIN DONO DEKH SAKTE HAIN - PAR PROFIT/KHARID KABHI NAHI
elif menu == "6. DARAZ STORE":
    if st.session_state.is_admin:
        st.header("6. DARAZ STORE - Customer View Preview - No Profit/Kharid Here")
    else:
        st.header("🛒 MEHAR MART OFFICIAL STORE")
        st.markdown("**Free Delivery | Cash on Delivery | 100% Pure**")
    
    if not st.session_state.products:
        st.warning("Abhi products add ho rahe hain - Jaldi ayenge!")
    else:
        sel = st.selectbox("Category Filter", ["All"] + list(set([x['category'] for x in st.session_state.products])))
        for p in st.session_state.products:
            if sel!="All" and p['category']!=sel: continue
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name'])
                st.caption(f"{p['category']} | {p['badge']} | {p['delivery']}")
                # SIRF FINAL PRICE - NO BUY, NO PROFIT
                st.markdown(f"### ~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF)")
                st.write(f"**Customer Pay: Rs.{p['final']} Only**")
                if p.get('highlights'): st.success(p['highlights'])
                if p.get('description'): st.write(p['description'])
                st.button(f"🛒 Order Now - {p['name']}", key=p['name'])
            st.divider()

else:
    st.header("7. MARKETING KING - ADMIN ONLY")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']} (was {prod['sell']})\n{prod['delivery']}\nOrder Now!"
        st.text_area("WhatsApp Caption - Customer Ko Bhejo - No Profit", wa, height=200)
