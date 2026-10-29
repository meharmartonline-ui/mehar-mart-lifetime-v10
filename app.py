# MEHAR MART V42 - 7 SYSTEMS - SHORT LINK REMOVED - FINAL
import streamlit as st, os, urllib.parse, pandas as pd
from PIL import Image
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="MEHAR MART V42 - 7 SYSTEMS", layout="wide")

# ★★★ SIRF AAPKA ASLI LINK - NO SHORT LINK ★★★
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

PASS_FILE = "admin_password.txt"
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return f.read().strip()
    return "mehar123"

st.sidebar.title("🔐 ADMIN LOGIN")
pwd = st.sidebar.text_input("Password", type="password", placeholder="mehar123")
if pwd == get_password() and pwd != "": st.session_state.is_admin = True

if st.session_state.is_admin:
    st.sidebar.success("✅ ADMIN LOGIN")
    st.sidebar.metric("👀 Visits", total_visits)
    st.sidebar.metric("📦 Orders", len(st.session_state.orders))
    st.sidebar.divider()
    st.sidebar.subheader("♾️ LIFETIME SYSTEMS")
    menu = st.sidebar.radio("System Select Karo:", 
        ["1. PRODUCT SYSTEM","2. STOCK & EXPIRY","3. SALES & ORDERS","4. MONEY SYSTEM","5. CLIENT SYSTEM","6. DARAZ STORE","7. ORDERS TRACKING"],
        label_visibility="collapsed"
    )
    st.sidebar.divider()
    st.sidebar.info("♾️ YE SYSTEM LIFETIME CHALEGA BHAI!\n\n1 Baar Product Add Karo Roz Sale Add Karo Hisaab Auto Hoga!")
    st.sidebar.text_input("Store Link:", value=STORE_LINK)
    st.sidebar.link_button("🔗 Store Kholo", STORE_LINK, use_container_width=True)
else:
    menu = "6. DARAZ STORE"

if menu == "1. PRODUCT SYSTEM":
    st.header("1. PRODUCT SYSTEM")
    with st.form("prod"):
        name=st.text_input("Product Name *"); sell=st.number_input("Selling Price",0,100000,3500); disc=st.number_input("Discount %",0,90,15)
        final=int(sell*(1-disc/100)) if disc>0 else sell; st.write(f"Final: Rs.{final}")
        buy=st.number_input("Kharid Price",0,100000,2000); stock=st.number_input("Stock",0,10000,50)
        expiry_days=st.number_input("Expiry Days",0,1000,180)
        highlights=st.text_area("Highlights","100% Khalis"); img_file=st.file_uploader("Photo",type=["jpg","png","jpeg"])
        sub=st.form_submit_button("💾 SAVE",use_container_width=True)
        if sub and name:
            img_bytes=img_file.getvalue() if img_file else None
            exp_date = datetime.now() + timedelta(days=expiry_days)
            st.session_state.products.append({"name":name,"sell":sell,"discount":disc,"final":final,"buy":buy,"stock":stock,"expiry":exp_date.strftime("%Y-%m-%d"),"highlights":highlights,"image_bytes":img_bytes})
            st.success("Save!")

elif menu == "2. STOCK & EXPIRY":
    st.header("2. STOCK & EXPIRY")
    if not st.session_state.products: st.warning("No products")
    else:
        for p in st.session_state.products:
            c1,c2,c3=st.columns(3)
            with c1: st.write(f"**{p['name']}** - Stock: {p['stock']}")
            with c2: st.write(f"Expiry: {p['expiry']}")
            with c3:
                if p['stock']<10: st.error("⚠️ Low Stock!")
            st.divider()

elif menu == "3. SALES & ORDERS":
    st.header("3. SALES & ORDERS")
    with st.form("sale"):
        prod_names = [p['name'] for p in st.session_state.products]
        sel_prod = st.selectbox("Product", prod_names) if prod_names else st.text_input("Product")
        qty=st.number_input("Qty",1,1000,1); price=st.number_input("Price",0,100000,3000)
        client=st.text_input("Client"); sub=st.form_submit_button("Sale Add",use_container_width=True)
        if sub:
            st.session_state.sales.append({"date":datetime.now().strftime("%Y-%m-%d"),"product":sel_prod,"qty":qty,"price":price,"total":qty*price,"client":client})
            st.success("Added!")
    if st.session_state.sales: st.dataframe(pd.DataFrame(st.session_state.sales),use_container_width=True)

elif menu == "4. MONEY SYSTEM":
    st.header("4. MONEY SYSTEM")
    if not st.session_state.sales: st.info("Koi sale nahi")
    else:
        df=pd.DataFrame(st.session_state.sales); total_sale=df['total'].sum()
        total_buy=0
        for s in st.session_state.sales:
            for p in st.session_state.products:
                if p['name']==s['product']: total_buy+=p['buy']*s['qty']
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Sale", f"Rs.{total_sale}")
        with c2: st.metric("Kharid", f"Rs.{total_buy}")
        with c3: st.metric("Munafa", f"Rs.{total_sale-total_buy}")
        st.dataframe(df,use_container_width=True)

elif menu == "5. CLIENT SYSTEM":
    st.header("5. CLIENT SYSTEM")
    with st.form("client"):
        cname=st.text_input("Client Name *"); cphone=st.text_input("Phone"); ccity=st.text_input("City")
        cbal=st.number_input("Baqaya",0,1000000,0); sub=st.form_submit_button("Save",use_container_width=True)
        if sub and cname:
            st.session_state.clients.append({"name":cname,"phone":cphone,"city":ccity,"baqaya":cbal,"date":datetime.now().strftime("%Y-%m-%d")})
            st.success("Save!")
    if st.session_state.clients: st.dataframe(pd.DataFrame(st.session_state.clients),use_container_width=True)

elif menu == "6. DARAZ STORE":
    if st.session_state.is_admin: st.header("6. DARAZ STORE - ADMIN")
    else: st.header("🛒 MEHAR MART OFFICIAL STORE")
    st.success(f"🔗 STORE LINK: {STORE_LINK}")
    st.code(STORE_LINK, language="text")
    st.caption(f"👀 {total_visits} visits | 🚚 Free Delivery All Pakistan")
    st.link_button("📤 WHATSAPP SHARE", f"https://wa.me/?text={urllib.parse.quote('MEHAR MART Order: '+STORE_LINK)}", use_container_width=True)
    st.divider()
    if len(st.session_state.cart)>0:
        st.warning(f"🛒 Cart: {len(st.session_state.cart)} items")
        total_bill=sum([i['final'] for i in st.session_state.cart])
        for i,item in enumerate(st.session_state.cart):
            ca,cb=st.columns([3,1])
            with ca: st.write(f"{item['name']} - Rs.{item['final']}")
            with cb:
                if st.button("Remove",key=f"rem{i}"): st.session_state.cart.pop(i); st.rerun()
        wa_cart="Salam MEHAR MART! Order:\n"+"\n".join([f"{x['name']} Rs.{x['final']}" for x in st.session_state.cart])+f"\nTotal Rs.{total_bill}\n{STORE_LINK}"
        st.link_button(f"✅ WHATSAPP ORDER Rs.{total_bill}", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_cart)}", type="primary", use_container_width=True)
        if st.button("📦 Tracking Me Save Karo",use_container_width=True):
            st.session_state.orders.append({"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"items":", ".join([x['name'] for x in st.session_state.cart]),"total":total_bill,"status":"WhatsApp"})
            pd.DataFrame(st.session_state.orders).to_csv(ORDER_FILE,index=False)
            st.session_state.cart=[]; st.success("Save!"); st.rerun()
        st.divider()
    if not st.session_state.products: st.warning("Product nahi - 1. PRODUCT SYSTEM me add karo")
    else:
        cols=st.columns(2)
        for idx,p in enumerate(st.session_state.products):
            with cols[idx%2]:
                with st.container(border=True):
                    if p.get('image_bytes'): st.image(Image.open(io.BytesIO(p['image_bytes'])),use_column_width=True)
                    st.markdown(f"**{p['name']}**"); st.markdown(f"~~Rs.{p['sell']}~~ **Rs.{p['final']}** ({p['discount']}% OFF)")
                    if st.button(f"🛒 Add to Cart",key=f"add{idx}",use_container_width=True):
                        st.session_state.cart.append(p); st.toast("Cart me!",icon="🛒"); st.rerun()
                    wa_msg=f"Salam! {p['name']} Rs.{p['final']} - {STORE_LINK}"
                    st.link_button("💬 Buy Now",f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(wa_msg)}",use_container_width=True)

elif menu == "7. ORDERS TRACKING":
    st.header("7. ORDERS TRACKING")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Visits",total_visits)
    with c2: st.metric("Orders",len(st.session_state.orders))
    with c3:
        tot=sum([o.get('total',0) for o in st.session_state.orders]); st.metric("Sale",f"Rs.{tot}")
    if os.path.exists(ORDER_FILE):
        df=pd.read_csv(ORDER_FILE); st.dataframe(df,use_container_width=True)
        st.download_button("📥 Excel Download",df.to_csv(index=False),"orders.csv","text/csv",use_container_width=True)
    elif st.session_state.orders: st.dataframe(pd.DataFrame(st.session_state.orders),use_container_width=True)
    else: st.info("Koi order nahi")
