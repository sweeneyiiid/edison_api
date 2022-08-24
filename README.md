SMG API
===============

## Installation

The application gets shipped via the python package manager pip. So make sure that you have [PIP](https://pypi.org/project/pip/) installed.
You can install the instance to run locally using the below commands:

```shell
cd SMG_API
python -m venv env
source env/bin/activate (mac)
env\scripts\activate (windows)
```

```shell
pip install -r requirements.txt
```

```shell
python application.py
```

You should should see the application at [http://127.0.0.1:5000]


## Connect to EC2 from terminal

```shell
ssh -i "public_key.pem" ubuntu@ec2-18-184-98-173.eu-central-1.compute.amazonaws.com
```

## Run Mongo Shell and Connect to DocDB

```shell
mongo --host docdb-2020-07-07-09-26-56.cg538cuwf6tw.eu-central-1.docdb.amazonaws.com:27017 --username <username> --password <password>
```

### Quick search
```shell
db.col.find()
```

### Mongo cheat sheet
https://gist.github.com/bradtraversy/f407d642bdc3b31681bc7e56d95485b6


## Testing
```shell
py.test -q tests/test_microgrid.py
```

## Testing API connection

There is some parallel work going on in the `smg_integration` repo.  One thing going on there is the creation of a pipeline to process data from the API format sent by SMG into the format expected by the existing Edison endpoint.

As of 2020-08-25, we have successully tested the push of a single Microgrid and Microgrid-ess pair of records manually from the MongoDB with fixed keys to the existing edison 1 endpoint.  See below for query checks to the existing edison dev DB.

```
select * from microgrid
where ext_key = 'Kapiri Mposhi_village'
/* id 12*/

select * from microgrid_hourly
where id_microgrid = 12
/*good load*/


select * from microgrid_ess
where ext_key = '1238_customer'
/* id 90 */

select * from wh_transaction 
where id_microgrid_ess = 90
/* ok, but no amt_paid or nbr_wh_avg */
```

However, we still need to figure out if/how the existing Java code in edison 1 handles watt hour calculations.  In particular, the following (MySQL database) fields are still NULL once the data has been processed from the API into the database.

```
wh_transaction.text_transaction_type
wh_transaction.date_end
wh_transaction.nbr_amt_paid
wh_transaction.nbr_wh_avg
```

So the post does't fail, but does the java code expect these to be populated within the post?  If so, we need to figure out a way to do that.








