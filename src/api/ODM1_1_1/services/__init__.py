__author__ = 'stephanie'
# from cv_service import CVService, refreshDB
from series_service import refreshDB, ODM, SeriesService
from edit_service import  EditService
from export_service import ExportService

__all__ = [ 'SeriesService', 'EditService', 'ExportService', 'ODM', 'refreshDB']
# 'CVService',
# def switch_service(version ):
#     cv_service.refreshDB(version)
#     series_service.refreshDB(version)