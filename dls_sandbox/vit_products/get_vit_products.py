import json
import pandas as pd
import numpy as np

in_path = 'C:/Users/DanielSweeney/Desktop/vitalite_pull/reeep_request_2021-01-18_2034.json'
out_path = 'C:/Users/DanielSweeney/Desktop/git_local/smg_api/dls_sandbox/vit_products/vit_product_set.csv'


with open(in_path) as f:
    hist_raw = json.load(f)
    

#hist_raw[0]
#
#set(['a', 'b', 1, 1, 2, 'a'])


missed_recs = 0
prod_list = []
for rec in hist_raw:

    try:
        prod_list.append(rec['productId'])    
    except:
        missed_recs += 1

print(missed_recs)

prod_set = set(prod_list)

print(prod_set)


#hist_ds = pd.DataFrame(hist_list)
#
#hist_ds.columns = ['key','dt','days']
#
#hist_ds.to_csv(pd_out, index=False)

