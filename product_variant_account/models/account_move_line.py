# Copyright 2026 Nathan Jones
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _compute_account_id(self):
        """Let a per-variant income/expense account override the computed one.

        Core resolves invoice-line accounts from the product *template*
        (``product_tmpl_id.get_product_accounts``), so a variant-specific
        account is invisible to it. We let core compute first, then, for
        invoice lines whose selected variant defines its own account,
        substitute it — applying the move's fiscal position exactly as core
        does so mapped accounts keep working.
        """
        super()._compute_account_id()
        for line in self:
            move = line.move_id
            if line.display_type != "product" or not line.product_id:
                continue
            if not move.is_invoice(include_receipts=True):
                continue
            # company_dependent fields must be read in the move's company.
            variant = line.with_company(line.company_id).product_id
            if move.is_sale_document(include_receipts=True):
                account = variant.variant_income_account_id
            elif move.is_purchase_document(include_receipts=True):
                account = variant.variant_expense_account_id
            else:
                continue
            if account:
                fpos = move.fiscal_position_id
                line.account_id = fpos.map_account(account) if fpos else account
