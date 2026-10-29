# MEHAR MART V45 ULTIMATE - V17 to V44 VERIFIED - NOTHING MISS - FINAL
import streamlit as st, os, urllib.parse, pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V45 ULTIMATE", layout="wide")

# ★★★ AAPKA ORIGINAL LINK - NO SHORT LINK - NO 404 ★★★
STORE_LINK = "https://mehar-mart-lifetime-v10-bunjwsm3soskfabyez28bv.streamlit.app"
WA_NUMBER = "923452352112"

if 'products' not in st.session_state: st.session_state.products = []
if 'cart' not in st.session_state: st.session_state.cart = []
if 'sales' not in st.session_state: st.session_state.sales = []
if 'clients' not in st.session_state: st.session_state.clients = []
if 'orders' not in st.session_state: st.session_state.orders = []
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

VISIT_FILE = "visits.txt"
ORDER_FILE = "orders.csv"

def get_visits():
    if os.path.exists(VISIT_FILE):
        try:
            with open(VISIT_FILE,"r") as f: return int(f.read().strip())
        except: return 0
    return 0

def add_visit_once():
    if 'visit_counted' not in st.session_state:
        v = get_visits() + 1
        with open(VISIT_FILE,"w") as f: f.write(str(v))
        st.session_state.visit_counted = True
        return v
    return get_visits()

total_visits = add_visit_once()

if os.path.exists(ORDER_FILE) and 'orders_loaded' not in st.session_state:
    try:
        st.session_state.orders = pd.read_csv(ORDER_FILE).to_dict('records')
        st.session_state.orders_loaded = True
    except: pass

def get_password():
    if os.path.exists("admin_password.txt"):
        with open("admin_password.txt","r") as f: return f.read().strip()
    return "mehar123"

st.sidebar.title("🔐 ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
if pwd == get_password() and pwd != "": st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    st.sidebar.metric("👀 Total Visits", total_visits)
    st.sidebar.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.metric("🛒 Cart", len(st.session_state.cart))
    menu = st.sidebar.radio("System Select Karo:", 
        ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"],
        label_visibility="collapsed"
    )
    st.sidebar.divider()
    st.sidebar.info("♾️ YE SYSTEM LIFETIME CHALEGA BHAI!\n1 Baar Product Add Karo Roz Sale Add Karo Hisaab Auto Hoga!")
    st.sidebar.text_input("Store Link - Copy Karo:", value=STORE_LINK)
    st.sidebar.link_button("🔗 Store Kholo", STORE_LINK, use_container_width=True)
else:
    menu = "6. DARAZ STORE"

# 1. PRODUCT SYSTEM - V17 + V20 COMPLETE
if menu == "1. PRODUCT SYSTEM":
    st.header("MEHAR MART V17 PROFIT LIVE Wala - COMPLETE")
    st.caption(f"Store: {STORE_LINK}")
    
    category = st.selectbox("Category", ["PURE HONEY","SIDR HONEY","BERI HONEY","OTHER"], index=0)
    product_name = st.text_input("Product Name *", placeholder="PURE HONEY - Beri Flowers honey")
    
    col_k, col_b = st.columns(2)
    with col_k:
        kharid_rate = st.number_input("Kharid Rate *", min_value=0, max_value=100000, value=2000, step=1)
    with col_b:
        bechne_rate = st.number_input("Bechne Rate *", min_value=0, max_value=100000, value=2500, step=1)
    
    discount_per = st.number_input("Discount %", min_value=0, max_value=90, value=15, step=1)
    stock = st.number_input("Stock", min_value=0, max_value=10000, value=50, step=1)
    brand = st.text_input("Brand", value="MEHAR MART")
    
    # ★★★ LIVE HISAAB - V17 WALA - 4 BOX ★★★
    customer_pay = int(bechne_rate * (1 - discount_per/100))
    profit = customer_pay - kharid_rate
    profit_per = int((profit/kharid_rate*100)) if kharid_rate>0 else 0
    
    st.divider()
    st.subheader("💰 LIVE HISAAB - Box Me")
    st.caption(f"Top pe Discount % {discount_per} us ke neeche Kharid us ke neeche Selling us ke neeche Customer Pay Box us ke neeche Profit Box tha - Aapki baat ke mutabiq")
    
    b1,b2,b3,b4 = st.columns(4)
    with b1:
        st.metric("Kharid Rate", f"Rs.{kharid_rate}")
        st.code(f"Kharid: {kharid_rate}")
    with b2:
        st.metric("Bechne Rate", f"Rs.{bechne_rate}")
        st.code(f"Selling: {bechne_rate}")
    with b3:
        st.metric("Customer Pay Karega", f"Rs.{customer_pay}", delta=f"-{discount_per}% Discount")
        st.success(f"**Customer Pay Box**\nRs.{customer_pay}")
    with b4:
        st.metric("PROFIT", f"Rs.{profit}", delta=f"{profit_per}% Munafa")
        if profit>0:
            st.success(f"**Profit Box**\nRs.{profit}")
        else:
            st.error(f"**Profit Box LOSS**\nRs.{profit}")
    
    if profit<200 and profit>=0:
        st.warning(f"⚠️ Profit kam hai Rs.{profit} - Discount kam karo ya Bechne Rate badhao!")
    elif profit>500:
        st.success(f"✅ MASHALLAH Zabardast Profit Rs.{profit} - {profit_per}%")
    
    st.divider()
    
    # ★★★ V20 WALE 3 BOX - AAPKI BLUE CIRCLE WALI SCREENSHOT ★★★
    st.subheader("📝 V20 Wale 3 Boxes - Jo Miss The - Ab Wapas")
    
    highlights = st.text_area("Highlights (Khali Hai)", placeholder="100% Pure\nNo Sugar", height=120, key="high")
    full_desc = st.text_area("Full Description (Khali Hai)", placeholder="Full detail...\nShahad k faide...", height=150, key="full")
    specs = st.text_area("Specifications (Khali Hai)", placeholder="Weight: 500gm\nOrigin: Pakistan", height=120, key="spec")
    
    st.subheader("📸 Photo Upload")
    img_file = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"], help="200MB per file • JPG, PNG")
    st.caption("200MB per file • JPG, PNG")
    
    st.divider()
    if st.button("💾 SAVE PRODUCT - LIVE HISAAB KE SAATH", use_container_width=True, type="primary"):
        if product_name:
            img_bytes = img_file.getvalue() if img_file else None
            exp_date = datetime.now() + timedelta(days=180)
            st.session_state.products.append({
                "name":product_name,"category":category,"sell":bechne_rate,"kharid":kharid_rate,
                "discount":discount_per,"final":customer_pay,"buy":kharid_rate,"stock":stock,
                "expiry":exp_date.strftime("%Y-%m-%d"),"profit":profit,"profit_per":profit_per,
                "brand":brand,"highlights":highlights,"full_desc":full_desc,"specs":specs,
                "image_bytes":img_bytes,"date":datetime.now().strftime("%Y-%m-%d")
            })
            st.balloons()
            st.success(f"✅ {product_name} Save Ho Gaya! Customer Pay Rs.{customer_pay} | Profit Rs.{profit} ({profit_per}%)")
        else:
            st.error("❌ Product Name likho Bhai!")

    if st.session_state.products:
        st.divider()
        st.subheader(f"📦 Saved Products ({len(st.session_state.products)})")
        for idx,p in enumerate(st.session_state.products):
            with st.container(border=True):
                c1,c2,c3 = st.columns([1,2,1])
                with c1:
                    if p.get('image_bytes'):
                        st.image(Image.open(io.BytesIO(p['image_bytes'])), width=100)
                with c2:
                    st.write(f"**{p['name']}** - {p['category']}")
                    st.write(f"Kharid Rs.{p['kharid']} | Bechna Rs.{p['sell']} | Discount {p['discount']}% | Customer Pay Rs.{p['final']} | Profit Rs.{p['profit']}")
                    st.caption(f"Highlights: {p.get('highlights','')[:50]} | Specs: {p.get('specs','')[:50]}")
                with c3:
                    if st.button(f"🗑️ Delete", key=f"del_prod_{idx}"):
                        st.session_state.products.pop(idx)
                        st.rerun()

# 2. STOCK & EXPIRY
elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if not st.session_state.products: st.warning("Koi product nahi - 1. PRODUCT SYSTEM me add karo")
    else:
        for p in st.session_state.products:
            with st.container(border=True):
                c1,c2,c3,c4 = st.columns(4)
                with c1: st.write(f"**{p['name']}**"); st.caption(p['category'])
                with c2: st.metric("Stock", p['stock']); st.metric("Profit", f"Rs.{p.get('profit',0)}")
                with c3: st.write(f"Expiry: {p['expiry']}"); st.write(f"Brand: {p.get('brand','')}")
                with c4:
                    if p['stock']<10: st.error("⚠️ Low Stock!")
                    else: st.success("✅ Stock OK")
                    exp = datetime.strptime(p['expiry'],"%Y-%m-%d")
                    if exp < datetime.now() + timedelta(days=30): st.error("⚠️ Expiry Near!")
                st.caption(f"H: {p.get('highlights','')} | D: {p.get('full_desc','')[:60]} | S: {p.get('specs','')}")

# 3. SALES & ORDERS
elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS - Roz Sale")
    with st.form("sale_form"):
        prod_names = [p['name'] for p in st.session_state.products]
        sel_prod = st.selectbox("Product", prod_names) if prod_names else st.text_input("Product Name")
        qty = st.number_input("Qty Sold", 1, 1000, 1)
        client = st.text_input("Client Name")
        submit = st.form_submit_button("Sale Add Karo", use_container_width=True)
        if submit:
            price=0; buy=0
            for p in st.session_state.products:
                if p['name']==sel_prod: price=p['final']; buy=p['buy']
            st.session_state.sales.append({"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"product":sel_prod,"qty":qty,"price":price,"buy":buy,"total":qty*price,"profit":(price-buy)*qty,"client":client})
            st.success(f"Sale Added! Profit Rs.{(price-buy)*qty}")
    if st.session_state.sales:
        df=pd.DataFrame(st.session_state.sales)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Profit from Sales", f"Rs.{df['profit'].sum()}")

# 4. MONEY SYSTEM
elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM - Munafa Hisaab")
    if not st.session_state.sales: st.info("Abhi koi sale nahi")
    else:
        df=pd.DataFrame(st.session_state.sales)
        c1,c2,c3 = st.columns(3)
        with c1: st.metric("💰 Total Sale", f"Rs.{df['total'].sum()}")
        with c2: st.metric("🛒 Total Kharid", f"Rs.{(df['buy']*df['qty']).sum()}")
        with c3: st.metric("📈 Total Munafa", f"Rs.{df['profit'].sum()}")
        st.dataframe(df, use_container_width=True)

# 5. CLIENT SYSTEM
elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    with st.form("client_form"):
        cname=st.text_input("Client Name *"); cphone=st.text_input("Phone"); ccity=st.text_input("City")
        cbal=st.number_input("Baqaya Rs.",0,1000000,0); sub=st.form_submit_button("Client Save",use_container_width=True)
        if sub and cname:
            st.session_state.clients.append({"name":cname,"phone":cphone,"city":ccity,"baqaya":cbal,"date":datetime.now().strftime("%Y-%m-%d")})
            st.success("Client Save!")
    if st.session_state.clients:
        st.dataframe(pd.DataFrame(st.session_state.clients), use_container_width=True)

# 6. DARAZ STORE
elif menu == "6. DARAZ STORE":
    if st.session_state.is_admin: st.header("6. DARAZ STORE - ADMIN VIEW")
    else: st.header("🛒 MEHAR MART - OFFICIAL STORE")
    st.success(f"🔗 STORE LINK: {STORE_LINK} - COPY KARKE SHARE KARO")
    st.code(STORE_LINK, language="text")
    st.caption(f"👀 {total_visits} log dekh chuke hain | 🚚 Free Delivery All Pakistan")
    st.link_button("📤 WHATSAPP SHARE", f"https://wa.me/?text={urllib.parse.quote('MEHAR MART Order Karo: '+STORE_LINK)}", use_container_width=True)
    st.divider()
    if len(st.session_state.cart)>0:
        st.warning(f"🛒 Aapke Cart me {len(st.session_state.cart)} items hain")
        total_bill=sum([i['final'] for i in st.session_state.cart])
        total_profit_cart=sum([i.get('profit',0) for i in st.session_state.cart])
        for i,item in enumerate(st.session_state.cart):
            ca,cb=st.columns([3,1])
            with ca: st.write(f"{i+1}. {item['name']} - Rs.{item['final']} (Profit Rs.{item.get('profit',0)}) | {item.get('highlights','')[:30]}")
            with cb:
                if st.button("Remove",key=f"rem_cart_{i}"): st.session_state.cart.pop(i); st.rerun()
        st.markdown(f"### 💰 Total Bill: Rs.{total_bill} | Aapka Munafa: Rs.{total_profit_cart}")
        wa_cart_text = f"Salam MEHAR MART! Mera Order:\n" + "\n".join([f"{x['name']} - Rs.{x['final']} - {x.get('specs','')}" for x in st.session_state.cart]) + f"\n\nTotal Bill: Rs.{total_bill}\nStore: {STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER - Rs.{total_bill}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_cart_text)}", type="primary", use_container_width=True)
        col_a,col_b = st.columns(2)
        with col_a:
            if st.button("📦 Order Tracking Me Save Karo", use_container_width=True):
                st.session_state.orders.append({"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"items":", ".join([x['name'] for x in st.session_state.cart]),"total":total_bill,"profit":total_profit_cart,"status":"WhatsApp Sent"})
                pd.DataFrame(st.session_state.orders).to_csv(ORDER_FILE,index=False)
                st.success("✅ Order Tracking Me Save Ho Gaya!")
                st.session_state.cart=[]
                st.rerun()
        with col_b:
            if st.button("❌ Cart Khali Karo", use_container_width=True):
                st.session_state.cart=[]
                st.rerun()
        st.divider()
    if not st.session_state.products: st.warning("Abhi koi product nahi - Admin se 1. PRODUCT SYSTEM me add karwao")
    else:
        cols=st.columns(2)
        for idx,p in enumerate(st.session_state.products):
            with cols[idx%2]:
                with st.container(border=True):
                    if p.get('image_bytes'):
                        st.image(Image.open(io.BytesIO(p['image_bytes'])), use_column_width=True)
                    st.markdown(f"**{p['name']}** - {p['category']}")
                    st.markdown(f"~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF)")
                    st.caption(f"{p.get('highlights','')} | {p.get('specs','')}")
                    st.caption(f"Profit: Rs.{p.get('profit',0)} | Stock: {p['stock']} | Free Delivery")
                    b1,b2 = st.columns(2)
                    with b1:
                        if st.button(f"🛒 Add to Cart", key
