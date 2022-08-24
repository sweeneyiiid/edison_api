import json
import pandas as pd
import numpy as np

in_path = 'C:/Users/DanielSweeney/Desktop/vitalite_pull/reeep_request_2021-01-18_2034.json'
out_path = 'C:/Users/DanielSweeney/Desktop/git_local/smg_api/dls_sandbox/vit_sales/data/vit_sales_payg.tab'


with open(in_path) as f:
    hist_raw = json.load(f)
    

rec = hist_raw[0]
#
#shs_key = rec['extKey']
#dt_acq = pd.to_datetime(rec['acquisitionDate']).date()
#product = rec['productId']
#province = rec['customer']['nameProvince']
#cust_key = rec['customer']['extKey']

hist_raw[10000]['customer']




missed_recs = 0
sls_list = []
for rec in hist_raw:

    try:
        shs_key = rec['extKey']
        cust_key = rec['customer']['extKey']
        dt_acq = pd.to_datetime(rec['acquisitionDate']).date()
        product = rec['productId']
        province = rec['customer']['nameProvince']
        sls_list.append([shs_key, cust_key,dt_acq, product, province])
    except:
        missed_recs += 1

print(missed_recs)



payg_ds = pd.DataFrame(sls_list)

payg_ds.columns = ['shs_key', 'cust_key', 'dt_acq', 'product', 'province']



#payg_ds.to_csv(out_path, index=False, sep='\t')

