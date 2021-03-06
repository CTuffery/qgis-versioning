#!/usr/bin/python
import versioning_base
from pyspatialite import dbapi2
import psycopg2
import os
import shutil

test_data_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = "/tmp"

# create the test database

os.system("dropdb epanet_test_db")
os.system("createdb epanet_test_db")
os.system("psql epanet_test_db -c 'CREATE EXTENSION postgis'")
os.system("psql epanet_test_db -f "+test_data_dir+"/epanet_test_db_unversioned.sql")

versioning_base.historize("dbname=epanet_test_db","epanet")

# try the update
wc = tmp_dir+"/bug_in_branch_after_commit_wc.sqlite"
if os.path.isfile(wc): os.remove(wc) 
versioning_base.checkout("dbname=epanet_test_db", ['epanet_trunk_rev_head.junctions', 'epanet_trunk_rev_head.pipes'], wc)

scur = versioning_base.Db( dbapi2.connect( wc ) )

scur.execute("SELECT * FROM pipes")
scur.execute("UPDATE pipes_view SET length = 1 WHERE OGC_FID = 1")
scur.commit()

versioning_base.commit(wc,'test', "dbname=epanet_test_db" )

versioning_base.add_branch("dbname=epanet_test_db","epanet","mybranch","add 'branch")
