

# def get_esp_name(self):
#         """
#         Get the esp name from the POST to use for collection creation
#         TODO: check if esp is mg or shs
#         db lookup to see if token matches esp, then get the curresponding esp name
#         """
#         esp_name = None
#         try:
#             esp_query = Esp.query.filter_by(text_api_token=self.token).first()
#             esp_name = esp_query.name_company
#             response = {
#             "status": "true",
#             'message': "valid"
#             }
#         except:
#             response = {
#                 "status": "false",
#                 'message': "esp token for this post is not valid"
#             }
#         self.response = response
#         return esp_name