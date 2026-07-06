# Copyright 2026 Nathan Jones
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models

# Mirror the domain core uses for the template-level income/expense accounts
# (account/models/product.py) so the variant override offers the same choices.
ACCOUNT_DOMAIN = (
    "['&', ('deprecated', '=', False), "
    "('account_type', 'not in', ('asset_receivable', 'liability_payable', "
    "'asset_cash', 'liability_credit_card', 'off_balance'))]"
)


class ProductProduct(models.Model):
    _inherit = "product.product"

    # NB: distinct field names on purpose. product.product `_inherits` from
    # product.template, so `property_account_income_id` is *delegated* to the
    # template (shared by every variant). Reusing that name here would break
    # the delegation; instead we add variant-only override fields.
    variant_income_account_id = fields.Many2one(
        comodel_name="account.account",
        company_dependent=True,
        ondelete="restrict",
        string="Variant Income Account",
        domain=ACCOUNT_DOMAIN,
        help="Income account used specifically for this variant. Leave empty "
        "to fall back to the account defined on the product template or its "
        "category.",
    )
    variant_expense_account_id = fields.Many2one(
        comodel_name="account.account",
        company_dependent=True,
        ondelete="restrict",
        string="Variant Expense Account",
        domain=ACCOUNT_DOMAIN,
        help="Expense account used specifically for this variant. Leave empty "
        "to fall back to the account defined on the product template or its "
        "category.",
    )

    def _get_product_accounts(self):
        """Let a per-variant account win over the template/category one.

        This covers consumers that resolve accounts through the *variant*
        (e.g. Point of Sale). Customer/vendor invoices resolve through the
        template instead, so those are handled in ``account.move.line``.
        """
        accounts = super()._get_product_accounts()
        if self.variant_income_account_id:
            accounts["income"] = self.variant_income_account_id
        if self.variant_expense_account_id:
            accounts["expense"] = self.variant_expense_account_id
        return accounts
