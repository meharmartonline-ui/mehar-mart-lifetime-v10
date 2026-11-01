# MEHAR MART V97 — Separate Public Store + Private Admin Login
# Existing V93 JSON files are reused. Client route never renders admin controls.
import streamlit as st
import os, json, io, base64, urllib.parse, hashlib, hmac, secrets
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="Mehar Mart", layout="wide", initial_sidebar_state="collapsed")

WA_NUMBER = "923452352112"
PRODUCT_FILE = "products.json"
PASS_FILE = "admin_password.txt"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"
ORDERS_FILE = "orders.json"
BACKUP_FILE = "products_backup.json"
ORDERS_BACKUP = "orders_backup.json"
DEFAULT_CATS = ["HONEY", "HOME & DECOR", "KITCHEN GADGETS", "HEALTH CARE & BEAUTY", "SKIN CARE PRODUCTS", "OTHER"]
DEFAULT_PASSWORD = os.environ.get("MEHAR_ADMIN_PASSWORD", "mehar123")

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        backup = BACKUP_FILE if path == PRODUCT_FILE else ORDERS_BACKUP if path == ORDERS_FILE else None
        if backup:
            try:
                with open(backup, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return default

def save_json(path, data):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        backup = BACKUP_FILE if path == PRODUCT_FILE else ORDERS_BACKUP if path == ORDERS_FILE else None
        if backup:
            with open(backup + ".tmp", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(backup + ".tmp", backup)
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False

def get_password_record():
    try:
        with open(PASS_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return DEFAULT_PASSWORD

def password_ok(candidate):
    stored = get_password_record()
    if stored.startswith("pbkdf2$"):
        try:
            _, salt_hex, digest = stored.split("$", 2)
            test = hashlib.pbkdf2_hmac("sha256", candidate.encode(), bytes.fromhex(salt_hex), 240000).hex()
            return hmac.compare_digest(test, digest)
        except Exception:
            return False
    return hmac.compare_digest(candidate, stored)

def set_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240000).hex()
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        f.write(f"pbkdf2${salt.hex()}${digest}")

def num(value):
    try:
        return int(float(value or 0))
    except Exception:
        return 0

def img_b64(upload, max_size=(900, 900), fmt="JPEG"):
    try:
        image = Image.open(upload).convert("RGB")
        image.thumbnail(max_size)
        buf = io.BytesIO()
        image.save(buf, format=fmt, quality=82, optimize=True)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None

def show_image(product):
    raw = product.get("image_b64")
    if raw:
        try:
            st.image(Image.open(io.BytesIO(base64.b64decode(raw))), use_container_width=True)
        except Exception:
            st.caption("Image display nahi ho saki.")

def migrate_products(products):
    changed = False
    for p in products:
        if not isinstance(p, dict):
            continue
        category = str(p.get("category", "") or "").upper().strip()
        if category in {"PURE HONEY", "BERI HONEY", "SIDR HONEY", "PURE", "BERI", "SIDR"} or "PURE HONEY" in category or "BERI HONEY" in category:
            p["category"] = "HONEY"
            changed = True
        if not p.get("product_id"):
            p["product_id"] = secrets.token_hex(6)
            changed = True
    return changed

# Session state
if "products" not in st.session_state:
    st.session_state.products = load_json(PRODUCT_FILE, [])
if not isinstance(st.session_state.products, list):
    st.session_state.products = []
if "orders" not in st.session_state:
    st.session_state.orders = load_json(ORDERS_FILE, [])
if "cart" not in st.session_state:
    st.session_state.cart = []
if "categories" not in st.session_state:
    st.session_state.categories = load_json(CAT_FILE, DEFAULT_CATS[:])
if not isinstance(st.session_state.categories, list):
    st.session_state.categories = DEFAULT_CATS[:]
for category in DEFAULT_CATS:
    if category not in st.session_state.categories:
        st.session_state.categories.append(category)
if "logo_b64" not in st.session_state:
    st.session_state.logo_b64 = load_json(LOGO_FILE, None)
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if migrate_products(st.session_state.products):
    save_json(PRODUCT_FILE, st.session_state.products)
save_json(CAT_FILE, st.session_state.categories)

# Routing:
# Client link: https://YOUR-APP.streamlit.app/
# Admin link:  https://YOUR-APP.streamlit.app/?admin=1
# ?admin=1 only shows login. It never authenticates by itself.
admin_route = st.query_params.get("admin") == "1"

st.markdown("""
<style>
header, footer {visibility:hidden;}
[data-testid="stToolbar"], [data-testid="stAppDeployButton"] {display:none;}
.block-container {padding-top:1rem; padding-bottom:3rem; max-width:1100px;}
.mm-header {background:#f85606;color:white;padding:13px 16px;border-radius:9px;
display:flex;justify-content:space-between;align-items:center;font-size:20px;font-weight:800;}
.mm-price {font-size:23px;font-weight:800;color:#f85606;}
.mm-old {font-size:13px;color:#888;text-decoration:line-through;}
</style>
""", unsafe_allow_html=True)

def make_order(items, total):
    orders = load_json(ORDERS_FILE, [])
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + secrets.token_hex(2).upper()
    saved_items = []
    for p in items:
        saved_items.append({
            "product_id": p.get("product_id", ""),
            "name": p.get("name", ""),
            "price": num(p.get("final", p.get("price", 0))),
            "category": p.get("category", ""),
            "quantity": 1
        })
    order = {
        "id": order_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "products": saved_items,
        "total": num(total),
        "status": "Pending",
        "reason": "",
        "stock_deducted": False
    }
    orders.append(order)
    save_json(ORDERS_FILE, orders)
    st.session_state.orders = orders
    return order_id

def wa_text(order_id, items, total):
    lines = ["Assalam-o-Alaikum", "Mehar Mart se order place karna hai.", f"Order ID: {order_id}", ""]
    for p in items:
        lines.extend([f"Product: {p.get('name','')}", f"Category: {p.get('category','')}",
                      f"Price: Rs. {num(p.get('final', p.get('price', 0)))}", ""])
    lines.extend([f"Total: Rs. {num(total)}", "Payment: Cash on Delivery",
                  "Delivery: All Over Pakistan", "Please confirm my order. Shukriya."])
    return "\n".join(lines)

def wa_button(order_id, items, total, label="Confirm Order on WhatsApp"):
    url = "https://wa.me/" + WA_NUMBER + "?text=" + urllib.parse.quote(wa_text(order_id, items, total))
    st.link_button(label, url, type="primary", use_container_width=True)

def admin_login():
    st.title("🔐 Mehar Mart Admin Login")
    st.write("Private Admin Panel — password ke baghair access nahi milega.")
    with st.form("admin_login_form"):
        password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)
    if submit:
        if password_ok(password):
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Password ghalat hai.")
    if st.button("← Client Store kholein", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.query_params.clear()
        st.rerun()

def admin_panel():
    products = st.session_state.products
    orders = load_json(ORDERS_FILE, [])
    st.title("MEHAR MART — ADMIN PANEL")
    confirmed = [o for o in orders if o.get("status") in ("Confirmed", "Delivered")]
    a, b, c = st.columns(3)
    a.metric("Pending Orders", sum(1 for o in orders if o.get("status") == "Pending"))
    b.metric("Confirmed / Delivered", len(confirmed))
    c.metric("Sales", f"Rs. {sum(num(o.get('total')) for o in confirmed):,}")
    menu = st.selectbox("Admin Menu", ["Dashboard", "PRODUCT SYSTEM", "ORDERS - DARAZ", "MONEY", "STOCK", "BACKUP", "SETTINGS"])

    if menu == "Dashboard":
        x, y = st.columns(2)
        x.metric("Total Products", len(products))
        y.metric("Total Orders", len(orders))
        st.info("Client store aur admin panel separate links par hain.")

    elif menu == "PRODUCT SYSTEM":
        st.subheader("Add / Edit Products")
        product_ids = ["NEW"] + [p.get("product_id") for p in products]
        selected_id = st.selectbox("Product edit karne ke liye select karein", product_ids,
            format_func=lambda pid: "➕ New Product" if pid == "NEW" else next((p.get("name", "Product") for p in products if p.get("product_id") == pid), str(pid)))
        editing = next((p for p in products if p.get("product_id") == selected_id), None) if selected_id != "NEW" else None
        cats = st.session_state.categories
        with st.form("product_editor"):
            old_cat = editing.get("category", cats[0]) if editing else cats[0]
            cat_idx = cats.index(old_cat) if old_cat in cats else 0
            category = st.selectbox("Category", cats, index=cat_idx)
            name = st.text_input("Product Name *", value=editing.get("name", "") if editing else "")
            c1, c2 = st.columns(2)
            with c1:
                purchase = st.number_input("Kharid Rate", min_value=0, max_value=1000000,
                    value=num(editing.get("kharid", editing.get("buy", 0))) if editing else 0, step=10)
            with c2:
                selling = st.number_input("Original Selling Rate", min_value=0, max_value=1000000,
                    value=num(editing.get("sell", editing.get("final", 0))) if editing else 0, step=10)
            c3, c4 = st.columns(2)
            with c3:
                discount = st.number_input("Discount %", min_value=0, max_value=90,
                    value=num(editing.get("discount", 0)) if editing else 0)
            with c4:
                stock = st.number_input("Stock", min_value=0, max_value=100000,
                    value=num(editing.get("stock", 0)) if editing else 0)
            expiry_default = datetime.now().date() + timedelta(days=180)
            try:
                if editing and editing.get("expiry"):
                    expiry_default = datetime.strptime(editing["expiry"], "%Y-%m-%d").date()
            except Exception:
                pass
            expiry = st.date_input("Expiry", value=expiry_default)
            highlights = st.text_area("Highlights", value=editing.get("highlights", "") if editing else "100% Pure — No Sugar, No Mix")
            description = st.text_area("Full Description", value=editing.get("full_desc", "") if editing else "MEHAR MART — Cash on Delivery")
            specs = st.text_area("Specifications", value=editing.get("specs", "") if editing else "")
            photo = st.file_uploader("Product Photo", type=["jpg", "jpeg", "png", "webp"])
            submitted = st.form_submit_button("UPDATE PRODUCT" if editing else "SAVE PRODUCT", type="primary", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Product name likhein.")
            else:
                final_price = round(selling * (1 - discount / 100))
                image_data = img_b64(photo) if photo else (editing.get("image_b64") if editing else None)
                item = {
                    "product_id": editing.get("product_id") if editing else secrets.token_hex(6),
                    "name": name.strip(), "category": category,
                    "sell": num(selling), "kharid": num(purchase), "buy": num(purchase),
                    "discount": num(discount), "final": num(final_price),
                    "stock": num(stock), "expiry": expiry.strftime("%Y-%m-%d"),
                    "profit": num(final_price) - num(purchase),
                    "highlights": highlights, "full_desc": description, "specs": specs,
                    "image_b64": image_data
                }
                if editing:
                    index = next(i for i, p in enumerate(products) if p.get("product_id") == selected_id)
                    products[index] = item
                else:
                    products.append(item)
                st.session_state.products = products
                save_json(PRODUCT_FILE, products)
                st.success("Product save/update ho gaya.")
                st.rerun()

        if products:
            st.markdown("#### Delete Product")
            del_id = st.selectbox("Delete ke liye product", [p.get("product_id") for p in products],
                format_func=lambda pid: next((p.get("name", "Product") for p in products if p.get("product_id") == pid), str(pid)),
                key="delete_product_id")
            if st.button("DELETE SELECTED PRODUCT"):
                st.session_state.products = [p for p in products if p.get("product_id") != del_id]
                save_json(PRODUCT_FILE, st.session_state.products)
                st.rerun()

        st.divider()
        st.subheader("Add Custom Category")
        with st.form("add_category_form"):
            new_category = st.text_input("New category name")
            add_category = st.form_submit_button("Add Category")
        if add_category and new_category.strip():
            value = new_category.strip().upper()
            if value not in st.session_state.categories:
                st.session_state.categories.append(value)
                save_json(CAT_FILE, st.session_state.categories)
                st.rerun()
            else:
                st.warning("Category pehle se mojood hai.")

    elif menu == "ORDERS - DARAZ":
        st.subheader("Orders")
        if not orders:
            st.info("Abhi koi order nahi.")
        else:
            filter_status = st.selectbox("Filter", ["All", "Pending", "Confirmed", "Delivered", "Cancelled", "Returned"])
            shown = orders if filter_status == "All" else [o for o in orders if o.get("status") == filter_status]
            for order in reversed(shown):
                idx = next((i for i, o in enumerate(orders) if o.get("id") == order.get("id")), None)
                if idx is None:
                    continue
                with st.container(border=True):
                    st.write(f"**Order ID:** {order.get('id','')} | {order.get('time','')}")
                    st.write(f"**{order.get('status','Pending')}** — Rs. {num(order.get('total')):,}")
                    for item in order.get("products", []):
                        st.caption(f"• {item.get('name','')} — Rs. {num(item.get('price')):,} — {item.get('category','')}")
                    if order.get("reason"):
                        st.warning(order["reason"])
                    x, y, z = st.columns(3)
                    with x:
                        if st.button("✅ Confirm", key=f"confirm_{idx}", use_container_width=True):
                            orders[idx]["status"] = "Confirmed"
                            save_json(ORDERS_FILE, orders)
                            st.rerun()
                    with y:
                        if st.button("📦 Delivered", key=f"delivered_{idx}", use_container_width=True):
                            orders[idx]["status"] = "Delivered"
                            save_json(ORDERS_FILE, orders)
                            st.rerun()
                    with z:
                        if st.button("❌ Cancel", key=f"cancel_{idx}", use_container_width=True):
                            orders[idx]["status"] = "Cancelled"
                            save_json(ORDERS_FILE, orders)
                            st.rerun()
                    with st.expander("Return / note"):
                        note = st.text_input("Reason", value=order.get("reason", ""), key=f"reason_{idx}")
                        if st.button("Mark Returned", key=f"returned_{idx}"):
                            orders[idx]["status"] = "Returned"
                            orders[idx]["reason"] = note
                            save_json(ORDERS_FILE, orders)
                            st.rerun()
                        if st.button("Save Note", key=f"save_note_{idx}"):
                            orders[idx]["reason"] = note
                            save_json(ORDERS_FILE, orders)
                            st.rerun()

    elif menu == "MONEY":
        confirmed_orders = [o for o in orders if o.get("status") in ("Confirmed", "Delivered")]
        pending_orders = [o for o in orders if o.get("status") == "Pending"]
        sales = sum(num(o.get("total")) for o in confirmed_orders)
        estimated_cost = 0
        for order in confirmed_orders:
            for item in order.get("products", []):
                product = next((p for p in products if p.get("product_id") == item.get("product_id")), None)
                if product:
                    estimated_cost += num(product.get("kharid", product.get("buy", 0))) * num(item.get("quantity", 1))
        a, b = st.columns(2)
        a.metric("Pending Orders", len(pending_orders))
        b.metric("Confirmed / Delivered", len(confirmed_orders))
        a, b = st.columns(2)
        a.metric("Sales Amount", f"Rs. {sales:,}")
        b.metric("Estimated Product Cost", f"Rs. {estimated_cost:,}")
        st.metric("Estimated Gross Difference", f"Rs. {sales - estimated_cost:,}")
        st.caption("Cost estimate current purchase rates par hai; historical purchase rate alag save nahi hota.")

    elif menu == "STOCK":
        st.subheader("Stock Management")
        for i, product in enumerate(products):
            with st.container(border=True):
                st.write(f"**{product.get('name','')}** — {product.get('category','')} — Stock: **{num(product.get('stock'))}**")
                a, b, c = st.columns(3)
                with a:
                    if st.button("➕ Plus 1", key=f"plus_{i}", use_container_width=True):
                        products[i]["stock"] = num(product.get("stock")) + 1
                        save_json(PRODUCT_FILE, products)
                        st.rerun()
                with b:
                    if st.button("➖ Minus 1", key=f"minus_{i}", use_container_width=True):
                        products[i]["stock"] = max(0, num(product.get("stock")) - 1)
                        save_json(PRODUCT_FILE, products)
                        st.rerun()
                with c:
                    updated_stock = st.number_input("Set stock", min_value=0, value=num(product.get("stock")), key=f"set_{i}")
                    if st.button("Update", key=f"set_btn_{i}", use_container_width=True):
                        products[i]["stock"] = num(updated_stock)
                        save_json(PRODUCT_FILE, products)
                        st.rerun()

    elif menu == "BACKUP":
        st.subheader("Backup & Restore")
        st.download_button("📥 Download Products Backup", json.dumps(products, ensure_ascii=False, indent=2),
                           file_name="mehar_products_backup.json", mime="application/json", use_container_width=True)
        st.download_button("📥 Download Orders Backup", json.dumps(orders, ensure_ascii=False, indent=2),
                           file_name="mehar_orders_backup.json", mime="application/json", use_container_width=True)
        product_upload = st.file_uploader("Restore Products JSON", type=["json"], key="restore_products")
        if product_upload and st.button("Restore Products"):
            try:
                data = json.load(product_upload)
                if isinstance(data, list):
                    migrate_products(data)
                    st.session_state.products = data
                    save_json(PRODUCT_FILE, data)
                    st.success("Products restore ho gaye.")
                    st.rerun()
                else:
                    st.error("Invalid products backup.")
            except Exception as e:
                st.error(f"Restore error: {e}")
        order_upload = st.file_uploader("Restore Orders JSON", type=["json"], key="restore_orders")
        if order_upload and st.button("Restore Orders"):
            try:
                data = json.load(order_upload)
                if isinstance(data, list):
                    save_json(ORDERS_FILE, data)
                    st.success("Orders restore ho gaye.")
                    st.rerun()
                else:
                    st.error("Invalid orders backup.")
            except Exception as e:
                st.error(f"Restore error: {e}")

    elif menu == "SETTINGS":
        st.subheader("Settings")
        if st.session_state.logo_b64:
            try:
                st.image(Image.open(io.BytesIO(base64.b64decode(st.session_state.logo_b64))), width=110)
            except Exception:
                pass
        logo_upload = st.file_uploader("Upload Store Logo", type=["png", "jpg", "jpeg"], key="store_logo")
        if logo_upload and st.button("Save Logo"):
            try:
                st.session_state.logo_b64 = img_b64(logo_upload, (300, 300), "PNG")
                save_json(LOGO_FILE, st.session_state.logo_b64)
                st.success("Logo save ho gaya.")
                st.rerun()
            except Exception as e:
                st.error(f"Logo error: {e}")

        st.divider()
        st.subheader("Change Admin Password")
        with st.form("password_change"):
            old = st.text_input("Old password", type="password")
            new = st.text_input("New password (minimum 10 characters)", type="password")
            confirm = st.text_input("Confirm new password", type="password")
            change = st.form_submit_button("Change Password", type="primary")
        if change:
            if not password_ok(old):
                st.error("Old password ghalat hai.")
            elif len(new) < 10:
                st.error("New password kam az kam 10 characters ka ho.")
            elif new != confirm:
                st.error("New passwords match nahi karte.")
            else:
                set_password(new)
                st.success("Password update ho gaya.")

        st.divider()
        st.warning("Neeche ke actions permanent hain.")
        if st.button("DELETE ALL ORDERS"):
            st.session_state.confirm_orders_delete = True
        if st.session_state.get("confirm_orders_delete"):
            st.error("Tamam orders delete karne hain?")
            yes, no = st.columns(2)
            with yes:
                if st.button("Yes — delete orders"):
                    save_json(ORDERS_FILE, [])
                    st.session_state.confirm_orders_delete = False
                    st.rerun()
            with no:
                if st.button("No — keep orders"):
                    st.session_state.confirm_orders_delete = False
                    st.rerun()
        if st.button("DELETE ALL PRODUCTS"):
            st.session_state.confirm_products_delete = True
        if st.session_state.get("confirm_products_delete"):
            st.error("Tamam products delete karne hain?")
            yes, no = st.columns(2)
            with yes:
                if st.button("Yes — delete products"):
                    st.session_state.products = []
                    save_json(PRODUCT_FILE, [])
                    st.session_state.confirm_products_delete = False
                    st.rerun()
            with no:
                if st.button("No — keep products"):
                    st.session_state.confirm_products_delete = False
                    st.rerun()

    st.divider()
    st.caption("Client URL: normal app link | Admin URL: normal app link ke end par ?admin=1")
    if st.button("LOG OUT", type="primary", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.query_params.clear()
        st.rerun()

def client_store():
    # Reload current products on each run so admin changes appear in the public store.
    products = load_json(PRODUCT_FILE, st.session_state.products)
    if isinstance(products, list):
        st.session_state.products = products
    logo_html = ""
    if st.session_state.logo_b64:
        logo_html = f"<img src='data:image/png;base64,{st.session_state.logo_b64}' style='height:29px;margin-right:8px;background:white;border-radius:4px;padding:2px;'>"
    st.markdown(f'<div class="mm-header"><span style="display:flex;align-items:center;">{logo_html}MEHAR MART</span><span>🛒 {len(st.session_state.cart)}</span></div>', unsafe_allow_html=True)
    st.caption("Quality Products at Affordable Prices • Cash on Delivery • Delivery All Over Pakistan")

    selected_id = st.session_state.selected_product
    if selected_id:
        product = next((p for p in products if p.get("product_id") == selected_id), None)
        if not product:
            st.session_state.selected_product = None
            st.rerun()
        if st.button("⬅ Back to Store", use_container_width=True):
            st.session_state.selected_product = None
            st.rerun()
        show_image(product)
        st.subheader(product.get("name", ""))
        st.caption(product.get("category", ""))
        st.markdown(f'<div class="mm-price">Rs. {num(product.get("final")):,}</div><span class="mm-old">Rs. {num(product.get("sell", product.get("final"))):,}</span> &nbsp; <b>{num(product.get("discount"))}% OFF</b>', unsafe_allow_html=True)
        if num(product.get("stock")) <= 0:
            st.error("Out of stock")
        else:
            a, b = st.columns(2)
            with a:
                if st.button("Add to Cart", type="primary", use_container_width=True):
                    st.session_state.cart.append(product)
                    st.rerun()
            with b:
                if st.button("Buy Now", use_container_width=True):
                    oid = make_order([product], num(product.get("final")))
                    st.success(f"Order {oid} place ho gaya.")
                    wa_button(oid, [product], num(product.get("final")))
        st.divider()
        st.subheader("Highlights")
        st.write(product.get("highlights", ""))
        st.subheader("Description")
        st.write(product.get("full_desc", ""))
        st.subheader("Specifications")
        st.write(product.get("specs", ""))
        return

    options = ["All"] + st.session_state.categories
    current = st.session_state.selected_category
    index = options.index(current) if current in options else 0
    selected = st.selectbox("Select Category", options, index=index)
    st.session_state.selected_category = selected
    search = st.text_input("Search products", placeholder="Search products...")
    visible = [p for p in products if isinstance(p, dict)]
    if selected != "All":
        visible = [p for p in visible if str(p.get("category", "")).upper() == selected.upper()]
    if search.strip():
        term = search.strip().lower()
        visible = [p for p in visible if term in str(p.get("name", "")).lower() or term in str(p.get("category", "")).lower()]

    if st.session_state.cart:
        with st.container(border=True):
            st.subheader(f"Cart — {len(st.session_state.cart)} products")
            total = 0
            for i, item in enumerate(st.session_state.cart):
                a, b = st.columns([4, 1])
                with a:
                    st.write(f"**{item.get('name','')}** — Rs. {num(item.get('final')):,}")
                with b:
                    if st.button("Remove", key=f"remove_cart_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
                total += num(item.get("final"))
            st.write(f"**Total: Rs. {total:,}**")
            if st.button(f"Checkout — Rs. {total:,}", type="primary", use_container_width=True):
                items = st.session_state.cart[:]
                oid = make_order(items, total)
                st.session_state.cart = []
                st.success(f"Order {oid} place ho gaya.")
                wa_button(oid, items, total)
            if st.button("Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

    st.write(f"**{len(visible)} Products**")
    if not visible:
        st.info("Is category mein abhi products available nahi.")
    for start in range(0, len(visible), 2):
        cols = st.columns(2)
        for col, product in zip(cols, visible[start:start+2]):
            with col:
                with st.container(border=True):
                    show_image(product)
                    st.write(f"**{product.get('name','')}**")
                    st.caption(product.get("category", ""))
                    st.markdown(f'<div class="mm-price">Rs. {num(product.get("final")):,}</div><span class="mm-old">Rs. {num(product.get("sell", product.get("final"))):,}</span>', unsafe_allow_html=True)
                    if num(product.get("stock")) <= 0:
                        st.caption("Out of stock")
                    else:
                        pid = product.get("product_id")
                        if st.button("View Details", key=f"view_{pid}", use_container_width=True):
                            st.session_state.selected_product = pid
                            st.rerun()
                        if st.button("Add to Cart", key=f"add_{pid}", type="primary", use_container_width=True):
                            st.session_state.cart.append(product)
                            st.rerun()
                        if st.button(f"Buy Now — Rs. {num(product.get('final')):,}", key=f"buy_{pid}", use_container_width=True):
                            oid = make_order([product], num(product.get("final")))
                            st.success(f"Order {oid} place ho gaya.")
                            wa_button(oid, [product], num(product.get("final")))

# APP ENTRY POINT
if admin_route:
    if st.session_state.admin_authenticated:
        admin_panel()
    else:
        admin_login()
else:
    # Public route contains only the shopping store. No admin link/button/login/panel.
    st.session_state.admin_authenticated = False
    client_store()
