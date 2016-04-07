import os.path
from odm2api.ODM1_1_1.services  import SeriesService, ExportService

from tests import test_util1_1_1 as test_util

import  pytest

@pytest.mark.skipif(True,
                    reason="ODM1.1 shim is out of date")
class TestExportService_1_1:
	def setup(self):		
		self.connection_string = "sqlite:///:memory:"
		self.series_service = SeriesService(self.connection_string, debug=False)
		self.session = self.series_service._session_factory.get_session()		
		engine = self.series_service._session_factory.engine
		test_util.build_db(engine)
		self.series = test_util.add_series(self.session)

		self.export_service = ExportService(self.series_service)

	def test_export_series_data_1_1(self, tmpdir):
		f = tmpdir.join("export.csv")
		filename = f.dirname + f.basename

		self.export_service.export_series_data(self.series.id, filename, True,True,True,True,True,True,True)

		assert os.path.isfile(filename) == True

	def test_export_series_metadata_1_1(self, tmpdir):
		f = tmpdir.join("export.xml")
		filename = f.dirname + f.basename

		ids = [self.series.id]
		self.export_service.export_series_metadata(ids, filename)

		assert os.path.isfile(filename) == True