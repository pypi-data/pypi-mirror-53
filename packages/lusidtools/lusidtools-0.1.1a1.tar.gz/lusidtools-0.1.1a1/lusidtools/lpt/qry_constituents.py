import pandas as pd
import datetime
from lusidtools.lpt import lpt
from lusidtools.lpt import lse
from lusidtools.lpt import stdargs

def parse(extend = None, args = None):
    return (
       stdargs.Parser(
            'Get Constituents',
             ['filename','limit','scope','portfolio','date','properties','asat']
         )
         .extend(extend)
         .parse(args)
    )

def process_args(api, args):

    def success(constituents):
        print(constituents.content)
        exit()
        df = lpt.to_df(constituents,[])

        return lpt.trim_df(df,args.limit)

    #properties = ['Instrument/default/Name']
    properties = []
    properties.extend(args.properties or [])

    result = api.call.get_reference_portfolio_constituents(
                args.scope,
                args.portfolio,
                effective_at=lpt.to_date(args.date),
                property_keys = properties
              )

    return result.bind(success)

# Standalone tool
def main():
    lpt.standard_flow(parse,lse.connect,process_args)
