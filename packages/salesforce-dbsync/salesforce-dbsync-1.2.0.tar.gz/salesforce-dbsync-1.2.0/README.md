# salesforce-dbsync
Python library to download data from Salesforce and synchronize with a relational database 


### Example ###

Following sample code downloads data from tables from Salesforce. 
It also creates a MySQL Database, sets up the mirror tables alongwith Indexes and inserts the data in the table.
Running the same script at a later date with Syncronize the Database table with any additions or changes in Salesforce
Deletion if records in Salesforce is currently not handeled
Only MySQL database is supported at this time

```python
from salesforce-dbsync import Screenwriter

```
```
Output:
```
