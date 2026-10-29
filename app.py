# MEHAR MART V46 - SYNTAX FIXED - FINAL WORKING
import streamlit as st
import os
import urllib.parse
import pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V46 FIXED", layout="wide")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

if 'products' not in st.session_state:
    st.session_state.products = []
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'sales' not in st.session_state:
    st.session_state.sales = []
if 'clients' not in st.session_state:
    st.session_state.clients = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def add_visit_once():
    if 'visit_counted' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE, "w") as f:
            f.write(str(v))
        st.session_state.visit_counted = True
        return v
    return get_visits()

total_visits = add_visit_once()

if os.path.exists(ORDER_FILE):
    if 'orders_loaded' not in st.session_state:
        try:
            st.session_state.orders = pd.read_csv(ORDER_FILE).to_dict('records')
            st.session_state.orders_loaded = True
        except:
            pass

def get_password():
    if os.path.exists("admin_password.txt"):
        with open("admin_password.txt", "r") as f:
            return f.read().strip()
    return "mehar123"

st.sidebar.title("ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password")
if pwd == get_password() and pwd != "":
    st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("ADMIN LOGIN")
    st.sidebar.metric("Visits", total_visits)
    menu = st.sidebar.radio("System", ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"])
    st.sidebar.text_input("Store Link", value=STORE_LINK)
else:
    menu = "6. DARAZ STORE"

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM - LIVE PROFIT")
    
    category = st.selectbox("Category", ["PURE HONEY","SIDR HONEY","BERI HONEY","OTHER"])
    product_name = st.text_input("Product Name *", placeholder="PURE HONEY")
    
    col1, col2 = st.columns(2)
    with col1:
        kharid_rate = st.number_input("Kharid Rate *", 0, 100000, 2000)
    with col2:
        bechne_rate = st.number_input("Bechne Rate *", 0, 100000, 2500)
    
    discount_per = st.number_input("Discount %", 0, 90, 15)
    stock = st.number_input("Stock", 0, 10000, 50)
    brand = st.text_input("Brand", value="MEHAR MART")
    
    customer_pay = int(bechne_rate * (1 - discount_per/100))
    profit = customer_pay - kharid_rate
    profit_per = int((profit/kharid_rate*100)) if kharid_rate>0 else 0
    
    st.divider()
    st.subheader("LIVE HISAAB - Box Me")
    
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.info(f"Kharid\nRs.{kharid_rate}")
    with b2:
        st.warning(f"Bechna\nRs.{bechne_rate}")
    with b3:
        st.success(f"Customer Pay\nRs.{customer_pay}")
    with b4:
        st.success(f"PROFIT\nRs.{profit}")
    
    st.divider()
    
    highlights = st.text_area("Highlights (Khali Hai)", placeholder="100% Pure\nNo Sugar", height=100)
    full_desc = st.text_area("Full Description (Khali Hai)", placeholder="Full detail", height=120)
    specs = st.text_area("Specifications (Khali Hai)", placeholder="Weight: 500gm", height=100)
    
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])
    st.caption("200MB per file JPG PNG")
    
    if st.button("SAVE PRODUCT", use_container_width=True, type="primary"):
        if product_name:
            img_bytes = None
            if img_file:
                img_bytes = img_file.getvalue()
            exp_date = datetime.now() + timedelta(days=180)
            new_product = {
                "name": product_name,
                "category": category,
                "sell": bechne_rate,
                "kharid": kharid_rate,
                "discount": discount_per,
                "final": customer_pay,
                "buy": kharid_rate,
                "stock": stock,
                "expiry": exp_date.strftime("%Y-%m-%d"),
                "profit": profit,
                "profit_per": profit_per,
                "brand": brand,
                "highlights": highlights,
                "full_desc": full_desc,
                "specs": specs,
                "image_bytes": img_bytes
            }
            st.session_state.products.append(new_product)
            st.success("Save Ho Gaya!")
            st.balloons()
        else:
            st.error("Product Name likho!")

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if not st.session_state.products:
        st.warning("No products")
    else:
        for p in st.session_state.products:
            st.write(f"{p['name']} - Stock {p['stock']} - Profit Rs.{p.get('profit',0)}")
            st.divider()

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("sale_form"):
        prod_list = [p['name'] for p in st.session_state.products]
        sel_prod = st.selectbox("Product", prod_list) if prod_list else st.text_input("Product")
        qty = st.number_input("Qty", 1, 1000, 1)
        client = st.text_input("Client")
        sub = st.form_submit_button("Sale Add")
        if sub:
            price = 0
            buy = 0
            for p in st.session_state.products:
                if p['name'] == sel_prod:
                    price = p['final']
                    buy = p['buy']
            new_sale = {"date": datetime.now().strftime("%Y-%m-%d"), "product": sel_prod, "qty": qty, "price": price, "total": qty*price, "profit": (price-buy)*qty, "client": client}
            st.session_state.sales.append(new_sale)
            st.success("Added!")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if st.session_state.sales:
        df = pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Profit", f"Rs.{df['profit'].sum()}")

elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    with st.form("client_form"):
        cname = st.text_input("Client Name *")
        cphone = st.text_input("Phone")
        ccity = st.text_input("City")
        cbal = st.number_input("Baqaya", 0, 1000000, 0)
        sub = st.form_submit_button("Save")
        if sub and cname:
            st.session_state.clients.append({"name": cname, "phone": cphone, "city": ccity, "baqaya": cbal})
            st.success("Save!")
    if st.session_state.clients:
        st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)

elif menu == "6. DARAZ STORE":
    st.header("MEHAR MART OFFICIAL STORE")
    st.code(STORE_LINK)
    st.caption(f"{total_visits} visits | Free Delivery")
    
    msg = "MEHAR MART Order: " + STORE_LINK
    wa_share = "https://wa.me/?text=" + urllib.parse.quote(msg)
    st.link_button("WHATSAPP SHARE", wa_share, use_container_width=True)
    st.divider()
    
    if len(st.session_state.cart) > 0:
        total_bill = 0
        for item in st.session_state.cart:
            total_bill = total_bill + item['final']
        st.warning(f"Cart: {len(st.session_state.cart)} items - Rs.{total_bill}")
        for i, item in enumerate(st.session_state.cart):
            ca, cb = st.columns([3,1])
            with ca:
                st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("Remove", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
        cart_text = "Salam! Order:\n"
        for x in st.session_state.cart:
            cart_text = cart_text + x['name'] + " Rs." + str(x['final']) + "\n"
        cart_text = cart_text + f"Total Rs.{total_bill}\n{STORE_LINK}"
        wa_link = "https://wa.me/" + WA_NUMBER + "?text=" + urllib.parse.quote(cart_text)
        st.link_button(f"WHATSAPP ORDER Rs.{total_bill}", wa_link, type="primary", use_container_width=True)
        if st.button("Tracking Me Save Karo", use_container_width=True):
            new_order = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "items": ", ".join([x['name'] for x in st.session_state.cart]), "total": total_bill, "status": "WhatsApp"}
            st.session_state.orders.append(new_order)
            pd.DataFrame(st.session_state.orders).to_csv(ORDER_FILE, index=False)
            st.session_state.cart = []
            st.success("Save!")
            st.rerun()
        st.divider()
    
    if not st.session_state.products:
        st.warning("No products - 1. PRODUCT SYSTEM me add karo")
    else:
        cols = st.columns(2)
        for idx, p in enumerate(st.session_state.products):
            with cols[idx % 2]:
                with st.container(border=True):
                    if p.get('image_bytes'):
                        st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
                    st.markdown(f"**{p['name']}**")
                    st.markdown(f"Rs.{p['final']} ({p['discount']}% OFF)")
                    st.caption(p.get('highlights',''))
                    if st.button("Add to Cart", key=f"add_{idx}", use_container_width=True):
                        st.session_state.cart.append(p)
                        st.rerun()
                    buy_msg = f"Salam! {p['name']} Rs.{p['final']} - {STORE_LINK}"
                    buy_link = "https://wa.me/" + WA_NUMBER + "?text=" + urllib.parse.quote(buy_msg)
                    st.link_button("Buy Now", buy_link, use_container_width=True)

elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    st.metric("Visits", total_visits)
    st.metric("Orders", len(st.session_state.orders))
    if os.path.exists(ORDER_FILE):
        df = pd.read_csv(ORDER_FILE)
        st.dataframe(df, use_container_width=True)
        st.download_button("Excel Download", df.to_csv(index=False), "orders.csv", "text/csv", use_container_width=True)
