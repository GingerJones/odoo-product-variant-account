=========================================
Product Variant Income & Expense Accounts
=========================================

.. |badge1| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

|badge1|

Odoo lets you configure an **income** and **expense** account on the product
*template* and the product *category*, but every variant of a template shares
those same accounts. This module adds a per-**variant** income/expense account
override, so different variants of the same product can post to different
accounts.

When a variant leaves the override empty, Odoo falls back to the usual
template / category account. The module is therefore safe to install on an
existing database: nothing changes until you set an override on a variant.

**Table of contents**

.. contents::
   :local:

Features
========

* An **Income Account** and **Expense Account** field on each product variant.
* Set them per variant directly from the product's **Accounting** tab (an
  editable list of variants) or from an individual variant's form.
* Overrides are applied on customer invoices (income), vendor bills (expense)
  and Point of Sale, with fiscal-position account mapping preserved.
* Accounts are company-dependent, matching the standard template accounts.

Requirement
===========

The per-variant accounts apply to products that have **actual variant
records**. A product only has separate variants when the related attribute's
**Variants Creation** mode is set to **Instantly**
(*Inventory → Configuration → Attributes*). If an attribute is set to
**Never (option)**, the product stays a single variant and the
**Variant-specific Accounts** list is not shown — the standard
template/category account is used instead.

Configuration
=============

The fields are visible to users in the *Show Accounting Features* group
(``account.group_account_readonly``), the same group that gates the standard
product income/expense accounts.

Usage
=====

#. Open a product that has more than one variant.
#. Go to the **Accounting** tab.
#. In the **Variant-specific Accounts** list, set an **Income Account** and/or
   **Expense Account** for the variants that need a specific account. Leave a
   variant blank to keep using the template/category account.
#. Alternatively, open a single variant (via the *Variants* smart button) and
   set the accounts on its own **Accounting** tab.

Invoices, vendor bills and POS orders for those variants will then post to the
variant-specific account.

Credits
=======

Authors
~~~~~~~

* Nathan Jones

Maintainers
~~~~~~~~~~~

This module is maintained by Nathan Jones.
