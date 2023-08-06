from pathlib import Path

from lusidtools.lpt import lpt
from lusidtools.lpt import lse
from lusidtools.lpt import create_instr      as ci
from lusidtools.lpt import create_properties as cp
from lusidtools.lpt import upload_portfolio  as up
from lusidtools.lpt import qry_holdings      as qh

secrets_file = Path(__file__).parent.parent.joinpath('secrets.json')

api = lse.connect(secrets=secrets_file, stats='-')  # stats to stdout

# Load instruments from the file: examples/ibm-msft.csv
ci.process_args(api, ci.parse(args=['examples/ibm-msft.csv']))

# Create Properties
cp.process_args(api, cp.parse(args=[
    '--prop',
    'Transaction/JLH/sub-acct',
    'Transaction/JLH/account',
    'Holding/JLH/prop1',
    'Holding/JLH/prop2'
]))


# Create Portfolios
for portfolio in ['JLH1', 'JLH2', 'JLH3']:
    up.process_args(api, up.parse(args=[
        'JLH',
        portfolio,
        '-c', 'TEST-PORTFOLIO-{}'.format(portfolio), 'USD', '2018-01-01',
        '-a', 'FIFO',
        '--shk', 'Transaction/JLH/account', 'Transaction/JLH/sub-acct'
    ])).if_left(lambda v: print(v))

# Load JLH1 Portfolio from first sheet from example Excel file
up.process_args(api, up.parse(args=[
    'JLH',
    'JLH1',
    '-p', 'examples/holdings-examples.xlsx', '2019-01-01'
]))

# Load JLH2 and JLH3 Portfolios from second sheet from example Excel file
up.process_args(api, up.parse(args=[
    'JLH',
    'col:portfolio-code',  # col: prefix indicates code is in the sheet
    '-p', 'examples/holdings-examples.xlsx:Multiple', '2019-01-01'
])).if_left(lambda v: print(v))

# Load JLH1 Transactions from first sheet from example Excel file
up.process_args(api, up.parse(args=[
    'JLH',
    'JLH1',
    '-t', 'examples/transactions-examples.xlsx'
])).if_left(lambda v: print(v))

# Load JLH2 and JLH3 Transactions from second sheet from example Excel file
up.process_args(api, up.parse(args=[
    'JLH',
    'col:portfolio-code',  # col: prefix indicates code is in the sheet
    '-t', 'examples/transactions-examples.xlsx:Multiple'
]))

# Query Portfolio JLH3
qh.process_args(api, qh.parse(args=['JLH', 'JLH3', '-t'])).match(
    left=lpt.display_error,
    right=lpt.display_df
)

# Display the LUSID call stats
api.dump_stats()
