import pandas
import random
from pathlib import Path
from constants import COLUMNS
from .ewardrobe_app.models import Brand, Category, Retailer, Color, Product


class DataLoader:
    @property
    def filenames(self) -> list:
        filesdir = Path(__file__).absolute().parent.parent.joinpath("data")
        filenames = [file for file in filesdir.iterdir() if file.suffix == ".csv"]
        return filenames

    def merge_data_sources(self, file) -> pandas.DataFrame:
        temp_data = pandas.read_csv(file, header=0)
        temp_data["price"].replace(to_replace=r"\$", value="", regex=True, inplace=True)
        temp_data = temp_data.drop(
            ["mrp", "style_attributes", "total_sizes", "available_size"], axis=1,
        )
        return temp_data

    @staticmethod
    def load_data(data):
        for index, row in data.iterrows():
            brand, _ = Brand.objects.get_or_create(brand_name=row["brand_name"])
            category, _ = Category.objects.get_or_create(
                category=row["product_category"]
            )
            retailer, _ = Retailer.objects.get_or_create(retailer=row["retailer"])
            color, _ = Color.objects.get_or_create(color=row["color"])
            Product.objects.create(
                name=row["product_name"],
                price=row["price"],
                url=row["pdp_url"],
                description=row["description"],
                rating=row["description"],
                reviews_count=row["description"],
                brand=brand,
                product_category=category,
                retailer=retailer,
                color=color,
            )

    def run(self):
        data = pandas.DataFrame(columns=COLUMNS)
        for file in self.filenames:
            data = data.append(
                self.merge_data_sources(file), ignore_index=True, sort=True
            )
        DataLoader.load_data(data)


if __name__ == "__main__":
    DataLoader().run()
