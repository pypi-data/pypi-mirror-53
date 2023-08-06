# salesforce-dbsync
Python library to download data from Salesforce and synchronize with a relational database 


### Example ###

This example performs the following steps for Salesforce Object 'Account' when run for the first time:
* Downloads Table Metadata from Salesforce
* Downloads Table Data from Salesforce, limited to a maximum of 10000 rows
* Creates a MySQL Database if one does not already exist
* Creates Tables in MySQL alongwith Indexes if the Table does not already exist
* Uploads the data into the MySQL Table

In the subsequent runs, it performs the following steps:
* Downloads Table Data from Salesforce
* Refreshes data in MySQL with new records or updates that from Salesforce
* Note: Deletes in Salesforce are ignored

```python
import sys
from screenwriter import Screenwriter
from salesforce_dbsync import Sync_Manager

def do_init ():
	global sw, sync_mgr
	sw = Screenwriter ()
	db_creds = {'user':'mysql_uid', 'passwd':'mysql_pwd', 'db':'TESTDB'}
	sf_creds = {'user':'sf_uid',    'passwd':'pb_pwd',    'token':'sf_tok'}
	control_map = {'min-SystemModstamp-date':'2019-01-01', 'dml-limit':10000}
	sync_mgr = Sync_Manager (sw, db_creds, sf_creds, control_map)

def do_main ():
	global sw, sync_mgr
	sync_mgr.add_sync_profile ('Account', ['Name','BillingStreet','BillingCountry'], ["BillingCountry = 'Canada'"])
	sync_mgr.init_mysql ()
	sync_mgr.init_sfdc ()
	sync_mgr.create_missing_db_tables ()
	sync_mgr.sync ()

do_init ()
do_main ()
```
