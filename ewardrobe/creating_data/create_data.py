import pandas as pd
import random

from creating_data.constants import (
    COLUMNS,
    BRAND_NAME,
    PRODUCT_CATEGORY,
    RETAILER,
    COLOR,
    FILESDIR,
    CSV_DIR,
)


def generate_data(column: str) -> list:
    if column == "price":
        return random.choices(range(5, 1600), k=1000)
    if column == "brand_name":
        return random.choices(BRAND_NAME, k=1000)
    if column == "product_category":
        return random.choices(PRODUCT_CATEGORY, k=1000)
    if column == "retailer":
        return random.choices(RETAILER, k=1000)
    if column == "rating":
        return random.choices(range(1, 6), k=1000)
    if column == "review_count":
        return random.choices(range(1, 150), k=1000)
    if column == "color":
        return random.choices(COLOR, k=1000)


def prepare_product_name(row: pd.Series) -> str:
    name_data = [row["brand_name"], row["color"], row["product_category"]]
    return " ".join(name_data)


def prepare_description(row: pd.Series) -> str:
    brand_name, color, product_category = (
        row["brand_name"],
        row["color"],
        row["product_category"],
    )
    description = f"Beautiful {color} {product_category} which fits every ocasion. Product was made with full attention to detail and environment by {brand_name}."

    if row["rating"] >= 3 and row["review_count"] >= 75:
        additional_opinion = f"{product_category} is very popular among our users and it has increadibly good opinions (look at rating). Give it a try!"
    elif row["rating"] >= 3 and row["review_count"] < 75:
        additional_opinion = f"{product_category} has increadibly good opinions (look at rating), so also our users guarantee that it will fit your wardrobe!"
    else:
        additional_opinion = random.choice(
            [
                "Try it yourself!",
                "Best quality guaranteed!",
                "Our users recommend it!",
                "Give it a try!",
            ]
        )
    return " ".join([description, additional_opinion])


def prepare_url(row: pd.Series) -> str:
    product_category = row["product_category"].lower()
    filenames = [
        file for file in FILESDIR.iterdir() if file.name.startswith(product_category)
    ]
    file = random.choice(filenames)
    return str(file).split("ewardrobe_app")[-1]


def add_columns(data_frame: pd.DataFrame) -> pd.DataFrame:
    product_names = []
    descriptions = []
    urls = []
    for _, row in data_frame.iterrows():
        product_names.append(prepare_product_name(row))
        descriptions.append(prepare_description(row))
        urls.append(prepare_url(row))

    data_frame["product_name"] = product_names
    data_frame["description"] = descriptions
    data_frame["pdp_url"] = urls
    return data_frame


def create_data() -> pd.DataFrame:
    data = dict()

    for column in COLUMNS:
        data[column] = generate_data(column)
    df = pd.DataFrame(data)

    return add_columns(df)


def save_data(data, csv_dir=CSV_DIR):
    data.to_csv(CSV_DIR.joinpath("generated_data.csv"), index=False)


def run():
    print("Generating data ...")
    data = create_data()
    print("Saving data ...")
    save_data(data)
