
from app import application

"""
Import routes and models from app folder
"""
from app import routes, models

"""
Cron test
"""
# from app.cronjobs import microgrid_ess


"""
Insert Update Test
"""
# from app.services.insert_update_sandbox import *


if __name__ == '__main__':
    application.run()
