# MEHAR MART V94 - FINAL - V93 + AI AGENT - NO DUMMY - LIFETIME
import streamlit as st, os, urllib.parse, json
from datetime import datetime, timedelta
from PIL import Image
import io, base64
import google.generativeai as genai

st.set_page_config(page_title="Mehar Mart", layout="wide", initial_sidebar_state="collapsed")

WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"
ORDERS_FILE = "orders.json"
BACKUP_FILE = "products_backup.json"
ORDERS_BACKUP = "orders_backup.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f:
                data=json.load(f)
                if data: return data
        except: pass
    if file==PRODUCT_FILE and os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE,"r") as f:
                data=json.load(f)
                if data: return data
        except: pass
    if file==ORDERS_FILE and os.path.exists(ORDERS_BACKUP):
        try:
            with open(ORDERS_BACKUP,"r") as f:
                data=json.load(f)
                if data: return data
        except: pass
    return default

def save_json(file,data):
    try:
        with open(file,"w") as f: json.dump(data,f)
        if file==PRODUCT_FILE:
            with open(BACKUP_FILE,"w") as bf: json.dump(data,bf)
        if file==ORDERS_FILE:
            with open(ORDERS_BACKUP,"w") as bf: json.dump(data,bf)
    except: pass

NEW_CATS = ["HONEY","HOME & DECOR","KITCHEN GADGETS","HEALTH CARE & BEAUTY","SKIN CARE PRODUCTS","OTHER"]

if 'products' not in st.session_state: st.session_state.products=load_json(PRODUCT_FILE, [])
if 'cart' not in st.session_state: st.session_state.cart=[]
if 'categories' not in st.session_state: 
    st.session_state.categories=NEW_CATS
    save_json(CAT_FILE, NEW_CATS)
if 'is_admin' not in st.session_state: st.session_state.is_admin=False
if 'logo_b64' not in st.session_state: st.session_state.logo_b64=load_json(LOGO_FILE, None)
if 'selected_product' not in st.session_state: st.session_state.selected_product=None
if 'orders' not in st.session_state: st.session_state.orders=load_json(ORDERS_FILE, [])
if 'selected_category' not in st.session_state: st.session_state.selected_category="All"
if 'chat_history' not in st.session_state: st.session_state.chat_history=[{"role":"assistant","content":"Salam Bhai! Mehar Mart Me Khush Amdeed! Aapko Kya Chahiye?"}]

def fix_old_categories():
    try:
        prods = load_json(PRODUCT_FILE, [])
        changed=False
        for p in prods:
            if not isinstance(p, dict): continue
            cat_raw = p.get('category','')
            if cat_raw is None: cat_raw=""
            cat=str(cat_raw).upper().strip()
            if cat in ['PURE HONEY','BERI HONEY','SIDR HONEY','PURE','BERI','SIDR'] or 'PURE HONEY' in cat or 'BERI HONEY' in cat:
                if p.get('category')!="HONEY":
                    p['category']="HONEY"; changed=True
        if changed:
            save_json(PRODUCT_FILE, prods)
            st.session_state.products=prods
    except: pass

fix_old_categories()

def get_password():
    if os.path.exists(PASS_FILE):
        try:
            with open(PASS_FILE,"r") as f: return f.read().strip()
        except: return "mehar123"
    return "mehar123"

def save_password(p):
    try:
        with open(PASS_FILE,"w") as f: f.write(p)
    except: pass

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True
    st.session_state.selected_category="All"

if not st.session_state.is_admin:
    st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;} [data-testid='stToolbar']{display:none;} [data-testid='stAppDeployButton']{display:none;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>footer {visibility: hidden;} [data-testid='stToolbar']{display:none;} [data-testid='stAppDeployButton']{display:none;}</style>", unsafe_allow_html=True)

def create_order(products_list, total):
    orders=load_json(ORDERS_FILE, [])
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(len(orders)+1)
    new_order={"id": order_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M"),"products": [{"name": p.get('name',''), "price": p.get('final', p.get('price',0)), "category": p.get('category','')} for p in products_list],"total": total,"status": "Pending","reason": ""}
    orders.append(new_order); save_json(ORDERS_FILE, orders); st.session_state.orders=orders; return order_id

def get_whatsapp_msg(order_id, products_list, total=None):
    msg = f"Asalam O Alaikum\nMehar Mart Order Krna Hy\n\nOrder ID: {order_id}\n\n"
    for p in products_list:
        msg+=f"Product: {p.get('name','')}\nCategory: {p.get('category','')}\nPrice: Rs.{p.get('final', p.get('price',0))}\n\n"
    if total and len(products_list)>1: msg+=f"Total: Rs.{total}\n\n"
    msg+="Please Confirm My Order - Shukria"
    return msg

# --- MENU ---
current_menu = "STORE VIEW"
if st.session_state.is_admin:
    st.markdown("### ADMIN PANEL - Mehar Mart")
    current_menu = st.selectbox("Menu", ["STORE VIEW", "MANAGE PRODUCTS", "ORDERS", "SETTINGS"])

# --- MANAGE PRODUCTS (ONLY ADMIN) ---
if current_menu == "MANAGE PRODUCTS" and st.session_state.is_admin:
    st.header("Add / Delete Products")
    with st.form("add_prod"):
        name = st.text_input("Product Name")
        cat = st.selectbox("Category", st.session_state.categories)
        price = st.number_input("Price", min_value=0)
        final_price = st.number_input("Final Price (Discount)", min_value=0)
        desc = st.text_area("Description")
        img = st.file_uploader("Image", type=["jpg","png","jpeg"])
        if st.form_submit_button("Add Product"):
            img_b64 = ""
            if img:
                pil = Image.open(img)
                buf = io.BytesIO()
                pil.save(buf, format="PNG")
                img_b64 = base64.b64encode(buf.getvalue()).decode()
            new_p = {"name": name, "category": cat, "price": price, "final": final_price if final_price>0 else price, "desc": desc, "image_b64": img_b64}
            prods = load_json(PRODUCT_FILE, [])
            prods.append(new_p)
            save_json(PRODUCT_FILE, prods)
            st.session_state.products = prods
            st.success("Product Added!")
    st.divider()
    for i, p in enumerate(load_json(PRODUCT_FILE, [])):
        st.write(f"{i+1}. {p.get('name')} - Rs.{p.get('final')}")
        if st.button(f"Delete {p.get('name')}", key=f"del_{i}"):
            prods = load_json(PRODUCT_FILE, [])
            del prods[i]
            save_json(PRODUCT_FILE, prods)
            st.session_state.products = prods
            st.rerun()

# --- STORE VIEW ---
if current_menu == "STORE VIEW":
    st.markdown("<h1 style='text-align:center;'>🛒 Mehar Mart - Lifetime Store</h1>", unsafe_allow_html=True)
    # Owner number HIDDEN from public - only in WhatsApp links
    
    prods = load_json(PRODUCT_FILE, [])
    st.session_state.products = prods

    search = st.text_input("🔍 Search Product", placeholder="e.g. Honey, Kitchen...")
    cats = ["All"] + st.session_state.categories
    sel_cat = st.selectbox("Category", cats, index=0)

    filtered = prods
    if sel_cat != "All":
        filtered = [p for p in filtered if p.get('category') == sel_cat]
    if search.strip():
        filtered = [p for p in filtered if search.lower() in p.get('name','').lower()]

    st.write(f"**{len(filtered)} Products Found**")

    if len(filtered) == 0:
        st.info("Filhal Products Load Ho Rahe Hain - Admin Se Rabta Karo: WhatsApp 03452352112")
    
    cols = st.columns(2)
    for idx, p in enumerate(filtered):
        col = cols[idx % 2]
        with col:
            with st.container(border=True):
                if p.get('image_b64'):
                    try:
                        img_data = base64.b64decode(p.get('image_b64'))
                        st.image(Image.open(io.BytesIO(img_data)), use_container_width=True)
                    except: pass
                st.markdown(f"**{p.get('name','')}**")
                st.caption(f"{p.get('category','')} | Rs. {p.get('final', p.get('price',''))}")
                if p.get('desc'):
                    st.write(p.get('desc')[:100])

                if st.button(f"Buy Now Rs.{p.get('final', p.get('price',''))}", key=f"buy_{idx}"):
                    oid = create_order([p], p.get('final', p.get('price','')))
                    msg = get_whatsapp_msg(oid, [p])
                    wa_link = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"
                    st.success(f"Order ID: {oid}")
                    st.link_button("📲 Confirm on WhatsApp", wa_link, use_container_width=True)

                # WHATSAPP BUTTON PER PRODUCT
                wa_text = f"Salam! Mehar Mart - Mujhe {p.get('name','')} chahiye. Price Rs.{p.get('final', p.get('price',''))}"
                wa_link2 = f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_text)}"
                st.link_button(f"📲 WhatsApp - {p.get('name','')[:20]}", wa_link2, use_container_width=True)

    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

    # ================= AI AGENT - JARVIS - AT BOTTOM =================
    st.divider()
    st.header("💬 Mehar Mart AI Agent - Jarvis")
    st.caption("Store pe hi sawal pucho - WhatsApp pe jane ki zaroorat nahi")

    for chat in st.session_state.chat_history:
        st.chat_message(chat["role"]).write(chat["content"])

    if user_q := st.chat_input("Yahan likho: e.g. Sasti chez dikhao, Honey hai?"):
        st.session_state.chat_history.append({"role": "user", "content": user_q})
        st.chat_message("user").write(user_q)

        live_prods = load_json(PRODUCT_FILE, [])
        if not live_prods:
            prod_info = "STORE EMPTY - No products in json"
        else:
            clean = [{"name": x.get('name'), "price": x.get('final', x.get('price')), "cat": x.get('category')} for x in live_prods]
            prod_info = str(clean)[:3500]

        try:
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"You are Jarvis for Mehar Mart. Roman Urdu. Live Products: {prod_info}. WA: {WA_NUMBER}. Rule: Never invent products. If empty, say WhatsApp pe rabta karo. Customer: {user_q}"
                ans = model.generate_content(prompt).text
            else:
                ans = f"Mehar Mart me {len(live_prods)} products hain. Aapka sawal: {user_q} - WhatsApp 03452352112 pe rabta karo"
        except Exception as e:
            ans = f"Mehar Mart me {len(live_prods)} products hain. Aapko kya chahiye? WhatsApp: 03452352112"

        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.chat_message("assistant").write(ans)
        wa_q = urllib.parse.quote(f"Salam Mehar Mart! {user_q}")
        st.link_button("📲 WhatsApp Pe Continue", f"https://wa.me/{WA_NUMBER}?text={wa_q}")
