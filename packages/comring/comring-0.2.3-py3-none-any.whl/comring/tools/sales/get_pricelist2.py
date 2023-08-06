from comring.lib import odoo
from comring.lib import config
import getpass
import logging
import csv

env = 'live'
out_file = '/tmp/data_pricelist.csv'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

conf = config.Config()

url = conf.env_get(env, 'server_url')
db = conf.env_get(env, 'database')
user = conf.env_get(env, 'user')

logging.info('Logging in to %s database [%s] as [%s]', url, db, user)
passwd = ''
try:
    passwd = getpass.getpass(prompt='Password for {}: '.format(user))
except Exception as err:
    logging.error('ERROR while getting password', exc_info=err)
    exit(1)

osv = odoo.Odoo(url)
try:
    client = osv.login(db, user, passwd)
except Exception as err:
    logging.error('ERROR while logging in', exc_info=err)
    exit(2)


def get_data(client, prod_ids, pricelist_id):
    data = client.read('product.product', prod_ids,
                       ['id', 'default_code', 'name', 'price'],
                       context={'pricelist': pricelist_id}
                       )
    return data


product_ids = client.search('product.product', [['sale_ok', '=', True]])
logging.debug('Got %d products to get', len(product_ids))

pricelist_ids = [1, 2301, 2303, 2305]
pricelist_keys = []
price_by_product_id = {}

for pl_id in pricelist_ids:
    pl_data = client.read_one('product.pricelist', pl_id, ['id', 'name'])
    pl_key = (pl_data['id'], pl_data['name'])
    pricelist_keys.append(pl_key)
    price_data = get_data(client, product_ids, pl_id)
    for pd in price_data:
        price_entry = price_by_product_id.setdefault(pd['id'], {
            'id': pd['id'],
            'default_code': pd['default_code'],
            'name': pd['name'],
        })
        price_entry[pl_key] = pd['price']

logging.info('Writing %d rows of data to %s', len(price_by_product_id), out_file)
with open(out_file, 'wt') as f:
    w = csv.writer(f)
    header = ['ID', 'Code', 'Name'] + [pk[1] for pk in pricelist_keys]
    w.writerow(header)
    for prod_id in price_by_product_id:
        price_data = price_by_product_id[prod_id]
        row = [price_data['id'], price_data['default_code'], price_data['name']]
        for pl_key in pricelist_keys:
            row.append(price_data[pl_key])
        w.writerow(row)

logging.info('Done')
