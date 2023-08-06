from comring.lib import tool, cache
import logging
import csv
import re

LOGGER = logging.getLogger(__name__)

class DOPFIValue():
    def __init__(self, instance):
        self.do_domain = []
        self.product_cache = None
        self.categ_cache = None
        self.instance = instance

    def get_pfi_value(self, do_numbers):
        pickings = self.instance.client.search_read('stock.picking', [('name', 'in', do_numbers), ('is_relate_to_so', '=', True), ('state', '=', 'done')], ['id', 'name', 'partner_id', 'create_date'])
        for picking in pickings:
            picking_print_data = self.instance.client.call('stock.picking', 'generate_data', [picking['id']], {'_print_type': 'proforma'})
            picking['pfi_value'] = 0
            if picking_print_data:
                picking['pfi_value'] = picking_print_data['amount_total']
            else:
                LOGGER.warn('PFI value not available for %s', picking['name'])
            picking['pfi_value_fmt'] = '{:,.2f}'.format(picking['pfi_value'])
        return pickings



