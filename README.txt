# MEHAR MART V104 — Permanent Cloud Edition

V104 preserves the V94 Streamlit + Supabase system and includes the order-confirmation stock fix.

## Order / stock rules
- Confirming an order subtracts only the ordered quantity from each matching product's stock.
- A product is NEVER deleted when an order is confirmed.
- If stock reaches 0, the product remains visible in the public shop with **Out of Stock** status.
- Add to Cart is disabled when stock is 0.
- Product deletion is available only through the Admin Product System's manual **Delete** button.
- Confirmation is protected against duplicate stock deductions using the `stock_deducted` order flag.
- If inventory is insufficient or a product record is missing, confirmation is blocked and stock is not changed.

Examples: stock 10, order quantity 1 → stock 9, product remains visible.
Stock 1, order quantity 1 → stock 0, product remains visible as Out of Stock.

## Package files
- `app.py` — complete Streamlit storefront and private Admin panel
- `requirements.txt` — Python dependencies
- `supabase_schema.sql` — Supabase tables and triggers
- `README.txt` — setup and deployment guide
- `tests/test_stock_logic.py` — regression tests for stock behavior

## Supabase setup
1. Supabase Dashboard → SQL Editor → New query → run `supabase_schema.sql`.
2. Streamlit Community Cloud → your app → Settings → Secrets:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SUPABASE_SECRET_KEY = "sb_secret_YOUR_SECRET_KEY"
ADMIN_PASSWORD = "ChooseYourOwnStrongPassword"
```

Keep the `sb_secret_...` key only in Streamlit server Secrets. Never paste it into chat, GitHub, app.py, or browser code.

## Deploy
1. Keep your original V93 and V94 backups unchanged.
2. Upload this package's `app.py` and `requirements.txt` to the GitHub repository connected to Streamlit Cloud.
3. Confirm the Supabase schema and Streamlit Secrets are configured.
4. Public store URL: your normal Streamlit URL.
5. Admin URL: append `?admin=1` to the public URL and log in with `ADMIN_PASSWORD`.

This ZIP does not contain your Supabase secret key or live database contents. Test with one sample product/order before accepting real orders.
