# MEHAR MART V104 - PERMANENT CLOUD EDITION
# Streamlit storefront + Supabase database
# Keep the Supabase secret key ONLY in Streamlit Cloud Secrets.

import streamlit as st
import os, json, io, base64, urllib.parse, hashlib, hmac, secrets, uuid
from datetime import datetime, timedelta, date
from PIL import Image
from supabase import create_client, Client

st.set_page_config(page_title="Mehar Mart", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

WA_NUMBER = "923452352112"
NEW_CATS = ["HONEY", "HOME & DECOR", "KITCHEN GADGETS", "HEALTH CARE & BEAUTY", "SKIN CARE PRODUCTS", "OTHER"]
LOCAL_FILES = {
    "products": "products.json",
    "orders": "orders.json",
    "categories": "categories.json",
    "logo": "logo.json",
}
DEFAULT_LOGO = None

# ---------- SUPABASE CONNECTION ----------
def get_secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return os.environ.get(name, default)

SUPABASE_URL = str(get_secret("SUPABASE_URL", "")).strip()
# Server-side secret key is recommended for this private Streamlit backend.
SUPABASE_KEY = str(get_secret("SUPABASE_SECRET_KEY", "")).strip()
ADMIN_INITIAL_PASSWORD = str(get_secret("ADMIN_PASSWORD", "")).strip()

@st.cache_resource(show_spinner=False)
def connect_supabase(url, key):
    return create_client(url, key)

db: Client | None = None
db_error = ""
if SUPABASE_URL and SUPABASE_KEY:
    try:
        db = connect_supabase(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        db_error = str(e)
else:
    db_error = "Streamlit Secrets mein SUPABASE_URL aur SUPABASE_SECRET_KEY configure karein."

# ---------- HELPERS ----------
def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def safe_int(value, default=0):
    try:
        return int(float(value))
    except Exception:
        return default

def db_get(table, row_id):
    if db is None:
        return None
    try:
        result = db.table(table).select("data").eq("id", str(row_id)).limit(1).execute()
        return result.data[0]["data"] if result.data else None
    except Exception as e:
        st.error(f"Database read error ({table}): {e}")
        return None

def db_get_all(table):
    if db is None:
        return []
    try:
        result = db.table(table).select("id,data").order("created_at", desc=False).execute()
        return [{"id": r["id"], **(r.get("data") or {})} for r in (result.data or [])]
    except Exception as e:
        st.error(f"Database read error ({table}): {e}")
        return []

def db_upsert(table, row_id, data):
    if db is None:
        raise RuntimeError("Supabase connection is not ready.")
    db.table(table).upsert({"id": str(row_id), "data": data}).execute()

def db_delete(table, row_id):
    if db is None:
        raise RuntimeError("Supabase connection is not ready.")
    db.table(table).delete().eq("id", str(row_id)).execute()

def get_setting(key, default=None):
    return db_get("app_settings", key) if db is not None else default

def set_setting(key, value):
    db_upsert("app_settings", key, value)

def load_products():
    return db_get_all("products") if db is not None else []

def save_product(product):
    db_upsert("products", product["id"], product)

def delete_product(product_id):
    db_delete("products", product_id)

def load_orders():
    return db_get_all("orders") if db is not None else []

def save_order(order):
    db_upsert("orders", order["id"], order)

def load_categories():
    value = get_setting("categories", NEW_CATS)
    return value if isinstance(value, list) and value else NEW_CATS.copy()

def save_categories(items):
    set_setting("categories", items)

def load_logo():
    return get_setting("store_logo", None)

def save_logo(value):
    set_setting("store_logo", value)

def load_local_json(filename, default):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def migrate_v93_local_data():
    """One-time import of V93 JSON files if the cloud database is still empty."""
    if db is None or get_setting("v93_migration_completed", False):
        return
    try:
        existing = db_get_all("products")
        if not existing:
            old_products = load_local_json(LOCAL_FILES["products"], [])
            if not old_products:
                old_products = load_local_json("products_backup.json", [])
            for i, item in enumerate(old_products):
                if not isinstance(item, dict):
                    continue
                item = dict(item)
                item.setdefault("id", str(uuid.uuid4()))
                item["id"] = str(item["id"])
                save_product(item)

        existing_orders = db_get_all("orders")
        if not existing_orders:
            old_orders = load_local_json(LOCAL_FILES["orders"], [])
            if not old_orders:
                old_orders = load_local_json("orders_backup.json", [])
            for i, item in enumerate(old_orders):
                if not isinstance(item, dict):
                    continue
                item = dict(item)
                item.setdefault("id", str(uuid.uuid4()))
                item["id"] = str(item["id"])
                save_order(item)

        cats = load_local_json(LOCAL_FILES["categories"], None)
        if isinstance(cats, list) and cats:
            save_categories(cats)
        logo = load_local_json(LOCAL_FILES["logo"], None)
        if logo:
            save_logo(logo)

        local_sources = [
            "products.json", "products_backup.json", "orders.json", "orders_backup.json",
            "categories.json", "logo.json"
        ]
        if any(os.path.exists(name) for name in local_sources):
            set_setting("v93_migration_completed", True)
            st.session_state["migration_notice"] = "V93 local JSON migration checked. Database is ready."
        else:
            st.session_state["migration_notice"] = "No local V93 JSON files found. Use Backup > Restore to import your saved files."
    except Exception as e:
        st.session_state["migration_error"] = str(e)

def image_to_b64(uploaded):
    if not uploaded:
        return None
    img = Image.open(uploaded).convert("RGB")
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def show_product_image(encoded, width=None):
    if not encoded:
        return
    try:
        st.image(Image.open(io.BytesIO(base64.b64decode(encoded))), width=width, use_container_width=(width is None))
    except Exception:
        st.caption("Product image could not be displayed.")

def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240000)
    return base64.b64encode(salt + digest).decode()

def verify_password(password, stored):
    try:
        raw = base64.b64decode(stored)
        salt, expected = raw[:16], raw[16:]
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240000)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False

def current_password_hash():
    stored = get_setting("admin_password_hash", None)
    if stored:
        return stored
    if ADMIN_INITIAL_PASSWORD:
        stored = hash_password(ADMIN_INITIAL_PASSWORD)
        set_setting("admin_password_hash", stored)
        return stored
    return None

def create_order(cart_items, total):
    orders = load_orders()
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(len(orders) + 1)
    # Keep one line per product and store its ordered quantity explicitly.
    grouped = {}
    for p in cart_items:
        pid = str(p.get("id", ""))
        key = pid or f"legacy-{p.get('name', '')}"
        if key not in grouped:
            grouped[key] = {
                "name": p.get("name", ""),
                "price": safe_int(p.get("final", p.get("price", 0))),
                "category": p.get("category", ""),
                "product_id": pid,
                "quantity": 0,
            }
        grouped[key]["quantity"] += 1
    new_order = {
        "id": order_id,
        "time": now_text(),
        "products": list(grouped.values()),
        "total": safe_int(total),
        "status": "Pending",
        "stock_deducted": False,
        "reason": "",
    }
    save_order(new_order)
    return order_id


def confirm_order_and_deduct_stock(order):
    """Deduct ordered quantities once; never delete a product on order confirmation."""
    if order.get("status") == "Confirmed" or order.get("stock_deducted"):
        order["status"] = "Confirmed"
        save_order(order)
        return "This order was already confirmed; stock was not deducted again."

    # Aggregate quantities by product ID (also supports older orders without quantity).
    quantities = {}
    for item in order.get("products", []):
        pid = str(item.get("product_id", "") or "")
        if not pid:
            continue  # Legacy order line without a product ID: do not guess a product.
        quantities[pid] = quantities.get(pid, 0) + max(1, safe_int(item.get("quantity", 1), 1))

    current_products = {str(p.get("id")): p for p in load_products()}
    missing = [pid for pid in quantities if pid not in current_products]
    if missing:
        raise ValueError("Order product is missing from inventory. No stock was changed; review this order manually.")

    insufficient = []
    for pid, qty in quantities.items():
        product = current_products[pid]
        available = max(0, safe_int(product.get("stock", 0)))
        if qty > available:
            insufficient.append(f"{product.get('name', pid)}: available {available}, ordered {qty}")
    if insufficient:
        raise ValueError("Insufficient stock. No stock was changed. " + "; ".join(insufficient))

    # Save only the updated stock value. The product record remains in Supabase.
    for pid, qty in quantities.items():
        product = current_products[pid]
        product["stock"] = safe_int(product.get("stock", 0)) - qty
        save_product(product)

    order["status"] = "Confirmed"
    order["stock_deducted"] = True
    order["stock_deducted_at"] = now_text()
    save_order(order)
    return "Order confirmed. Stock reduced by ordered quantity; product remains listed (Out of Stock at zero)."

def whatsapp_message(order_id, products_list, total=None):
    msg = f"Asalam O Alaikum\nMehar Mart Order\n\nOrder ID: {order_id}\n\n"
    for p in products_list:
        msg += f"Product: {p.get('name','')}\nCategory: {p.get('category','')}\nPrice: Rs.{p.get('final',p.get('price',0))}\n\n"
    if total is not None:
        msg += f"Total: Rs.{total}\n\n"
    msg += "Please Confirm My Order - Shukria"
    return msg

# ---------- SESSION ----------
for key, default in {
    "cart": [], "is_admin": False, "selected_product": None,
    "selected_category": "All", "admin_authenticated": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- DATABASE STATUS ----------
if db is None:
    st.error("Mehar Mart database connection ready nahi hai.")
    st.code('SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"\nSUPABASE_SECRET_KEY = "sb_secret_..."\nADMIN_PASSWORD = "your-strong-admin-password"', language="toml")
    st.warning("Supabase SQL schema run karein aur Streamlit Cloud → App settings → Secrets mein values add karein.")
    st.stop()

# Verify required tables exist
try:
    db.table("products").select("id").limit(1).execute()
    db.table("orders").select("id").limit(1).execute()
    db.table("app_settings").select("id").limit(1).execute()
except Exception as e:
    st.error("Supabase tables abhi create nahi huin. Package ke `supabase_schema.sql` ko Supabase SQL Editor mein run karein.")
    st.code(str(e))
    st.stop()

migrate_v93_local_data()
if st.session_state.get("migration_error"):
    st.warning("V93 migration notice: " + st.session_state["migration_error"])

# ---------- STYLE ----------
st.markdown("""
<style>
header, footer {visibility:hidden;}
[data-testid="stToolbar"], [data-testid="stAppDeployButton"] {display:none;}
.block-container {padding-top:1rem; padding-bottom:3rem; max-width:1100px;}
.mm-header {background:#f85606;color:white;padding:13px 16px;border-radius:8px;font-size:21px;font-weight:800;display:flex;justify-content:space-between;align-items:center;}
.mm-price {font-size:23px;font-weight:800;color:#f85606;}
.mm-muted {color:#777;font-size:13px;}
</style>
""", unsafe_allow_html=True)

# ---------- ADMIN AUTH ----------
def admin_login():
    st.title("🔐 Mehar Mart Admin Login")
    stored = current_password_hash()
    if not stored:
        st.error("Admin password configure nahi hai. Streamlit Secrets mein ADMIN_PASSWORD add karein.")
        return
    with st.form("admin_login_form"):
        pwd = st.text_input("Admin Password", type="password")
        submitted = st.form_submit_button("LOGIN", type="primary", use_container_width=True)
    if submitted:
        if verify_password(pwd, stored):
            st.session_state.admin_authenticated = True
            st.session_state.is_admin = True
            st.rerun()
        else:
            st.error("Password incorrect.")

# Admin mode via explicit login; no password in URL.
if st.query_params.get("admin") == "1" and not st.session_state.admin_authenticated:
    admin_login()
    st.stop()

if st.session_state.admin_authenticated:
    st.session_state.is_admin = True

# ---------- ADMIN PANEL ----------
if st.session_state.is_admin:
    st.markdown('<div class="mm-header">MEHAR MART — ADMIN PANEL <span>☁️ V104</span></div>', unsafe_allow_html=True)
    products = load_products()
    orders = load_orders()
    menu = st.selectbox("Admin Menu", ["DASHBOARD", "STORE VIEW", "PRODUCT SYSTEM", "ORDERS - DARAZ", "MONEY", "STOCK", "BACKUP", "SETTINGS"])
    pending = len([o for o in orders if o.get("status") == "Pending"])
    confirmed = [o for o in orders if o.get("status") in ["Confirmed", "Delivered"]]
    a,b,c = st.columns(3)
    a.metric("Products", len(products))
    b.metric("Pending Orders", pending)
    c.metric("Confirmed Sales", f"Rs.{sum(safe_int(o.get('total')) for o in confirmed)}")

    top1, top2 = st.columns(2)
    with top1:
        if st.button("OPEN PUBLIC STORE", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.admin_authenticated = False
            st.rerun()
    with top2:
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.admin_authenticated = False
            st.query_params.clear()
            st.rerun()
    st.divider()

    if menu == "DASHBOARD":
        st.subheader("Cloud Database Status")
        st.success("Connected to Supabase. Products and orders are read from cloud database.")
        st.write(f"Products: **{len(products)}**")
        st.write(f"Orders: **{len(orders)}**")
        st.info("Public customers ko store ka normal link dein. Admin link ke end mein `?admin=1` lagayein.")

    elif menu == "STORE VIEW":
        st.info("Public store preview ke liye Admin logout karein ya OPEN PUBLIC STORE dabayein.")

    elif menu == "PRODUCT SYSTEM":
        st.subheader("Product System — Add / Edit / Delete")
        cats = load_categories()
        if not cats:
            cats = NEW_CATS.copy()
        with st.expander("Manage Categories"):
            new_cat = st.text_input("New Category Name")
            if st.button("ADD CATEGORY"):
                if new_cat.strip() and new_cat.strip().upper() not in [x.upper() for x in cats]:
                    cats.append(new_cat.strip().upper())
                    save_categories(cats)
                    st.success("Category added.")
                    st.rerun()
            st.write("Current: " + " | ".join(cats))
            if st.button("RESET DEFAULT CATEGORIES"):
                save_categories(NEW_CATS.copy())
                st.rerun()

        existing_ids = [p.get("id") for p in products]
        edit_options = ["➕ Add New Product"] + [
    f"{p.get('name', 'Unnamed')} — {str(p.get('id') or '')[:8]}"
    for p in products
    if isinstance(p, dict)
]
        choice = st.selectbox("Select product to edit", edit_options)
        editing = None
        if choice != "➕ Add New Product":
            selected_id = choice.split(" — ")[-1]
            editing = next((p for p in products if str(p.get("id","")).startswith(selected_id)), None)

        with st.form("product_form", clear_on_submit=(editing is None)):
            st.markdown("**Product details**")
            pname = st.text_input("Product Name *", value=(editing or {}).get("name", ""))
            current_cat = (editing or {}).get("category", cats[0] if cats else "OTHER")
            cat_index = cats.index(current_cat) if current_cat in cats else 0
            category = st.selectbox("Category", cats, index=cat_index)
            x1,x2 = st.columns(2)
            with x1:
                kharid = st.number_input("Kharid Rate", min_value=0, max_value=10000000, value=safe_int((editing or {}).get("kharid",0)))
            with x2:
                sell = st.number_input("Original / Bechne Rate", min_value=0, max_value=10000000, value=safe_int((editing or {}).get("sell", (editing or {}).get("final",0))))
            x3,x4 = st.columns(2)
            with x3:
                discount = st.number_input("Discount %", min_value=0, max_value=90, value=safe_int((editing or {}).get("discount",0)))
            with x4:
                stock = st.number_input("Stock", min_value=0, max_value=100000, value=safe_int((editing or {}).get("stock",0)))
            old_expiry = (editing or {}).get("expiry", (date.today()+timedelta(days=180)).isoformat())
            try:
                expiry_default = date.fromisoformat(old_expiry)
            except Exception:
                expiry_default = date.today()+timedelta(days=180)
            expiry = st.date_input("Expiry", value=expiry_default)
            highlights = st.text_area("Highlights", value=(editing or {}).get("highlights",""))
            full_desc = st.text_area("Full Description", value=(editing or {}).get("full_desc",""))
            specs = st.text_area("Specifications", value=(editing or {}).get("specs",""))
            photo = st.file_uploader("Product Photo (optional)", type=["jpg","jpeg","png"], key=f"photo_{(editing or {}).get('id','new')}")
            save_btn = st.form_submit_button("SAVE PRODUCT TO CLOUD", type="primary", use_container_width=True)

        if save_btn:
            if not pname.strip():
                st.error("Product name required.")
            else:
                old_image = (editing or {}).get("image_b64")
                new_image = image_to_b64(photo) if photo else old_image
                final_price = round(sell * (1 - discount/100))
                product = {
                    "id": (editing or {}).get("id", str(uuid.uuid4())),
                    "name": pname.strip(), "category": category,
                    "sell": sell, "kharid": kharid, "discount": discount,
                    "final": final_price, "buy": kharid, "stock": stock,
                    "expiry": expiry.isoformat(), "profit": final_price-kharid,
                    "highlights": highlights, "full_desc": full_desc,
                    "specs": specs, "image_b64": new_image,
                }
                try:
                    save_product(product)
                    st.success("Product Supabase cloud database mein save ho gaya.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Product save failed: {e}")

        st.divider()
        st.subheader(f"Saved Products ({len(products)})")
        for p in products:
            with st.container(border=True):
                cc1,cc2,cc3 = st.columns([3,1,1])
                with cc1:
                    st.write(f"**{p.get('name','')}**")
                    st.caption(f"{p.get('category','')} · Rs.{p.get('final',0)} · Stock {p.get('stock',0)}")
                with cc2:
                    if st.button("Delete", key=f"delete_{p['id']}"):
                        try:
                            delete_product(p["id"])
                            st.success("Product deleted.")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                with cc3:
                    if st.button("Refresh", key=f"refresh_{p['id']}"):
                        st.rerun()

    elif menu == "ORDERS - DARAZ":
        st.subheader("Orders")
        filter_status = st.selectbox("Filter", ["All","Pending","Confirmed","Delivered","Cancelled","Returned"])
        filtered = orders if filter_status == "All" else [o for o in orders if o.get("status") == filter_status]
        confirmed_orders = [o for o in orders if o.get("status") in ["Confirmed","Delivered"]]
        q1,q2 = st.columns(2)
        q1.metric("Sale Count", len(confirmed_orders))
        q2.metric("Sale Amount", f"Rs.{sum(safe_int(o.get('total')) for o in confirmed_orders)}")
        for o in reversed(filtered):
            with st.container(border=True):
                st.write(f"**ID: {o.get('id','')}** · {o.get('time','')} · **{o.get('status','')}** · Rs.{o.get('total',0)}")
                for item in o.get("products", []):
                    st.caption(f"- {item.get('name','')} — Rs.{item.get('price',0)} — {item.get('category','')}")
                reason = st.text_input("Reason (optional)", value=o.get("reason",""), key=f"reason_{o['id']}")
                cols = st.columns(4)
                for col, status in zip(cols, ["Confirmed","Delivered","Cancelled","Returned"]):
                    with col:
                        if st.button(status, key=f"status_{o['id']}_{status}", use_container_width=True):
                            try:
                                o["reason"] = reason
                                if status == "Confirmed":
                                    result_message = confirm_order_and_deduct_stock(o)
                                    st.success(result_message)
                                else:
                                    o["status"] = status
                                    save_order(o)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Order status update failed: {e}")

    elif menu == "MONEY":
        confirmed_orders = [o for o in orders if o.get("status") in ["Confirmed","Delivered"]]
        pending_orders = [o for o in orders if o.get("status") == "Pending"]
        st.metric("Pending Orders", len(pending_orders))
        st.metric("Confirmed / Delivered Orders", len(confirmed_orders))
        st.metric("Sales Amount", f"Rs.{sum(safe_int(o.get('total')) for o in confirmed_orders)}")
        st.metric("Total Products", len(products))

    elif menu == "STOCK":
        st.subheader("Stock Management")
        for p in products:
            with st.container(border=True):
                st.write(f"**{p.get('name','')}** — Stock: {p.get('stock',0)}")
                new_stock = st.number_input("Set stock", min_value=0, max_value=100000, value=safe_int(p.get("stock",0)), key=f"stock_{p['id']}")
                if st.button("UPDATE STOCK", key=f"stock_btn_{p['id']}", use_container_width=True):
                    p["stock"] = new_stock
                    save_product(p)
                    st.success("Stock updated in cloud.")
                    st.rerun()

    elif menu == "BACKUP":
        st.subheader("Cloud Backup / Restore")
        products_json = json.dumps(products, ensure_ascii=False, indent=2)
        orders_json = json.dumps(orders, ensure_ascii=False, indent=2)
        st.download_button("DOWNLOAD PRODUCTS BACKUP", products_json, file_name="mehar_products_v94.json", mime="application/json", use_container_width=True)
        st.download_button("DOWNLOAD ORDERS BACKUP", orders_json, file_name="mehar_orders_v94.json", mime="application/json", use_container_width=True)
        uploaded = st.file_uploader("Restore Products JSON", type=["json"], key="restore_products_json")
        if uploaded and st.button("RESTORE PRODUCTS TO CLOUD"):
            try:
                data = json.load(uploaded)
                if not isinstance(data, list):
                    raise ValueError("JSON must contain a list.")
                for item in data:
                    if isinstance(item, dict):
                        item.setdefault("id", str(uuid.uuid4()))
                        item["id"] = str(item["id"])
                        save_product(item)
                st.success(f"{len(data)} product records imported.")
                st.rerun()
            except Exception as e:
                st.error(f"Restore failed: {e}")
        uploaded_orders = st.file_uploader("Restore Orders JSON", type=["json"], key="restore_orders_json")
        if uploaded_orders and st.button("RESTORE ORDERS TO CLOUD"):
            try:
                data = json.load(uploaded_orders)
                if not isinstance(data, list):
                    raise ValueError("JSON must contain a list.")
                for item in data:
                    if isinstance(item, dict):
                        item.setdefault("id", str(uuid.uuid4()))
                        item["id"] = str(item["id"])
                        save_order(item)
                st.success(f"{len(data)} order records imported.")
                st.rerun()
            except Exception as e:
                st.error(f"Orders restore failed: {e}")
        st.caption("Restore adds/updates records by ID; it does not automatically erase existing cloud data.")

    elif menu == "SETTINGS":
        st.subheader("Store Settings")
        logo = load_logo()
        if logo:
            show_product_image(logo, width=100)
        logo_upload = st.file_uploader("Upload Store Logo", type=["png","jpg","jpeg"])
        if st.button("SAVE LOGO TO CLOUD") and logo_upload:
            try:
                save_logo(image_to_b64(logo_upload))
                st.success("Logo saved.")
                st.rerun()
            except Exception as e:
                st.error(str(e))
        st.divider()
        st.subheader("Change Admin Password")
        old_password = st.text_input("Current Password", type="password", key="old_pw")
        new_password = st.text_input("New Password", type="password", key="new_pw")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pw")
        if st.button("CHANGE PASSWORD", type="primary"):
            stored = current_password_hash()
            if not verify_password(old_password, stored or ""):
                st.error("Current password incorrect.")
            elif len(new_password) < 8:
                st.error("Use at least 8 characters.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            else:
                set_setting("admin_password_hash", hash_password(new_password))
                st.success("Admin password updated in cloud database.")

    st.stop()

# ---------- PUBLIC STORE ----------
products = load_products()
categories = load_categories()
logo = load_logo()

st.markdown('<div class="mm-header">🛒 MEHAR MART <span>🛍️</span></div>', unsafe_allow_html=True)
if logo:
    show_product_image(logo, width=95)

st.caption("Cash on Delivery · Delivery All Over Pakistan")
cart_count = len(st.session_state.cart)
cart_total = sum(safe_int(p.get("final",0)) for p in st.session_state.cart)

if st.session_state.selected_product:
    product = next((p for p in products if p.get("id") == st.session_state.selected_product), None)
    if not product:
        st.session_state.selected_product = None
        st.rerun()
    if st.button("⬅ BACK TO STORE", use_container_width=True):
        st.session_state.selected_product = None
        st.rerun()
    show_product_image(product.get("image_b64"))
    st.title(product.get("name",""))
    st.caption(product.get("category",""))
    st.markdown(f'<div class="mm-price">Rs. {product.get("final",0)}</div>', unsafe_allow_html=True)
    if safe_int(product.get("sell", product.get("final",0))) > safe_int(product.get("final",0)):
        st.markdown(f"<del>Rs. {product.get('sell')}</del>  **{product.get('discount',0)}% OFF**")
    if safe_int(product.get("stock",0)) <= 0:
        st.warning("Currently out of stock.")
    else:
        p1,p2 = st.columns(2)
        with p1:
            if st.button("ADD TO CART", type="primary", use_container_width=True):
                st.session_state.cart.append(product)
                st.success("Added to cart.")
                st.rerun()
        with p2:
            if st.button("BUY NOW", use_container_width=True):
                oid = create_order([product], product.get("final",0))
                msg = whatsapp_message(oid, [product], product.get("final",0))
                st.success(f"Order {oid} saved.")
                st.link_button("CONFIRM ON WHATSAPP", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", use_container_width=True)
    st.divider()
    st.subheader("Highlights"); st.write(product.get("highlights",""))
    st.subheader("Description"); st.write(product.get("full_desc",""))
    st.subheader("Specifications"); st.write(product.get("specs",""))
else:
    st.subheader("Shop Products")
    selected_category = st.selectbox("Category", ["All"] + categories)
    search = st.text_input("Search products", placeholder="Search products...")
    with st.expander(f"🛒 Cart ({cart_count})", expanded=cart_count > 0):
        if not st.session_state.cart:
            st.info("Your cart is empty.")
        else:
            for i, item in enumerate(st.session_state.cart):
                left,right = st.columns([4,1])
                with left:
                    st.write(f"**{item.get('name','')}** — Rs.{item.get('final',0)}")
                with right:
                    if st.button("✕", key=f"remove_cart_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            cart_total = sum(safe_int(p.get("final",0)) for p in st.session_state.cart)
            st.write(f"**Total: Rs.{cart_total}**")
            if st.button(f"CHECKOUT — Rs.{cart_total}", type="primary", use_container_width=True):
                oid = create_order(st.session_state.cart, cart_total)
                msg = whatsapp_message(oid, st.session_state.cart, cart_total)
                st.success(f"Order {oid} saved in cloud.")
                st.link_button("CONFIRM ORDER ON WHATSAPP", f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}", use_container_width=True)
            if st.button("CLEAR CART", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

    visible = [p for p in products if isinstance(p, dict)]
    if selected_category != "All":
        visible = [p for p in visible if str(p.get("category","")).upper() == selected_category.upper()]
    if search.strip():
        term = search.strip().lower()
        visible = [p for p in visible if term in str(p.get("name","")).lower() or term in str(p.get("category","")).lower()]
    st.write(f"**{len(visible)} products available**")
    if not visible:
        st.info("Products abhi available nahi hain. Admin panel se products add karein.")
    for p in visible:
        with st.container(border=True):
            show_product_image(p.get("image_b64"))
            st.subheader(p.get("name",""))
            st.caption(p.get("category",""))
            st.markdown(f'<div class="mm-price">Rs. {p.get("final",0)}</div>', unsafe_allow_html=True)
            sell_price = safe_int(p.get("sell", p.get("final",0)))
            if sell_price > safe_int(p.get("final",0)):
                st.markdown(f"<del>Rs.{sell_price}</del>  **{p.get('discount',0)}% OFF**")
            if safe_int(p.get("stock",0)) <= 0:
                st.warning("Out of stock")
            b1,b2 = st.columns(2)
            with b1:
                if st.button("VIEW DETAILS", key=f"view_{p['id']}", use_container_width=True):
                    st.session_state.selected_product = p["id"]
                    st.rerun()
            with b2:
                if st.button("ADD TO CART", key=f"add_{p['id']}", type="primary", use_container_width=True, disabled=safe_int(p.get("stock",0)) <= 0):
                    st.session_state.cart.append(p)
                    st.success("Added.")
                    st.rerun()

st.markdown("<div style='height:90px'></div>", unsafe_allow_html=True)
