__author__ = 'stephanie'





import ODM1_1_1.models as ODM1
import ODM2.LikeODM1.models as ODM2


#Set Default
ODM = ODM1

def refreshDB(ver):
    if ver == 1.1:
        ODM = ODM1
    elif ver == 2.0:
        ODM = ODM2

