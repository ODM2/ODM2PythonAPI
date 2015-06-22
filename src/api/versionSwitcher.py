__author__ = 'stephanie'




dbtype = 10

if dbtype == 2.0:
    import ODM1_1_1.models as ODM
else :
    import ODM2.LikeODM1.models as ODM

#one time thing, easier



import ODM1_1_1.models as ODM1
import ODM2.LikeODM1.models as ODM2

class Series():
    @staticmethod
    def get(dbtype):
        if dbtype =='2.0':
            return ODM2.Series
        else:
            return ODM1.Series
    #pass
#can change whenever called, must create one for each class.


class Series():
    @staticmethod
    def get(dbconn):
        try:
            dbconn.query(ODM1.ODMVersion).all()
        except:
            pass








class SpeciationCV():
    pass


class TopicCategoryCV():
    pass


class Unit():
    pass


class ValueTypeCV():
    pass


class CensorCodeCV():
    pass


class DataTypeCV():
    pass


class GeneralCategoryCV():
    pass


class ISOMetadata():
    pass


class LabMethod():
    pass


class Method():
    pass


class ODMVersion():
    pass


class OffsetType():
    pass


class Qualifier():
    pass


class QualityControlLevel():
    pass


class Sample():
    pass


class SampleMediumCV():
    pass


class SampleTypeCV():
    pass


class SpatialReference():
    pass


class Site():
    pass


class SiteTypeCV():
    pass


class Source():
    pass


class Variable():
    pass


class VariableNameCV():
    pass


class VerticalDatumCV():
    pass


class DataValue():
    pass