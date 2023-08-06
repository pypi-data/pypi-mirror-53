#!/usr/bin/env python3

# Ad Hoc script for GLPI 18512 - Request data korporat

import os
import csv
import re
import psycopg2
from loguru import logger as LOGGER

from comring.lib import odoo

ODOO_URL = 'https://odoo.pti-cosmetics.com'

#data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'glpi_18512.csv')
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'glpi_18512b.csv')

invoice_list = []
LOGGER.info('Reading invoice list data')
with open(data_path, 'rt') as f:
    reader = csv.DictReader(f)
    for row in reader:
        invoice_list.append({'number': row['number']})

LOGGER.info('Connecting to Odoo')
server = odoo.Odoo(ODOO_URL)
client = server.login('paragon', 'it-agustianes', 'aghi2kaisa6G')

LOGGER.info('Fetching data from Odoo')
for inv in invoice_list:
    oinv = client.search_read_one('account.invoice', [('number', '=', inv['number'])], ['id', 'number', 'name'])
    if oinv:
        inv['id'] = oinv['id']
        inv['name'] = oinv['name']

LOGGER.info('Parsing invoice references')
pattern = re.compile(r'([A-Z]+) / ([A-Z0-9]+) / ([A-Z ]+)')
by_dc_by_unit = {}
for inv in invoice_list:
    ref = inv.get('name', '')
    match = pattern.match(ref)
    dc_alias = korporat_ref = korporat_unit = ''
    if match:
        dc_alias = match.group(1)
        korporat_ref = match.group(2)
        korporat_unit = match.group(3)
    if korporat_unit == 'MAKE OVER':
        korporat_unit = 'mo'

    if dc_alias and korporat_ref and korporat_unit:
        key = (dc_alias, korporat_unit)
        invoices = by_dc_by_unit.setdefault(key, [])
        invoices.append({'ref': korporat_ref, 'odoo_number': inv['number'], 'total': 0, 'paid': 0, 'due': 0})

LOGGER.info('Reading invoice details from korporat')
conn = psycopg2.connect('host=10.3.5.13 port=5479 user=anes password=ptiuser1234 dbname=korporat')
cur = conn.cursor()
for dc, unit in by_dc_by_unit:
    invoices = by_dc_by_unit.get((dc, unit))
    for inv in invoices:
        inv_ref = inv.get('ref', None)
        if not inv_ref:
            continue
        query = 'SELECT nobon, jumhartag, bayar FROM ' + dc.lower() + '.' + unit.lower() + '_datjual_bon WHERE nobon = %s;'
        cur.execute(query, (inv_ref,))
        res = cur.fetchone()
        if res:
            inv['total'] = res[1] or 0
            inv['paid'] = res[2] or 0
            inv['due'] = inv['total'] - inv['paid']
cur.close()
conn.close()

LOGGER.info('Writing result')
with open('/tmp/output_glpi_18512.csv', 'wt') as f:
    writer = csv.DictWriter(f, ['odoo_number', 'ref', 'total', 'paid', 'due'])
    writer.writeheader()
    for dc, unit in by_dc_by_unit:
        invoices = by_dc_by_unit.get((dc, unit))
        for inv in invoices:
            writer.writerow(inv)

LOGGER.info('All Done!')
