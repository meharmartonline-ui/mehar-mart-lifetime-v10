import streamlit as st
import io
import base64
import urllib.parse
from PIL import Image
import google.generativeai as genai
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mehar Mart - Lifetime", page_icon="🛒", layout="wide")

# --- SESSION INIT - NO DUMMY DATA ---
if "products" not in st.session_state:
    st.session_state.products = []  # Bilkul Khali - Koi Watch, AirPods Nahi!
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Salam Bhai! Mehar Mart Me Khush Amdeed! Aapko Kya Chahiye?"}]

# --- HELPER ---
def create_order(items, total):
    oid = f"MM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    st.session_state.orders.append({"id": oid, "items": items, "total": total, "date": str(datetime.now())})
    return oid

# --- HEADER ---
st.title("🛒 Mehar Mart - Lifetime Store")
st.caption("Owner WhatsApp: 03452352112 | 100% Original Products")

# --- ADMIN PANEL (Aap Ke Liye) ---
with st.expander("🔐 Admin Panel - Product Add Karo (Sirf Aap Ke Liye)"):
    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        category = st.text_input("Category", value="General")
        price = st.number_input("Price Rs.", min_value=0)
        desc = st.text_area("Description")
        img_file = st.file_uploader("Product Image", type=["jpg","png","jpeg"])
        submit = st.form_submit_button("Add Product")
        if submit and name and price:
            img_b64 = ""
            if img_file:
                img = Image.open(img_file)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                img_b64 = base64.b64encode(buf.getvalue()).decode()
            st.session_state.products.append({"name": name, "category": category, "price": price, "desc": desc, "image_b64": img_b64})
            st.success(f"{name} Add Ho Gaya!")

# --- SEARCH & CATEGORY ---
search = st.text_input("🔍 Search Product")
categories = ["All"] + list(set([p.get('category','General') for p in st.session_state.products]))
selected = st.selectbox("Category", categories, index=0)

prods = st.session_state.products
if selected != "All":
    prods = [p for p in prods if p.get('category') == selected]
if search.strip():
    prods = [p for p in prods if search.lower() in p.get('name','').lower()]

st.write(f"**{len(prods)} Products Found**")

if len(prods) == 0:
    st.info("No Products in Store - Admin Panel Se Add Karo. Customer ko bolo WhatsApp 03452352112 pe rabta kare.")
    if st.button("Show All Products"):
        st.session_state.selected_category = "All"
        st.rerun()

# --- PRODUCT DISPLAY ---
for idx, p in enumerate(prods):
    try:
        real_idx = st.session_state.products.index(p)
    except:
        real_idx = idx
    
    with st.container(border=True):
        if p.get('image_b64'):
            try:
                img_data = base64.b64decode(p.get('image_b64'))
                st.image(Image.open(io.BytesIO(img_data)), use_container_width=True)
            except:
                pass
        
        st.write(f"**{p.get('name','')}**")
        st.caption(f"{p.get('category','')} | Rs. {p.get('price','')}")
        st.markdown(f"<div style='margin-bottom:10px'>{p.get('desc','')}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("View Details", key=f"view_{idx}"):
                st.session_state.selected_product = p
        with c2:
            if st.button("Add to Cart", key=f"cart_{idx}"):
                st.session_state.cart.append(p)
                st.toast(f"{p.get('name')} Added!")
        
        if st.button(f"Buy Now Rs.{p.get('price','')}", key=f"buy_{idx}", use_container_width=True):
            oid = create_order([p], p.get('price',''))
            st.success(f"Order Created: {oid} - WhatsApp pe rabta karo!")

        # --- WHATSAPP BUTTON - HAR PRODUCT PE ---
        wa_text = f"Salam Mehar Mart! Mujhe {p.get('name','')} chahiye. Price Rs.{p.get('price','')} Order karna hai."
        wa_encoded = urllib.parse.quote(wa_text)
        wa_link = f"https://wa.me/923452352112?text={wa_encoded}"
        st.link_button(f"📲 WhatsApp Pe Order - {p.get('name','')}", wa_link, use_container_width=True)

st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)

# ================================================
# --- JARVIS AI AGENT - STORE PE HI - FINAL ---
# ================================================
st.divider()
st.header("💬 Mehar Mart AI Agent - Jarvis")
st.caption("Store pe hi sawal pucho - WhatsApp pe jane ki zaroorat nahi")

for chat in st.session_state.chat_history:
    st.chat_message(chat["role"]).write(chat["content"])

if user_q := st.chat_input("Yahan likho: e.g. Sasti chez dikhao, Kapre hain?"):
    st.session_state.chat_history.append({"role": "user", "content": user_q})
    st.chat_message("user").write(user_q)

    # Live Data - No Dummy
    live_products = st.session_state.products
    if not live_products:
        prod_info = "STORE IS EMPTY. No products available right now."
    else:
        # Only send name, price, category to AI - not full base64
        clean_list = [{"name": x.get('name'), "price": x.get('price'), "category": x.get('category')} for x in live_products]
        prod_info = str(clean_list)

    # Jarvis Reply Logic
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            system = f"""
            You are Jarvis, AI Agent for Mehar Mart. Speak in Roman Urdu friendly style.
            Owner WhatsApp: 03452352112
            LIVE STORE DATA (Only Truth): {prod_info}
            RULES:
            1. NEVER mention dummy products like Watch, AirPods, Wallet, Headphones if not in LIVE DATA.
            2. If STORE IS EMPTY, say: Bhai store khali hai, WhatsApp 03452352112 pe rabta karo.
            3. If products exist, show them with price.
            4. For order, ask Name + Address + Phone.
            5. Be helpful, short.
            """
            resp = model.generate_content(system + f"\nCustomer: {user_q}\nJarvis:")
            ans = resp.text
        else:
            ans = f"Live me {len(live_products)} products hain. WhatsApp 03452352112 pe rabta karo. Question: {user_q}"
    except Exception as e:
        ans = f"Mehar Mart me {len(live_products)} products available hain. Aapko kya chahiye? WhatsApp: 03452352112"

    st.session_state.chat_history.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
    
    # Quick WhatsApp Continue
    wa_q = urllib.parse.quote(f"Salam! Mehar Mart - {user_q}")
    wa_link_q = f"https://wa.me/923452352112?text={wa_q}"
    st.link_button("📲 WhatsApp Pe Continue Karo", wa_link_q)
