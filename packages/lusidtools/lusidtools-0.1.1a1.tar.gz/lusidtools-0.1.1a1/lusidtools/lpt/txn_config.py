import pandas as pd
import dateutil
from lusidtools.lpt import lpt
from lusidtools.lpt import lse
from lusidtools.lpt import stdargs
from lusidtools.lpt import txn_config_yaml as tcy

def parse(extend = None, args = None):
    return (
       stdargs.Parser('Get/Set transaction configuration',['filename','limit'])
         .add('action',choices=('get','set','try'),
              help="get or set the config. 'Try' can be used to validate a custom encoding")
         .add('--raw',action='store_true', help = 'use raw (non custom) encoding')
         .add('--json',action='store_true', help = 'display the json to be sent')
         .extend(extend)
         .parse(args)
    )

def process_args(api,args):
    y =  tcy.TxnConfigYaml(api.models)

    if args.action == 'get':
       def get_success(result):
          y.dump(result.content.values,args.filename,args.raw)
          return None 
 
       return api.call.list_configuration_transaction_types().bind(get_success)

    if args.action == 'try':
       ffs = y.load(args.filename)
       y.dump(ffs,"{}-try".format(args.filename))

    if args.action == 'set':
       def set_success(result):
          print(y.get_yaml(result.content.values))
          return None 
 
       txn_types = y.load_update(args.filename)
       #y.dump(ffs,"{}-set".format(args.filename),True)
       if args.json:
           print(txn_types)
           return None
       else:
           return api.call.set_configuration_transaction_types(
                   types=txn_types
           ).bind(set_success)

# Standalone tool
def main():
    lpt.standard_flow(parse,lse.connect,process_args)
