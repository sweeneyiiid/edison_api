import json
import pandas as pd
import numpy as np

in_path = 'C:/Users/DanielSweeney/Desktop/vitalite_pull/reeep_request_2021-01-18_2034.json'
out_path = 'C:/Users/DanielSweeney/Desktop/git_local/smg_api/dls_sandbox/vit_sales/data/vit_defaults_payg.tab'


with open(in_path) as f:
    hist_raw = json.load(f)
    

rec = hist_raw[1000]
#
#shs_key = rec['extKey']
#dt_acq = pd.to_datetime(rec['acquisitionDate']).date()
#product = rec['productId']
#province = rec['customer']['nameProvince']
#cust_key = rec['customer']['extKey']

rec





paygt = rec['paygTransactions']

curr_pmt = []
curr_dt = []
for i in paygt:
    curr_pmt.append(i['amtPayment'])
    curr_dt.append(pd.to_datetime(i['dtPayment']).date())
tot_pmt = sum(curr_pmt) 
max_dt = max(curr_dt) 
   

tot_pmt = np.NaN
max_dt = pd.NaT



hist_raw[10000]['customer']




missed_recs = 0
sls_list = []
for rec in hist_raw:

    try:
        #system data
        shs_key = rec['extKey']
        cust_key = rec['customer']['extKey']
        dt_acq = pd.to_datetime(rec['acquisitionDate']).date()
        product = rec['productId']
        province = rec['customer']['nameProvince']
        
        pmt_type= rec['paymentType']
        down_pmt = rec['downPayment']
        ttl_fin= rec['totalFinancedAtTimeOfPurchase']

        try:
            paid_off_dt= pd.to_datetime(rec['datePaidOff']).date()
        except:
            paid_off_dt = pd.NaT

        #summarize payment data
        try:
            paygt = rec['paygTransactions']
            curr_pmt = []
            curr_dt = []
            for i in paygt:
                curr_pmt.append(i['amtPayment'])
                curr_dt.append(pd.to_datetime(i['dtPayment']).date())
            tot_pmt = sum(curr_pmt) 
            max_dt = max(curr_dt) 
        except:
            tot_pmt = np.NaN
            max_dt = pd.NaT

        #list element for move to pandas
        sls_list.append([shs_key, cust_key, dt_acq, product, province, pmt_type, paid_off_dt, down_pmt, ttl_fin, tot_pmt, max_dt])


    except:
        missed_recs += 1

print(missed_recs)



payg_ds = pd.DataFrame(sls_list)

payg_ds.columns = ['shs_key', 'cust_key', 'dt_acq', 'product', 'province', 'pmt_type', 'paid_off_dt', 'down_pmt', 'ttl_fin', 'tot_pmt', 'max_dt']



payg_ds.to_csv(out_path, index=False, sep='\t')

