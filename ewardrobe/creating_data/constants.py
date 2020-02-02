from pathlib import Path

FILESDIR = (
    Path(__file__).absolute().parent.parent.joinpath("ewardrobe_app/static/products")
)
CSV_DIR = Path(__file__).absolute().parent.parent.joinpath("data")

COLUMNS = [
    "price",
    "brand_name",
    "product_category",
    "retailer",
    "rating",
    "review_count",
    "color",
]


BRAND_NAME = [
    "Nike",
    "Adidas",
    "Levis",
    "Gucci",
    "Calvin Klein",
    "Versace",
    "Lacoste",
    "Tommy Hilfiger",
]
PRODUCT_CATEGORY = [
    "T-shirt",
    "Top",
    "Trousers",
    "Pullover",
    "Dress",
    "Coat",
    "Shirt",
    "Sneakers",
    "Socks",
    "Pajamas",
]
RETAILER = ["Guess", "Steve Madden", "Old Navy", "Stone Island", "Abbey Dawn"]
COLOR = [
    "Bare",
    "Baby pink",
    "Vanilla",
    "Baby blue",
    "Canary",
    "Blond",
    "Grey",
    "Desert",
    "Bittersweet",
    "Avocado",
    "Black",
    "Alabaster",
    "Amber",
    "Auburn",
]
