from app import application, config, api
from flask import jsonify, request
from flask_restplus import Api, Resource, fields
from app.models.esp_model import Esp, EspSchema
from app.services.auth_service import token_required
from app.services.microgrid_service import MicroGridImport
from app.services.microgrid_ess_service import MicroGridESSImport
from app.services.shs_ess_service import ShsEssImport

from app.utils.fields_validation import NullableString, NullableInteger, NestedWithEmpty, NullableFloat

esp_schema = EspSchema()
esps_schema = EspSchema(many=True)

"""
ESP namespace
"""
ns_users = api.namespace(
    'esp', doc=False, description='Individual ESP registeration')


@api.hide
@ns_users.route('/<string:token>')
class EspList(Resource):
    """
    A class to get a registered esps from Edison
    """
    @api.doc('Get information about registered esp in the system', security="apiKey")
    # @token_required
    def get(self, token):
        """
        returns info about this specific esp
        """

        # all_users = Esp.query.all()
        single_esp = Esp.query.filter_by(text_api_token=token).first()
        result = esp_schema.dump(single_esp)
        response = {
            'data': result,
            'status_code': 202
        }
        return jsonify(response)


"""
MicroGrid ESS namespace
"""
ns_microgrid_ess = api.namespace(
    'microgrids/microgrid-ess', description='Microgrid ESS post data')

wh_transaction = ns_microgrid_ess.model('MG_ESS_Transactions', {
    'extKey': fields.String()
})

single_microgrid_ess = ns_microgrid_ess.model('MicroGrid_ESS', {
    'extKey': fields.String(required=True),
    'customer': fields.Nested(
        ns_microgrid_ess.model('MG_ESS_Customer', {
            'extKey': fields.String(required=False),
            'partyType': fields.String(),
            'nameFirst': fields.String(),
            'nameLast': fields.String(),
            'nameProvince': fields.String(),
            'nameCity': NullableString(),
            'cdAreaCode': NullableString(),
            'nameVillage': NullableString(),
            'textAddress': NullableString(),
            'textPhoneNumber': NullableString(),
            'textEmail': NullableString(),
            'textGender': fields.String()
        })
    ),
    'beneficiary': NullableString(),
    'microgrid': fields.Nested(
        ns_microgrid_ess.model('MG_ESS_Microgrid', {
            'extKey': fields.String(),
            'nameProvince': NullableString(),
            'nameCity': NullableString(),
            'nameVillage': NullableString(),
            'textCoordinates': NullableString(),
            'managers': NullableString(),
            'dtInstallation': NullableString(),
            'nbrAvgSolarInsolationAnnual': NullableString(),
            'nbrBaseLoadKw': NullableString(),
            'nbrCapacityKw': NullableString(),
            'nbrStorageKwh': NullableString(),
            'microgridHourlys': NullableString(),
            'partyOperations': NullableString()
        })
    ),
    'connectionDate': NullableString(example='2019-07-13'),
    'paymentStatus': fields.String(example="Active"),
    'productUse': NullableString(example='Household'),
    'subProductUse': NullableString(),
    'appliances': NullableString(),
    'events': NullableString(),
    'whTransactions': fields.List(fields.Nested(wh_transaction, skip_none=True))
})

"""
Multiple post json for microgrid ess
"""
multi_microgrid_ess = ns_microgrid_ess.model(
    "MicroGrid_ESS", single_microgrid_ess)


@ns_microgrid_ess.route('/<string:token>')
class MicrogridESS(Resource):
    @api.response(201, 'MicroGridESS post')
    @api.doc('New MicroGridESS', security="apiKey")
    # @token_required
    @api.expect([multi_microgrid_ess], validate=True)
    def post(self, token):
        """
        Adds a new MicroGrid ESS to the database
        """
        """
        Plan
        check for exisitng MicroGrid, if yes the update information and if no then create a new one
        added  new query param for token (accomodate existing infrastructure)
        """
        # micro grid ess import class
        mg_ess_import = MicroGridESSImport(api.payload, token)
        res = mg_ess_import.output()
        return res


"""
Microgrid namespace
"""
ns_microgrid = api.namespace(
    'microgrids/microgrid', description='Microgrid post data')

microgrid_events_model = ns_microgrid.model('MG_Events', {
    'extKey': NullableString(),
    "textDescription": NullableString(),
    "textEventType": NullableString()
})

microgrid_managers_model = ns_microgrid.model('MG_Managers', {
    "cdAreaCode": NullableString(),
    "extKey": NullableString(),
    "nameCity": NullableString(),
    "nameFirst": NullableString(),
    "nameLast": NullableString(),
    "nameVillage": NullableString(),
    "partyType": NullableString(example="Managers"),
    "textAddress": NullableString(),
    "textEmail": NullableString(),
    "textPhoneNumber": NullableString(),
    "nameProvince": NullableString(example="Lusaka"),
    "textGender": NullableString()
})

"""
Microgrid hourly model hidden for now
"""

microgrid_hourlys_model = ns_microgrid.model('MG_Hourlys', {
    'extKey': NullableString(),
    "nbrAvgWh": fields.Float(allow_null=True, skip_none=True),
    "nbrHour": NullableString(),
    "nbrPeakWh": NullableString()
})

microgrid_rco_model = ns_microgrid.model('MG_rco', {
    "cdAreaCode": NullableString(),
    "extKey": NullableString(),
    "nameCity": NullableString(),
    "nameFirst": NullableString(),
    "nameLast": NullableString(),
    "nameVillage": NullableString(),
    "partyType": NullableString(example="RCO"),
    "textAddress": NullableString(),
    "textEmail": NullableString(),
    "textPhoneNumber": NullableString(),
    "nameProvince": NullableString(example="Copperbelt"),
    "textGender": NullableString(example="M")
})

microgrid_rto_model = ns_microgrid.model('MG_rto', {
    "cdAreaCode": NullableString(),
    "extKey": NullableString(),
    "nameCity": NullableString(),
    "nameFirst": NullableString(),
    "nameLast": NullableString(),
    "nameVillage": NullableString(),
    "partyType": NullableString(example="RTO"),
    "textAddress": NullableString(),
    "textEmail": NullableString(),
    "textPhoneNumber": NullableString(),
    "nameProvince": NullableString(example="Copperbelt"),
    "textGender": NullableString(example="M")
})

single_microgrid = ns_microgrid.model('Microgrid', {
    "averageAnnualSolarInsolation": NullableString(),
    "baseLoadKw": NullableString(allow_null=True, skip_none=True),
    "capacityKw": NullableString(),
    "cityName": NullableString(),
    "coordinates": NullableString(),
    "events": fields.List(fields.Nested(microgrid_events_model, skip_none=True)),
    "extKey": fields.String(),
    "installationDate": fields.String(),
    "managers": fields.List(fields.Nested(microgrid_managers_model, skip_none=True)),
    "microgridHourlys": fields.List(fields.Nested(microgrid_hourlys_model, allow_null=True, skip_none=True)),
    "rco": fields.Nested(microgrid_rco_model, allow_null=True, skip_none=True),
    "rto": fields.Nested(microgrid_rto_model, allow_null=True, skip_none=True),
    "storageKwh": NullableString(),
    "villageName": NullableString(),
    "provinceName": NullableString(example="Copperbelt")
})


"""
Multiple post for microgrid
"""
multi_microgrid = ns_microgrid_ess.model("MicroGrid", single_microgrid)


@ns_microgrid.route('/<string:token>')
class MicroGrid(Resource):
    @api.response(201, 'MicroGrid post')
    @api.doc('New MicroGrid', security="apiKey")
    # @token_required
    @api.expect([multi_microgrid], validate=False)
    def post(self, token):
        """
        Adds a new MicroGrid to the database
        """
        # micro grid import class
        mg_import = MicroGridImport(api.payload, token)
        res = mg_import.output()
        return res


"""
SHS namespace
"""

ns_shs_ess = api.namespace('shs/ess', description='SHS ESS post data')

shs_customer_model = ns_shs_ess.model('SHS_customer', {
    'extKey': NullableString(),
})

shs_seller_model = ns_shs_ess.model('SHS_seller', {
    'extKey': NullableString(),
})

shs_paygtransaction_model = ns_shs_ess.model('SHS_payg', {
    'extKey': NullableString(),
    'amtPayment': NullableInteger(),
    'dtPayment': NullableInteger(),
    'textPaymentStatus': NullableString(),
    'textTransactionType': NullableString(),
    'textSms': NullableString(),
})

single_shs_ess = ns_shs_ess.model('SHSESS', {
    "extKey": NullableString(example="ess_example_1", description='customer ext_key in string'),
    "customer": fields.Nested(shs_customer_model, allow_null=True, skip_none=True, description='container for customer object'),
    "beneficiary": NullableString(),
    "seller": fields.Nested(shs_seller_model, allow_null=True, skip_none=True),
    "productId": NullableString( example="prod_example_1"),
    "acquisitionDate": NullableInteger(allow_null=True, skip_none=True, example="1602079630000", description='acquisition date in unix timestamp'),
    "paymentType": NullableString(allow_null=True, skip_none=True,  example="PAYG"),
    "planDuration": NullableInteger(allow_null=True, skip_none=True ),
    "minimumPaymentPerMonth": NullableInteger(allow_null=True, skip_none=True),
    "downPayment": NullableInteger(allow_null=True, skip_none=True),
    "datePaidOff": NullableString(allow_null=True, skip_none=True),
    "daysPaid": NullableInteger(),
    "daysToPay": NullableInteger(),
    "currentDaysOutstanding": NullableInteger(allow_null=True, skip_none=True),
    "totalDaysOutstanding": NullableInteger(allow_null=True, skip_none=True),
    "totalFinancedAtTimeOfPurchase": NullableInteger(allow_null=True, skip_none=True),
    "productUse": NullableString(allow_null=True, skip_none=True),
    "productSubUse": NullableString(allow_null=True, skip_none=True),
    "serialNumber": NullableString(allow_null=True, skip_none=True),
    "repossessionDate": NullableString(allow_null=True, skip_none=True),
    "paygTransactions": fields.List(fields.Nested(shs_paygtransaction_model, allow_null=True, skip_none=True)),
    'events': NullableString()
})

"""
Multiple SHS Posts
"""
multi_shs_ess = ns_shs_ess.model("SHS_ESS", single_shs_ess)

@ns_shs_ess.route('/<string:token>')
class ShsEss(Resource):
    @api.response(201, 'SHS ESS post')
    @api.doc('New SHS ESS', security="apiKey")
    @api.expect([multi_shs_ess], validate=False)
    def post(self, token):
        """
        Adds a new shs ess to the system
        """
        # shs grid import class
        # micro grid ess import class

        shs_ess_import = ShsEssImport(api.payload, token)
        res = shs_ess_import.output()
        return res

