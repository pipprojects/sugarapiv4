# sugarapiv4
Client library for SugarCRM 6 REST API V4
===============================
Introduction
------------
This library allows access to the V4 REST API on SugarCRM 6

*Important* notes
-----------------
This library contains code from the Python webservices library
https://github.com/gddc/python_webservices_library
released under the BSD license - see LICENSE.txt

Usage
-----

V4 REST API
-----------
http://support.sugarcrm.com/Documentation/Sugar_Developer/Sugar_Developer_Guide_6.5/Application_Framework/Web_Services/Method_Calls/


Read a record by SQL query
--------------------------
Args = {
    "module_name": "Contacts",
    "query": "contacts.id = 'd0a9d59b-5c23-3777-8674-56c36cf14b0d'",
    "select_fields": ["id", "first_name", "last_name", "full_name"],
}
data = conn.Read_Record(Args)


Read a record by ID
-------------------
Args = {
    "module_name": "Contacts",
    "select_fields": ["id", "first_name", "last_name", "full_name"],
}
ID = "d0a9d59b-5c23-3777-8674-56c36cf14b0d"
data = conn.Read_Record_By_ID(ID, Args)

Create a record
---------------
Args = {
    "module_name": "Contacts",
    "name_value_list": {
        "first_name": "Stan",
        "last_name": "Smith",
    },
}
data = conn.Create_Record(Args)

Update a record by ID
---------------------
Args = {
    "module_name": "Contacts",
    "name_value_list": {
        "last_name": "Griffin",
    },
}
ID = "d0a9d59b-5c23-3777-8674-56c36cf14b0d"
data = conn.Update_Record_By_ID(ID, Args)

Anything else
-------------
Use the call method with paramters from the method as listed here
Http://support.sugarcrm.com/Documentation/Sugar_Developer/Sugar_Developer_Guide_6.5/Application_Framework/Web_Services/Method_Calls/

The arguments list can be passed as a list rather than a dict using Native=True

eg
Args =[
    "Contacts",
    "contacts.last_name like 'Smith%'",
    "",
    "",
    ["id", "first_name", "last_name", "full_name"],
]
data = sugarcrm.call("get_entry_list", Args, Native=True)

TODO
----
All the other calls


Licence
-------
This software is released under the BSD license. Refer to the
LICENSE.txt file for more information.


