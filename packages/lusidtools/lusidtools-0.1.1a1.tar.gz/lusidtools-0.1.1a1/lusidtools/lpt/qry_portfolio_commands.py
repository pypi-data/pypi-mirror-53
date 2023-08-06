import pandas as pd
from lusidtools.lpt import lse
from lusidtools.lpt import stdargs
from lusidtools.lpt import lpt

def parse(extend = None, args = None):
    return (
       stdargs.Parser('Get Portfolios',['filename','limit','portfolio','scope','asat'])
         .add('--date')
         .extend(extend)
         .parse(args)
    )

def process_args(api,args):

    def success(result):
        print (result.content)

    return api.call.get_portfolio_commands(
       scope=args.scope,
       code=args.portfolio,
       effective_at=lpt.to_date(args.date)
    ).bind(success)
 

# Standalone tool
def main():
    lpt.standard_flow(parse,lse.connect,process_args)

