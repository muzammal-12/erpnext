# 🇵🇰 ERPNext Pakistan Localization + RBAC System

This repository provides a complete ERPNext customization with:

- ✅ Pakistan-specific Tax Setup (FBR/SRB compliance)
- ✅ Automated Annexure-C (DSI) and SRB Sales Tax Reports
- ✅ Full working Upload to IRIS feature
- ✅ Custom Role-Based Access Control (RBAC) system for departmental workflows

---

## 📦 Requirements

- ERPNext: v15.70.1  
- Frappe: v15.74.0  
- Python 3.10+  
- MariaDB, Redis, Node.js, Yarn  
- Bench CLI installed and site created (e.g. `erpsite.local`)

---

## 🔧 Installation

1. **Clone the App:**

```bash
cd ~/frappe-bench/apps
git clone https://github.com/muzammal-12/erpnext.git
````

2. **Install on your site:**

```bash
cd ~/frappe-bench
bench --site erpsite.local install-app erpnext
bench --site erpsite.local migrate
bench --site erpsite.local clear-cache
```

---

## 🧭 Feature Overview

### 🇵🇰 Pakistan Tax System Setup Page

**Path:** `erpnext/accounts/page/pakistan_tax_setup/`

UI available under **Accounting > Pakistan Tax Setup**

* Store National Tax Numbers:

  * NIC
  * NTN
  * STRN
* Buttons to:

  * Create customers with tax metadata
  * Generate and download Annexure-C and SRB CSVs
  * Open FBR IRIS upload portal with one click
* No login restrictions — Upload to IRIS works for any user

---

### 📊 DSI & SRB Sales Tax Reports

Available under **Accounting > Reports**

#### DSI Annexure C

* Filters:

  * `from_date`
  * `to_date`
  * `company`
* Button: **Upload to IRIS** (downloads CSV + opens IRIS)
* Exports located in:
  `sites/erpsite.local/private/files/DSI_*.csv`

#### SRB Sales Tax Report

* Filters:

  * `from_date`
  * `to_date`
  * `company`
* Same upload/export behavior
* CSV is SRB-compliant and IRIS-ready

---

### 🔐 Custom RBAC System

**Files:**

* `erpnext/custom_scripts/rbac_roles.py`
* `erpnext/hooks.py`

Granular role control by module and workspace:

* Tax Officer → only accounting + reports
* Restaurant Manager → POS & Sales only
* Stock Clerk → warehouse + inventory
* Admin → full access

All access rights are enforced via Python backend logic and hooks — not just UI-level.

---

## 🧾 Directory Structure

```
erpnext/
├── accounts/
│   ├── page/pakistan_tax_setup/
│   └── report/
│       ├── dsi_annexure_c/
│       └── srb_sales_tax_report/
├── api/tax_report_api.py
├── custom_scripts/
│   ├── create_pakistan_tax_page_ui.py
│   ├── refresh_tax_fields.py
│   └── rbac_roles.py
├── fixtures/
└── hooks.py
```

---

## 💡 Developer Tips

### Reload reports manually if needed

```bash
bench --site erpsite.local reload-doc erpnext accounts/report dsi_annexure_c
bench --site erpsite.local reload-doc erpnext accounts/report srb_sales_tax_report
bench --site erpsite.local migrate
bench --site erpsite.local clear-cache
```

### If you get KeyError like `from_date` or `company`

Make sure:

* Report `.json` defines filters correctly
* `.sql` file uses them like: `... WHERE invoice_date BETWEEN %(from_date)s AND %(to_date)s`

---

## 🛠 Git Push Instructions

```bash
cd ~/frappe-bench/apps/erpnext
git add .
git commit -m "Added Pakistan Tax System + Upload to IRIS + RBAC System"
git push origin main
```

---

## 🙋‍♂️ Maintainer

* GitHub: [muzammal-12](https://github.com/muzammal-12)
* Contact: See GitHub profile

---

## 📝 License

MIT — free for commercial and educational use

---

## 📅 Last Updated

**July 22, 2025**

```

---

Let me know if you’d like me to generate badges, a GIF demo, or a `pakistan_tax_setup.py` test file!
```
