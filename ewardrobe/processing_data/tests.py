from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pandas
from django.test import TestCase

from ewardrobe_app.models import Brand, Category, Color, Product, Retailer
from processing_data.constants import COLUMNS
from processing_data.prepare_data import DataLoader


class TestDataLoader(TestCase):
    def setUp(self):
        data = defaultdict(list)
        extended_columns = COLUMNS[:]
        extended_columns.extend(
            ["mrp", "style_attributes", "total_sizes", "available_size"]
        )
        for column in extended_columns:
            if column in ["price", "rating", "review_count"]:
                data[column].extend(
                    ["1", "10", "5", "8", "12", "67", "21", "35", "99", "109"]
                )
            else:
                data[column].extend(10 * ["test"])
        self.dataframe = pandas.DataFrame(data, columns=extended_columns)
        self.dataframe = self.dataframe.astype(str)
        self.dir = TemporaryDirectory()

        self.csv_1 = NamedTemporaryFile(
            suffix=".csv", prefix="test", dir=self.dir.name, delete=False
        )
        self.dataframe.to_csv(self.csv_1.name, index=False)

        self.csv_2 = NamedTemporaryFile(
            suffix=".csv", prefix="test", dir=self.dir.name, delete=False
        )
        self.dataframe.to_csv(self.csv_2.name, index=False)

        self.csv_3 = NamedTemporaryFile(
            suffix=".csv", prefix="test", dir=self.dir.name, delete=False
        )
        self.dataframe.to_csv(self.csv_3.name, index=False)

        self.other = NamedTemporaryFile(
            suffix=".pdf", prefix="pdf", dir=self.dir.name, delete=False
        )
        self.loader = DataLoader(Path(self.dir.name).absolute())

    def test_filenames(self):
        assert len(self.loader.filenames) == 3
        assert len(list(filter(lambda x: x.suffix == ".csv", self.loader.filenames)))
        assert len(
            list(filter(lambda x: x.name.startswith("test"), self.loader.filenames))
        )

    def test_load_data_from_source(self):
        for file in [self.csv_1, self.csv_2, self.csv_3]:
            data = self.loader.load_data_from_source(file)
            assert all(data.columns == COLUMNS)
            assert len(data["price"]) == 10

    def test_load_data_to_db(self):
        data1 = self.loader.load_data_from_source(self.csv_1)
        self.loader.load_data_to_db(data1)
        assert Product.objects.all().count() == 10
        assert Brand.objects.all().count() == 1
        assert Category.objects.all().count() == 1
        assert Color.objects.all().count() == 1
        assert Retailer.objects.all().count() == 1

        data2 = self.loader.load_data_from_source(self.csv_2)
        self.loader.load_data_to_db(data2)
        assert Product.objects.all().count() == 20
        assert Brand.objects.all().count() == 1
        assert Category.objects.all().count() == 1
        assert Color.objects.all().count() == 1
        assert Retailer.objects.all().count() == 1

        data3 = self.loader.load_data_from_source(self.csv_3)
        self.loader.load_data_to_db(data3)
        assert Product.objects.all().count() == 30
        assert Brand.objects.all().count() == 1
        assert Category.objects.all().count() == 1
        assert Color.objects.all().count() == 1
        assert Retailer.objects.all().count() == 1
