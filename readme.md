# CKAN Deduplication Script

This script connects to a CKAN instance and identifies datasets (`packages`) that share the same `uri`, either at the top-level or inside the `extras`. It then retains only the most recently modified version of each duplicate group and marks the rest as deleted.

---

## 🚀 Features

- Fetches all active datasets from a CKAN instance
- Extracts `uri` from top-level and `extras`
- Groups datasets by `uri`
- Detects duplicates (same `uri`)
- Keeps only the latest version (by `metadata_modified`)
- Marks older duplicates as `deleted` (soft delete)

---

## 📦 Requirements

Install Python dependencies using pip:

```bash
pip install -r requirements.txt
```
You may optionally create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  
```

## ⚙️ Configuration

### 🔗 CKAN Endpoint

Edit the Python script to configure your CKAN instance and API key:

```python
ckan = RemoteCKAN('https://ckan.your-domain.nl', apikey='your-api-key')
```

### 🔐 Retrieving Your CKAN API Key

Your API key is stored in **1Password**.

1. Open **1Password**.
2. Search for **"CKAN API TOKEN"**.
3. Locate the entry for the appropriate environment (e.g. `test`, `acc`, `production`).
4. Copy the key and paste it into the script in place of `'your-api-key'`.

## 🧪 Running the Script

To execute the deduplication process:

```bash
python deduplicate_ckan.py
```

