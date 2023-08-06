import os
import logging
from comring.lib import odoo, tool
from prettytable import PrettyTable
from . import mappers, loaders

MAPPING_FILE = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', 'mapping.xls')

LOGGER  = logging.getLogger(__name__)

class PayrollTool(tool.SimpleTool):
    payroll_file = ''
    company = ''
    journal_name = ''
    journal_id = 0
    date = ''
    group_data = None
    accounts_ok = False
    dc_ok = False

    def boot_add_arguments(self, parser):
        super().boot_add_arguments(parser)
        parser.add_argument('company', help='Company')
        parser.add_argument('journal', help='Journal name')
        parser.add_argument('date', help='Date of journal entry (YYYY-MM-DD)')
        parser.add_argument('file', help='Payroll report file')
        return True

    def boot_process_arguments(self, args):
        super().boot_process_arguments(args)
        self.company = args.company
        self.journal_name = args.journal
        self.date = args.date
        self.payroll_file = args.file
        return True

    def identify_journal(self):
        self.journal_id = self.search('account.journal', [['name', '=', self.journal_name]], pos='one')

    def identify_accounts(self):
        names = list(set([acc for acc, cl, dc, aa in self.group_data]))
        accounts = self.search_read('account.account', [['name', 'in', names]], ['id', 'code', 'name'])
        accounts_map = {acc['name']: acc for acc in accounts}

        self.accounts_ok = True
        for gkey in self.group_data:
            g = self.group_data[gkey]
            g['account_id'] = 0
            g['account_code'] = ''
            g['account_name'] = ''
            acc = accounts_map.get(gkey[0], None)
            if not acc:
                LOGGER.warn('Account not found in Odoo: %s', gkey[0])
                self.accounts_ok = False
                continue
            g['account_id'] = acc['id']
            g['account_code'] = acc['code']
            g['account_name'] = acc['name']
        return True

    def get_dc(self):
        names = list(set([dc for acc, ct, dc, aa in self.group_data]))
        dcs = self.search_read('res.partner', [['name', 'in', names], ['is_dc', '=', True]], ['id', 'name'])
        dc_map = {dc['name']: dc for dc in dcs}

        self.dc_ok = True
        for gkey in self.group_data:
            g = self.group_data[gkey]
            g['dc_id'] = 0
            g['dc_name'] = ''
            dc = dc_map.get(gkey[2], None)
            if not dc:
                LOGGER.warn('DC not found in odoo: %s', gkey[2])
                self.dc_ok = False
                continue
            g['dc_id'] = dc['id']
            g['dc_name'] = dc['name']
        return True

    def get_analytic_account(self):
        names = list(set([aa for acc, ct, dc, aa in self.group_data]))
        analytic_accounts = self.search_read('account.analytic.account', [['name', 'in', names]], ['id', 'code', 'name'])
        aa_map = {aa['code']: aa for aa in analytic_accounts}

        self.aa_ok = True
        for gkey in self.group_data:
            g = self.group_data[gkey]
            g['analytic_account_id'] = 0
            g['analytic_account'] = ''
            aa = aa_map.get(gkey[3], None)
            if not aa:
                LOGGER.warn('Analytic Account not found in odoo: %s', gkey[3])
                self.aa_ok = False
                continue
            g['analytic_account_id'] = aa['id']
            g['analytic_account'] = '{} {}'.format(aa['code'], aa['name'])
        return True

    def report_stdout(self):
        pt = PrettyTable()
        pt.field_names = ["Account", "DC", "Debit", "Credit", "Account Code", "Analytic Account"]
        pt.sortby = 'Debit'
        pt.reversesort = True
        pt.align['Account'] = 'l'
        pt.align['DC'] = 'l'
        pt.align['Debit'] = 'r'
        pt.align['Credit'] = 'r'
        for gkey in self.group_data:
            g = self.group_data[gkey]
            pt.add_row([
                g['account_name'],
                g['dc_name'],
                str(g['value']) if g['type'] == 'debit' else '',
                str(g['value']) if g['type'] == 'credit' else '',
                g['account_code'],
                g['analytic_account'],
            ])
        print(pt)

    def create_je(self):
        je_data = {
            'date': self.date,
            'ref': 'Percobaan Payroll',
            'journal_id': self.journal_id,
        }

        j_items = []
        for gkey in self.group_data:
            gd = self.group_data[gkey]
            j_items.append((0, 0, {
                'account_id': gd['account_id'],
                'name': gd['account_name'],
                'dc_id': gd['dc_id'],
                'analytic_account_id': gd['analytic_account_id'],
                'debit': gd['value'] if gd['type'] == 'debit' else 0,
                'credit': gd['value'] if gd['type'] == 'credit' else 0
            }))

        je_data['line_ids'] = j_items

        res = self.create('account.move', je_data)
        LOGGER.info('Journal Entry created: %r', res)
    
    def main(self):
        # Load mapper
        mapper = mappers.Mapper()
        mapper.load(MAPPING_FILE)

        # Load data
        loader = loaders.XLSLoaderV2()
        loader.load(self.payroll_file)

        # Map data
        self.group_data = mapper.map_by_cost_center(loader.detail_cost_center)
        
        # Identify journal
        self.identify_journal()

        # Identify accounts
        self.identify_accounts()

        # Identify DC
        self.get_dc()

        # Identify analytic accounts
        self.get_analytic_account()

        # Report as table
        self.report_stdout()

        # Create JE
        #self.create_je()

if __name__ == '__main__':
    odoo.load_envs(os.path.expanduser('~/.config/odoopti.yaml'))
    tool = PayrollTool()
    tool.bootstrap()
    tool.connect()
    tool.main()
