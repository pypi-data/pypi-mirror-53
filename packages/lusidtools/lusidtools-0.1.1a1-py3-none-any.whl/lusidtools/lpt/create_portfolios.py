import pandas as pd
import os
import argparse
from lusidtools.lpt import lpt
from lusidtools.lpt import lse
from lusidtools.lpt import stdargs
from lusidtools.lpt.record import Rec
from lusidtools.lpt.either import Either

# column names
CA_SCOPE = 'corporateActionSourceId.scope'
CA_CODE  = 'corporateActionSourceId.code'

def parse(extend = None, args = None):
    return (
       stdargs.Parser('Create Portfolios')
         .add('input')
         .extend(extend)
         .parse(args)
    )

def process_args(api, args):

    df = pd.read_csv(args.input)

    prop_keys= [col for col in df.columns.values if col.startswith('P:')]
    sh_keys= [col for col in df.columns.values if col.startswith('SHK:')]



    jlh = api.from_df(df, api.models.CreateTransactionPortfolioRequest)
    print(jlh)
    exit()
 
def main():
    lpt.standard_flow(parse,lse.connect,process_args)
