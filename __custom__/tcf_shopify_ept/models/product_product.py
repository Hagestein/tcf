import logging
from datetime import datetime
from odoo.exceptions import Warning
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_qty_on_hand(self, warehouse, product_list):
        on_hand_products = self.env['product.product'].with_context(dict(self._context, warehouse=warehouse.id)).read_group([('id', 'in', product_list.ids)], fields=['free_qty'])
        _logger.info(on_hand_products)
        onhand_list = []
        # This is needed to keep the rest of the modules working
        for on_hand_product in on_hand_products:
            onhand_list.append({'product_id': on_hand_product['id'], 'stock': on_hand_product['free_qty']})
        return onhand_list

    def get_forecated_qty(self, warehouse, product_list):
        va_products = self.env['product.product'].with_context(dict(self._context, warehouse=warehouse.id)).read_group([('id', 'in', product_list.ids)], fields=['virtual_available'])
        _logger.info(va_products)
        va_list = []
        # This is needed to keep the rest of the modules working
        for va_product in va_products:
            va_list.append({'product_id': va_product['id'], 'stock': va_product['virtual_available']})
        return va_list
