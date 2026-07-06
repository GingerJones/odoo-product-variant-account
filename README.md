# Odoo – Product Variant Income & Expense Accounts

[![License: LGPL-3](https://img.shields.io/badge/licence-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0-standalone.html)
![Odoo 18.0](https://img.shields.io/badge/Odoo-18.0-714B67.svg)

An Odoo 18 module that lets you set an **income** and **expense** account **per
product variant**. Odoo natively configures these accounts only on the product
*template* and *category*, so every variant shares the same accounts. This
module adds a per-variant override that is applied on customer invoices, vendor
bills and Point of Sale — with fiscal-position mapping preserved.

When a variant leaves the override empty, Odoo falls back to the usual
template / category account, so the module is safe to install on an existing
database.

## Repository layout

This repository is an Odoo addons directory: point your `addons_path` (or your
Odoo.sh repository) at the repository root, and the module below is detected
automatically.

```
.
└── product_variant_account/     # the Odoo module
```

## Installation

1. Clone this repository into a directory on your Odoo `addons_path`
   (on Odoo.sh, commit it to the repository your build tracks):

   ```bash
   git clone https://github.com/<your-org>/odoo-product-variant-account.git
   ```

2. Restart Odoo and update the apps list.
3. Install **Product Variant Income & Expense Accounts** from the Apps menu.

## Requirement

The per-variant accounts apply to products that have **actual variant
records**. A product only has separate variants when the related attribute's
**Variants Creation** mode is set to **Instantly**
(*Inventory → Configuration → Attributes*). Attributes set to **Never (option)**
keep the product as a single variant, so the **Variant-specific Accounts** list
is not shown and the standard template/category account is used.

## Usage

1. Open a product that has more than one variant.
2. Go to the **Accounting** tab.
3. In the **Variant-specific Accounts** list, set an income and/or expense
   account for the variants that need one. Leave a variant blank to keep using
   the template/category account.
4. Alternatively, open an individual variant (via the *Variants* smart button)
   and set the accounts on its own **Accounting** tab.

## Tests

```bash
odoo -d <db> --test-enable --test-tags /product_variant_account -i product_variant_account --stop-after-init
```

## License

[LGPL-3](LICENSE) © Nathan Jones
