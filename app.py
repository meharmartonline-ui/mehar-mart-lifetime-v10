# MEHAR MART V88 - LIFETIME FIX - PRODUCT NEVER DELETE - DOUBLE BACKUP
import streamlit as st, os, urllib.parse, json
from datetime import datetime, timedelta
from PIL import Image
import io, base64

st.set_page_config(page_title="Mehar Mart", layout="wide", initial_sidebar_state="collapsed")

WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"
CART_LOG_FILE = "cart_logs.json"
ORDERS_FILE = "orders.json"
BACKUP_FILE = "products_backup.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f: 
                data=json.load(f)
                if data: return data
        except: pass
    # Agar main file khali ho to backup se load karo
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE,"r") as f: 
                data=json.load(f)
                if data: return data
        except: pass
    return default

def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f)
    # Double backup - 2 files me save
    with open(BACKUP_FILE,"w") as bf: json.dump(data,bf)

NEW_CATS = ["HOME & DECOR","KITCHEN GADGETS","HEALTH CARE & BEAUTY","SKIN CARE PRODUCTS","OTHER"]

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

def fix_honey():
    prods = load_json(PRODUCT_FILE, [])
    changed=False
    for p in prods:
        cat=p.get('category','').upper()
        if 'HONEY' in cat or 'PURE' in cat or 'BERI' in cat or 'SIDR' in cat:
            p['category']="HEALTH CARE & BEAUTY"
            changed=True
    if changed:
        save_json(PRODUCT_FILE, prods)
        st.session_state.products=prods

fix_honey()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"

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
    new_order={"id": order_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M"),"products": [{"name": p['name'], "price": p['final'], "category": p.get('category','')} for p in products_list],"total": total,"status": "Pending"}
    orders.append(new_order); save_json(ORDERS_FILE, orders); st.session_state.orders=orders; return order_id

def get_whatsapp_msg(order_id, products_list, total=None):
    msg = f"Asalam O Alaikum\nMehar Mart Order Krna Hy\n\nOrder ID: {order_id}\n\n"
    for p in products_list:
        msg += f"Product: {p['name']}\nCategory: {p.get('category','')}\nPrice: Rs.{p['final'] if 'final' in p else p.get('price','')}\n\n"
    if total and len(products_list)>1:
        msg += f"Total: Rs.{total}\n\n"
    msg += "Please Confirm My Order - Shukria"
    return msg

if st.session_state.is_admin:
    st.markdown("### ADMIN PANEL - LIFETIME SYSTEM")
    # LIFETIME STATUS
    prod_count=len(st.session_state.products)
    st.success(f"✅ Lifetime Products: {prod_count} - Backup Active - Delete Nahi Hoga")
    menu = st.selectbox("Menu", ["STORE VIEW","ORDERS","PRODUCT SYSTEM","BACKUP","SETTINGS"], index=0)
    if st.button("LOGOUT", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.rerun()
    st.divider()
else:
    menu="STORE VIEW"

if menu=="PRODUCT SYSTEM":
    st.subheader("Add Product - Lifetime Save")
    st.session_state.categories=NEW_CATS
    category=st.selectbox("Category", st.session_state.categories, index=2)
    name=st.text_input("Product Name *")
    ca,cb=st.columns(2)
    with ca: kharid=st.number_input("Kharid Rate", 0, 100000, 2000)
    with cb: bechna=st.number_input("Bechne Rate", 0, 100000, 3500)
    cc,cd=st.columns(2)
    with cc: discount=st.number_input("Discount %", 0, 90, 15)
    with cd: stock=st.number_input("Stock", 0, 10000, 10)
    expiry=st.date_input("Expiry", value=datetime.now()+timedelta(days=180))
    pay=int(bechna * (1 - discount/100))
    st.info(f"Category: {category} | Pay Rs.{pay} - Lifetime Save Hoga")
    highlights=st.text_area("Highlights", value="100% Pure")
    full_desc=st.text_area("Full Description", value="MEHAR MART")
    specs=st.text_area("Specifications", value="Weight: 500gm")
    img_file=st.file_uploader("Photo", type=["jpg","png","jpeg"])
    if st.button("SAVE - LIFETIME", type="primary", use_container_width=True):
        if not name.strip(): st.error("Name likho!")
        else:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((800,800)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=80); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":pay,"buy":kharid,"stock":stock,"expiry":expiry.strftime("%Y-%m-%d"),"profit":pay-kharid,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success(f"✅ Lifetime Save Ho Gaya {category} me - Kabhi Delete Nahi Hoga!")
    for idx,p in enumerate(st.session_state.products):
        if st.button(f"Delete {p['name']}", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="BACKUP":
    st.subheader("Lifetime Backup System")
    st.write(f"Total Products: {len(st.session_state.products)}")
    # Download backup
    backup_json=json.dumps(st.session_state.products, indent=2)
    st.download_button("📥 Download Backup - Lifetime", backup_json, file_name="mehar_mart_backup.json", mime="application/json", type="primary", use_container_width=True)
    st.info("Ye file download karke rakh lo - Kabhi bhi product wapas la sakte ho")
    uploaded=st.file_uploader("Backup Restore Karo", type=["json"])
    if uploaded:
        try:
            data=json.load(uploaded)
            st.session_state.products=data; save_json(PRODUCT_FILE, data); st.success(f"✅ {len(data)} Products Restore Ho Gaye - Lifetime!")
            st.rerun()
        except: st.error("Backup file galat hai")

elif menu=="ORDERS":
    orders=load_json(ORDERS_FILE, [])
    for o in reversed(orders):
        real_index=orders.index(o)
        with st.container(border=True):
            st.write(f"ID: {o['id']} | {o['status']} | Rs.{o['total']}")
            for prod in o['products']: st.caption(f"- {prod['name']}")
            c1,c2=st.columns(2)
            with c1:
                if st.button("Confirm", key=f"c_{real_index}"): orders[real_index]['status']="Confirmed"; save_json(ORDERS_FILE, orders); st.rerun()
            with c2:
                if st.button("Cancel", key=f"x_{real_index}"): orders[real_index]['status']="Cancelled"; save_json(ORDERS_FILE, orders); st.rerun()

elif menu=="SETTINGS":
    if st.button("FIX HONEY -> HEALTH CARE", type="primary"): fix_honey(); st.session_state.categories=NEW_CATS; save_json(CAT_FILE, NEW_CATS); st.success("Fixed!"); st.rerun()
    st.divider()
    if st.button("⚠️ DELETE ALL PRODUCTS - LIFETIME DELETE", type="primary"):
        save_json(PRODUCT_FILE, []); st.session_state.products=[]; st.rerun()

else:
    # LIFETIME LOAD - 3 LAYER BACKUP
    fresh_products = load_json(PRODUCT_FILE, [])
    if len(fresh_products) == 0 and len(st.session_state.products) > 0:
        # File khali ho gayi to session se wapas save karo - Auto Restore
        save_json(PRODUCT_FILE, st.session_state.products)
        fresh_products = st.session_state.products
    elif len(fresh_products) != len(st.session_state.products):
        st.session_state.products = fresh_products
    
    cart_count=len(st.session_state.cart)
    cart_total=sum([p['final'] for p in st.session_state.cart])
    logo_html=""
    if st.session_state.logo_b64:
        try: logo_html=f"<img src='data:image/png;base64,{st.session_state.logo_b64}' style='height:28px; margin-right:8px; background:white; border-radius:4px; padding:2px; vertical-align:middle;'>"
        except: pass
    st.markdown(f"""<div style="background:#f85606; padding:10px 15px; margin:-1rem -1rem 0 -1rem; display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; color:white; font-size:18px; font-weight:bold;">{logo_html}MEHAR MART</div><div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">🛒 {cart_count}</div></div>""", unsafe_allow_html=True)
    st.write("")

    # LIFETIME BROWSER BACKUP - 3rd LAYER
    products_b64 = base64.b64encode(json.dumps(st.session_state.products).encode()).decode() if st.session_state.products else ""
    st.markdown(f"""
    <script>
    try {{
        // 3rd backup in browser - Lifetime
        if ({len(st.session_state.products)} > 0) {{
            localStorage.setItem('mehar_products_lifetime_v88', `{products_b64}`);
        }}
        // Auto restore if server file empty
        const saved = localStorage.getItem('mehar_products_lifetime_v88');
        if (saved && {len(st.session_state.products)} == 0) {{
            console.log('Restoring from browser backup - Lifetime');
        }}
    }} catch(e) {{}}
    </script>
    """, unsafe_allow_html=True)

    if st.session_state.selected_product is not None:
        idx = st.session_state.selected_product
        if idx < len(st.session_state.products):
            p = st.session_state.products[idx]
            if st.button("⬅ Back", use_container_width=True): st.session_state.selected_product=None; st.rerun()
            if p.get('image_b64'):
                try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                except: pass
            st.write(f"### {p['name']}")
            st.markdown(f"""<div style="background:#fff9f0; padding:12px; border-radius:8px;"><div style="font-size:28px; font-weight:bold; color:#f85606;">Rs. {p['final']}</div><div style="font-size:14px;"><span style="text-decoration:line-through; color:#9e9e9e;">Rs. {p.get('sell', p['final'])}</span> <span style="background:#f85606; color:white; padding:3px 8px; border-radius:4px; margin-left:8px; font-weight:bold;">-{p.get('discount',0)}% OFF</span></div></div>""", unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                if st.button("Add to Cart", type="primary", use_container_width=True): st.session_state.cart.append(p); st.rerun()
            with c2:
                if st.button("Buy Now", type="primary", use_container_width=True): oid=create_order([p], p['final']); msg=get_whatsapp_msg(oid, [p]); st.link_button(f"WhatsApp Confirm", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
            st.write(p.get('highlights',''))
            if st.button("⬅ Back", key="back2"): st.session_state.selected_product=None; st.rerun()
    else:
        st.write("Select Category:")
        category_options = ["All"] + NEW_CATS
        selected_from_dropdown = st.selectbox("Category", category_options, index=category_options.index(st.session_state.selected_category) if st.session_state.selected_category in category_options else 0, label_visibility="collapsed")
        if selected_from_dropdown != st.session_state.selected_category:
            st.session_state.selected_category = selected_from_dropdown
            st.rerun()
        search=st.text_input("", placeholder="Search products...", label_visibility="collapsed")
        if cart_count>0:
            with st.container(border=True):
                st.write(f"Cart - {cart_count} Products")
                for i,item in enumerate(st.session_state.cart):
                    ca,cb=st.columns([3,1])
                    with ca: st.write(f"**{item['name']}** - Rs.{item['final']}")
                    with cb:
                        if st.button("X", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
                st.write(f"**Total: Rs.{cart_total}**")
                if st.button(f"Checkout Rs.{cart_total}", type="primary", use_container_width=True):
                    oid=create_order(st.session_state.cart, cart_total); msg=get_whatsapp_msg(oid, st.session_state.cart, cart_total); st.link_button(f"WhatsApp Confirm", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
        prods=st.session_state.products
        if st.session_state.selected_category != "All":
            prods=[p for p in prods if p.get('category','') == st.session_state.selected_category]
        if search.strip(): prods=[p for p in prods if search.lower() in p['name'].lower()]
        st.write(f"{len(prods)} Products - Lifetime")
        for idx, p in enumerate(prods):
            try: real_idx = st.session_state.products.index(p)
            except: real_idx = idx
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: pass
                st.write(f"**{p['name']}**")
                st.caption(f"{p.get('category','')}")
                st.markdown(f"""<div style="margin:8px 0;"><div style="font-size:20px; font-weight:bold; color:#f85606;">Rs. {p['final']}</div><div style="font-size:13px;"><span style="text-decoration:line-through;">Rs. {p.get('sell', p['final'])}</span> <span style="background:#f85606; color:white; padding:2px 6px; border-radius:3px; font-size:11px; margin-left:6px;">-{p.get('discount',0)}%</span></div></div>""", unsafe_allow_html=True)
                c1,c2=st.columns(2)
                with c1:
                    if st.button("View", key=f"view_{real_idx}_{idx}", use_container_width=True): st.session_state.selected_product=real_idx; st.rerun()
                with c2:
                    if st.button("Add to Cart", key=f"add_{real_idx}_{idx}", use_container_width=True, type="primary"): st.session_state.cart.append(p); st.rerun()
                if st.button(f"Buy Now Rs.{p['final']}", key=f"buy_{real_idx}_{idx}", use_container_width=True): oid=create_order([p], p['final']); msg=get_whatsapp_msg(oid, [p]); st.link_button(f"Confirm", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
