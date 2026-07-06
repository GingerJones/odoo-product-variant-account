# Copyright 2026 Nathan Jones
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestProductVariantAccount(AccountTestInvoicingCommon):
    """The variant-specific account must win over the template/category one on
    customer invoices (income) and vendor bills (expense), while variants that
    define no override keep falling back to the template account.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.income_template = cls.copy_account(cls.company_data["default_account_revenue"])
        cls.income_variant = cls.copy_account(cls.company_data["default_account_revenue"])
        cls.expense_template = cls.copy_account(cls.company_data["default_account_expense"])
        cls.expense_variant = cls.copy_account(cls.company_data["default_account_expense"])

        attribute = cls.env["product.attribute"].create(
            {
                "name": "Test Color",
                "create_variant": "always",
                "value_ids": [(0, 0, {"name": "Red"}), (0, 0, {"name": "Blue"})],
            }
        )
        cls.template = cls.env["product.template"].create(
            {
                "name": "Variant Account Test Product",
                "property_account_income_id": cls.income_template.id,
                "property_account_expense_id": cls.expense_template.id,
                "attribute_line_ids": [
                    (0, 0, {"attribute_id": attribute.id, "value_ids": [(6, 0, attribute.value_ids.ids)]})
                ],
            }
        )
        cls.variant_overridden = cls.template.product_variant_ids[0]
        cls.variant_plain = cls.template.product_variant_ids[1]
        cls.variant_overridden.variant_income_account_id = cls.income_variant
        cls.variant_overridden.variant_expense_account_id = cls.expense_variant

    def _line_for(self, move_type, product):
        move = self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner_a.id,
                "invoice_line_ids": [(0, 0, {"product_id": product.id, "quantity": 1})],
            }
        )
        return move.invoice_line_ids

    def test_income_override_on_customer_invoice(self):
        line = self._line_for("out_invoice", self.variant_overridden)
        self.assertEqual(line.account_id, self.income_variant)

    def test_income_fallback_on_customer_invoice(self):
        line = self._line_for("out_invoice", self.variant_plain)
        self.assertEqual(line.account_id, self.income_template)

    def test_expense_override_on_vendor_bill(self):
        line = self._line_for("in_invoice", self.variant_overridden)
        self.assertEqual(line.account_id, self.expense_variant)

    def test_expense_fallback_on_vendor_bill(self):
        line = self._line_for("in_invoice", self.variant_plain)
        self.assertEqual(line.account_id, self.expense_template)

    def test_override_survives_posting(self):
        line = self._line_for("out_invoice", self.variant_overridden)
        line.move_id.action_post()
        self.assertEqual(line.move_id.state, "posted")
        self.assertEqual(line.account_id, self.income_variant)

    def test_get_product_accounts_prefers_variant(self):
        accounts = self.variant_overridden._get_product_accounts()
        self.assertEqual(accounts["income"], self.income_variant)
        self.assertEqual(accounts["expense"], self.expense_variant)
