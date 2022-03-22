# -*- coding: utf-8 -*-
# Copyright© 2017- erp-m <http://www.erp-m.eu>
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

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
            _logger.info("Set Price: Product: %s" % variant.product_id.name)
            price = instance.shopify_pricelist_id.get_product_price(variant.product_id, 1.0, partner=False,
                                                                    uom_id=variant.product_id.uom_id.id)
            _logger.info("Set Price: Price: %s" % price)
            incl_price = variant.product_id.taxes_id.filtered(
                lambda x: x.company_id.id == self.env.user.company_id.id).compute_all(
                    price,
                    self.env.user.company_id.currency_id,
                    product=variant.product_id)['total_included']
            variant_vals.update({'price': float(incl_price)})
            _logger.info("Set Price: InclPrice: %s" % incl_price)
        return variant_vals