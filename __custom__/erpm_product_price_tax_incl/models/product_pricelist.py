# -*- coding: utf-8 -*-
# Copyright© 2017- erp-m <http://www.erp-m.eu>

from odoo import models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def get_products_price(self,
                           products,
                           quantities,
                           partners,
                           date=False,
                           uom_id=False):
        res = super(ProductPricelist, self).get_products_price(products,
                                                               quantities,
                                                               partners,
                                                               date=date,
                                                               uom_id=uom_id)
        if self._context.get('tax_incl'):
            company_id = (self._context.get('company_id')
                          or self.env.user.company_id.id)
            for product in products:
                res[product.id] = product.taxes_id.filtered(
                    lambda x: x.company_id.id == company_id).compute_all(
                        res[product.id], product=product)['total_included']
        return res

    def get_product_price(self,
                          product,
                          quantity,
                          partner,
                          date=False,
                          uom_id=False):
        getprice = super(ProductPricelist,
                         self).get_product_price(product,
                                                 quantity,
                                                 partner,
                                                 date=date,
                                                 uom_id=uom_id)
        if self._context.get('tax_incl'):
            company_id = (self._context.get('company_id')
                          or self.env.user.company_id.id)
            getprice = product.taxes_id.filtered(
                lambda x: x.company_id.id == company_id).compute_all(
                    getprice, product=product)['total_included']
        return getprice
