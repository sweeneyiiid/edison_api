
import json

base_payload_path = './payloads/sql_test_'


#esp_token - how do we test this???
#esp_key = [3 for i in range(20)]

ess_key = ['ess_test_1',
           'ess_test_2',
           'ess_test_1',
           'ess_test_1',
           'ess_test_3',
           'ess_test_4',
           'ess_test_5',
           'ess_test_6',
           'ess_test_1',
           'ess_test_1',
           'ess_test_1',
           'ess_test_1',
           'ess_test_7',
           'ess_test_8',
           'ess_test_1',
           'ess_test_1',
           'ess_test_1',
           'ess_test_9',
           'ess_test_1',
           'ess_test_1']

cust_key = ['cust_test_1',
            'cust_test_2',
            'cust_test_3',
            'cust_test_4',
            'cust_test_1',
            'cust_test_1',
            'cust_test_5',
            'cust_test_6',
            'cust_test_1',
            'cust_test_1',
            'cust_test_7',
            'cust_test_8',
            'cust_test_1',
            'cust_test_1',
            'cust_test_1',
            'cust_test_1',
            'cust_test_1',
            'cust_test_9',
            'cust_test_1',
            'cust_test_1']

payg_key = ['payg_test_1',
            'payg_test_2',
            'payg_test_3',
            'payg_test_4',
            'payg_test_5',
            'payg_test_6',
            'payg_test_1',
            'payg_test_1',
            'payg_test_7',
            'payg_test_8',
            'payg_test_1',
            'payg_test_1',
            'payg_test_1',
            'payg_test_1',
            'payg_test_1',
            'payg_test_1',
            'payg_test_9',
            '',
            '',
            '']

seller_key = ['seller_test_1',
              'seller_test_1',
              'seller_test_2',
              'seller_test_1',
              'seller_test_3',
              'seller_test_1',
              'seller_test_4',
              'seller_test_1',
              'seller_test_5',
              'seller_test_1',
              'seller_test_6',
              'seller_test_1',
              'seller_test_7',
              'seller_test_1',
              'seller_test_8',
              'seller_test_1',
              'seller_test_1',
              'seller_test_1',
              'seller_test_1',
              'seller_test_1']

prod_key = ['prod_test_1' for _ in range(20)]

event_key = ['',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             'event_test_1',
             '',
             'event_test_2',
             '']
             


# pre_cond_query = """
    # select count(*) from {} where id_esp = {} and ext_key = {}
    # """.format('SHS_ESS', esp_token, ess_key[i])

null=None
base_payload = {
#    "extKey": curr_ess,
    "customer": {
#        "extKey": curr_cust,
        "partyType": "Customer",
        "nameFirst": "John",
        "nameLast": "Customer1",
        "nameProvince": "Lusaka",
        "nameCity": "Shantumbu",
        "cdAreaCode": 260,
        "nameVillage": null,
        "textAddress": "asdf",
        "textPhoneNumber": "+123",
        "textEmail": null,
        "textGender": "M"
    },
    "beneficiary": null,
    "seller": {
#        "extKey": curr_seller,
        "partyType": "Seller",
        "nameFirst": "John",
        "nameLast": "Seller1",
        "nameProvince": null,
        "nameCity": null,
        "cdAreaCode": 260,
        "nameVillage": null,
        "textAddress": null,
        "textPhoneNumber": "+123",
        "textEmail": "seller1@supamoto.com",
        "textGender": null
    },
#    "productId": "PT000233",
    "acquisitionDate": 1602229140000,
    "paymentType": "PAYG",
    "planDuration": 1106,
    "minimumPaymentPerMonth": 80.0,
    "downPayment": 150.0,
    "datePaidOff": null,
    "daysPaid": 30,
    "daysToPay": 1050,
    "currentDaysOutstanding": 0,
    "totalDaysOutstanding": 0,
    "totalFinancedAtTimeOfPurchase": 2950.0,
    "productUse": "Household",
    "productSubUse": null,
    "serialNumber": "76656644",
    "repossessionDate": null,
    "paygTransactions": [
        {
#            "extKey": "PA107500957",
            "amtPayment": 150.0,
            "dtPayment": 1602079630000,
            "textPaymentStatus": "Active",
            "textTransactionType": "Mobile Money",
            "textSms": "Thank you!"
        }
    ],
    "events": [ { "eventType":"warantee" }]
}

#check number of cases
n_cases = len(ess_key)

#create payloads
for i in range(n_cases):
    curr_payload = base_payload.copy()
    
    #ESS
    curr_payload["extKey"] = ess_key[i]
    
    #Customer
    curr_payload["customer"]["extKey"] = cust_key[i]
    
    #Payg
    #https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary
    if payg_key[i] == '':
        curr_payload.pop('paygTransactions',None)
    else:
        curr_payload["paygTransactions"][0]["extKey"] = payg_key[i]

    
    #Seller
    curr_payload["seller"]["extKey"] = seller_key[i]
    
    #Product
    curr_payload["productId"] = prod_key[i]
    
    #Event
    #https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary
    if event_key[i] == '':
        curr_payload.pop('events',None)
    else:
        curr_payload["events"][0]["extKey"] = event_key[i]
    
    #save payload
    with open(base_payload_path+str(i+1)+'.json', 'w') as f:
        json.dump(curr_payload, f)
    

    
    
