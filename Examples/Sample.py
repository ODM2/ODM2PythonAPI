from __future__ import (absolute_import, division, print_function)

__author__ = 'stephanie'

#import matplotlib.pyplot as plt




from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import *
from odm2api.ODM2.services import CreateODM2
# Create a connection to the ODM2 database
# ----------------------------------------


#connect to database
# createconnection (dbtype, servername, dbname, username, password)
# session_factory = dbconnection.createConnection('connection type: sqlite|mysql|mssql|postgresql', '/your/path/to/db/goes/here', 2.0)#sqlite
session_factory = dbconnection.createConnection('postgresql', 'localhost', 'odm2', 'ODM', 'odm')
# session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')#mysql

# session_factory= dbconnection.createConnection('mssql', "(local)", "ODM2", "ODM", "odm")#win MSSQL

# session_factory= dbconnection.createConnection('mssql', "arroyoodm2", "", "ODM", "odm")#mac/linux MSSQL
# session_factory = dbconnection.createConnection('sqlite', '/Users/stephanie/DEV/YODA-Tools/tests/test_files/XL_specimen.sqlite', 2.0)










#_session = session_factory.getSession()
read = ReadODM2(session_factory)
create = CreateODM2(session_factory)


# Run some basic sample queries.
# ------------------------------
# Get all of the variables from the database and print their names to the console
allVars = read.getVariables()
print ("\n-------- Information about Variables ---------")
for x in allVars:
    print(x.VariableCode + ": " + x.VariableNameCV)



# Get all of the people from the database
allPeople = read.getPeople()
print ("\n-------- Information about People ---------")
for x in allPeople:
    print(x.PersonFirstName + " " + x.PersonLastName)

try:
    print("\n-------- Information about an Affiliation ---------")
    allaff = read.getAffiliations()
    for x in allaff:
        print(x.PersonObj.PersonFirstName + ": " + str(x.OrganizationID))
except Exception as e:
    print("Unable to demo getAllAffiliations", e)

# Get all of the SamplingFeatures from the database that are Sites
try:
    print ("\n-------- Information about Sites ---------")
    siteFeatures = read.getSamplingFeatures(type= 'site')
    # siteFeatures = read.getSamplingFeatures(type='Site')
    numSites = len(siteFeatures)
    print ("Successful query")
    for x in siteFeatures:
        print(x.SamplingFeatureCode + ": " + x.SamplingFeatureTypeCV )
except Exception as e:
    print("Unable to demo getSamplingFeaturesByType", e)


# Now get the SamplingFeature object for a SamplingFeature code
try:
    sf = read.getSamplingFeatures(codes=['USU-LBR-Mendon'])[0]
    print(sf)
    print("\n-------- Information about an individual SamplingFeature ---------")
    print("The following are some of the attributes of a SamplingFeature retrieved using getSamplingFeatureByCode(): \n")
    print("SamplingFeatureCode: " + sf.SamplingFeatureCode)
    print("SamplingFeatureName: " + sf.SamplingFeatureName)
    print("SamplingFeatureDescription: %s" % sf.SamplingFeatureDescription)
    print("SamplingFeatureGeotypeCV: %s" % sf.SamplingFeatureGeotypeCV)
    print("SamplingFeatureGeometry: %s" % sf.FeatureGeometry)
    print("Elevation_m: %s" % str(sf.Elevation_m))
except Exception as e:
    print("Unable to demo getSamplingFeatureByCode: ", e)

#add sampling feature
print("\n------------ Create Sampling Feature --------- \n")
try:
    # from odm2api.ODM2.models import SamplingFeatures
    session = session_factory.getSession()
    newsf = Sites(FeatureGeometryWKT = "POINT(-111.946 41.718)", Elevation_m=100, ElevationDatumCV=sf.ElevationDatumCV,
    SamplingFeatureCode= "TestSF",SamplingFeatureDescription = "this is a test in sample.py",
    SamplingFeatureGeotypeCV= "Point", SamplingFeatureTypeCV=sf.SamplingFeatureTypeCV,SamplingFeatureUUID= sf.SamplingFeatureUUID+"2",
    SiteTypeCV="cave", Latitude= "100", Longitude= "-100", SpatialReferenceID= 0)

    c=create.createSamplingFeature(newsf)
    #session.commit()
    print("new sampling feature added to database", c)

except Exception as e :
    print("error adding a sampling feature: " + str(e))


# Drill down and get objects linked by foreign keys
print("\n------------ Foreign Key Example --------- \n",)
try:
    # Call getResults, but return only the first result
    firstResult = read.getResults()[0]
    print("The FeatureAction object for the Result is: ", firstResult.FeatureActionObj)
    print("The Action object for the Result is: ", firstResult.FeatureActionObj.ActionObj)
    print ("\nThe following are some of the attributes for the Action that created the Result: \n" +
           "ActionTypeCV: " + firstResult.FeatureActionObj.ActionObj.ActionTypeCV + "\n" +
           "ActionDescription: " + firstResult.FeatureActionObj.ActionObj.ActionDescription + "\n" +
           "BeginDateTime: " + str(firstResult.FeatureActionObj.ActionObj.BeginDateTime) + "\n" +
           "EndDateTime: " + str(firstResult.FeatureActionObj.ActionObj.EndDateTime) + "\n" +
           "MethodName: " + firstResult.FeatureActionObj.ActionObj.MethodObj.MethodName + "\n" +
           "MethodDescription: " + firstResult.FeatureActionObj.ActionObj.MethodObj.MethodDescription)
except Exception as e:
    print("Unable to demo Foreign Key Example: ", e)


# Now get a particular Result using a ResultID
print("\n------- Example of Retrieving Attributes of a Result -------")
try:
    tsResult = read.getResults(ids = [1])[0]
    print (
        "The following are some of the attributes for the TimeSeriesResult retrieved using getResults(ids=[1]): \n" +
        "ResultTypeCV: " + tsResult.ResultTypeCV + "\n" +
        # Get the ProcessingLevel from the TimeSeriesResult's ProcessingLevel object
        "ProcessingLevel: " + tsResult.ProcessingLevelObj.Definition + "\n" +
        "SampledMedium: " + tsResult.SampledMediumCV + "\n" +
        # Get the variable information from the TimeSeriesResult's Variable object
        "Variable: " + tsResult.VariableObj.VariableCode + ": " + tsResult.VariableObj.VariableNameCV + "\n"
                               #"AggregationStatistic: " + tsResult.AggregationStatisticCV + "\n" +

        # Get the site information by drilling down
        "SamplingFeature: " + tsResult.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode + " - " +
        tsResult.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName)
except Exception as e:
    print("Unable to demo Example of retrieving Attributes of a time Series Result: ", e)

# Get the values for a particular TimeSeriesResult
print("\n-------- Example of Retrieving Time Series Result Values ---------")

tsValues = read.getResultValues(resultid = 1)  # Return type is a pandas datafram

# Print a few Time Series Values to the console
# tsValues.set_index('ValueDateTime', inplace=True)
try:
    print(tsValues.head())
except Exception as e:
    print(e)

# Plot the time series

try:
    plt.figure()
    ax=tsValues.plot(x='ValueDateTime', y='DataValue')

    plt.show()
except Exception as e:
    print("Unable to demo plotting of tsValues: ", e)
