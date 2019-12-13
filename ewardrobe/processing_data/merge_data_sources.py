import pandas
from pathlib import Path
from constance import COLUMNS


def get_filenames() -> list:
    filesdir = Path(__file__).absolute().parent.parent.joinpath("data")
    filenames = [file for file in filesdir.iterdir() if file.suffix == ".csv"]
    return filenames


def merge_files(filenames: list) -> pandas.DataFrame:
    data = pandas.DataFrame(columns=COLUMNS)
    for file in filenames:
        data = data.append(pandas.read_csv(file, header=0))
    return data


if __name__ == "__main__":
    filenames = get_filenames()
    data = merge_files(filenames)
