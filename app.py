
import streamlit as st
import json
import os
import io
import base64
import hashlib
import hmac
import secrets
import urllib.parse
from datetime import datetime, timedelta
from PIL import Image

# ==========================================
# MEHAR MART V97 - COMPLETE SINGLE FILE
# ==========================================

st.set_page_config(
    page_title="MEHAR MART V97",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WA_NUMBER = "923452352112"

PRODUCT_FILE = "products.json"
ORDERS_FILE = "orders.json"
CAT_FILE = "categories.json"
LOGO_FILE = "logo.json"
PASS_FILE = "admin_password.txt"

PRODUCT_BACKUP = "products_backup.json"
ORDERS_BACKUP = "orders_backup.json"

NEW_CATS = [
    "HONEY",
    "HOME & DECOR",
    "KITCHEN GADGETS",
    "HEALTH CARE & BEAUTY",
    "SKIN CARE PRODUCTS",
    "OTHER"
]

# ==========================================
# JSON DATABASE
# ==========================================

def load_json(file, default):
    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    backups = {
        PRODUCT_FILE: PRODUCT_BACKUP,
        ORDERS_FILE: ORDERS_BACKUP
    }

    backup = backups.get(file)

    if backup and os.path.exists(backup):
        try:
            with open(backup, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return default


def save_json(file, data):
    try:
        temp = file + ".tmp"

        with open(temp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(temp, file)

        backups = {
            PRODUCT_FILE: PRODUCT_BACKUP,
            ORDERS_FILE: ORDERS_BACKUP
        }

        if file in backups:
            backup = backups[file]
            temp_backup = backup + ".tmp"

            with open(temp_backup, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            os.replace(temp_backup, backup)

        return True

    except Exception as e:
        st.error(f"Database Error: {e}")
        return False


# ==========================================
# PASSWORD SECURITY
# ==========================================

def get_password_hash(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    ).hex()

    return "PBKDF2:" + salt + ":" + hashed


def check_password(password):
    if not os.path.exists(PASS_FILE):
        return password == "mehar123"

    try:
        with open(PASS_FILE, "r", encoding="utf-8") as f:
            saved = f.read().strip()

        if saved.startswith("PBKDF2:"):
            _, salt, expected = saved.split(":")
            actual = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode(),
                salt.encode(),
                200000
            ).hex()

            return hmac.compare_digest(actual, expected)

        # Old V96 plain-text password compatibility
        return hmac.compare_digest(password, saved)

    except Exception:
        return False


def save_password(password):
    try:
        with open(PASS_FILE, "w", encoding="utf-8") as f:
            f.write(get_password_hash(password))
        return True
    except Exception:
        return False


# ==========================================
# PRODUCT DATA MIGRATION
# ==========================================

def normalize_products(products):
    changed = False

    for p in products:
        if not isinstance(p, dict):
            continue

        if not p.get("product_id"):
            p["product_id"] = secrets.token_hex(8)
            changed = True

        if "final" not in p:
            p["final"] = p.get("price", p.get("sell", 0))
            changed = True

        if "sell" not in p:
            p["sell"] = p.get("final", 0)
            changed = True

        if "stock" not in p:
            p["stock"] = 0
            changed = True

        cat = str(p.get("category", "")).upper().strip()

        if "HONEY" in cat or cat in ["PURE", "BERI", "SIDR"]:
            if p.get("category") != "HONEY":
                p["category"] = "HONEY"
                changed = True

    return products, changed


# ==========================================
# SESSION STATE
# ==========================================

if "products" not in st.session_state:
    data = load_json(PRODUCT_FILE, [])
    if not isinstance(data, list):
        data = []

    data, changed = normalize_products(data)
    st.session_state.products = data

    if changed:
        save_json(PRODUCT_FILE, data)

if "orders" not in st.session_state:
    data = load_json(ORDERS_FILE, [])
    st.session_state.orders = data if isinstance(data, list) else []

if "cart" not in st.session_state:
    st.session_state.cart = []

if "categories" not in st.session_state:
    cats = load_json(CAT_FILE, NEW_CATS)
    st.session_state.categories = cats if isinstance(cats, list) else NEW_CATS

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Salam Bhai! Mehar Mart mein khush amdeed! Aapko kya chahiye?"
        }
    ]

if "edit_product" not in st.session_state:
    st.session_state.edit_product = None

if "notice" not in st.session_state:
    st.session_state.notice = ""

# ==========================================
# CSS DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #f7f8fa;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}
.main-header {
    background: #f85606;
    color: white;
    padding: 17px;
    border-radius: 12px;
    font-size: 23px;
    font-weight: bold;
    text-align: center;
}
.product-card {
    background: white;
    padding: 12px;
    border-radius: 12px;
}
.price {
    color: #f85606;
    font-size: 21px;
    font-weight: bold;
}
div.stButton > button {
    border-radius: 9px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def refresh_products():
    st.session_state.products = load_json(PRODUCT_FILE, [])


def refresh_orders():
    st.session_state.orders = load_json(ORDERS_FILE, [])


def get_product(product_id):
    for p in st.session_state.products:
        if p.get("product_id") == product_id:
            return p
    return None


def save_product(product):
    products = st.session_state.products

    for i, old in enumerate(products):
        if old.get("product_id") == product.get("product_id"):
            products[i] = product
            save_json(PRODUCT_FILE, products)
            st.session_state.products = products
            return

    products.append(product)
    save_json(PRODUCT_FILE, products)
    st.session_state.products = products


def delete_product(product_id):
    products = [
        p for p in st.session_state.products
        if p.get("product_id") != product_id
    ]

    st.session_state.products = products
    save_json(PRODUCT_FILE, products)


def create_order(products_list, total):
    refresh_orders()

    order_id = (
        datetime.now().strftime("%Y%m%d%H%M%S")
        + secrets.token_hex(2).upper()
    )

    order_products = []

    for p in products_list:
        order_products.append({
            "product_id": p.get("product_id"),
            "name": p.get("name", ""),
            "price": int(p.get("final", p.get("price", 0))),
            "category": p.get("category", ""),
            "quantity": 1
        })

    order = {
        "id": order_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "products": order_products,
        "total": int(total),
        "status": "Pending",
        "reason": "",
        "stock_deducted": False
    }

    st.session_state.orders.append(order)
    save_json(ORDERS_FILE, st.session_state.orders)

    return order_id


def get_whatsapp_msg(order_id, products, total):
    msg = (
        "Assalam O Alaikum\n"
        "MEHAR MART ORDER\n\n"
        f"Order ID: {order_id}\n\n"
    )

    for p in products:
        msg += (
            f"Product: {p.get('name', '')}\n"
            f"Category: {p.get('category', '')}\n"
            f"Price: Rs.{p.get('final', p.get('price', 0))}\n\n"
        )

    msg += (
        f"Total: Rs.{total}\n\n"
        "Please confirm my Cash on Delivery order.\n"
        "Shukriya!"
    )

    return msg


def whatsapp_link(message):
    return (
        "https://wa.me/"
        + WA_NUMBER
        + "?text="
        + urllib.parse.quote(message)
    )


def order_status(order_id, status):
    refresh_orders()

    for order in st.session_state.orders:
        if order.get("id") != order_id:
            continue

        old_status = order.get("status", "Pending")

        if old_status == status:
            return

        # Deduct stock only on confirmation
        if status in ["Confirmed", "Delivered"] and not order.get("stock_deducted", False):

            for item in order.get("products", []):
                product = get_product(item.get("product_id"))

                if product:
                    qty = int(item.get("quantity", 1))
                    product["stock"] = max(
                        0,
                        int(product.get("stock", 0)) - qty
                    )

            order["stock_deducted"] = True
            save_json(PRODUCT_FILE, st.session_state.products)

        # Restore stock when a confirmed order is cancelled
        if status == "Cancelled" and order.get("stock_deducted", False):

            for item in order.get("products", []):
                product = get_product(item.get("product_id"))

                if product:
                    qty = int(item.get("quantity", 1))
                    product["stock"] = (
                        int(product.get("stock", 0)) + qty
                    )

            order["stock_deducted"] = False
            save_json(PRODUCT_FILE, st.session_state.products)

        order["status"] = status

        save_json(ORDERS_FILE, st.session_state.orders)
        return


def image_from_product(p):
    if not p.get("image_b64"):
        return None

    try:
        raw = base64.b64decode(p["image_b64"])
        return Image.open(io.BytesIO(raw))
    except Exception:
        return None


# ==========================================
# JARVIS SMART AI - NO API REQUIRED
# ==========================================

def get_smart_answer(question):
    products = [
        p for p in st.session_state.products
        if isinstance(p, dict)
    ]

    q = question.lower().strip()

    if not products:
        return "Bhai, abhi store mein products available nahi hain."

    if any(x in q for x in ["sasta", "sasti", "cheap", "kam price", "lowest"]):
        available = [
            p for p in products
            if int(p.get("stock", 0)) > 0
        ]

        if not available:
            return "Bhai, abhi stock available nahi hai."

        p = min(
            available,
            key=lambda x: int(x.get("final", 0))
        )

        return (
            f"Sab se sasta product ye hai:\n\n"
            f"✅ {p.get('name')}\n"
            f"Price: Rs.{p.get('final')}"
        )

    if any(x in q for x in ["mehnga", "expensive", "highest"]):
        p = max(
            products,
            key=lambda x: int(x.get("final", 0))
        )

        return (
            f"Sab se mehnga product:\n"
            f"{p.get('name')} - Rs.{p.get('final')}"
        )

    matched = []

    for p in products:
        name = str(p.get("name", "")).lower()
        category = str(p.get("category", "")).lower()

        words = q.split()

        if (
            q in name
            or q in category
            or any(
                len(w) >= 3 and (w in name or w in category)
                for w in words
            )
        ):
            matched.append(p)

    if matched:
        answer = "Jee Bhai! Ye products available hain:\n\n"

        for p in matched[:10]:
            answer += (
                f"✅ {p.get('name')}\n"
                f"Price: Rs.{p.get('final')}\n"
                f"Stock: {p.get('stock', 0)}\n\n"
            )

        return answer

    if any(x in q for x in ["list", "products", "sab", "kya hai"]):
        answer = f"Mehar Mart mein {len(products)} products hain:\n\n"

        for p in products[:15]:
            answer += (
                f"• {p.get('name')} - Rs.{p.get('final')}\n"
            )

        return answer

    if any(x in q for x in ["delivery", "cod", "payment"]):
        return (
            "Bhai, Mehar Mart Cash on Delivery orders leta hai. "
            "Delivery All Over Pakistan ke liye WhatsApp par order confirm karein."
        )

    return (
        "Salam Bhai! Main Mehar Mart ka Smart Assistant hoon. "
        "Aap product ka naam, Honey, price, sasti cheez ya delivery ke bare mein pooch sakte hain."
    )


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-header">🛒 MEHAR MART</div>',
    unsafe_allow_html=True
)

st.caption(
    "Quality Products at Affordable Prices | "
    "Cash on Delivery | Delivery All Over Pakistan"
)

if st.session_state.notice:
    st.success(st.session_state.notice)
    st.session_state.notice = ""

# ==========================================
# ADMIN LOGIN
# ==========================================

if not st.session_state.is_admin:

    with st.expander("Admin Login"):
        with st.form("admin_login"):
            password = st.text_input(
                "Admin Password",
                type="password"
            )

            login = st.form_submit_button(
                "LOGIN",
                use_container_width=True
            )

            if login:
                if check_password(password):
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Wrong Password!")

else:

    st.subheader("🔐 ADMIN PANEL")

    orders = load_json(ORDERS_FILE, [])
    pending = sum(
        1 for o in orders
        if o.get("status") == "Pending"
    )

    confirmed = sum(
        1 for o in orders
        if o.get("status") in ["Confirmed", "Delivered"]
    )

    a, b, c = st.columns(3)

    a.metric("Products", len(st.session_state.products))
    b.metric("Pending Orders", pending)
    c.metric("Confirmed Orders", confirmed)

    menu = st.selectbox(
        "ADMIN MENU",
        [
            "STORE VIEW",
            "PRODUCT SYSTEM",
            "ORDERS - DARAZ",
            "MONEY",
            "STOCK",
            "BACKUP & RESTORE",
            "SETTINGS"
        ]
    )

    if st.button("LOGOUT", use_container_width=True):
        st.session_state.is_admin = False
        st.rerun()

    st.divider()

# ==========================================
# PRODUCT SYSTEM
# ==========================================

if st.session_state.is_admin and menu == "PRODUCT SYSTEM":

    st.subheader("PRODUCT SYSTEM")

    st.write("Add New Product / Edit Existing Product")

    edit_id = st.selectbox(
        "Select Product to Edit",
        ["NEW PRODUCT"] + [
            p.get("product_id")
            for p in st.session_state.products
        ],
        format_func=lambda x: (
            "NEW PRODUCT"
            if x == "NEW PRODUCT"
            else next(
                (
                    p.get("name", "Product")
                    for p in st.session_state.products
                    if p.get("product_id") == x
                ),
                x
            )
        )
    )

    old = (
        get_product(edit_id)
        if edit_id != "NEW PRODUCT"
        else {}
    ) or {}

    with st.form("product_form"):

        categories = st.session_state.categories

        old_category = old.get("category", "HONEY")

        category = st.selectbox(
            "Category",
            categories,
            index=(
                categories.index(old_category)
                if old_category in categories else 0
            )
        )

        name = st.text_input(
            "Product Name *",
            value=old.get("name", "")
        )

        col1, col2 = st.columns(2)

        with col1:
            buy = st.number_input(
                "Kharid Rate",
                min_value=0,
                max_value=1000000,
                value=int(old.get("kharid", 0))
            )

        with col2:
            sell = st.number_input(
                "Selling Rate",
                min_value=0,
                max_value=1000000,
                value=int(old.get("sell", old.get("final", 0)))
            )

        col3, col4 = st.columns(2)

        with col3:
            discount = st.number_input(
                "Discount %",
                min_value=0,
                max_value=90,
                value=int(old.get("discount", 0))
            )

        with col4:
            stock = st.number_input(
                "Stock",
                min_value=0,
                max_value=100000,
                value=int(old.get("stock", 0))
            )

        expiry = st.date_input(
            "Expiry",
            value=(
                datetime.strptime(old["expiry"], "%Y-%m-%d").date()
                if old.get("expiry")
                else (datetime.now() + timedelta(days=180)).date()
            )
        )

        highlights = st.text_area(
            "Highlights",
            value=old.get("highlights", "")
        )

        description = st.text_area(
            "Full Description",
            value=old.get("full_desc", "")
        )

        specs = st.text_area(
            "Specifications",
            value=old.get("specs", "")
        )

        photo = st.file_uploader(
            "Product Photo",
            type=["jpg", "jpeg", "png", "webp"]
        )

        submitted = st.form_submit_button(
            "SAVE PRODUCT",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not name.strip():
            st.error("Product Name zaroori hai!")

        elif sell < buy:
            st.error("Selling price kharid rate se kam hai!")

        else:

            image_b64 = old.get("image_b64")

            if photo:
                try:
                    img = Image.open(photo).convert("RGB")
                    img.thumbnail((800, 800))

                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=80)

                    image_b64 = base64.b64encode(
                        buffer.getvalue()
                    ).decode()

                except Exception as e:
                    st.error(f"Image Error: {e}")

            final_price = int(sell * (1 - discount / 100))

            product = {
                "product_id": old.get(
                    "product_id",
                    secrets.token_hex(8)
                ),
                "name": name.strip(),
                "category": category,
                "sell": int(sell),
                "kharid": int(buy),
                "discount": int(discount),
                "final": final_price,
                "buy": int(buy),
                "stock": int(stock),
                "expiry": expiry.strftime("%Y-%m-%d"),
                "profit": final_price - int(buy),
                "highlights": highlights,
                "full_desc": description,
                "specs": specs,
                "image_b64": image_b64
            }

            save_product(product)
            st.success("Product Saved Successfully!")
            st.rerun()

    st.divider()
    st.subheader("ALL PRODUCTS")

    for p in list(st.session_state.products):

        with st.container(border=True):

            st.write(
                f"**{p.get('name')}** | "
                f"{p.get('category')} | "
                f"Rs.{p.get('final')}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "DELETE",
                    key="delete_" + p["product_id"]
                ):
                    delete_product(p["product_id"])
                    st.rerun()

            with col2:
                st.write(
                    f"Stock: {p.get('stock', 0)}"
                )

# ==========================================
# ORDERS
# ==========================================

elif st.session_state.is_admin and menu == "ORDERS - DARAZ":

    st.subheader("CUSTOMER ORDERS")

    refresh_orders()

    if not st.session_state.orders:
        st.info("No orders yet.")

    for order in reversed(st.session_state.orders):

        with st.container(border=True):

            st.write(
                f"**Order ID:** {order.get('id')}"
            )

            st.write(
                f"Time: {order.get('time')} | "
                f"Status: {order.get('status')}"
            )

            st.write(
                f"Total: Rs.{order.get('total')}"
            )

            for p in order.get("products", []):
                st.write(
                    f"• {p.get('name')} - Rs.{p.get('price')}"
                )

            current_status = order.get("status", "Pending")

            if current_status == "Pending":

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "CONFIRM",
                        key="confirm_" + order["id"]
                    ):
                        order_status(order["id"], "Confirmed")
                        st.rerun()

                with c2:
                    if st.button(
                        "CANCEL",
                        key="cancel_" + order["id"]
                    ):
                        order_status(order["id"], "Cancelled")
                        st.rerun()

            elif current_status == "Confirmed":

                if st.button(
                    "MARK DELIVERED",
                    key="deliver_" + order["id"]
                ):
                    order_status(order["id"], "Delivered")
                    st.rerun()

            elif current_status == "Cancelled":
                st.error("Order Cancelled")

            else:
                st.success("Order Delivered")

# ==========================================
# MONEY MANAGEMENT
# ==========================================

elif st.session_state.is_admin and menu == "MONEY":

    st.subheader("MONEY MANAGEMENT")

    orders = load_json(ORDERS_FILE, [])

    completed = [
        o for o in orders
        if o.get("status") in ["Confirmed", "Delivered"]
    ]

    sales = sum(
        int(o.get("total", 0))
        for o in completed
    )

    cost = 0

    for order in completed:
        for item in order.get("products", []):
            product = get_product(item.get("product_id"))

            if product:
                cost += (
                    int(product.get("kharid", 0))
                    * int(item.get("quantity", 1))
                )

    profit = sales - cost

    a, b, c = st.columns(3)

    a.metric("Total Sales", f"Rs.{sales}")
    b.metric("Estimated Cost", f"Rs.{cost}")
    c.metric("Estimated Profit", f"Rs.{profit}")

    st.caption(
        "Profit is estimated using the current product purchase rates. "
        "Historical purchase costs are not separately recorded."
    )

    st.subheader("ORDER SUMMARY")

    st.write("Total Orders:", len(orders))
    st.write("Completed Orders:", len(completed))
    st.write("Pending Orders:", pending if 'pending' in locals() else sum(
        1 for o in orders if o.get("status") == "Pending"
    ))

# ==========================================
# STOCK MANAGEMENT
# ==========================================

elif st.session_state.is_admin and menu == "STOCK":

    st.subheader("STOCK MANAGEMENT")

    for p in st.session_state.products:

        with st.container(border=True):

            st.write(f"**{p.get('name')}**")

            st.write(
                f"Available Stock: {p.get('stock', 0)}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(
                    "+1",
                    key="plus_" + p["product_id"]
                ):
                    p["stock"] = int(p.get("stock", 0)) + 1
                    save_json(PRODUCT_FILE, st.session_state.products)
                    st.rerun()

            with col2:
                if st.button(
                    "-1",
                    key="minus_" + p["product_id"]
                ):
                    p["stock"] = max(
                        0,
                        int(p.get("stock", 0)) - 1
                    )
                    save_json(PRODUCT_FILE, st.session_state.products)
                    st.rerun()

            with col3:
                if int(p.get("stock", 0)) <= 5:
                    st.warning("LOW STOCK")

# ==========================================
# BACKUP AND RESTORE
# ==========================================

elif st.session_state.is_admin and menu == "BACKUP & RESTORE":

    st.subheader("BACKUP & RESTORE")

    products_json = json.dumps(
        st.session_state.products,
        ensure_ascii=False,
        indent=2
    )

    orders_json = json.dumps(
        st.session_state.orders,
        ensure_ascii=False,
        indent=2
    )

    st.download_button(
        "DOWNLOAD PRODUCTS BACKUP",
        products_json,
        file_name="mehar_products_backup.json",
        mime="application/json",
        use_container_width=True
    )

    st.download_button(
        "DOWNLOAD ORDERS BACKUP",
        orders_json,
        file_name="mehar_orders_backup.json",
        mime="application/json",
        use_container_width=True
    )

    st.divider()

    st.subheader("RESTORE BACKUP")

    restore_type = st.selectbox(
        "Select Backup Type",
        ["Products", "Orders"]
    )

    uploaded_backup = st.file_uploader(
        "Upload JSON Backup",
        type=["json"]
    )

    if uploaded_backup and st.button(
        "RESTORE BACKUP",
        type="primary"
    ):

        try:
            restored = json.load(uploaded_backup)

            if not isinstance(restored, list):
                raise ValueError("Backup must contain a list.")

            if restore_type == "Products":

                restored, _ = normalize_products(restored)

                if save_json(PRODUCT_FILE, restored):
                    st.session_state.products = restored
                    st.success("Products Restored!")
                    st.rerun()

            else:

                valid = all(
                    isinstance(o, dict)
                    and "id" in o
                    and isinstance(o.get("products", []), list)
                    for o in restored
                )

                if not valid:
                    raise ValueError("Invalid orders backup.")

                if save_json(ORDERS_FILE, restored):
                    st.session_state.orders = restored
                    st.success("Orders Restored!")
                    st.rerun()

        except Exception as e:
            st.error(f"Restore Error: {e}")

# ==========================================
# SETTINGS
# ==========================================

elif st.session_state.is_admin and menu == "SETTINGS":

    st.subheader("ADMIN SETTINGS")

    with st.form("password_change"):

        old_password = st.text_input(
            "Old Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        change = st.form_submit_button(
            "CHANGE PASSWORD",
            type="primary"
        )

    if change:

        if not check_password(old_password):
            st.error("Old password incorrect!")

        elif len(new_password) < 8:
            st.error("New password kam az kam 8 characters ka hona chahiye.")

        elif new_password != confirm_password:
            st.error("Passwords do not match!")

        elif save_password(new_password):
            st.success("Password Changed Successfully!")

    st.divider()

    st.subheader("STORE CATEGORIES")

    for cat in st.session_state.categories:
        st.write("•", cat)

    new_category = st.text_input("Add New Category")

    if st.button("ADD CATEGORY"):

        category = new_category.strip().upper()

        if category and category not in st.session_state.categories:
            st.session_state.categories.append(category)
            save_json(CAT_FILE, st.session_state.categories)
            st.success("Category Added!")
            st.rerun()

# ==========================================
# CUSTOMER STORE
# ==========================================

else:

    refresh_products()

    products = [
        p for p in st.session_state.products
        if isinstance(p, dict)
    ]

    if st.session_state.selected_product:

        p = get_product(st.session_state.selected_product)

        if p:

            if st.button("← BACK TO STORE"):
                st.session_state.selected_product = None
                st.rerun()

            img = image_from_product(p)

            if img:
                st.image(img, use_container_width=True)

            st.title(p.get("name", "Product"))

            st.caption(p.get("category", ""))

            st.markdown(
                f'<div class="price">Rs. {p.get("final", 0)}</div>',
                unsafe_allow_html=True
            )

            st.write(p.get("highlights", ""))

            st.write(p.get("full_desc", ""))

            st.write("Specifications:")
            st.write(p.get("specs", ""))

            st.write(
                f"Stock Available: {p.get('stock', 0)}"
            )

            if st.button(
                "ADD TO CART",
                type="primary",
                use_container_width=True,
                disabled=int(p.get("stock", 0)) <= 0
            ):

                st.session_state.cart.append(
                    p["product_id"]
                )

                st.success("Added to Cart!")
                st.rerun()

            if st.button(
                f"BUY NOW - Rs.{p.get('final', 0)}",
                use_container_width=True,
                disabled=int(p.get("stock", 0)) <= 0
            ):

                oid = create_order([p], p.get("final", 0))

                message = get_whatsapp_msg(
                    oid,
                    [p],
                    p.get("final", 0)
                )

                st.link_button(
                    "CONFIRM ORDER ON WHATSAPP",
                    whatsapp_link(message),
                    type="primary",
                    use_container_width=True
                )

        else:
            st.session_state.selected_product = None
            st.rerun()

    else:

        st.markdown("### 🛍️ SHOP OUR PRODUCTS")

        col1, col2 = st.columns([3, 1])

        with col1:
            search = st.text_input(
                "Search",
                placeholder="Search products..."
            )

        with col2:
            cart_count = len(st.session_state.cart)
            st.metric("Cart", cart_count)

        categories = ["All"] + st.session_state.categories

        category = st.selectbox(
            "Select Category",
            categories
        )

        # CART

        if st.session_state.cart:

            with st.container(border=True):

                st.subheader("🛒 YOUR CART")

                cart_products = []

                for product_id in st.session_state.cart:
                    product = get_product(product_id)

                    if product:
                        cart_products.append(product)

                for i, item in enumerate(cart_products):

                    c1, c2 = st.columns([4, 1])

                    with c1:
                        st.write(
                            f"{item.get('name')} - "
                            f"Rs.{item.get('final')}"
                        )

                    with c2:
                        if st.button("X", key=f"remove_{i}"):
                            st.session_state.cart.pop(i)
                            st.rerun()

                cart_total = sum(
                    int(p.get("final", 0))
                    for p in cart_products
                )

                st.subheader(f"TOTAL: Rs.{cart_total}")

                can_checkout = bool(cart_products) and all(
                    int(p.get("stock", 0)) > 0
                    for p in cart_products
                )

                if st.button(
                    "CHECKOUT",
                    type="primary",
                    use_container_width=True,
                    disabled=not can_checkout
                ):

                    oid = create_order(
                        cart_products,
                        cart_total
                    )

                    message = get_whatsapp_msg(
                        oid,
                        cart_products,
                        cart_total
                    )

                    st.session_state.cart = []
                    st.session_state.notice = (
                        f"Order {oid} created. WhatsApp par confirm karein."
                    )

                    st.link_button(
                        "WHATSAPP ORDER CONFIRM",
                        whatsapp_link(message),
                        type="primary",
                        use_container_width=True
                    )

        # FILTER PRODUCTS

        filtered = products

        if category != "All":
            filtered = [
                p for p in filtered
                if p.get("category", "").upper() == category.upper()
            ]

        if search.strip():
            filtered = [
                p for p in filtered
                if search.lower() in p.get("name", "").lower()
            ]

        st.write(f"**{len(filtered)} Products Found**")

        if not filtered:
            st.info("Is category mein abhi products available nahi hain.")

        cols = st.columns(2)

        for i, p in enumerate(filtered):

            with cols[i % 2]:

                with st.container(border=True):

                    img = image_from_product(p)

                    if img:
                        st.image(
                            img,
                            use_container_width=True
                        )

                    st.write(f"**{p.get('name', '')}**")

                    st.caption(
                        p.get("category", "")
                    )

                    st.markdown(
                        f'<div class="price">Rs.{p.get("final", 0)}</div>',
                        unsafe_allow_html=True
                    )

                    if p.get("discount", 0):
                        st.caption(
                            f"{p.get('discount')}% OFF"
                        )

                    if int(p.get("stock", 0)) <= 0:
                        st.error("Out of Stock")

                    if st.button(
                        "VIEW DETAILS",
                        key="view_" + p["product_id"],
                        use_container_width=True
                    ):
                        st.session_state.selected_product = p["product_id"]
                        st.rerun()

                    if st.button(
                        "ADD TO CART",
                        key="add_" + p["product_id"],
                        type="primary",
                        use_container_width=True,
                        disabled=int(p.get("stock", 0)) <= 0
                    ):
                        st.session_state.cart.append(
                            p["product_id"]
                        )
                        st.rerun()

                    if st.button(
                        "BUY NOW",
                        key="buy_" + p["product_id"],
                        use_container_width=True,
                        disabled=int(p.get("stock", 0)) <= 0
                    ):

                        oid = create_order(
                            [p],
                            p.get("final", 0)
                        )

                        message = get_whatsapp_msg(
                            oid,
                            [p],
                            p.get("final", 0)
                        )

                        st.link_button(
                            "WHATSAPP CONFIRM",
                            whatsapp_link(message),
                            use_container_width=True
                        )

# ==========================================
# JARVIS AI CUSTOMER ASSISTANT
# ==========================================

st.divider()

st.header("🤖 MEHAR MART AI AGENT - JARVIS")

st.caption(
    "Smart Product Assistant | Basic Mode | No Gemini API Required"
)

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

user_question = st.chat_input(
    "Salam! Product ke bare mein poochhein..."
)

if user_question:

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    answer = get_smart_answer(user_question)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

if st.button("CLEAR CHAT"):
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Salam Bhai! Mehar Mart mein khush amdeed!"
        }
    ]
    st.rerun()

st.divider()

st.markdown(
    """
    **MEHAR MART**

    Quality Products at Affordable Prices

    Cash on Delivery | Delivery All Over Pakistan

    """
)

st.link_button(
    "CONTACT MEHAR MART ON WHATSAPP",
    "https://wa.me/" + WA_NUMBER,
    use_container_width=True
)
