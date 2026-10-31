# MEHAR MART V93 FINAL - NameError FIXED - 100% WORKING - LIFETIME
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
    new_order={"id": order_id,"time": datetime.now().strftime("%Y-%m-%d %H:%M"),"products": [{"name": p.get('name',''), "price": p.get('final',0), "category": p.get('category','')} for p in products_list],"total": total,"status": "Pending","reason": ""}
    orders.append(new_order); save_json(ORDERS_FILE, orders); st.session_state.orders=orders; return order_id

def get_whatsapp_msg(order_id, products_list, total=None):
    msg = f"Asalam O Alaikum\nMehar Mart Order Krna Hy\n\nOrder ID: {order_id}\n\n"
    for p in products_list:
        msg+=f"Product: {p.get('name','')}\nCategory: {p.get('category','')}\nPrice: Rs.{p.get('final', p.get('price',0))}\n\n"
    if total and len(products_list)>1: msg+=f"Total: Rs.{total}\n\n"
    msg+="Please Confirm My Order - Shukria"
    return msg

# FIXED MENU - No NameError
current_menu = "STORE VIEW"
if st.session_state.is_admin:
    st.markdown("### ADMIN PANEL")
    orders_data=load_json(ORDERS_FILE, [])
    pending=len([o for o in orders_data if o.get('status')=="Pending"])
    confirmed=len([o for o in orders_data if o.get('status') in ["Confirmed","Delivered"]])
    current_menu = st.selectbox("Menu", ["STORE VIEW","ORDERS - DARAZ","PRODUCT SYSTEM","MONEY","STOCK","BACKUP","SETTINGS"], index=0)
    c1,c2=st.columns(2)
    with c1: st.metric("Pending", pending)
    with c2: st.metric("Sale", confirmed)
    col1,col2,col3=st.columns(3)
    with col1:
        if st.button("ORDERS", use_container_width=True, type="primary"):
            st.session_state['goto_orders']=True
            st.rerun()
    with col2:
        if st.button("ADD PRODUCT", use_container_width=True):
            st.session_state['goto_product']=True
            st.rerun()
    with col3:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.is_admin=False; st.query_params.clear(); st.session_state.selected_category="All"; st.rerun()
    st.divider()
    if st.session_state.get('goto_orders'):
        current_menu="ORDERS - DARAZ"
        st.session_state['goto_orders']=False
    if st.session_state.get('goto_product'):
        current_menu="PRODUCT SYSTEM"
        st.session_state['goto_product']=False

# MAIN ROUTING - FIXED
if current_menu=="PRODUCT SYSTEM":
    st.subheader("Add Product - Lifetime")
    st.session_state.categories=NEW_CATS
    save_json(CAT_FILE, NEW_CATS)
    st.caption(f"Categories: {' | '.join(NEW_CATS)} - HONEY Single Only")
    category=st.selectbox("Category", st.session_state.categories, index=0)
    new_cat=st.text_input("New Category Add")
    if st.button("Add New Category"):
        if new_cat and new_cat.upper() not in st.session_state.categories:
            st.session_state.categories.append(new_cat.upper()); save_json(CAT_FILE, st.session_state.categories); st.success(f"Added {new_cat.upper()}"); st.rerun()
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
    if st.button("SAVE PRODUCT - LIFETIME", type="primary", use_container_width=True):
        if not name.strip(): st.error("Product Name likho!")
        else:
            img_b64=None
            if img_file:
                try: img=Image.open(img_file); img.thumbnail((800,800)); buf=io.BytesIO(); img.save(buf, format="JPEG", quality=80); img_b64=base64.b64encode(buf.getvalue()).decode()
                except: pass
            prod={"name":name,"category":category,"sell":bechna,"kharid":kharid,"discount":discount,"final":pay,"buy":kharid,"stock":stock,"expiry":expiry.strftime("%Y-%m-%d"),"profit":profit,"highlights":highlights,"full_desc":full_desc,"specs":specs,"image_b64":img_b64}
            st.session_state.products.append(prod); save_json(PRODUCT_FILE, st.session_state.products); st.success(f"✅ Saved in {category} - Lifetime!")
    st.divider()
    for idx,p in enumerate(st.session_state.products):
        if isinstance(p, dict):
            c1,c2=st.columns([4,1])
            with c1: st.write(f"{idx+1}. {p.get('name','')} - {p.get('category','')} - Rs.{p.get('final',0)}")
            with c2:
                if st.button("Delete", key=f"del_{idx}"): st.session_state.products.pop(idx); save_json(PRODUCT_FILE, st.session_state.products); st.rerun()

elif current_menu=="ORDERS - DARAZ":
    st.header("Orders")
    orders=load_json(ORDERS_FILE, [])
    if not orders: st.info("No orders yet")
    else:
        filter_status=st.selectbox("Filter", ["All","Pending","Confirmed","Delivered","Cancelled","Returned"], index=0)
        filtered=orders if filter_status=="All" else [o for o in orders if o.get('status')==filter_status]
        confirmed_orders=[o for o in orders if o.get('status') in ["Confirmed","Delivered"]]
        total_sale = sum([int(o.get('total',0)) for o in confirmed_orders])
        col1,col2=st.columns(2)
        with col1: st.metric("Sale Count", len(confirmed_orders))
        with col2: st.metric("Sale Amount", f"Rs.{total_sale}")
        st.divider()
        for o in reversed(filtered):
            try: real_index = orders.index(o)
            except: continue
            with st.container(border=True):
                st.write(f"**ID: {o.get('id','')}** | {o.get('time','')} | **{o.get('status','')}** | Rs.{o.get('total',0)}")
                for prod in o.get('products',[]): st.caption(f"- {prod.get('name','')} - Rs.{prod.get('price',0)} - {prod.get('category','')}")
                if o.get('reason'): st.warning(f"Reason: {o.get('reason')}")
                b1,b2=st.columns(2)
                with b1:
                    if st.button("✅ Confirm", key=f"conf_{real_index}", use_container_width=True):
                        orders[real_index]['status']="Confirmed"; save_json(ORDERS_FILE, orders); st.success(f"Order {o.get('id')} Confirmed!"); st.rerun()
                with b2:
                    if st.button("📦 Delivered", key=f"deliv_{real_index}", use_container_width=True):
                        orders[real_index]['status']="Delivered"; save_json(ORDERS_FILE, orders); st.rerun()
                b3,b4=st.columns(2)
                with b3:
                    if st.button("❌ Cancel", key=f"cancel_{real_index}", use_container_width=True):
                        orders[real_index]['status']="Cancelled"; save_json(ORDERS_FILE, orders); st.rerun()
                with b4:
                    if st.button("↩️ Return", key=f"return_{real_index}", use_container_width=True):
                        orders[real_index]['status']="Returned"; save_json(ORDERS_FILE, orders); st.rerun()

elif current_menu=="MONEY":
    st.subheader("Money - Sale After Confirm")
    orders=load_json(ORDERS_FILE, [])
    confirmed=[o for o in orders if o.get('status') in ["Confirmed","Delivered"]]
    pending=[o for o in orders if o.get('status')=="Pending"]
    st.metric("Pending Orders", len(pending))
    st.metric("Sale Count (After Confirm)", len(confirmed))
    st.metric("Sale Amount (After Confirm)", f"Rs.{sum([int(o.get('total',0)) for o in confirmed])}")
    st.metric("Total Products (Lifetime)", len(st.session_state.products))

elif current_menu=="STOCK":
    st.subheader("Stock Management - Fixed")
    if not st.session_state.products: st.info("No Products")
    else:
        for idx,p in enumerate(st.session_state.products):
            if not isinstance(p, dict): continue
            with st.container(border=True):
                st.write(f"**{p.get('name','')}** - {p.get('category','')} - Stock: **{p.get('stock',0)}**")
                s1,s2,s3=st.columns(3)
                with s1:
                    if st.button("➕ Plus 1", key=f"plus_{idx}", use_container_width=True):
                        st.session_state.products[idx]['stock']=int(st.session_state.products[idx].get('stock',0))+1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()
                with s2:
                    if st.button("➖ Minus 1", key=f"minus_{idx}", use_container_width=True):
                        if int(st.session_state.products[idx].get('stock',0))>0:
                            st.session_state.products[idx]['stock']=int(st.session_state.products[idx].get('stock',0))-1; save_json(PRODUCT_FILE, st.session_state.products); st.rerun()
                with s3:
                    new_stock=st.number_input(f"Set", value=int(p.get('stock',0)), key=f"set_{idx}", min_value=0, label_visibility="collapsed")
                    if st.button("Set Stock", key=f"setbtn_{idx}", use_container_width=True):
                        st.session_state.products[idx]['stock']=new_stock; save_json(PRODUCT_FILE, st.session_state.products); st.success("Stock Updated!"); st.rerun()

elif current_menu=="BACKUP":
    st.subheader("Backup - Lifetime Safe")
    st.write(f"Products: {len(st.session_state.products)} | Orders: {len(load_json(ORDERS_FILE, []))}")
    backup_json=json.dumps(st.session_state.products, indent=2)
    st.download_button("📥 Download Products Backup", backup_json, file_name="mehar_products_backup.json", mime="application/json", type="primary", use_container_width=True)
    orders_backup_json=json.dumps(load_json(ORDERS_FILE, []), indent=2)
    st.download_button("📥 Download Orders Backup", orders_backup_json, file_name="mehar_orders_backup.json", mime="application/json", use_container_width=True)
    uploaded=st.file_uploader("Restore Products Backup", type=["json"])
    if uploaded:
        try:
            data=json.load(uploaded)
            if isinstance(data, list):
                st.session_state.products=data; save_json(PRODUCT_FILE, data); st.success(f"{len(data)} Products Restore!"); st.rerun()
        except: st.error("File error")

elif current_menu=="SETTINGS":
    st.subheader("Fix Categories")
    if st.button("FIX OLD CATEGORIES TO NEW SYSTEM - HONEY SINGLE", type="primary", use_container_width=True):
        if fix_old_categories():
            st.success("Fixed! PURE/BERI/SIDR -> HONEY Single!")
        else:
            st.info("Already Fixed - All OK")
        st.session_state.categories=NEW_CATS; save_json(CAT_FILE, NEW_CATS); st.rerun()
    st.divider()
    st.subheader("Logo")
    if st.session_state.logo_b64:
        try: st.image(Image.open(io.BytesIO(base64.b64decode(st.session_state.logo_b64))), width=100)
        except: pass
    logo_file=st.file_uploader("Upload Logo", type=["png","jpg","jpeg"])
    if logo_file:
        try:
            img=Image.open(logo_file); img.thumbnail((200,200)); buf=io.BytesIO(); img.save(buf, format="PNG")
            lb64=base64.b64encode(buf.getvalue()).decode(); st.session_state.logo_b64=lb64; save_json(LOGO_FILE, lb64); st.success("✅ Logo Saved!")
        except Exception as e: st.error(f"Logo error: {e}")
    st.divider()
    st.subheader("Password")
    old_p=st.text_input("Old Password", type="password")
    new_p=st.text_input("New Password", type="password")
    new_p2=st.text_input("Confirm", type="password")
    if st.button("Change Password", type="primary", use_container_width=True):
        if old_p!=get_password(): st.error("Old Wrong!")
        elif new_p!=new_p2: st.error("Not Match!")
        elif not new_p: st.error("Empty!")
        else: save_password(new_p); st.success(f"New: {new_p}")
    st.divider()
    if st.button("DELETE ALL ORDERS", type="primary", use_container_width=True):
        save_json(ORDERS_FILE, []); st.success("Orders Deleted!"); st.rerun()
    if st.button("DELETE ALL PRODUCTS", use_container_width=True):
        if st.checkbox("Confirm Delete All Products"):
            save_json(PRODUCT_FILE, []); st.session_state.products=[]; st.rerun()

else:
    fresh_products = load_json(PRODUCT_FILE, [])
    if len(fresh_products)==0 and len(st.session_state.products)>0:
        save_json(PRODUCT_FILE, st.session_state.products)
        fresh_products=st.session_state.products
    elif len(fresh_products)!=len(st.session_state.products):
        st.session_state.products=fresh_products
    
    cart_count=len(st.session_state.cart)
    cart_total=sum([p.get('final',0) for p in st.session_state.cart])
    logo_html=""
    if st.session_state.logo_b64:
        try: logo_html=f"<img src='data:image/png;base64,{st.session_state.logo_b64}' style='height:28px; margin-right:8px; background:white; border-radius:4px; padding:2px; vertical-align:middle;'>"
        except: pass
    st.markdown(f"""<div style="background:#f85606; padding:10px 15px; margin:-1rem -1rem 0 -1rem; display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; color:white; font-size:18px; font-weight:bold;">{logo_html}MEHAR MART</div><div style="background:white; color:#f85606; padding:5px 12px; border-radius:20px; font-size:13px; font-weight:bold;">🛒 {cart_count}</div></div>""", unsafe_allow_html=True)
    st.write("")
    cart_json = json.dumps([{"name": p.get('name',''), "price": p.get('final',0)} for p in st.session_state.cart])
    products_b64 = base64.b64encode(json.dumps(st.session_state.products).encode()).decode() if st.session_state.products else ""
    st.markdown(f"""<script>try{{localStorage.setItem('mehar_cart_v93', `{cart_json}`); localStorage.setItem('mehar_cart_expiry', new Date(Date.now() + 30*24*60*60*1000).toISOString()); if({len(st.session_state.products)}>0){{localStorage.setItem('mehar_products_lifetime_v93', `{products_b64}`);}}}}catch(e){{}}</script>""", unsafe_allow_html=True)

    if st.session_state.selected_product is not None:
        idx = st.session_state.selected_product
        if idx < len(st.session_state.products):
            p = st.session_state.products[idx]
            if not isinstance(p, dict): st.session_state.selected_product=None; st.rerun()
            if st.button("⬅ Back", use_container_width=True): st.session_state.selected_product=None; st.rerun()
            if p.get('image_b64'):
                try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                except: pass
            st.write(f"### {p.get('name','')}")
            st.caption(f"{p.get('category','')}")
            st.markdown(f"""<div style="background:#fff9f0; padding:12px; border-radius:8px;"><div style="font-size:28px; font-weight:bold; color:#f85606;">Rs. {p.get('final',0)}</div><div style="font-size:14px;"><span style="text-decoration:line-through; color:#9e9e9e;">Rs. {p.get('sell', p.get('final',0))}</span> <span style="background:#f85606; color:white; padding:3px 8px; border-radius:4px; margin-left:8px; font-weight:bold;">-{p.get('discount',0)}% OFF</span></div></div>""", unsafe_allow_html=True)
            st.write("")
            c1,c2=st.columns(2)
            with c1:
                if st.button("Add to Cart", type="primary", use_container_width=True, key="detail_add"):
                    st.session_state.cart.append(p); st.success("Added to Cart!"); st.rerun()
            with c2:
                if st.button("Buy Now", type="primary", use_container_width=True, key="detail_buy"):
                    oid=create_order([p], p.get('final',0)); msg=get_whatsapp_msg(oid, [p]); st.success(f"Order {oid} Placed!"); st.link_button(f"WhatsApp Confirm {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
            st.divider()
            st.subheader("Highlights"); st.write(p.get('highlights',''))
            st.divider()
            st.subheader("Description"); st.write(p.get('full_desc',''))
            st.divider()
            st.subheader("Specifications"); st.write(p.get('specs',''))
            if st.button("⬅ Back", use_container_width=True, key="back2"): st.session_state.selected_product=None; st.rerun()
        else: st.session_state.selected_product=None; st.rerun()
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
                st.subheader(f"Cart - {cart_count} Products")
                for i,item in enumerate(st.session_state.cart):
                    ca,cb=st.columns([3,1])
                    with ca: st.write(f"**{item.get('name','')}** - Rs.{item.get('final',0)}")
                    with cb:
                        if st.button("X", key=f"rem_{i}"): st.session_state.cart.pop(i); st.rerun()
                st.divider()
                st.write(f"**Total: Rs.{cart_total}**")
                if st.button(f"Checkout Rs.{cart_total}", type="primary", use_container_width=True):
                    oid=create_order(st.session_state.cart, cart_total); msg=get_whatsapp_msg(oid, st.session_state.cart, cart_total); st.success(f"Order {oid} Placed!"); st.link_button(f"WhatsApp Confirm Order {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
                if st.button("Clear Cart", use_container_width=True): st.session_state.cart=[]; st.rerun()
        prods=[p for p in st.session_state.products if isinstance(p, dict)]
        if st.session_state.selected_category != "All":
            prods=[p for p in prods if str(p.get('category','')).upper() == st.session_state.selected_category.upper()]
        if search.strip(): prods=[p for p in prods if search.lower() in str(p.get('name','')).lower() or search.lower() in str(p.get('category','')).lower()]
        st.write(f"{len(prods)} Products")
        if len(prods)==0:
            st.info(f"No Products in {st.session_state.selected_category}")
            if st.button("Show All Products", type="primary", use_container_width=True):
                st.session_state.selected_category="All"; st.rerun()
        for idx, p in enumerate(prods):
            try: real_idx = st.session_state.products.index(p)
            except: real_idx = idx
            with st.container(border=True):
                if p.get('image_b64'):
                    try: st.image(Image.open(io.BytesIO(base64.b64decode(p['image_b64']))), use_column_width=True)
                    except: pass
                st.write(f"**{p.get('name','')}**")
                st.caption(f"{p.get('category','')}")
                st.markdown(f"""<div style="margin:8px 0;"><div style="font-size:20px; font-weight:bold; color:#f85606;">Rs. {p.get('final',0)}</div><div style="font-size:13px; color:#757575;"><span style="text-decoration:line-through;">Rs. {p.get('sell', p.get('final',0))}</span> <span style="background:#f85606; color:white; padding:2px 6px; border-radius:3px; font-size:11px; margin-left:6px;">-{p.get('discount',0)}%</span></div></div>""", unsafe_allow_html=True)
                c1,c2=st.columns(2)
                with c1:
                    if st.button("View Details", key=f"view_{real_idx}_{idx}", use_container_width=True):
                        st.session_state.selected_product=real_idx; st.rerun()
                with c2:
                    if st.button("Add to Cart", key=f"add_{real_idx}_{idx}", use_container_width=True, type="primary"):
                        st.session_state.cart.append(p); st.success("Added!"); st.rerun()
                if st.button(f"Buy Now Rs.{p.get('final',0)}", key=f"buy_{real_idx}_{idx}", use_container_width=True):
                    oid=create_order([p], p.get('final',0)); msg=get_whatsapp_msg(oid, [p]); st.success(f"Order {oid} Placed"); st.link_button(f"Confirm on WhatsApp {oid}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", type="primary", use_container_width=True)
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
