import logging


from sqlalchemy import distinct, func


from ...ODMconnection import SessionFactory
from ...versionSwitcher import ODM#.models import Site, Variable, Unit, Series, DataValue, Qualifier, OffsetType, Sample, Method, QualityControlLevel, ODMVersion
from ...base import serviceBase
#from odmtools.common.logger import LoggerTool
import pandas as pd

#tool = LoggerTool()
#logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class SeriesService(serviceBase):
    # Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg


    def reset_session(self):
        self._session = self._session_factory.get_session()  # Reset the session in order to prevent memory leaks

    def get_db_version(self):
        return self._session.query(ODM.ODMVersion).first().version_number

#####################
#
# Get functions
#
#####################

    # Site methods
    def get_all_sites(self):
        """

        :return: List[Sites]
        """
        return self._session.query(ODM.Site).order_by(ODM.Site.code).all()


    def get_used_sites(self):
        """
        Return a list of all sites that are being referenced in the Series Catalog Table
        :return: List[Sites]
        """
        try:
            site_ids = [x[0] for x in self._session.query(distinct(ODM.Series.site_id)).all()]
        except:
            site_ids = None

        if not site_ids:
            return None

        Sites = []
        for site_id in site_ids:
            Sites.append(self._session.query(ODM.Site).filter_by(id=site_id).first())

        return Sites


    def get_site_by_id(self, site_id):
        """
        return a Site object that has an id=site_id
        :param site_id: integer- the identification number of the site
        :return: Sites
        """
        try:
            return self._session.query(ODM.Site).filter_by(id=site_id).first()
        except:
            return None

    # Variables methods
    def get_used_variables(self):
        """
        #get list of used variable ids
        :return: List[Variables]
        """

        try:
            var_ids = [x[0] for x in self._session.query(distinct(ODM.Series.variable_id)).all()]
        except:
            var_ids = None

        if not var_ids:
            return None

        Variables = []

        #create list of variables from the list of ids
        for var_id in var_ids:
            Variables.append(self._session.query(ODM.Variable).filter_by(id=var_id).first())

        return Variables

    def get_all_variables(self):
        """

        :return: List[Variables]
        """
        return self._session.query(ODM.Variable).all()

    def get_variable_by_id(self, variable_id):
        """

        :param variable_id: int
        :return: Variables
        """
        try:
            return self._session.query(ODM.Variable).filter_by(id=variable_id).first()
        except:
            return None

    def get_variable_by_code(self, variable_code):
        """

        :param variable_code:  str
        :return: Variables
        """
        try:
            return self._session.query(ODM.Variable).filter_by(code=variable_code).first()
        except:
            return None

    def get_variables_by_site_code(self, site_code):  # covers NoDV, VarUnits, TimeUnits
        """
        Finds all of variables at a site
        :param site_code: str
        :return: List[Variables]
        """
        try:
            var_ids = [x[0] for x in self._session.query(distinct(ODM.Series.variable_id)).filter_by(
                site_code=site_code).all()]
        except:
            var_ids = None

        variables = []
        for var_id in var_ids:
            variables.append(self._session.query(ODM.Variable).filter_by(id=var_id).first())

        return variables

    # Unit methods
    def get_all_units(self):
        """

        :return: List[Units]
        """
        return self._session.query(ODM.Unit).all()

    def get_unit_by_name(self, unit_name):
        """

        :param unit_name: str
        :return: Units
        """
        try:
            return self._session.query(ODM.Unit).filter_by(name=unit_name).first()
        except:
            return None

    def get_unit_by_id(self, unit_id):
        """

        :param unit_id: int
        :return: Units
        """
        try:
            return self._session.query(ODM.Unit).filter_by(id=unit_id).first()
        except:
            return None


    def get_all_qualifiers(self):
        """

        :return: List[Qualifiers]
        """
        result = self._session.query(ODM.Qualifier).order_by(ODM.Qualifier.code).all()
        return result

    def get_qualifiers_by_series_id(self, series_id):
        """

        :param series_id:
        :return:
        """
        subquery = self._session.query(ODM.DataValue.qualifier_id).outerjoin(
            ODM.Series.data_values).filter(ODM.Series.id == series_id, ODM.DataValue.qualifier_id != None).distinct().subquery()
        return self._session.query(ODM.Qualifier).join(subquery).distinct().all()

    #QCL methods
    def get_all_qcls(self):
        return self._session.query(ODM.QualityControlLevel).all()

    def get_qcl_by_id(self, qcl_id):
        try:
            return self._session.query(ODM.QualityControlLevel).filter_by(id=qcl_id).first()
        except:
            return None

    def get_qcl_by_code(self, qcl_code):
        try:
            return self._session.query(ODM.QualityControlLevel).filter_by(code=qcl_code).first()
        except:
            return None

    # Method methods
    def get_all_methods(self):
        return self._session.query(ODM.Method).all()

    def get_method_by_id(self, method_id):
        try:
            result = self._session.query(ODM.Method).filter_by(id=method_id).first()
        except:
            result = None
        return result

    def get_method_by_description(self, method_code):
        try:
            result = self._session.query(ODM.Method).filter_by(description=method_code).first()
        except:
            result = None
        return result

    def get_offset_types_by_series_id(self, series_id):
        """

        :param series_id:
        :return:
        """
        subquery = self._session.query(ODM.DataValue.offset_type_id).outerjoin(
            ODM.Series.data_values).filter(ODM.Series.id == series_id, ODM.DataValue.offset_type_id != None).distinct().subquery()
        return self._session.query(ODM.OffsetType).join(subquery).distinct().all()

    def get_samples_by_series_id(self, series_id):
        """

        :param series_id:
        :return:
        """

        subquery = self._session.query(ODM.DataValue.sample_id).outerjoin(ODM.Series.data_values).filter(ODM.Series.id == series_id, ODM.DataValue.sample_id != None).distinct().subquery()
        return self._session.query(ODM.Sample).join(subquery).distinct().all()

    # Series Catalog methods
    def get_all_series(self):
        """
        Returns all series as a modelObject
        :return: List[Series]
        """

        #logger.debug("%s" % self._session.query(Series).order_by(Series.id).all())
        return self._session.query(ODM.Series).order_by(ODM.Series.id).all()

    def get_series_by_site(self , site_id):
        """

        :param site_id: int
        :return: List[Series]
        """
        try:
            selectedSeries = self._session.query(ODM.Series).filter_by(site_id=site_id).order_by(ODM.Series.id).all()
            return selectedSeries
        except:
            return None

    def get_series_by_id(self, series_id):
        """

        :param series_id: int
        :return: Series
        """
        try:
            return self._session.query(ODM.Series).filter_by(id=series_id).first()
        except Exception as e:
            print e
            return None

    def get_series_by_id_quint(self, site_id, var_id, method_id, source_id, qcl_id):
        """

        :param site_id:
        :param var_id:
        :param method_id:
        :param source_id:
        :param qcl_id:
        :return: Series
        """
        try:
            return self._session.query(ODM.Series).filter_by(
                site_id=site_id, variable_id=var_id, method_id=method_id,
                source_id=source_id, quality_control_level_id=qcl_id).first()
        except:
            return None

    def get_series_from_filter(self):
        # Pass in probably a Series object, match it against the database
        pass


    #Data Value Methods
    def get_values_by_series(self, series_id):
        '''

        :param series_id:  Series id
        :return: pandas dataframe
        '''
        series= self.get_series_by_id(series_id)
        if series:
            q = self._session.query(ODM.DataValue).filter_by(
                    site_id=series.site_id,
                    variable_id=series.variable_id,
                    method_id=series.method_id,
                    source_id=series.source_id,
                    quality_control_level_id=series.quality_control_level_id)

            query=q.statement.compile(dialect=self._session_factory.engine.dialect)
            data= pd.read_sql_query(sql= query,
                              con = self._session_factory.engine,
                              params = query.params )
            #return data.set_index(data['LocalDateTime'])
            return data
        else:
            return None

    def get_all_values_df(self):
        """

        :return: Pandas DataFrame object
        """
        q = self._session.query(ODM.DataValue).order_by(ODM.DataValue.local_date_time)
        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query, con=self._session_factory.engine,
                          params=query.params)
        columns = list(data)

        columns.insert(0, columns.pop(columns.index("DataValue")))
        columns.insert(1, columns.pop(columns.index("LocalDateTime")))
        columns.insert(2, columns.pop(columns.index("QualifierID")))

        data = data.ix[:, columns]
        return data.set_index(data['LocalDateTime'])

    def get_all_values_list(self):
        """

        :return:
        """
        result = self._session.query(ODM.DataValue).order_by(ODM.DataValue.local_date_time).all()
        return [x.list_repr() for x in result]

    def get_all_values(self):
        return self._session.query(ODM.DataValue).order_by(ODM.DataValue.local_date_time).all()

    @staticmethod
    def calcSeason(row):

        month = int(row["Month"])

        if month in [1, 2, 3]:
            return 1
        elif month in[4, 5, 6]:
            return 2
        elif month in [7, 8, 9]:
            return 3
        elif month in [10, 11, 12]:
            return 4

    def get_all_plot_values(self):
        """

        :return:
        """
        q = self._session.query(ODM.DataValue.data_value.label('DataValue'),
                                   ODM.DataValue.local_date_time.label('LocalDateTime'),
                                   ODM.DataValue.censor_code.label('CensorCode'),
                                   func.strftime('%m', ODM.DataValue.local_date_time).label('Month'),
                                   func.strftime('%Y',ODM.DataValue.local_date_time).label('Year')
                                   #DataValue.local_date_time.strftime('%m'),
                                   #DataValue.local_date_time.strftime('%Y'))
        ).order_by(ODM.DataValue.local_date_time)
        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query,
                                 con=self._session_factory.engine,
                                 params=query.params)
        data["Season"] = data.apply(self.calcSeason, axis=1)
        return data.set_index(data['LocalDateTime'])

    def get_plot_values(self, seriesID, noDataValue, startDate = None, endDate = None ):
        """

        :param seriesID:
        :param noDataValue:
        :param startDate:
        :param endDate:
        :return:
        """
        series = self.get_series_by_id(seriesID)

        DataValues = [
            (dv.data_value, dv.local_date_time, dv.censor_code, dv.local_date_time.strftime('%m'),
                dv.local_date_time.strftime('%Y'))
            for dv in series.data_values
            if dv.data_value != noDataValue if dv.local_date_time >= startDate if dv.local_date_time <= endDate
        ]
        data = pd.DataFrame(DataValues, columns=["DataValue", "LocalDateTime", "CensorCode", "Month", "Year"])
        data.set_index(data['LocalDateTime'], inplace=True)
        data["Season"] = data.apply(self.calcSeason, axis=1)
        return data



    def get_data_value_by_id(self, id):
        """

        :param id:
        :return:
        """
        try:
            return self._session.query(ODM.DataValue).filter_by(id=id).first()
        except:
            return None

    def get_all_sources(self):
        try:
            return self._session.query(ODM.Source).all()
        except:
            return None


#####################
#
#Update functions
#
#####################
    def update_series(self, series):
        """

        :param series:
        :return:
        """
        merged_series = self._session.merge(series)
        self._session.add(merged_series)
        self._session.commit()

    def update_dvs(self, dv_list):
        """

        :param dv_list:
        :return:
        """
        merged_dv_list = map(self._session.merge, dv_list)
        self._session.add_all(merged_dv_list)
        self._session.commit()

#####################
#
#Create functions
#
#####################
    def save_series(self, series, dvs):
        """ Save to an Existing Series
        :param series:
        :param data_values:
        :return:
        """

        if self.series_exists(series):

            try:
                self._session.add(series)
                self._session.commit()
                self.save_values(dvs)
            except Exception as e:
                self._session.rollback()
                raise e
            #logger.debug("Existing File was overwritten with new information")
            return True
        else:
            #logger.debug("There wasn't an existing file to overwrite, please select 'Save As' first")
            # there wasn't an existing file to overwrite
            raise Exception("Series does not exist, unable to save. Please select 'Save As'")


    def save_new_series(self, series, dvs):
        """ Create as a new catalog entry
        :param series:
        :param data_values:
        :return:
        """
        # Save As case
        if self.series_exists(series):
            msg = "There is already an existing file with this information. Please select 'Save' or 'Save Existing' to overwrite"
            #logger.debug(msg)
            raise Exception(msg)
        else:
            try:
                self._session.add(series)
                self._session.commit()
                self.save_values(dvs)
                #self._session.add_all(dvs)
            except Exception as e:
                self._session.rollback()
                raise e


        #logger.debug("A new series was added to the database, series id: "+str(series.id))
        return True

    def save_values(self, values):
        """

        :param values: pandas dataframe
        :return:
        """
        values.to_sql(name="datavalues", if_exists='append', con=self._session_factory.engine, index=False)


    def create_new_series(self, data_values, site_id, variable_id, method_id, source_id, qcl_id):
        """

        :param data_values:
        :param site_id:
        :param variable_id:
        :param method_id:
        :param source_id:
        :param qcl_id:
        :return:
        """
        self.update_dvs(data_values)
        series = ODM.Series()
        series.site_id = site_id
        series.variable_id = variable_id
        series.method_id = method_id
        series.source_id = source_id
        series.quality_control_level_id = qcl_id

        self._session.add(series)
        self._session.commit()
        return series

    def create_method(self, description, link):
        """

        :param description:
        :param link:
        :return:
        """
        meth = ODM.Method()
        meth.description = description
        if link is not None:
            meth.link = link

        self._session.add(meth)
        self._session.commit()
        return meth

    def create_variable_by_var(self, var):
        """

        :param var:  Variable Object
        :return:
        """
        try:
            self._session.add(var)
            self._session.commit()
            return var
        except:
            return None

    def create_variable(
            self, code, name, speciation, variable_unit_id, sample_medium,
            value_type, is_regular, time_support, time_unit_id, data_type,
            general_category, no_data_value):
        """

        :param code:
        :param name:
        :param speciation:
        :param variable_unit_id:
        :param sample_medium:
        :param value_type:
        :param is_regular:
        :param time_support:
        :param time_unit_id:
        :param data_type:
        :param general_category:
        :param no_data_value:
        :return:
        """
        var = ODM.Variable()
        var.code = code
        var.name = name
        var.speciation = speciation
        var.variable_unit_id = variable_unit_id
        var.sample_medium = sample_medium
        var.value_type = value_type
        var.is_regular = is_regular
        var.time_support = time_support
        var.time_unit_id = time_unit_id
        var.data_type = data_type
        var.general_category = general_category
        var.no_data_value = no_data_value

        self._session.add(var)
        self._session.commit()
        return var

    def create_qcl(self, code, definition, explanation):
        """

        :param code:
        :param definition:
        :param explanation:
        :return:
        """
        qcl = ODM.QualityControlLevel()
        qcl.code = code
        qcl.definition = definition
        qcl.explanation = explanation

        self._session.add(qcl)
        self._session.commit()
        return qcl


    def create_qualifier_by_qual(self, qualifier):
        self._session.add(qualifier)
        self._session.commit()
        return qualifier

    def create_qualifier(self,  code, description):
        """

        :param code:
        :param description:
        :return:
        """
        qual = ODM.Qualifier()
        qual.code = code
        qual.description = description

        return self.create_qualifier_by_qual(qual)

#####################
#
# Delete functions
#
#####################

    def delete_series(self, series):
        """

        :param series:
        :return:
        """
        self.delete_values_by_series(series)

        delete_series = self._session.merge(series)
        self._session.delete(delete_series)
        self._session.commit()


    def delete_values_by_series(self, series):
        """

        :param series:
        :return:
        """
        try:
            return self._session.query(ODM.DataValue).filter_by(site_id = series.site_id,
                                                                 variable_id = series.variable_id,
                                                                 method_id = series.method_id,
                                                                 source_id = series.source_id,
                                                                 quality_control_level_id = series.quality_control_level_id).delete()
        except:
            return None

    def delete_dvs(self, id_list):
        """

        :param id_list: list of ids
        :return:
        """
        self._session.query(ODM.DataValue).filter(ODM.DataValue.id.in_(id_list)).delete(False)

#####################
#
#Exist functions
#
#####################


    def series_exists(self, series):
        """

        :param series:
        :return:
        """
        return self.series_exists_quint(
            series.site_id,
            series.variable_id,
            series.method_id,
            series.source_id,
            series.quality_control_level_id
        )

    def series_exists_quint(self, site_id, var_id, method_id, source_id, qcl_id):
        """

        :param site_id:
        :param var_id:
        :param method_id:
        :param source_id:
        :param qcl_id:
        :return:
        """
        try:
            result = self._session.query(ODM.Series).filter_by(
                site_id=site_id,
                variable_id=var_id,
                method_id=method_id,
                source_id=source_id,
                quality_control_level_id=qcl_id
            ).one()

            return True
        except:
            return False
    def qcl_exists(self, q):
        """

        :param q:
        :return:
        """
        try:
            result = self._session.query(ODM.QualityControlLevel).filter_by(code=q.code, definition=q.definition).one()
            return True
        except:

            return False

    def method_exists(self, m):
        """

        :param m:
        :return:
        """
        try:
            result = self._session.query(ODM.Method).filter_by(description=m.description).one()
            return True
        except:
            return False

    def variable_exists(self, v):
        """

        :param v:
        :return:
        """
        try:
            result = self._session.query(ODM.Variable).filter_by(code=v.code,
                                                                  name=v.name, speciation=v.speciation,
                                                                  variable_unit_id=v.variable_unit_id,
                                                                  sample_medium=v.sample_medium,
                                                                  value_type=v.value_type, is_regular=v.is_regular,
                                                                  time_support=v.time_support,
                                                                  time_unit_id=v.time_unit_id, data_type=v.data_type,
                                                                  general_category=v.general_category,
                                                                  no_data_value=v.no_data_value).one()
            return result
        except:
            return None