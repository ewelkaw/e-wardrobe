import pandas
import random
from pathlib import Path
from constants import COLUMNS


def get_filenames() -> list:
    filesdir = Path(__file__).absolute().parent.parent.joinpath("data")
    filenames = [file for file in filesdir.iterdir() if file.suffix == ".csv"]
    return filenames


def merge_files(filenames: list) -> pandas.DataFrame:
    data = pandas.DataFrame(columns=COLUMNS)
    for file in filenames:
        temp_data = pandas.read_csv(file, header=0)
        for idx, value in enumerate(temp_data["price"]):
            new_price = float(temp_data["price"].iloc[idx][1:])
            temp_data["price"].iloc[idx] = new_price
        data = data.append(temp_data)
    data = data.drop(
        ["mrp", "style_attributes", "total_sizes", "available_size"], axis=1
    )
    return data


if __name__ == "__main__":
    filenames = get_filenames()
    data = merge_files(filenames)
    print(data)
