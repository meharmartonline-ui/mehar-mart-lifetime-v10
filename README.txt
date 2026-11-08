# MEHAR MART V94 - Permanent Cloud Edition

## Files
- `app.py` - Streamlit store + private admin panel
- `requirements.txt` - Python packages
- `supabase_schema.sql` - Database tables

## 1. Create Supabase tables
1. Open Supabase Dashboard.
2. Open SQL Editor -> New query.
3. Paste all of `supabase_schema.sql`.
4. Click Run.

## 2. Add Streamlit Cloud Secrets
Open Streamlit Community Cloud -> your app -> Settings -> Secrets.
Add:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SUPABASE_SECRET_KEY = "sb_secret_YOUR_SECRET_KEY"
ADMIN_PASSWORD = "SetYourOwnStrongAdminPassword"
```

IMPORTANT:
- Use the `sb_secret_...` key only in Streamlit server Secrets.
- Never put `sb_secret_...` in app.py, GitHub, browser code, or chat.
- The publishable key is not used by this server-side V94 setup.
- Do not send secrets/screenshots that reveal secret values.

## 3. Deploy
Upload `app.py`, `requirements.txt` to the GitHub repository used by Streamlit Cloud.
Keep V93 separately as a backup; do not overwrite your only V93 copy.

## 4. Admin
Open the public app URL and append `?admin=1` to the URL.
Example: `https://your-app.streamlit.app/?admin=1`
Log in using `ADMIN_PASSWORD` set in Streamlit Secrets.

After first login, V94 stores a salted PBKDF2 password hash in Supabase. You can then change the password from Admin -> SETTINGS.

## 5. V93 data migration
V94 can import local V93 JSON files only if those files are present in the Streamlit app runtime during the first launch:
- products.json or products_backup.json
- orders.json or orders_backup.json
- categories.json
- logo.json

If Streamlit Cloud has already lost those files, use V93 Admin -> BACKUP to download the JSON backups and then use V94 Admin -> BACKUP to restore products. Orders can be imported by preparing an orders JSON importer in a future patch; keep your original order backup safe.

## Notes
- Product images are stored as base64 inside JSONB product data. This is easy for a small shop migration, but large catalogs may eventually benefit from Supabase Storage.
- This is a first cloud-connected V94 release. Test with one sample product and one test order before sharing the public link widely.
- The Streamlit admin login is server-side. Do not expose Supabase secret key to customers.
