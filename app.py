# MEHAR MART V86 - CLEAN CLIENT - NO EXTRA TEXT - NO DARAZ WORD ON CLIENT SIDE
import streamlit as st, os, urllib.parse, json
from datetime import datetime, timedelta
from PIL import Image
import io, base64

st.set_page_config(page_title="Mehar Mart", layout="wide", initial_sidebar_state="collapsed")

STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"
VISIT_FILE = "visits.txt"
CART_LOG_FILE = "cart_logs.json"
ORDERS_FILE = "orders.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f: return json.load(f)
        except: return default
    return default
def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f)

NEW_DARAZ_CATEGORIES = ["HONEY","HOME & DECOR","KITCHEN GADGETS","HEALTH CARE & BEAUTY","SKIN CARE PRODUCTS","OTHER"]

if 'products' not in st.session_state: st.session_state.products=load_json(PRODUCT_FILE, [])
if 'cart' not in st.session_state: st.session_state.cart=[]
if 'categories' not in st.session_state: 
    st.session_state.categories=NEW_DARAZ_CATEGORIES
    save_json(CAT_FILE, NEW_DARAZ_CATEGORIES)
if 'is_admin' not in st.session_state: st.session_state.is_admin=False
if 'admin_menu' not in st.session_state: st.session_state.admin_menu="STORE VIEW"
if 'logo_b64' not in st.session_state: st.session_state.logo_b64=load_json(LOGO_FILE, None)
if 'selected_product' not in st.session_state: st.session_state.selected_product=None
if 'orders' not in st.session_state: st.session_state.orders=load_json(ORDERS_FILE, [])
if 'selected_category' not in st.session_state: st.session_state.selected_category="All"

def fix_old_categories():
    prods = load_json(PRODUCT_FILE, [])
    changed = False
    for p in prods:
        old_cat = p.get('category','').upper()
        if 'HONEY' in old_cat or 'PURE' in old_cat or 'BERI' in old_cat or 'SIDR' in old_cat:
            if p.get('category') != "HONEY":
                p['category'] = "HONEY"
                changed = True
        elif 'HOME' in old_cat or 'DECOR' in old_cat:
            p['category'] = "HOME & DECOR"
            changed = True
        elif 'KITCHEN' in old_cat or 'GADGET' in old_cat:
            p['category'] = "KITCHEN GADGETS"
            changed = True
        elif 'HEALTH' in old_cat:
            p['category'] = "HEALTH CARE & BEAUTY"
            changed = True
        elif 'SKIN' in old_cat or 'BEAUTY' in old_cat:
            p['category'] = "SKIN CARE PRODUCTS"
            changed = True
    if changed:
        save_json(PRODUCT_FILE, prods)
        st.session_state.products = prods

fix_old_categories()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"
def save_password(p):
    with open(PASS_FILE,"w") as f: f.write(p)
def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE,"r") as f: return int(f.read().strip())
        except: return 0
    return 0

if st.query_params.get("admin")==get_password():
    st.session_state.is_admin=True
    st.session_state.selected_category="All"

if not st.session_state.is_admin:
    st.markdown("<style>header, footer {visibility: hidden;} .block-container{padding-top:0rem;} [data-testid='stToolbar']{display:none;} [data-testid='stAppDeployButton']{display:none;}</style>", unsafe_allow_html=True)
    if st.session_state.selected_category not in ["All"] + st.session_state.categories:
        st.session_state.selected_category="All"
else:
    st.markdown("<style>footer {visibility: hidden;} [data-testid='stToolbar']{display:none;} [data-testid='stAppDeployButton']{display:none;}</style>", unsafe_allow_html=True)

def create_order(products_list, total):
    orders=load_json(ORDERS_FILE, [])
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(len(orders)+1)
    new_order={"id": order_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M"),"products": [{"name": p['name'], "price": p['final'], "category": p.get('category','')} for p in products_list],"total": total,"status": "Pending","reason": ""}
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
    st.markdown("### ADMIN PANEL")
    menu = st.selectbox("Menu", ["STORE VIEW","ORDERS","PRODUCT SYSTEM","MONEY","STOCK","SETTINGS"], index=0)
    st.session_state.admin_menu=menu
    orders_data=load_json(ORDERS_FILE, [])
    pending=len([o for o in orders_data if o['status']=="Pending"])
    confirmed=len([o for o in orders_data if o['status'] in ["Confirmed","Delivered"]])
    c1,c2=st.columns(2)
    with c1: st.button(f"Pending: {pending}", use_container_width=True)
    with c2: st.button(f"Sale: {confirmed}", use_container_width=True)
    col1,col2,col3=st.columns(3)
    with col1:
        if st.button("ORDERS", use_container_width=True, type="primary"): st.session_state.admin_menu="ORDERS"; st.rerun()
    with col2:
        if st.button("ADD PRODUCT", use_container_width=True): st.session_state.admin_menu="PRODUCT SYSTEM"; st.rerun()
    with col3:
        if st.button("LOGOUT", use_container_width=True): st.session_state.is_admin=False; st.query_params.clear(); st.session_state.selected_category="All"; st.rerun()
    st.divider()
else:
    menu="STORE VIEW"

if menu=="PRODUCT SYSTEM":
    st.subheader("Add Product")
    st.session_state.categories = NEW_DARAZ_CATEGORIES
    save_json(CAT_FILE, NEW_DARAZ_CATEGORIES)
    category=st.selectbox("Category", st.session_state.categories, index=0)
    new_cat=st.text_input("New Category Add")
    if st.button("Add New Category"):
        if new_cat and new_cat.upper() not in st.session_state.categories:
            st.session_state.categories.append(new_cat.upper()); save_json(CAT_FILE, st.session_state.categories); st.success(f"Category {new_cat.upper()} Added!"); st.rerun()
    name=st.text_input("Product Name *")
    ca,cb=st.columns(2)
    with ca: kharid=st.number_input("Kharid Rate", 0, 100000, 2000)
    with cb: bechna=st.number_input("Bechne Rate", 0, 100000, 3500)
    cc,cd=st.columns(2)
    with cc: discount=st.number_input("Discount %", 0, 90, 15)
    with cd: stock=st.number_input("Stock", 0, 10000, 10)
    expiry=st.date_input("Expiry", value=datetime.now()+timedelta(days=180))
    pay=int(bechna * (1 - discount/100)); profit=pay - kharid
    st.info(f"Category: {category} | Original Rs.{bechna} | Pay Rs.{pay} | Profit Rs.{profit}")
    highlights=st.text_area("Highlights", value="100% Pure - No Sugar, No Mix")
    full_desc=st.text_area("Full Description", value="MEHAR MART - Cash on Delivery")
    specs=st.text_area("Specifications", value="Weight: 500gm\nBrand: MEHAR MART")
    img_file=st.file_uploader("Photo", type=["jpg","png","jpeg"])
    if st.button("SAVE PRODUCT", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Product Name likho!")
        else:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((800,800)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=80); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":pay,"buy":kharid,"stock":stock,"expiry":expiry.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success(f"Saved in {category}!")
    st.divider()
    st.write("Categories: " + " | ".join(st.session_state.categories))
    for idx,p in enumerate(st.session_state.products):
        c1,c2=st.columns([4,1])
        with c1: st.write(f"{idx+1}. {p['name']} - {p.get('category','')} - Rs.{p['final']}")
        with c2:
            if st.button("Delete", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="ORDERS":
    st.header("Orders")
    orders=load_json(ORDERS_FILE, [])
    if not orders: st.info("No orders")
    else:
        filter_status=st.selectbox("Filter", ["All","Pending","Confirmed","Delivered","Cancelled","Returned"], index=0)
        filtered=orders if filter_status=="All" else [o for o in orders if o['status']==filter_status]
        confirmed_orders=[o for o in orders if o['status'] in ["Confirmed","Delivered"]]
        st.metric("Sale Count", len(confirmed_orders))
        st.metric("Sale Amount", f"Rs.{sum([o['total'] for o in confirmed_orders])}")
        st.divider()
        for o in reversed(filtered):
            real_index = orders.index(o)
            with st.container(border=True):
                st.write(f"**ID: {o['id']}** | {o['time']} | **{o['status']}** | Rs.{o['total']}")
                for prod in o['products']: st.caption(f"- {prod['name']} - Rs.{prod['price']} - {prod.get('category','')}")
                if o.get('reason'): st.warning(f"Reason: {o['reason']}")
                c1,c2,c3,c4=st.columns(4)
                with c1:
                    if st.button("Confirm", key=f"conf_{real_index}"): orders[real_index]['status']="Confirmed"; save_json(ORDERS_FILE, orders); st.rerun()
                with c2:
                    if st.button("Delivered", key=f"deliv_{real_index}"): orders[real_index]['status']="Delivered"; save_json(ORDERS_FILE, orders); st.rerun()
                with c3:
                    if st.button("Cancel", key=f"cancel_{real_index}"): orders[real_index]['status']="Cancelled"; save_json(ORDERS_FILE, orders); st.rerun()
                with c4:
                    if st.button("Return", key=f"return_{real_index}"): orders[real_index]['status']="Returned"; save_json(ORDERS_FILE, orders); st.rerun()

elif menu=="MONEY":
    orders=load_json(ORDERS_FILE, [])
    confirmed=[o for o in orders if o['status'] in ["Confirmed","Delivered"]]
    st.metric("Sale Count", len(confirmed))
    st.metric("Sale Amount", f"Rs.{sum([o['total'] for o in confirmed])}")

elif menu=="STOCK":
    for idx,p in enumerate(st.session_state.products):
        st.write(f"{p['name']} - {p.get('category','')} - Stock {p['stock']}")
        if st.button(f"Plus {idx}"): st.session_state.products[idx]['stock']+=1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif menu=="SETTINGS":
    st.subheader("Fix Categories")
    if st.button("FIX OLD CATEGORIES TO NEW SYSTEM", type="primary"):
        fix_old_categories()
        st.session_state.categories = NEW_DARAZ_CATEGORIES
        save_json(CAT_FILE, NEW_DARAZ_CATEGORIES)
        st.success("Fixed! All old categories -> New system")
        st.rerun()
    st.divider()
    st.subheader("Logo")
    logo_file=st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])
    if logo_file:
        try: img=Image.open(logo_file); img.thumbnail((200,200)); buf=io.BytesIO(); img.save(buf, format="PNG"); lb64=base64.b64encode(buf.getvalue()).decode(); st.session_state.logo_b64=lb64; save_json(LOGO_FILE, lb64); st.success("Logo Saved")
        except: pass
    old_p=st.text_input("Old", type="password")
    new_p=st.text_input("New", type="password")
    new_p2=st.text_input("Confirm", type="password")
    if st.button("Change Password", type="primary"):
        if old_p!=get_password(): st.error("Wrong old")
        elif new_p!=new_p2: st.error("Not match")
        elif not new_p: st.error("Empty")
        else: save_password(new_p); st.success(f"New: {new_p}")
    if st.button("DELETE ALL ORDERS", type="primary"):
        save_json(ORDERS_FILE, []); st.rerun()

else:
    fresh_products = load_json(PRODUCT_FILE, [])
    if len(fresh_products) != len(st.session_state.products):
        st.session_state.products = fresh_products
    
    cart_count=len(st.session_state.cart)
    cart_total=sum([p['final'] for p in st.session_state.cart])
    logo_html=""
    if st.session_state.logo_b64:
        try: logo_html=f"<img src='data:image/png;base64,{st.session_state.logo_b64}' style='height:28px; margin-right:8px; background:white; border-radius:4px; padding:2px; vertical-align:middle;'>"
        except: pass
    st.markdown(f"""
    <div style="background:#f85606; padding:10px 15px; margin:-1rem -1rem 0 -1rem; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; color:white; font-size:18px; font-weight:bold;">{logo_html}MEHAR MART</div>
    <div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">🛒 {cart_count}</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    cart_json = json.dumps([{"name": p['name'], "price": p['final'], "cat": p.get('category','')} for p in st.session_state.cart])
    st.markdown(f"""
    <script>
    try {{
        localStorage.setItem('mehar_cart_v86', `{cart_json}`);
        localStorage.setItem('mehar_cart_time_v86', new Date().toISOString());
        localStorage.setItem('mehar_cart_expiry', new Date(Date.now() + 30*24*60*60*1000).toISOString());
    }} catch(e) {{}}
    </script>
    """, unsafe_allow_html=True)

    if st.session_state.selected_product is not None:
        idx = st.session_state.selected_product
        if idx < len(st.session_state.products):
            p = st.session_state.products[idx]
            if st.button("⬅ Back", use_container_width=True):
                st.session_state.selected_product=None; st.rerun()
            if p.get('image_b64'):
                try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                except: pass
            st.write(f"### {p['name']}")
            st.caption(f"{p.get('category','')}")
            st.markdown(f"""
            <div style="background:#fff9f0; padding:12px; border-radius:8px;">
            <div style="font-size:28px; font-weight:bold; color:#f85606;">Rs. {p['final']}</div>
            <div style="font-size:14px;"><span style="text-decoration:line-through; color:#9e9e9e;">Rs. {p.get('sell', p['final'])}</span> <span style="background:#f85606; color:white; padding:3px 8px; border-radius:4px; margin-left:8px; font-weight:bold;">-{p.get('discount',0)}% OFF</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            c1,c2=st.columns(2)
            with c1:
                if st.button("Add to Cart", type="primary", use_container_width=True, key="detail_add"):
                    logs=load_json(CART_LOG_FILE, []); logs.append({"product":p['name'],"time":datetime.now().strftime("%Y-%m-%d %H:%M")}); save_json(CART_LOG_FILE, logs); st.session_state.cart.append(p); st.success("Added to Cart"); st.rerun()
            with c2:
                if st.button("Buy Now", type="primary", use_container_width=True, key="detail_buy"):
                    oid=create_order([p], p['final'])
                    whatsapp_msg = get_whatsapp_msg(oid, [p])
                    st.success(f"Order {oid} Placed")
                    st.link_button(f"WhatsApp Confirm {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}", type="primary", use_container_width=True)
            st.divider()
            st.subheader("Highlights")
            st.write(p.get('highlights',''))
            st.divider()
            st.subheader("Description")
            st.write(p.get('full_desc',''))
            st.divider()
            st.subheader("Specifications")
            st.write(p.get('specs',''))
            if st.button("⬅ Back", use_container_width=True, key="back2"):
                st.session_state.selected_product=None; st.rerun()
        else:
            st.session_state.selected_product=None; st.rerun()
    else:
        # CLEAN DROPDOWN - NO EXTRA TEXT - JUST SELECT CATEGORY
        st.write("Select Category:")
        category_options = ["All"] + NEW_DARAZ_CATEGORIES
        selected_from_dropdown = st.selectbox("Category", category_options, index=category_options.index(st.session_state.selected_category) if st.session_state.selected_category in category_options else 0, label_visibility="collapsed")
        if selected_from_dropdown != st.session_state.selected_category:
            st.session_state.selected_category = selected_from_dropdown
            st.rerun()
        
        search=st.text_input("", placeholder="Search products...", label_visibility="collapsed")
        
        if cart_count>0:
            with st.container(border=True):
                st.subheader(f"Cart - {cart_count} Products")
                for i,item in enumerate(st.session_state.cart):
                    ca,cb=st.columns([3,1])
                    with ca: st.write(f"**{item['name']}** - Rs.{item['final']}")
                    with cb:
                        if st.button("X", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
                st.divider()
                st.write(f"**Total: Rs.{cart_total}**")
                if st.button(f"Checkout Rs.{cart_total}", type="primary", use_container_width=True):
                    oid=create_order(st.session_state.cart, cart_total)
                    whatsapp_msg = get_whatsapp_msg(oid, st.session_state.cart, cart_total)
                    st.success(f"Order {oid} Placed")
                    st.link_button(f"WhatsApp Confirm Order {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}", type="primary", use_container_width=True)
                if st.button("Clear Cart", use_container_width=True):
                    st.session_state.cart=[]; st.rerun()
        
        prods=st.session_state.products
        if st.session_state.selected_category != "All":
            prods=[p for p in prods if p.get('category','') == st.session_state.selected_category]
        
        if search.strip(): 
            prods=[p for p in prods if search.lower() in p['name'].lower() or search.lower() in p.get('category','').lower()]
        
        st.write(f"{len(prods)} Products")
        
        if len(prods)==0:
            st.info(f"No Products in {st.session_state.selected_category}")
            if st.button("Show All Products", type="primary", use_container_width=True):
                st.session_state.selected_category="All"; st.rerun()
        
        for idx, p in enumerate(prods):
            try:
                real_idx = st.session_state.products.index(p)
            except:
                real_idx = idx
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: pass
                st.write(f"**{p['name']}**")
                st.caption(f"{p.get('category','')}")
                st.markdown(f"""
                <div style="margin:8px 0;">
                <div style="font-size:20px; font-weight:bold; color:#f85606;">Rs. {p['final']}</div>
                <div style="font-size:13px; color:#757575;"><span style="text-decoration:line-through;">Rs. {p.get('sell', p['final'])}</span> <span style="background:#f85606; color:white; padding:2px 6px; border-radius:3px; font-size:11px; margin-left:6px;">-{p.get('discount',0)}%</span></div>
                </div>
                """, unsafe_allow_html=True)
                c1,c2=st.columns(2)
                with c1:
                    if st.button("View Details", key=f"view_{real_idx}_{idx}", use_container_width=True):
                        st.session_state.selected_product=real_idx; st.rerun()
                with c2:
                    if st.button("Add to Cart", key=f"add_{real_idx}_{idx}", use_container_width=True, type="primary"):
                        logs=load_json(CART_LOG_FILE, []); logs.append({"product":p['name'],"time":datetime.now().strftime("%Y-%m-%d %H:%M")}); save_json(CART_LOG_FILE, logs); st.session_state.cart.append(p); st.success("Added!"); st.rerun()
                if st.button(f"Buy Now Rs.{p['final']}", key=f"buy_{real_idx}_{idx}", use_container_width=True):
                    oid=create_order([p], p['final'])
                    whatsapp_msg = get_whatsapp_msg(oid, [p])
                    st.success(f"Order {oid} Placed")
                    st.link_button(f"Confirm on WhatsApp {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}", type="primary", use_container_width=True)
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
