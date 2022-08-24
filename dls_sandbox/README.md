# Connect to MLAB from python (local)

Pymongo is already installed in the `smg_api` environment.

OK, I dont have access to my base environment, and I don't want to mess around with the `smg_api` environment (which is not conda-based), so I am gonna create my own new conda environment that I can play around with and access from spyder.

Following instructions I found on [stack overflow](https://stackoverflow.com/questions/30170468/how-to-run-spyder-in-virtual-environment).

# Switching to personal machine

***if this works out I can give instructions to Ali/whoever to install on my office PC***

 - log into [mongodb](https://cloud.mongodb.com/) (note, actually not from mlab, they have apparently depricated that site).
 - go to clusters and click "connect"
  - there are two options `mongo shell` and a GUI called `Compass`, I am going to install both

### Mongo shell

I am gonna 

 - download zip file
 - extract files and move to `C:\mongodb_shell\`
 
This is accessed through the command line, which means I could use `cmd` or git bash (or possibly the anaconda shell).  It also means that I need to add the location to with windows PATH variable.

First gonna try through `cmd` [using guidance from the web](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/#:~:text=The%20Windows%20System%20PATH%20tells,the%20system%20PATH%20by%20default.).

 - in start menu search for "advanced systems settings"
 - open it and click on "environment variables" 
 - find the `Path` variable and click "edit" 
 - click "new" then paste in path (in this case `C:\mongodb_shell\bin\`) and click "ok"

Ok, looks like that worked, just need the right connection string from `cmd`:

```
mongo "mongodb+srv://cluster0.ok5iq.mongodb.net/microgrid" --username admin
```

Ok, works, prompt comes up for the password, once you enter that, you get the mongo prompt, example below:

```
MongoDB Enterprise atlas-10urrk-shard-0:PRIMARY> db.getName()
microgrid
```

### Compass

This is a GUI, we'll see how it goes.

Downloaded and installed no problem, now just need to learn a little more about using mongo.

# Data Simulator

Create sim data to load into MongoDB

### Microgrid const values 

One weird thing about the `microgrid_ess` post is that it has a lot of microgrid values duplicated in it.  My first operating assumption is gonna be that all of those can be null except the microgrid `extKey`.  Once I have that, I will test the post, and then if it doesn't fail, will continue from there.  If it does fail, have to figure out what data is actually actually needs to exist in current enviromnent.

Constant values in actual data (just repeat):

```
nbr_avg_solar_insolation_annual		2135
nbr_base_load_kw		0.3
nbr_capacity_kw		6
nbr_storage_kwh		30
```

### hourlies

right now just making these random `floats` without regard for how much customers have purchases, or battery capacity, or whatever.




### date conversion

https://www.epochconverter.com/

https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime

https://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p

```
import datetime as dt
mytime = dt.datetime(2012,4,1,0,0)
mytime_ms = int(mytime.timestamp())*1000
```


### location names

outrageous, the microgrid post follows a different naming convention that the **microgrid element within the microgrid ess post**.

```
mg_ind["extKey"] = mg_ik["extKey"]
mg_ind["nameProvince"] = mg_ik["provinceName"]
mg_ind["nameCity"] = mg_ik["cityName"]
mg_ind["nameVillage"] = mg_ik["villageName"]
```

# Replacing keys

One of the important fixes for the situation here will be replacing the ESS `extKey` with the customer `extKey`.

There are a few steps here, but let me first jot a couple of key things and then decide how to approach them:

 1. Figure out how to do a field swap using the `$project` functionality within the aggregation framework.
 2. Figure out how to make this work in terms of daily or hourly updates (just filter by time??? get last update from "to" collection and use that to limit records pulled from "from" collection)
 3. Figure out the best way to include aggregation pipeline in existing framework (even docDB???)
 4. do I have to do something similar for microgrid `extKey` and village (in both ESS post and MG post)
 5. Time wise, need to make sure that MG is posted before ESS for any period

## STEP 1: Query projections

Will replace field values using [projection](https://docs.mongodb.com/manual/reference/operator/aggregation/project/) functionality within the aggregation framework. 

Setting up in the `mlab_connect.py` script in this directory.

Also, to work on testing solutions with non-reeep data, adding `key_replacement_sketch.py`.  

 - Have basic key replacement
 - have basic [accessing nested elements](https://docs.mongodb.com/manual/tutorial/query-embedded-documents/)
 - Need to figure out updating strategies
     - append based on time? based on checking what's already there?
     - scrub out-db each time?
     - what to do with mongo-assigned keys
     - also need to figure it out on both sides: incoming and outgoing
         - solutions may be different

Ok, before I get into more detailed thinking on updating strategies, want to move from my play data to (still play) microgrid data.

One thing in moving from play data to microgrid data, is that I want to keep certain fields within arrays or sub documents, so how to do that?

Ok, worked well in personal data, now we have several use cases for actual data.

### Simple key replacement

Completed testing on non-reeep play data, moving to `key_replacement.py` to start working on simulated microgrid data.

 - Microgrid key replacement works
 - ESS key replacement will be a little tricker because I want to keep part of microgrid subdocument, but not it's key
 - Got ESS to work with sim data
 - So I need to figure out how to indicate which fields to keep, but still keep them within the subdocument
 
Also, note, I am keeping the old key in `rawExtKey`, which we will need to strip out when sending the data to the Edison 1 endpoint.  This occurs in three places:

 - In microgrid, in the main doc
 - In microgrid-ess in the main doc and in the microgrid subdocument

Per Prachi, she thinks that existing java code may handle tier calculations, so I am gonna write some code that just tries to take data out of the DB and drop into JSON to be posted to Edison 1 endpoint.  Once I get this set up, want to test it in our intg environment before moving to actual dev enviromnent.

https://stackoverflow.com/questions/19674311/json-serializing-mongodb

***Heads up, remember need to drop some fields, including nested raw key and `_id`.***
 
### ad hoc tier calculations

In this case we want to do an ad hoc analysis to calculate the tiers (based on 90 day watt-hour/day average) for all connections.

 - anybody who has had power in the past 90 days is active
     - purchase date + days purchased
 - average wH is calculated over the min of 90 days and date of first purchase

The fields we need for this are:

 - Customer extKey: `$customer.extKey`
 - Connection date: `connectionDate`
     - need to convert from milliseconds to datetime or date
 - a bunch of stuff from `whTransactions`
	 - start date of purchse: `dtStart`
         - need to convert from milliseconds to datetime or date
	 - days purchased: `nbrDaysPurchased`
	 - Amp limit : `nbrCentaLimit{x}`, x in 1 to 5
	     - Q: is this really in "centaAmps"?
	 - Socket start and stop times: `socket{m}{ss}{n}`
	     - m in 1 to 5, n in 0 to 4, ss in ["Start", "Stop"]
		 - Note: see data generator for handling socket naming
		 - Note: have XX59, may need to do XX59 + 1, like if mod 60 != 0
		 - Note: or maybe just round up to nearest integer after calculation

***How much of the Wh logic can be done in pipeline vs. in python?***
		 

***Quick aside, not sure where to document this, so doing it here for now: connecting EC2 to S3***

 - using [instructions](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-access-s3-bucket/) from AWS
 - create new IAM role
 - install AWS CLI tool, `sudo apt install awscli`
 - ok, worked, use: `aws s3 cp mg.json s3://microgrid-data-upload/mg.json`

***END quick aside***





















