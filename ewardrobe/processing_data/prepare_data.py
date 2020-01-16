import pandas

from ewardrobe_app.models import Brand, Category, Color, Product, Retailer
from processing_data.constants import COLUMNS, FILESDIR


class DataLoader:
    def __init__(self, filesdir=FILESDIR):
        self.filesdir = filesdir

    @property
    def filenames(self) -> list:
        filenames = [file for file in self.filesdir.iterdir() if file.suffix == ".csv"]
        return filenames

    def load_data_from_source(self, file) -> pandas.DataFrame:
        temp_data = pandas.read_csv(
            file, header=0, dtype={"price": str, "rating": float}
        )
        temp_data["price"].replace(to_replace=r"\$", value="", regex=True, inplace=True)
        temp_data = temp_data.drop(
            ["mrp", "style_attributes", "total_sizes", "available_size"], axis=1,
        )
        return temp_data

    @staticmethod
    def load_data_to_db(data: pandas.DataFrame):
        for index, row in data.iterrows():
            brand, _ = Brand.objects.get_or_create(brand_name=row["brand_name"])
            category, _ = Category.objects.get_or_create(
                category=row["product_category"]
            )
            retailer, _ = Retailer.objects.get_or_create(retailer=row["retailer"])
            color, _ = Color.objects.get_or_create(color=row["color"])
            Product.objects.create(
                name=row["product_name"],
                price=row["price"].split("-")[0],
                url=row["pdp_url"],
                description=row["description"],
                rating=row["rating"],
                review_count=row["review_count"],
                brand=brand,
                product_category=category,
                retailer=retailer,
                color=color,
            )

    def run(self):
        data = pandas.DataFrame(columns=COLUMNS)
        for file in self.filenames:
            data = data.append(
                self.load_data_from_source(file), ignore_index=True, sort=True
            )
        DataLoader.load_data_to_db(data.fillna(0))
