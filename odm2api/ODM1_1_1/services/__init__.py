__author__ = 'stephanie'
# from cv_service import CVService, refreshDB
from odm2api.ODM1_1_1.services.series_service import  SeriesService
from odm2api.ODM1_1_1.services.edit_service import  EditService
from odm2api.ODM1_1_1.services.export_service import ExportService
ODM = SeriesService.ODM

__all__ = [ 'SeriesService', 'EditService', 'ExportService', 'ODM']
# 'CVService',
# def switch_service(version ):
#     cv_service.refreshDB(version)
#     series_service.refreshDB(version)