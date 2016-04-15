The following are lists of functions supported by the ODM2 Python API

ODM2 API Get Functions
---
**getActions()**
* Pass nothing - get a list of all Action objects
* Pass ActionID - get a single Action object
* Pass ActionType - get a list of all Actions of the type passed

**getAffilations()**
* Pass nothing - get a list of all affiliation objects
* Pass a PersonID - get a list of all affilication objects for a person

**getDatasets()**
* Pass nothing - get a list of all dataset objects
* Pass a DatasetCode - get a single dataset object

**getEquipment()**
* Pass nothing - get a list of all equipment objects

**getMethods()**
* Pass nothing - returns a full list of method objects
* Pass a MethodID - returns a single method object
* Pass a MethodCode - returns a single method object

**getModels()**
* Pass nothing - get a list of all model objects
* Pass a ModelCode - get a single model object

**getOrganizations()**
* Pass nothing - returns a list of all organization objects
* Pass OrganizationID - returns a single organization object
* Pass OrganizationCode - rturns a single organization object

**getPeople()**
* Pass nothing - returns a list of all people objects
* Pass PersonID - returns a single people object
* Pass PersonName - returns a single people object

**getProcessingLevels()**
* Pass nothing - returns a full list of processing level objects
* Pass ProcessingLevelID - returns a single processing level object
* Pass ProcessingLevelCode - returns a single processing level object

**getRelatedActions()**
* Pass an ActionID - get a list of Action objects related to the input action along with the relatinship type

**getRelatedModels()**
* Pass a ModelID - get a list of model objects related to the model having ModelID
* Pass a ModelCode - get a list of model objects related to the model having ModeCode

**getRelatedSamplingFeatures()**
* Pass a SamplingFeatureID - get a list of sampling feature objects related to the input sampling feature along with the relationship type

**getResults()**
* Pass nothing - Returns a list of result objects (without values) with types specific to each result in the list
* Pass a ResultID - Returns a single result object (without values) with type specific to that result
* Pass an ActionID - Returns a list of result objects (without values) for an ActionID
* Pass a ResultType - Returns a list of result objects (without values) of that type

**getResultValues()**
* Pass a ResultID - Returns a result values object of type that is specific to the result type
* Pass a ResultID and a date range - returns a result values object of type that is specific to the result type with values between the input date range
NOTE:  Another option here would be to put a flag on getResults that specifies whether values should be returned

**getSamplingFeatures()**
* Pass nothing - returns a list of all sampling feature objects with each object of type specific to that sampling feature
* Pass a SamplingFeatureID - returns a single sampling feature object
* Pass a SamplingFeatureCode - returns a single sampling feature object
* Pass a SamplingFeatureType - returns a list of sampling feature objects of the type passed in 

**getSimulations()**
* Pass nothing - get a list of all model simuation objects
* Pass a SimulationName - get a single simulation object
* Pass an ActionID - get a single simulation object

**getUnits()**
* Pass nothing - returns a list of all units objects
* Pass UnitsID - returns a single units object
* Pass UnitsName - returns a single units object

**getVariables()**
* Pass nothing - returns full list of variable objects
* Pass a VariableID - returns a single variable object
* Pass a VariableCode - returns a single variable object


ODM2 API Create Functions
---
**createVariable()**

**createMethod()**

**createProcessingLevel()**

**createSamplingFeature()**

**createUnit()**

**createOrganization()**

**createPerson()**

**createAffiliation()**

**createDataset()**

**createDatasetResults()**

**createAction()**

**createRelatedAction()**

**createResult()**

**createResultValues()** 

**createSamplingFeature()**

**createSpatialReference()**

**createModel()**

**createRelatedModel()**

**createSimulation()**
