# -*- coding: utf-8 -*-
# Copyright© 2017- erp-m <http://www.erp-m.eu>
from odoo import models, fields, api


class ShopifyProductProductEpt(models.Model):
    _inherit = "shopify.product.product.ept"

    def shopify_prepare_variant_vals(self, instance, variant, is_set_price, is_set_basic_detail):
        """
        Inherit to adjust the shopify price in including BTW
        """
        variant_vals = super(ShopifyProductProductEpt,
                             self).shopify_prepare_variant_vals(
                                 instance, variant, is_set_price,
                                 is_set_basic_detail)
        if is_set_price:
            price = instance.shopify_pricelist_id.with_context(
                tax_incl=True).get_product_price(
                    variant.product_id,
                    1.0,
                    partner=False,
                    uom_id=variant.product_id.uom_id.id)
            variant_vals.update({'price': float(price)})
        return variant_vals