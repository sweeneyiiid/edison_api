# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:30:40 2020

@author: DanielSweeney
"""


import numpy as np
import random as r
import datetime as dt
import json

out_mg = 'C:/Users/DanielSweeney/Desktop/git_local/smg_api/dls_sandbox/sim_data/sim_mg_post.json'
out_mg_ess = 'C:/Users/DanielSweeney/Desktop/git_local/smg_api/dls_sandbox/sim_data/sim_mg_ess_post.json'


#==============================================================================
# STEP 0: setup and utilities
#==============================================================================

#sim runs - three minigrids of 10 customers each, for 40 days
N_mg = 2
N_cust = 3
N_days = 4

#province
regions = ['Lusaka',
           'Central',
           'Southern',
           'Copperbelt',
           'Eastern',
           'Western',
           'North-Western',
           'Muchinga',
           'Luapula',
           'Northern']
region_weights = [8,15,4,11,13,1,2,1,3,1]


# tier based coeff
co2 = {1:9.76,2:21.71,3:45.8}
lamp = {1:2,2:3,3:4}
watt = {1:10,2:17,3:50}

#acquistion date parameters
start_date = dt.datetime(2020,6,1)
max_days = 900
wgt = lambda x: np.sin((x-60)/60)+1 + x/max_days
day_weights = [wgt(i) for i in range(max_days)]


#company IDs
comp_ids = {4:"Standard Microgrid",3:"Emerging Cooking Solutions",1:"Vitalite",2:"Fenix"}



#==============================================================================
# STEP 1: ESS/Customer Simulation
#  - Primary loop, covers main (impact), portfolio, and risk JSONs
#==============================================================================

mg_post = []
mg_ess_post = []

#For minigrid =====================================================
for i in range(N_mg):
    
    #define const params (incl nulls?)    
    #NOTE: No JSON saved here, just to be repeatedly used later
    
    
    province = r.choices(regions, weights = region_weights)[0]

    
    mg_i_const = {
            "averageAnnualSolarInsolation":2135,
            "baseLoadKw":0.3,
            "capacityKw":6,
            "cityName":province,
            "coordinates":"null",
            "installationDate":"2020-07-09T13:07:49.646Z",
            "storageKwh":30,
            "villageName":"village_"+str(i),
            "provinceName":province,
            "events": [
                    {
                            "extKey": "event_"+str(i),
                            "textDescription": "string",
                            "textEventType": "Warranty"
                            }
                    ]
            }
    
    rto = {
            "cdAreaCode": 0,
            "extKey": "rto_"+str(i),
            "nameCity": "string",
            "nameFirst": "string",
            "nameLast": "string",
            "nameVillage": "string",
            "partyType": "RTO",
            "textAddress": "string",
            "textEmail": "string",
            "textPhoneNumber": "string",
            "nameProvince": "string",
            "textGender": "X"
            }    
        
    
    rco = {
            "cdAreaCode": 0,
            "extKey": "rco_"+str(i),
            "nameCity": "string",
            "nameFirst": "string",
            "nameLast": "string",
            "nameVillage": "string",
            "partyType": "RCO",
            "textAddress": "string",
            "textEmail": "string",
            "textPhoneNumber": "string",
            "nameProvince": "string",
            "textGender": "X"
            }    
    
    mgr = [{
            "cdAreaCode": 0,
            "extKey": "mgr_"+str(i),
            "nameCity": "string",
            "nameFirst": "string",
            "nameLast": "string",
            "nameVillage": "string",
            "partyType": "RCO",
            "textAddress": "string",
            "textEmail": "string",
            "textPhoneNumber": "string",
            "nameProvince": "string",
            "textGender": "X"
            }]

    mg_i_const["rco"] = rco
    mg_i_const["rto"] = rto
    mg_i_const["managers"] = mgr


    # this is the seller, stored at wh transaction level, 
    # but making constant for now
    sls = {
            "cdAreaCode": 0,
            "extKey": "seller_"+str(i),
            "nameCity": "string",
            "nameFirst": "string",
            "nameLast": "string",
            "nameVillage": "string",
            "partyType": "Seller",
            "textAddress": "string",
            "textEmail": "string",
            "textPhoneNumber": "string",
            "nameProvince": "string",
            "textGender": "X"
            }    

    
    #For customer
    for j in range(N_cust):

        #define const params (incl nulls?)    
        #NOTE: No JSON defined here
        ess_ij_const = {
                "beneficiary":None,
                "paymentStatus":"Active",
                "productUse":"Household",
                "subProductUse":None,
                "appliances":None,
                "events":None,
                "connectionDate":int(start_date.timestamp())*1000
                }

        cust = {
                "extKey":"cust_"+str(i)+"_"+str(j),
                "partyType":"Customer",
                "nameFirst": "John",
                "nameLast": "Doe",
                "nameProvince":province,
                "nameCity":province,
                "cdAreaCode":0,
                "nameVillage":"village_"+str(i),
                "textAddress":None,
                "textPhoneNumber":None,
                "textEmail":None,
                "textGender":"X"
                }

        ess_ij_const["customer"] = cust
        
        #For date (variable stuff)
        for k in range(N_days):
            
            date_sample = start_date + dt.timedelta(days=k)
            date_as_string = date_sample.strftime("%Y-%m-%d")
            
            #for MG, only do once if j == 0
            if j == 0:
                mg_ik = mg_i_const.copy()
                #define extKey as key plus current date in yyyy-mm-dd format
                mg_ik["extKey"] = str(i) + "_" + date_as_string

                #create hourlies
                hourlies = []
                
                for l in range(24):
                    wh_avg = 100 * r.random() / (abs(l-12)+1)

                    hourlies.append({
                            "extKey":"hourly_"+str(l),
                            "nbrAvgWh":wh_avg, #just something to make it cyclical
                            "nbrHour": l,
                            "nbrPeakWh": wh_avg + 20*r.random()
                            })
                
                mg_ik["microgridHourlys"] = hourlies

                #add daily mg post as dict
                mg_post.append(mg_ik)
                

            #daily values for , INCLUDING KEYS FOR ESS
            
            ess_ijk = ess_ij_const.copy()
            
            mg_ind = {}
            mg_ind["extKey"] = mg_ik["extKey"]
            mg_ind["nameProvince"] = mg_ik["provinceName"]
            mg_ind["nameCity"] = mg_ik["cityName"]
            mg_ind["nameVillage"] = mg_ik["villageName"]
            
            ess_ijk["microgrid"] = mg_ind	
            
            ess_ijk["extKey"] = "ess_" + str(i) + "_" + str(j) + "_" + date_as_string
	
            #Watt hour values
            wh_ijk = {
                    "extKey": "wh_" + str(i) + "_" + str(j) + "_" + date_as_string,
                    "seller":sls,
                    "dtStart":1000*int(date_sample.timestamp()),
                    "nbrDaysPurchased":1,
                    "nbrAmtPaidZmw":16+i,
                    "textPaymentStatus":"Active"
                    }
            
            #wh sockets
            for m in range(5):
                wh_ijk["nbrCentaAmpLimit"+str(m+1)] = 5
                wh_ijk["socket"+ str(m+1) + "Appliance"] = "string"

                prestart = "socket"+ str(m+1)+"Start"
                prestop = "socket"+ str(m+1)+"Stop"

                #start/stop
                for n in range(5):
                    
                    if m == 0:
                        if n == 0:
                            wh_ijk[prestart+str(n)] = "1800"
                            wh_ijk[prestop+str(n)] = "2359"
                    elif m == 1:
                        if n == 0:
                            wh_ijk[prestart+str(n)] = "0800"
                            wh_ijk[prestop+str(n)] = "2359"
                    else:
                        wh_ijk[prestart+str(n)] = "0000"
                        wh_ijk[prestop+str(n)] = "0000"
                        
            #Save customer posts as dict
            ess_ijk["whTransactions"] = [wh_ijk]
            mg_ess_post.append(ess_ijk)


with open(out_mg, 'w') as f:
    json.dump(mg_post, f)

with open(out_mg_ess, 'w') as f:
    json.dump(mg_ess_post, f)

wh_ijk

#mytime = dt.datetime(2012,4,1,0,0)
#
#mytime_ms = int(mytime.timestamp())*1000
#
#mytime_ms
#
#x = {"a":1, "b":2}
#
#y = [x]
