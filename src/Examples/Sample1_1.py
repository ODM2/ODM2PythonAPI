__author__ = 'stephanie'

import matplotlib.pyplot as plt
from matplotlib import dates
import pprint
from api.ODMconnection import dbconnection
from api.ODM1_1_1.services import SeriesService


# Create a connection to the ODM2 database
# ----------------------------------------

#createconnection (dbtype, servername, dbname, username, password)
#session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
# session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm2', 'ODM', 'ODM123!!', 2)


#ODM1 DB
session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm', "ODM", "ODM123!!", 1.1)

pp = pprint.PrettyPrinter(indent=8)

print
print "************************************************"
print "\t\tODM2 -> ODM1 Demo: "
print "************************************************"
print

odm1service = SeriesService(session_factory)
pp.pprint(session_factory)

print
print "************************************************"
print "\t\tUnits: get_all_units()"
print "************************************************"
print

pp.pprint(odm1service.get_all_units())

print
print "************************************************"
print "\t\tSites: get_all_sites()"
print "************************************************"
print

pp.pprint(odm1service.get_all_sites())

print
print "************************************************"
print "\t\tMethods: get_all_methods()"
print "************************************************"
print

pp.pprint(odm1service.get_all_methods())

print
print "************************************************"
print "\t\tVariables: get_all_variables()"
print "************************************************"
print

pp.pprint(odm1service.get_all_variables())

print
print "************************************************"
print "\t\tData Sources: get_all_Source()"
print "************************************************"
print

pp.pprint(odm1service.get_all_sources())


print
print "************************************************"
print "\t\tData Values: get_all_series()"
print "************************************************"
print

pp.pprint(odm1service.get_all_series())


print
print "************************************************"
print "\t\tData Values: get_all_DataValues()"
print "************************************************"
print

pp.pprint(odm1service.get_values_by_series(1))

