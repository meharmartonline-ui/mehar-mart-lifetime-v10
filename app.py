import streamlit as st, pandas as pd, io
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont
import json

st.set_page_config(page_title="MEHAR MART LIFETIME", page_icon="♾️", layout="wide")
st.markdown("<h1 style='text-align:center'>♾️ MEHAR MART - LIFETIME SYSTEM V10</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Ek Baar Banao, Lifetime Chalao - Bhai ka Wada!</p>", unsafe_allow_html=True)

if 'products' not in st.session_state: st.session_state.products = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'expenses' not in st.session_state: st.session_state.expenses = []

# LIFETIME SIDEBAR
st.sidebar.title("♾️ LIFETIME SYSTEMS")
system = st.sidebar.radio("System Select Karo:", ["1. PRODUCT SYSTEM", "2. STOCK & EXPIRY", "3. SALES & ORDERS", "4. MONEY SYSTEM", "5. CLIENT SYSTEM"])

ALL_CATS = ["Honey 🍯", "Masala 🌶️", "Dry Fruits", "Gadgets 🍳", "Home Decor", "Beauty", "Clothing", "Custom"]

# SYSTEM 1: PRODUCT
if system == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT BANANA SYSTEM - Lifetime")
    c1,c2 = st.columns(2)
    with c1:
        title = st.text_input("Product Name", "Sidr Honey 500g")
        cat = st.selectbox("Category", ALL_CATS)
        buy = st.number_input("Kharid Rate (Rs)", 1000)
        sell = st.number_input("Bechne Rate (Rs)", 1999)
        profit = sell - buy
        st.metric("Profit / Piece", f"Rs. {profit}", f"{int(profit/buy*100)}%")
        mfg = st.date_input("MFG", date.today())
        exp = st.date_input("Expire", date.today()+timedelta(days=365))
        sku = st.text_input("SKU", f"MM-{len(st.session_state.products)+1:03d}")
        img = st.file_uploader("Image", type=['jpg','png','jpeg'])
    with c2:
        if img:
            im = Image.open(img).convert("RGB")
            st.image(im, use_column_width=True)
            if st.button("♾️ LIFETIME SAVE"):
                st.session_state.products.append({
                    "SKU": sku, "Title": title, "Cat": cat, "Buy": buy, "Sell": sell, "Profit": profit,
                    "MFG": str(mfg), "Expire": str(exp), "DaysLeft": (exp-date.today()).days,
                    "Stock": 50 # default stock
                })
                st.success("Lifetime me Save Ho Gaya Bhai!")

# SYSTEM 2: STOCK
elif system == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY SYSTEM - Auto Alert")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        st.dataframe(df, use_column_width=True)
        # Alerts
        expiring = df[df['DaysLeft'] <= 30]
        if not expiring.empty:
            st.error(f"⚠️ {len(expiring)} Product Expire Hone Wale Hain! Jaldi Becho!")
            st.dataframe(expiring)
        low_stock = df[df['Stock'] <= 10]
        if not low_stock.empty:
            st.warning(f"📦 {len(low_stock)} Products ka Stock Kam Hai!")
    else: st.info("Pehle Product System me Product Add Karo")

# SYSTEM 3: SALES
elif system == "3. SALES & ORDERS":
    st.header("3. SALES SYSTEM - Roz ki Sale")
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)
        prod_list = df['Title'].tolist()
        sel_prod = st.selectbox("Kaunsa Product Becha?", prod_list)
        qty = st.number_input("Kitne Piece?", 1, 100, 1)
        cust_name = st.text_input("Customer Name / WhatsApp")
        city = st.text_input("City", "Karachi")
        
        prod_data = df[df['Title'] == sel_prod].iloc[0]
        total = prod_data['Sell'] * qty
        total_profit = prod_data['Profit'] * qty
        
        st.info(f"Total Bill: Rs. {total} | Profit: Rs. {total_profit}")
        if st.button("💰 Order Confirm"):
            st.session_state.orders.append({
                "Date": str(date.today()), "Customer": cust_name, "Product": sel_prod,
                "Qty": qty, "Total": total, "Profit": total_profit, "City": city
            })
            # stock minus
            idx = df[df['Title'] == sel_prod].index[0]
            st.session_state.products[idx]['Stock'] -= qty
            st.success(f"MASHALLAH Order Done! Rs. {total_profit} Profit!")
    else: st.info("Pehle Product Add Karo")
    
    if st.session_state.orders:
        st.markdown("---")
        st.subheader("Aaj ke Orders")
        st.dataframe(pd.DataFrame(st.session_state.orders), use_column_width=True)

# SYSTEM 4: MONEY
elif system == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - Roz ka Hisaab")
    c1,c2,c3 = st.columns(3)
    if st.session_state.orders:
        odf = pd.DataFrame(st.session_state.orders)
        total_sale = odf['Total'].sum()
        total_profit = odf['Profit'].sum()
        with c1: st.metric("Total Sale", f"Rs. {total_sale}")
        with c2: st.metric("Total Profit", f"Rs. {total_profit}")
        with c3: st.metric("Total Orders", len(odf))
    
    st.markdown("---")
    st.subheader("Kharcha Add Karo")
    exp_title = st.text_input("Kharcha Kis Cheez Ka?", "Daraz Ads")
    exp_amt = st.number_input("Kitna Kharcha?", 0)
    if st.button("Kharcha Save"):
        st.session_state.expenses.append({"Date": str(date.today()), "Title": exp_title, "Amount": exp_amt})
        st.success("Kharcha Save!")
    
    if st.session_state.expenses:
        edf = pd.DataFrame(st.session_state.expenses)
        st.dataframe(edf)
        if st.session_state.orders:
            net_profit = total_profit - edf['Amount'].sum()
            st.metric("NET PROFIT (Sale - Kharcha)", f"Rs. {net_profit}", delta_color="normal")

# SYSTEM 5: CLIENT
elif system == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM - Wapis Lane ka System")
    st.markdown("""
    **Lifetime Client Lane ke 3 Rules:**
    1.  **Har Order ke Baad:** WhatsApp pe "Shukriya Bhai 🍯 Agli Baar 10% Off" bhejo
    2.  **Har Juma ko:** Broadcast - "Juma Mubarak Offer - Aaj Free Delivery Karachi"
    3.  **Har Mahine:** Purane clients ko "Bhai Honey Khatam hua hoga, Naya Stock Aya Hai" message
    """)
    if st.session_state.orders:
        odf = pd.DataFrame(st.session_state.orders)
        clients = odf['Customer'].unique()
        st.success(f"Total Clients Lifetime: {len(clients)}")
        st.dataframe(odf[['Customer','Product','Date']])
        
        # Download Clients Excel
        buf = io.BytesIO()
        odf.to_excel(buf, index=False)
        st.download_button("⬇️ CLIENT LIST DOWNLOAD (Lifetime)", buf.getvalue(), "lifetime_clients.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.markdown("### Auto WhatsApp Message Generator")
    cname = st.text_input("Client Name", "Bhai")
    if st.button("Message Banao"):
        st.code(f"Asalam O Alaikum {cname} Bhai! Mehar Mart se 🍯\nAapka Order ka Shukriya!\nAgli Baar 10% Off Hai Aapke Liye!\n\nOrder Karein: 03XX-XXXXXXX")

st.sidebar.markdown("---")
st.sidebar.info("♾️ YE SYSTEM LIFETIME CHALEGA BHAI!\n\n1 Baar Product Add Karo\nRoz Sale Add Karo\nHisaab Auto Hoga!")

# FINAL DOWNLOAD ALL
if st.session_state.products:
    st.sidebar.markdown("---")
    df_all = pd.DataFrame(st.session_state.products)
    buf_all = io.BytesIO()
    df_all.to_excel(buf_all, index=False)
    st.sidebar.download_button("⬇️ FULL LIFETIME DATA DOWNLOAD", buf_all.getvalue(), "MEHAR_MART_LIFETIME_V10.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
