# -*- coding: utf-8 -*-
# Copyright© 2017- erp-m <http://www.erp-m.eu>
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    lst_price_incl_tax = fields.Float(
        string='Sale Price (incl VAT)',
        compute='_compute_taxed_lst_price',
        digits=dp.get_precision('Product Price'),
    )

    @api.depends('taxes_id', 'lst_price')
    def _compute_taxed_lst_price(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        for product in self:
            product.lst_price_incl_tax = product.taxes_id.filtered(
                lambda x: x.company_id.id == company_id).compute_all(
                    product.lst_price,
                    self.env.user.company_id.currency_id,
                    product=product)['total_included']
