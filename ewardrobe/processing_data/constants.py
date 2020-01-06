from pathlib import Path

COLUMNS = [
    "product_name",
    "price",
    "pdp_url",
    "brand_name",
    "product_category",
    "retailer",
    "description",
    "rating",
    "review_count",
    "color",
]

FILESDIR = Path(__file__).absolute().parent.parent.joinpath("data")
