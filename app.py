# MEHAR MART V33 ULTIMATE - WHATSAPP ORDER + QR - FULL CODE - FINAL
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
import io, os
import urllib.parse

st.set_page_config(page_title="MEHAR MART V33", layout="wide")

if 'products' not in st.session_state: st.session_state.products = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# WHATSAPP NUMBER - AAPKA NUMBER - 03452352112 - 92 LAGA KE
WA_NUMBER = "923452352112"  # 0 hata ke 92 lagaya - number show nahi hoga customer ko

PASS_FILE = "admin_password.txt"
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return "mehar123"
def set_password(new_pass):
    with open(PASS_FILE, "w") as f: f.write(new_pass)

# LOGIN - AUTO
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

# 1. PRODUCT SYSTEM
if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - ADMIN ONLY")
    with st.form("product_form", clear_on_submit=False):
        c1,c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Category *", ["PURE HONEY","MASALA","DRY FRUIT","GADGET","ATTA","OTHER","OIL","SHAMPOO","SOAP"])
            name = st.text_input("Product Name *", "", placeholder="Pure Beri Flowers Honey 500gm")
            disc = st.number_input("Discount % - UPAR", 0, 90, 15)
            buy = st.number_input("Kharid Rate - ADMIN ONLY", 0, 100000, 2000)
            sell = st.number_input("Selling Price *", 0, 100000, 3500)
            final_price = int(sell * (1-disc/100)) if disc>0 else sell
            profit = final_price - buy
            st.number_input("Customer Pay Karega - BOX ME", value=final_price, disabled=True)
            st.number_input("💰 Munafa - BOX ME - ADMIN ONLY", value=profit, disabled=True)
            stock = st.number_input("Stock *", 0, 10000, 50)
        with c2:
            brand = st.text_input("Brand", "MEHAR MART")
            weight = st.text_input("Weight", "500gm")
            badge = st.selectbox("Badge", ["BEST SELLER","NEW","LIMITED STOCK","100% PURE","SALE"])
            delivery = st.selectbox("Delivery Option *", ["🚚 Free Delivery - All Pakistan","💵 Cash on Delivery - All Pakistan","🚚 Free Delivery Karachi","💵 Cash on Delivery Karachi","💵 Cash on Delivery - Rs.150 Delivery Charge"])
            expiry = st.date_input("Expiry", datetime.now()+timedelta(days=365))
        highlights = st.text_area("Highlights", "", height=80)
        desc = st.text_area("Full Description", "", height=120)
        specs = st.text_area("Specifications", "", height=80)
        img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])
        st.markdown(f"### 💰 LIVE: Kharid {buy} | Selling {sell} | Disc {disc}% | Customer Pay {final_price} | Munafa {profit}")
        submitted = st.form_submit_button("♾️ LIFETIME SAVE", use_container_width=True)
        if submitted:
            if not name: st.error("Name Likho!")
            else:
                img_bytes = img_file.getvalue() if img_file else None
                st.session_state.products.append({"date":str(datetime.now().date()),"category":cat,"name":name,"brand":brand,"buy":buy,"sell":sell,"discount":disc,"final":final_price,"stock":stock,"weight":weight,"expiry":str(expiry),"delivery":delivery,"badge":badge,"highlights":highlights,"description":desc,"specs":specs,"image_bytes":img_bytes,"profit":profit})
                st.success("Save Ho Gaya!"); st.balloons()
    st.divider()
    st.subheader("✅ Our Products - Admin")
    if st.session_state.products:
        for p in st.session_state.products:
            st.markdown(f"**{p['category']} | {p['name']} | Final Rs.{p['final']} | Buy Rs.{p['buy']} | Profit Rs.{p['profit']}**")
            if p.get('image_bytes'):
                try: st.image(Image.open(io.BytesIO(p['image_bytes'])), width=200)
                except: pass
            st.divider()

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY - ADMIN ONLY")
    if st.session_state.products:
        df=pd.DataFrame([{k:v for k,v in p.items() if k!='image_bytes'} for p in st.session_state.products])
        st.dataframe(df[["date","category","name","stock","expiry","final","buy","profit"]], use_container_width=True)
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
    st.header("4. MONEY SYSTEM - PRIVATE")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("TOTAL MUNAFA - SIRF AAP", f"Rs. {df['profit'].sum()}")

elif menu == "5. CLIENT SYSTEM - EXCEL":
    st.header("5. CLIENT SYSTEM - EXCEL - ADMIN ONLY")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.download_button("📥 EXCEL", df.to_csv(index=False).encode('utf-8'), "clients.csv", "text/csv")

# 6. DARAZ STORE - CUSTOMER ORDER VIA WHATSAPP + QR - NUMBER SHOW NAHI HOGA
elif menu == "6. DARAZ STORE":
    if st.session_state.is_admin:
        st.header("6. DARAZ STORE - Preview")
    else:
        st.header("🛒 MEHAR MART OFFICIAL STORE")
        st.markdown("**🔥 Best Price | 🚚 Free Delivery | 💵 Cash on Delivery**")

    # WHATSAPP QR - SIDEBAR ME BHI - NUMBER SHOW NAHI HOGA
    st.sidebar.divider()
    st.sidebar.subheader("💬 WhatsApp Order QR")
    st.sidebar.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://wa.me/923452352112", caption="Scan Karo - Order Karo - Number Show Nahi Hoga")
    st.sidebar.link_button("💬 WhatsApp Pe Baat Karo", f"https://wa.me/{WA_NUMBER}", use_container_width=True)

    if not st.session_state.products:
        st.warning("Products add ho rahe hain")
        # QR yahan bhi customer ko dikhega
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://wa.me/923452352112", width=250, caption="WhatsApp QR - Scan to Order")
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
                st.markdown(f"### ~~Rs.{p['sell']}~~ Rs.{p['final']} ({p['discount']}% OFF)")
                st.write(f"Customer Pay: Rs.{p['final']} Only")
                if p.get('highlights'): st.success(p['highlights'])
                if p.get('description'): st.write(p['description'])

                # WHATSAPP ORDER BUTTON - NUMBER SHOW NAHI HOGA - DIRECT ACTION
                msg = f"Salam MEHAR MART! Mujhe order karna hai:\n\nProduct: {p['name']}\nPrice: Rs.{p['final']} ({p['discount']}% OFF)\nDelivery: {p['delivery']}\n\nPlease order confirm karein."
                encoded_msg = urllib.parse.quote(msg)
                wa_link_product = f"https://wa.me/{WA_NUMBER}?text={encoded_msg}"
                
                st.link_button(f"💬 WhatsApp Pe Order Karo - {p['name']}", wa_link_product, use_container_width=True)
                st.caption("QR Scan Karke Bhi Order Kar Sakte Hain - Number Show Nahi Hoga")

            st.divider()
        
        st.divider()
        st.subheader("💬 WhatsApp QR Se Order Karo - Easy")
        c1,c2=st.columns([1,2])
        with c1:
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://wa.me/923452352112", caption="Scan Karo - WhatsApp Khulega")
        with c2:
            st.markdown("### Kaise Order Karein?")
            st.markdown("1. **Order Button Dabao** - WhatsApp Khulega\n2. **QR Scan Karo** - WhatsApp Khulega\n3. Number show nahi hoga - Sirf Action Button\n4. Direct MEHAR MART se baat")
            st.link_button("💬 ABHI WHATSAPP PE ORDER KARO - CLICK", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote('Salam MEHAR MART! Order karna hai')}", use_container_width=True)

else:
    st.header("7. MARKETING KING")
    if st.session_state.products:
        pname=st.selectbox("Product", [x['name'] for x in st.session_state.products])
        prod=[x for x in st.session_state.products if x['name']==pname][0]
        wa=f"🍯 *{prod['name']}* - Rs.{prod['final']} (was {prod['sell']})"
        st.text_area("WhatsApp Caption", wa, height=200)
