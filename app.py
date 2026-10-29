# MEHAR MART V40 - FINAL COMPLETE - NOTHING MISS - DARAZ CART + TRACKING
import streamlit as st
import urllib.parse, os, pandas as pd
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="MEHAR MART V40 FINAL", layout="wide")

# ★★★ AAPKA 100% WORKING LINKS ★★★
STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"
SHORT_LINK_TRY = "https://tinyurl.com/meharmart2026" # Aap jab bana loge to ye chalega

if 'products' not in st.session_state: st.session_state.products = []
if 'cart' not in st.session_state: st.session_state.cart = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"

# VISIT COUNTER - FIXED - DOUBLE COUNT NAHI
def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE,"r") as f: return int(f.read().strip())
        except: return 0
    return 0

def add_visit_once():
    # Sirf ek dafa per session count badhega - Reload pe nahi
    if 'visit_counted' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE,"w") as f: f.write(str(v))
        st.session_state.visit_counted = True
        return v
    return get_visits()

total_visits = add_visit_once()

# ORDERS LOAD KARO - RELOAD PE BHI RAHEGA
if os.path.exists(ORDER_FILE) and 'orders_loaded' not in st.session_state:
    try:
        df_old = pd.read_csv(ORDER_FILE)
        st.session_state.orders = df_old.to_dict('records')
        st.session_state.orders_loaded = True
    except:
        st.session_state.orders = []
else:
    if 'orders' not in st.session_state: st.session_state.orders = []

PASS_FILE = "admin_password.txt"
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f: return f.read().strip()
    return "mehar123"

# SIDEBAR LOGIN
st.sidebar.title("🔐 ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
if pwd == get_password() and pwd != "": st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    st.sidebar.metric("👀 Total Visits", total_visits)
    st.sidebar.metric("🛒 Cart Items", len(st.session_state.cart))
    st.sidebar.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.divider()
    st.sidebar.subheader("🔗 Links - Copy Karo")
    st.sidebar.text_input("Store Link:", value=STORE_LINK, key="s1")
    st.sidebar.code(STORE_LINK)
    st.sidebar.link_button("🔗 Store Kholo", STORE_LINK, use_container_width=True)
    menu = st.sidebar.radio("MENU", ["6. DARAZ STORE","1. PRODUCT SYSTEM","3. ORDERS TRACKING"])
else:
    menu = "6. DARAZ STORE"

if menu == "6. DARAZ STORE":
    if st.session_state.is_admin: st.header("6. DARAZ STORE - ADMIN VIEW")
    else: st.header("🛒 MEHAR MART - OFFICIAL STORE")

    # ★★★ SHORT LINK COPY BOX - AAPKI SCREENSHOT WALI JAGAH - WAPAS LAGA DIYA ★★★
    st.success("👇 STORE LINK - COPY KARKE SHARE KARO - 100% WORKING - NO 404")
    colA,colB = st.columns([3,1])
    with colA:
        st.text_input("🔗 Short/Long Link - Click Karke Copy Karo:", value=STORE_LINK, key="main_link")
        st.code(STORE_LINK, language="text")
        st.caption(f"TinyURL try: {SHORT_LINK_TRY} (aap banaoge to chalega)")
    with colB:
        st.link_button("🔗 OPEN STORE", STORE_LINK, use_container_width=True)
        st.link_button("📤 WHATSAPP SHARE", f"https://wa.me/?text={urllib.parse.quote('🍯 MEHAR MART Order Karo: '+STORE_LINK)}", use_container_width=True)
    
    st.caption(f"👀 {total_visits} log ye store dekh chuke hain | 🚚 Free Delivery All Pakistan")
    st.divider()

    # CART TOP BAR - DARAZ JAISA
    cart_count = len(st.session_state.cart)
    c1,c2,c3 = st.columns([2,1,1])
    with c1:
        if cart_count>0: st.warning(f"🛒 Aapke Cart me {cart_count} items hain - Neeche dekho")
    with c2:
        st.metric("CART", f"{cart_count} items")
    with c3:
        if cart_count>0:
            if st.button("❌ Cart Khali Karo", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

    # CART DETAIL
    if st.session_state.cart:
        st.success("🛒 AAPKA CART - DARAZ JAISE:")
        total_bill = 0
        cart_text = "Salam MEHAR MART! Mera Order:\n"
        for i, item in enumerate(st.session_state.cart):
            ca,cb,cc = st.columns([3,1,1])
            with ca: st.write(f"{i+1}. {item['name']} - Rs.{item['final']}")
            with cb: st.write(f"Stock: {item['stock']}")
            with cc:
                if st.button(f"Remove", key=f"rem_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            total_bill += item['final']
            cart_text += f"{i+1}. {item['name']} - Rs.{item['final']}\n"
        cart_text += f"\nTotal Bill: Rs.{total_bill}\nStore: {STORE_LINK}"
        st.markdown(f"### 💰 Total Bill: Rs.{total_bill}")
        
        b1,b2 = st.columns(2)
        with b1:
            wa_cart_link = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(cart_text)}"
            st.link_button(f"✅ WHATSAPP ORDER - Rs.{total_bill}", wa_cart_link, use_container_width=True, type="primary")
        with b2:
            if st.button("📦 Order Confirm - Tracking Me Save Karo", use_container_width=True):
                order_data = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "items": ", ".join([x['name'] for x in st.session_state.cart]), "total": total_bill, "status": "WhatsApp Sent"}
                st.session_state.orders.append(order_data)
                pd.DataFrame(st.session_state.orders).to_csv(ORDER_FILE, index=False)
                st.success("✅ Order Tracking Me Save!")
                st.session_state.cart = []
                st.rerun()
        st.divider()

    # PRODUCTS - DARAZ GRID
    st.subheader("🍯 Products - Add to Cart Karo")
    if not st.session_state.products:
        st.warning("Abhi koi product nahi - Admin se add karwao - Product System me jao")
    else:
        cols = st.columns(2)
        for idx, p in enumerate(st.session_state.products):
            with cols[idx % 2]:
                with st.container(border=True):
                    if p.get('image_bytes'):
                        st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
                    st.markdown(f"**{p['name']}**")
                    st.markdown(f"~~Rs.{p['sell']}~~  **Rs.{p['final']}**  ({p['discount']}% OFF)")
                    st.caption(f"Stock: {p['stock']} | Free Delivery")
                    b1,b2 = st.columns(2)
                    with b1:
                        if st.button(f"🛒 Add to Cart", key=f"add_{idx}", use_container_width=True):
                            st.session_state.cart.append(p)
                            st.toast(f"{p['name']} Cart me!", icon="🛒")
                            st.rerun()
                    with b2:
                        wa_msg = f"Salam MEHAR MART! Order: {p['name']} Rs.{p['final']} - Link: {STORE_LINK}"
                        st.link_button(f"💬 Buy Now", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_msg)}", use_container_width=True)
                    if st.session_state.is_admin:
                        if st.button(f"🗑️ Delete {p['name']}", key=f"del_{idx}"):
                            st.session_state.products.pop(idx)
                            st.rerun()

elif menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM")
    with st.form("prod"):
        name=st.text_input("Product Name *"); sell=st.number_input("Selling Price",0,100000,3500); disc=st.number_input("Discount %",0,90,15)
        final=int(sell*(1-disc/100)) if disc>0 else sell; st.write(f"Final Price: Rs.{final}")
        buy=st.number_input("Kharid Price (Admin only)",0,100000,2000); stock=st.number_input("Stock",0,10000,50)
        highlights=st.text_area("Highlights","100% Khalis | Qudrati"); img_file=st.file_uploader("Product Photo",type=["jpg","png","jpeg"])
        sub=st.form_submit_button("💾 SAVE PRODUCT",use_container_width=True)
        if sub and name:
            img_bytes=img_file.getvalue() if img_file else None
            st.session_state.products.append({"name":name,"sell":sell,"discount":disc,"final":final,"buy":buy,"stock":stock,"highlights":highlights,"image_bytes":img_bytes})
            st.success(f"✅ {name} Save Ho Gaya!")

elif menu == "3. ORDERS TRACKING":
    st.header("3. 📊 VISITOR + ORDER TRACKING")
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("👀 Total Visits", total_visits)
    with c2: st.metric("📦 Total Orders", len(st.session_state.orders))
    with c3:
        total_sale = sum([o.get('total',0) for o in st.session_state.orders])
        st.metric("💰 Total Sale", f"Rs.{total_sale}")
    
    if os.path.exists(ORDER_FILE):
        df = pd.read_csv(ORDER_FILE)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Excel Download", df.to_csv(index=False), "mehar_orders.csv", "text/csv", use_container_width=True)
    else:
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Abhi koi order nahi")
