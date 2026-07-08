# Copyright 2026 Nathan Jones
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Product Variant Accounts",
    "version": "18.0.1.0.2",
    "summary": "Set the income and expense account per product variant, so "
    "different variants of the same product post to different accounts.",
    "author": "Nathan Jones",
    "website": "https://nath.uk",
    "support": "support@nath.uk",
    "license": "LGPL-3",
    "category": "Accounting/Accounting",
    "depends": ["account"],
    "data": ["views/product_views.xml"],
    "images": [
        "static/description/banner.png",
        "static/description/variant_accounts_tab.png",
        "static/description/attributes_variants_tab.png",
    ],
    "development_status": "Production/Stable",
    "installable": True,
    "application": True,
}
