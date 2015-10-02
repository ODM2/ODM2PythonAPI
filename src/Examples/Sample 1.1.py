__author__ = 'stephanie'
import sys
import os
from api.ODMconnection import dbconnection
import pprint
from api.ODM1_1_1.services import SeriesService

this_file = os.path.realpath(__file__)
directory = os.path.dirname(this_file)
sys.path.insert(0, directory)



# ----------------------------------------
conns = [
    #connection to the ODM1 database
    dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm', "ODM", "ODM123!!", 1.1),
    #connection to the ODM2 database
    dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm2', 'ODM', 'ODM123!!', 2.0)]


for conn in conns:
    pp = pprint.PrettyPrinter(indent=8)

    print
    print "************************************************"
    print "\t\tODM2 -> ODM1 Demo: "
    print "************************************************"
    print

    odm1service = SeriesService(conn)
    odm1service.refreshDB(conn.version)
    pp.pprint(conn)

    print
    print "************************************************"
    print "\t\tUnits: get_all_units()"
    print "************************************************"
    print

    pp.pprint(odm1service.get_unit_by_id(321))

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

    pp.pprint(odm1service.get_method_by_id(8))

    print
    print "************************************************"
    print "\t\tVariables: get_all_variables()"
    print "************************************************"
    print

    pp.pprint(odm1service.get_variable_by_id(10))

    print
    print "************************************************"
    print "\t\tData Sources: get_all_Source()"
    print "************************************************"
    print

    pp.pprint(odm1service.get_all_sources())

    print
    print "************************************************"
    print "\t\tSeries: get_all_series()"
    print "************************************************"
    print

    ser = odm1service.get_series_by_id(1)
    pp.pprint(ser)
    ser = odm1service.get_series_by_id(173)
    pp.pprint(ser)
    if ser:
        print ser.variable


    print
    print "************************************************"
    print "\t\tData Values: get_all_DataValues()"
    print "************************************************"
    print

    pp.pprint(odm1service.get_values_by_series(1))
    pp.pprint(odm1service.get_values_by_series(173))
    print "The end"


