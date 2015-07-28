# CV imports
'''
from .ODM1_1_1.models import SessionFactory, VerticalDatumCV, SiteTypeCV, VariableNameCV, SpeciationCV, SampleMediumCV, \
    alueTypeCV, DataTypeCV, GeneralCategoryCV, CensorCodeCV, TopicCategoryCV, SampleTypeCV, OffsetType, Sample, \
    Qualifier, Unit
'''
from ...versionSwitcher import ODM
from ...base import serviceBase
from sqlalchemy import not_


class CVService(serviceBase):


    # Controlled Vocabulary get methods

    #return a list of all terms in the cv
    def get_vertical_datum_cvs(self):
        result = self._session.query(ODM.VerticalDatumCV).order_by(ODM.VerticalDatumCV.term).all()
        return result

    def get_samples(self):
        result = self._session.query(ODM.Sample).order_by(ODM.Sample.lab_sample_code).all()
        return result



    def get_site_type_cvs(self):
        result = self._session.query(ODM.SiteTypeCV).order_by(ODM.SiteTypeCV.term).all()
        return result

    def get_variable_name_cvs(self):
        result = self._session.query(ODM.VariableNameCV).order_by(ODM.VariableNameCV.term).all()
        return result

    def get_offset_type_cvs(self):
        result = self._session.query(ODM.OffsetType).order_by(ODM.OffsetType.id).all()
        return result

    def get_speciation_cvs(self):
        result = self._session.query(ODM.SpeciationCV).order_by(ODM.SpeciationCV.term).all()
        return result

    def get_sample_medium_cvs(self):
        result = self._session.query(ODM.SampleMediumCV).order_by(ODM.SampleMediumCV.term).all()
        return result

    def get_value_type_cvs(self):
        result = self._session.query(ODM.ValueTypeCV).order_by(ODM.ValueTypeCV.term).all()
        return result

    def get_data_type_cvs(self):
        result = self._session.query(ODM.DataTypeCV).order_by(ODM.DataTypeCV.term).all()
        return result

    def get_general_category_cvs(self):
        result = self._session.query(ODM.GeneralCategoryCV).order_by(ODM.GeneralCategoryCV.term).all()
        return result

    def get_censor_code_cvs(self):
        result = self._session.query(ODM.CensorCodeCV).order_by(ODM.CensorCodeCV.term).all()
        return result

    def get_sample_type_cvs(self):
        result = self._session.query(ODM.SampleTypeCV).order_by(ODM.SampleTypeCV.term).all()
        return result

    def get_units(self):
        result = self._session.query(ODM.Unit).all()
        return result

    def get_units_not_uni(self):
        result = self._session.query(ODM.Unit).filter(not_(ODM.Unit.name.contains('angstrom'))).all()
        return result

    def get_units_names(self):
        result = self._session.query(ODM.Unit.name).all()
        return result

    # return a single cv
    def get_unit_by_name(self, unit_name):
        result = self._session.query(ODM.Unit).filter_by(name=unit_name).first()
        return result

    def get_unit_by_id(self, unit_id):
        result = self._session.query(ODM.Unit).filter_by(id=unit_id).first()
        return result
