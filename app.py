# MEHAR MART V35 CHECKED - FINAL - KUCH MISS NAHI - DYNAMIC WHATSAPP
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io, os
import urllib.parse

st.set_page_config(page_title="MEHAR MART V35 CHECKED", layout="wide")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

WA_NUMBER = "923452352112"  # 03452352112
PASS_FILE = "admin_password.txt"
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return "mehar123"
def set_password(new_pass):
    with open(PASS_FILE, "w") as f: f.write(new_pass)

st.sidebar.title("🔐 MEHAR MART LOGIN")
current_pass = get_password()
pwd_input = st.sidebar.text_input("Admin Password", type="password", placeholder="mehar123")

if pwd_input == current_pass and pwd_input != "":
    st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    if st.sidebar.button("Logout"):
        st.session_state.is_admin = False
        st.rerun()
    st.sidebar.divider()
    st.sidebar.subheader("🔑 Password Reset")
    with st.sidebar.expander("Password Change"):
        old = st.text_input("Purana", type="password", key="old")
        new = st.text_input("Naya", type="password", key="new")
        confirm = st.text_input("Confirm", type="password", key="confirm")
        if st.button("Change Karo"):
            if old != current_pass: st.sidebar.error("Purana ghalat!")
            elif new == "": st.sidebar.error("Naya khali!")
            elif new != confirm: st.sidebar.error("Match nahi!")
            else:
                set_password(new)
                st.sidebar.success(f"Ho gaya! Naya: {new}")
                st.balloons()
                st.rerun()
    menu = st.sidebar.radio("7 MENU", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM - EXCEL","6. DARAZ STORE","7. MARKETING KING"])
else:
    if pwd_input != "": st.sidebar.error("Ghalat password")
    else: st.sidebar.warning("👤 CUSTOMER VIEW")
    menu = "6. DARAZ STORE"

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - ADMIN ONLY")
    with st.form("product_form", clear_on_submit=False):
        c1,c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Category *", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER","OIL","SHAMPOO","SOAP","RICE","CREAM"])
            name = st.text_input("Product Name *", "", placeholder="Pure Beri Flowers Honey 500gm - 100% Pure")
            disc = st.number_input("Discount % - UPAR HAI", 0, 90, 15)
            buy = st.number_input("Kharid Rate - ADMIN ONLY", 0, 100000, 2000)
            sell = st.number_input("Selling Price *", 0, 100000, 3500)
            final_price = int(sell * (1-disc/100)) if disc>0 else sell
            profit = final_price - buy
            st.number_input("Customer Pay Karega - BOX ME - Naya", value=final_price, disabled=True)
            st.number_input("💰 Aapka Munafa - BOX ME - Naya", value=profit, disabled=True)
            stock = st.number_input("Stock *", 0, 10000, 50)
        with c2:
            brand = st.text_input("Brand", "MEHAR MART")
            weight = st.text_input("Weight", "500gm")
            badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE","OFFER"])
            delivery = st.selectbox("Delivery Option *", ["🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi","💵 Cash on Delivery Karachi","💵 Cash on Delivery - Rs.150 Delivery Charge","🚚 Free Delivery Lahore / Karachi"])
            expiry = st.date_input("Expiry Date", datetime.now()+timedelta(days=365))
        highlights = st.text_area("Highlights", "", placeholder="100% Pure\nNo Sugar", height=90)
        desc = st.text_area("Full Description - Client Dekhega", "", placeholder="Pure honey...", height=120)
        specs = st.text_area("Specifications", "", placeholder="Weight: 500gm", height=90)
        img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])
        st.divider()
        st.markdown(f"### 💰 LIVE HISAAB - AAKHIR ME: Kharid Rs.{buy} | Selling Rs.{sell} | Disc {disc}% | Customer Pay Rs.{final_price} | Munafa Rs.{profit}")
        submitted = st.form_submit_button("♾️ LIFETIME SAVE - Click", use_container_width=True)
        if submitted:
            if not name: st.error("Name Likho Bhai!")
            else:
                img_bytes = img_file.getvalue() if img_file else None
                st.session_state.products.append({"date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,"buy":buy,"sell":sell,"discount":disc,"final":final_price,"stock":stock,"weight":weight,"expiry":str(expiry),"delivery":delivery,"badge":badge,"highlights":highlights,"description":desc,"specs":specs,"image_bytes":img_bytes,"profit":profit})
                st.success(f"Save Ho Gaya! {name} | Customer Pay {final_price} | Munafa {profit}"); st.balloons()
    st.divider()
    st.subheader("✅ Our Products - Admin View - Full Details")
    if st.session_state.products:
        for p in st.session_state.products:
            st.markdown(f"**{p['category']} | {p['name']} | Final Rs.{p['final']} (was {p['sell']}) {p['discount']}% OFF | {p['delivery']}**")
            st.caption(f"ADMIN: Buy Rs.{p['buy']} Profit Rs.{p['profit']} - Customer ko ye nahi dikhega")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=250)
                except: pass
            if p.get('highlights'): st.info(p['highlights'])
            if p.get('description'): st.write(p['description'])
            if p.get('specs'): st.caption(p['specs'])
            st.divider()

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - ADMIN ONLY")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["date","category","name","stock","expiry","final","buy","profit","brand"]], use_container_width=True)
        st.bar_chart(df.groupby("category")["stock"].sum())

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS - ADMIN ONLY")
    with st.form("sale_form"):
        cname=st.text_input("Customer Name"); city=st.text_input("City")
        if st.session_state.products:
            pname=st.selectbox("Product", [p['name'] for p in st.session_state.products])
            qty=st.number_input("Qty",1,100,1)
            s=st.form_submit_button("Sale Karo")
            if s:
                for p in st.session_state.products:
                    if p['name']==pname:
                        p['stock']-=qty
                        st.session_state.sales.append({"customer":cname,"city":city,"product":pname,"qty":qty,"total":p['final']*qty,"profit":(p['final']-p['buy'])*qty})
                        st.success("Sale!")

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - PRIVATE - SIRF AAP")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA - SIRF AAP", f"Rs. {df['profit'].sum()}")

elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.download_button("📥 EXCEL", df.to_csv(index=False).encode('utf-8'), "clients.csv", "text/csv")

elif menu == "6. DARAZ STORE":
    if st.session_state.is_admin: st.header("6. DARAZ STORE - Preview")
    else: st.header("🛒 MEHAR MART OFFICIAL STORE")
    
    if not st.session_state.products:
        st.warning("Products add ho rahe hain")
    else:
        sel = st.selectbox("Category Filter", ["All"] + list(set([x['category'] for x in st.session_state.products])))
        for p in st.session_state.products:
            if sel!="All" and p['category']!=sel: continue
            col1,col2=st.columns([1,2])
            with col1:
                if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
            with col2:
                st.subheader(p['name'])
                st.caption(f"{p['category']} | {p['badge']} | {p['brand']} - {p['weight']} | {p['delivery']}")
                st.markdown(f"### ~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF)")
                if p.get('highlights'): st.success(p['highlights'])
                if p.get('description'): st.write(p['description'])
                if p.get('specs'): st.caption(p['specs'])

                # DYNAMIC SYSTEM - JO PRODUCT HOGA USI KA MESSAGE JAYEGA
                dynamic_msg = f"Salam MEHAR MART! Mujhe order karna hai:\n\nProduct: {p['name']}\nCategory: {p['category']}\nBrand: {p['brand']}\nWeight: {p['weight']}\nPrice: Rs.{p['final']} (was Rs.{p['sell']}) {p['discount']}% OFF\nDelivery: {p['delivery']}\n\nPlease order confirm karein."
                wa_link_dynamic = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(dynamic_msg)}"
                st.link_button(f"💬 WhatsApp Pe Order Karo - {p['name'][:35]}", wa_link_dynamic, use_container_width=True)

            st.divider()

else:
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']}"
        st.text_area("Caption", wa, height=200)
