import pandas as pd
from lusidtools.lpt import lpt
from lusidtools.lpt import lse
from lusidtools.lpt import stdargs


AGG_INSTR = 'Instrument/default/Name'
AGG_UID   = 'Instrument/default/LusidInstrumentId'
AGG_PV    = 'Holding/default/PV'
AGG_PRC   = 'Holding/default/Price'
AGG_UNITS = 'Holding/default/Units'
AGG_COST  = 'Holding/default/Cost'
AGG_TYPE  = 'Holding/default/Type'
AGG_RATE  = 'Holding/default/ExchangeRate'

AGG_RIC   = 'Instrument/default/RIC'
AGG_PDATE = 'Holding/default/TaxlotPurchaseDate'
AGG_PPRICE= 'Holding/default/TaxlotPurchasePrice'

INSTR = 'Instrument'
UID   = 'Id'
TYPE  = 'Type'
UNITS = 'Units'
PRICE = 'Price'
COST  = 'Cost'
LVAL  = 'MV(local)'
RATE  = 'Fx Rate'
PVAL  = 'Mkt Val'
RIC   = 'RIC'
PDATE = 'PurchaseDate'
PPRICE= 'PurchasePrice'


def parse(extend = None, args = None):
    return (
       stdargs.Parser('Get Aggregate Holdings',['filename','limit'])
         .add('scope', help='Scope')
         .add('portfolio', help='Portfolio id')
         .add('dates', nargs='*', metavar='YYYY-MM_DD')
         .add('-m','--monitor', action = 'store_true', help = 'monitor the run')
         .add('--pricing-scope', default = 'MyScope', dest='pricing_scope', help = 'scope for pricing')
         .add('--recipe', default="datascope-permid", help = 'valuation engine recipe')
         .extend(extend)
         .parse(args)
    )

def process_args(api, args):

    if len(args.dates) == 1:
       return run_query(api,args,args.dates[0]).bind(lambda x : x[1])
    else:
       i = [1]

       records = []

       dates = iter(args.dates)

       def get_daily_record():
           try:
              active_date = next(dates)
           except StopIteration:
              print("It's All Over")
              return finished()

           def got_daily_record(result):
               stats,df = result

               pv = df[PVAL].sum()
             
               num_pos = len(df)
               df = df[(df[UNITS] != 0) | (df[TYPE] != 'Position')] # get rid of zero positions
               rec = df.groupby([TYPE]).size().to_dict()
               rec['PV'] = pv
               rec['#'] = i[0]
               rec['Date'] = active_date
               rec['Zeros'] = num_pos - len(df)
               rec['Duration'] = stats.duration
               rec['LUSID'] = stats.elapsed
               rec['Id'] = stats.requestId
               rec['Start-Time'] = stats.startTime

               records.append(rec)

               if args.monitor:
                  print("{: 3} {}: {:,.2f} Duration: {}, LUSID: {}".format(i[0],active_date,pv,stats.duration,stats.elapsed))

               i[0] += 1

               if 0 < args.limit < i[0]:
                  return finished()

               return get_daily_record()

           return run_query(api,args,active_date).match(
              left  = finished,
              right = got_daily_record
           )

       def finished(error=None):
  
           if error is not None:
              lpt.display_error(error)

           if(len(records) == 0):
              print("No results")
              exit(-1)

           df = pd.DataFrame.from_records(records)

           leading_cols = ['#','Start-Time','Date','PV','Duration','LUSID','Id']

           cols = set(df.columns.values)
           other_cols = list(sorted(cols - set(leading_cols)))
 
           for col in other_cols:
              df[col] = df[col].fillna(0).astype(int)
      
           return lpt.trim_df(df[leading_cols + other_cols],args.limit)

    return get_daily_record()

def run_query(api,args,date):

   request = api.models.AggregationRequest(
      recipe_id=api.models.ResourceId(args.pricing_scope or args.scope,args.recipe),
      effective_at=lpt.to_date(date),
      metrics=[
         api.models.AggregateSpec(AGG_PV,'Value'),
         api.models.AggregateSpec(AGG_UNITS,'Value'),
         api.models.AggregateSpec(AGG_COST,'Value'),
         api.models.AggregateSpec(AGG_RATE,'Value'),
         api.models.AggregateSpec(AGG_PRC,'Value'),
         api.models.AggregateSpec(AGG_RIC,'Value'),
         api.models.AggregateSpec(AGG_INSTR,'Value'),
         api.models.AggregateSpec(AGG_UID,'Value'),
         api.models.AggregateSpec(AGG_TYPE,'Value'),
         api.models.AggregateSpec(AGG_PDATE,'Value'),
         api.models.AggregateSpec(AGG_PPRICE,'Value')]
      #group_by=[AGG_RIC,AGG_INSTR,AGG_UID,AGG_TYPE,AGG_PDATE,AGG_PPRICE]
   )

   # Called if get_aggregation_by_portfolio() succeeds
   def success(result):
       df = pd.DataFrame.from_records(
              result.content.data
            ) [[AGG_TYPE,AGG_INSTR,AGG_UID,AGG_UNITS,AGG_COST,AGG_PRC,AGG_RATE,AGG_PV,AGG_RIC,AGG_PDATE,AGG_PPRICE]]

       df[LVAL]  = df[AGG_PV] / df[AGG_RATE]

       df.rename(
         columns = {
           AGG_INSTR:INSTR,
           AGG_UNITS:UNITS,
           AGG_COST:COST,
           AGG_PRC:PRICE,
           AGG_TYPE:TYPE,
           AGG_UID:UID,
           AGG_RATE:RATE,
           AGG_PV:PVAL,
           AGG_RIC:RIC,
           AGG_PDATE:PDATE,
           AGG_PPRICE:PPRICE
         },
         inplace=True
       )
       df = df[df[UNITS] != 0] 

       return result.stats, df[[UID,TYPE,RIC,INSTR,PDATE,PPRICE,UNITS,COST,PRICE,LVAL,RATE,PVAL]]
   
   return api.call.get_aggregation_by_portfolio(
             args.scope,
             args.portfolio,
             request
          ).bind(success)

def main():
    lpt.standard_flow(parse,lse.connect,process_args)
