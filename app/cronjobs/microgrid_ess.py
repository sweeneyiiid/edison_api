from app.services.microgrid_ess_export_service import MicroGridESSExport
from app.pipelines import aggregate_by_date
from app.pipelines import key_replacement

"""
Export Microgrid ESS post from mongodb to esp uri
STEPS
Key Replacement
Wh Calculation
Export to URI

Using the ESS Export Class
    GET specific ESP Token
    Provide Params
        params.collection (specify collection name or defaults to ESP name)
        params.pipeline (specify pipeline of defaults to collection.find())
"""

# TEST_TOKEN = "f4b31f51-9d30-4826-b13b-ebc2ffe1d3f2"
TEST_TOKEN = "d5cbdb8b-68c9-4613-aeb8-793e3a8805bc"
# TEST_TOKEN = "b13b-ebc2ffe1d3f2"

# input collection name
coll_in_name = "actual"

# output collection name
coll_out_name = "rekey_test"


"""
Instatiate MG_ESS Class
STEP 1: Select date => start and <= end
relatively small
Add database as part of param
"""
PARAMS = {}
MG_Export = MicroGridESSExport(TEST_TOKEN, PARAMS)

"""
STEP 2: Rekey
{"payload":{"counts":{"Beneficiary-Ignored":1},
"errors":["MicrogridEss 1169_customer: Microgrid ExtKey is required","MicrogridEss 1169_customer: Watt Hours per Day is required","WhTransaction 85811: Payment Status is required","WhTransaction 85811: Transaction Type must be one of [Cash, Mobile Money, Token, Other]"],"success":false}}
"""
MG_Export.run_pipeline("actual", key_replacement.ess_pipeline)


"""
STEP 3: WH Calculation
Additional steps: 
    Daily Wh_calculation
    Other Changes
    wh_transaction.text_transaction_type
    - wh_transaction.date_end
    wh_transaction.nbr_amt_paid
    - wh_transaction.nbr_wh_avg
"""
MG_Export.get_wh_calculation('rekey_test')


"""
STEP 4: Post to URI
# http://ec2-18-156-5-118.eu-central-1.compute.amazonaws.com:8443/external-data/microgrid-ess/d5cbdb8b-68c9-4613-aeb8-793e3a8805bc
https://devedisonapi.bgfz.org:8443/edison-dev/external-data/microgrid-ess/d5cbdb8b-68c9-4613-aeb8-793e3a8805bc
"""
# uri = "http://ec2-18-156-5-118.eu-central-1.compute.amazonaws.com:8443/edison-dev/external-data/microgrid-ess/"
uri = "https://devedisonapi.bgfz.org:8443/edison-dev/external-data/microgrid-ess/"
post = MG_Export.post_data_to_dev("rekey_test", uri)
print(post.status_code)
