__author__ = 'stephanie'
import sys
import os


import matplotlib.pyplot as plt
from matplotlib import dates


#this will be removed when we can installthe api
# this_file = os.path.realpath(__file__)
# directory = os.path.dirname(os.path.dirname(this_file))
# print directory
# sys.path.insert(0, directory)

from api.ODMconnection import dbconnection
from api.ODM2.services.readService import *
# Create a connection to the ODM2 database
# ----------------------------------------


#connect to database
#createconnection (dbtype, servername, dbname, username, password)
#session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')
session_factory = dbconnection.createConnection('sqlite', '/Users/stephanie/DEV/DBs/ODM2.sqlite', 2.0)
# session_factory= dbconnection.createConnection('mssql')



#_session = session_factory.getSession()

read = ReadODM2(session_factory)



# Run some basic sample queries.
# ------------------------------
# Get all of the variables from the database and print their names to the console
allVars = read.getVariables()

for x in allVars:
    print x.VariableCode + ": " + x.VariableNameCV



# Get all of the people from the database
allPeople = read.getPeople()

for x in allPeople:
    print x.PersonFirstName + " " + x.PersonLastName

try:
    print "\n-------- Information about an Affiliation ---------"
    allaff = read.getAllAffiliations()
    for x in allaff:
        print x.PersonObj.PersonFirstName + ": " + str(x.OrganizationID)
except Exception as e:
    print "Unable to demo getAllAffiliations", e

# Get all of the SamplingFeatures from the database that are Sites
try:
    siteFeatures = read.getSamplingFeaturesByType('Site')
    numSites = len(siteFeatures)

    for x in siteFeatures:
        print x.SamplingFeatureCode + ": " + x.SamplingFeatureName
except Exception as e:
    print "Unable to demo getSamplingFeaturesByType", e



# Now get the SamplingFeature object for a SamplingFeature code
try:
    sf = read.getSamplingFeatureByCode('USU-LBR-Mendon')
    print "\n-------- Information about an individual SamplingFeature ---------"
    print (
        "The following are some of the attributes of a SamplingFeature retrieved using getSamplingFeatureByCode(): \n" +
        "SamplingFeatureCode: " + sf.SamplingFeatureCode + "\n" +
        "SamplingFeatureName: " + sf.SamplingFeatureName + "\n" +
        "SamplingFeatureDescription: " + sf.SamplingFeatureDescription + "\n" +
        "SamplingFeatureGeotypeCV: " + sf.SamplingFeatureGeotypeCV + "\n" +
        "SamplingFeatureGeometry: " + sf.FeatureGeometry + "\n" +
        "Elevation_m: " + str(sf.Elevation_m))
except Exception as e:
    print "Unable to demo getSamplingFeatureByCode: ", e

#add sampling feature
print "\n------------ Create Sampling Feature --------- \n",
try:
    from api.ODM2.models import SamplingFeatures
    newsf = SamplingFeatures()
    session = session_factory.getSession()
    newsf.FeatureGeometry = "POINT(-111.946 41.718)"
    newsf.Elevation_m=100
    newsf.ElevationDatumCV=sf.ElevationDatumCV
    newsf.SamplingFeatureCode= "TestSF"
    newsf.SamplingFeatureDescription = "this is a test to add Feature Geomotry"
    newsf.SamplingFeatureGeotypeCV= "Point"
    newsf.SamplingFeatureTypeCV=sf.SamplingFeatureTypeCV
    newsf.SamplingFeatureUUID= sf.SamplingFeatureUUID+"2"
    session.add(newsf)
    #session.commit()
    print "new sampling feature added to database", newsf

except Exception as e :
    print "error adding a sampling feature: " + str(e)


# Drill down and get objects linked by foreign keys
print "\n------------ Foreign Key Example --------- \n",
try:
    # Call getResults, but return only the first result
    firstResult = read.getResults()[0]
    print "The FeatureAction object for the Result is: ", firstResult.FeatureActionObj
    print "The Action object for the Result is: ", firstResult.FeatureActionObj.ActionObj
    print ("\nThe following are some of the attributes for the Action that created the Result: \n" +
           "ActionTypeCV: " + firstResult.FeatureActionObj.ActionObj.ActionTypeCV + "\n" +
           "ActionDescription: " + firstResult.FeatureActionObj.ActionObj.ActionDescription + "\n" +
           "BeginDateTime: " + str(firstResult.FeatureActionObj.ActionObj.BeginDateTime) + "\n" +
           "EndDateTime: " + str(firstResult.FeatureActionObj.ActionObj.EndDateTime) + "\n" +
           "MethodName: " + firstResult.FeatureActionObj.ActionObj.MethodObj.MethodName + "\n" +
           "MethodDescription: " + firstResult.FeatureActionObj.ActionObj.MethodObj.MethodDescription)
except Exception as e:
    print "Unable to demo Foreign Key Example: ", e


# Now get a particular Result using a ResultID
print "\n------- Example of Retrieving Attributes of a Time Series Result -------"
try:
    tsResult = read.getTimeSeriesResultByResultId(19)
    print (
        "The following are some of the attributes for the TimeSeriesResult retrieved using getTimeSeriesResultByResultID(): \n" +
        "ResultTypeCV: " + tsResult.ResultTypeCV + "\n" +
        # Get the ProcessingLevel from the TimeSeriesResult's ProcessingLevel object
        "ProcessingLevel: " + tsResult.ProcessingLevelObj.Definition + "\n" +
        "SampledMedium: " + tsResult.SampledMediumCV + "\n" +
        # Get the variable information from the TimeSeriesResult's Variable object
        "Variable: " + tsResult.VariableObj.VariableCode + ": " + tsResult.VariableObj.VariableNameCV + "\n"
                                                                                                        "AggregationStatistic: " + tsResult.AggregationStatisticCV + "\n" +
        "Elevation_m: " + str(sf.Elevation_m) + "\n" +
        # Get the site information by drilling down
        "SamplingFeature: " + tsResult.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode + " - " +
        tsResult.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName)
except Exception as e:
    print "Unable to demo Example of retrieving Attributes of a time Series Result: ", e

# Get the values for a particular TimeSeriesResult
print "\n-------- Example of Retrieving Time Series Result Values ---------"

tsValues = read.getTimeSeriesResultValuesByResultId(19)  # Return type is a pandas dataframe

# Print a few Time Series Values to the console
# tsValues.set_index('ValueDateTime', inplace=True)
try:
    print tsValues.head()
except Exception as e:
    print e

# Plot the time series

try:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tsValues.plot(x='ValueDateTime', y='DataValue', kind='line',
                  title=tsResult.VariableObj.VariableNameCV + " at " + tsResult.FeatureActionObj.SamplingFeatureObj.SamplingFeatureName,
                  ax=ax)
    ax.set_ylabel(tsResult.VariableObj.VariableNameCV + " (" + tsResult.UnitObj.UnitsAbbreviation + ")")
    ax.set_xlabel("Date/Time")
    ax.xaxis.set_minor_locator(dates.MonthLocator())
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.YearLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n%Y'))
    ax.grid(True)
    plt.show()
except Exception as e:
    print "Unable to demo plotting of tsValues: ", e
