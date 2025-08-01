import argparse
from logging import INFO, basicConfig
from multiprocessing import Pool
from os import getenv
from pathlib import Path

from ..config import data_dir
from . import gdal

basicConfig(level=INFO, format="%(asctime)s %(levelname)s %(message)s")


def convert(input_path: Path, input_glob: str) -> None:
    """Convert files to Parquet."""
    if input_glob:
        results = []
        pool = Pool()
        for input_file in sorted(input_path.glob(input_glob)):
            output_path = input_file.relative_to(input_path).with_suffix(".parquet")
            output_file = data_dir / output_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            result = pool.apply_async(gdal.main, [input_file, output_file])
            results.append(result)
        pool.close()
        pool.join()
        for result in results:
            result.get()
    else:
        output_path = data_dir / f"{input_path.stem}.parquet"
        gdal.main(input_path, output_path)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Download ESRI data.")
    parser.add_argument("--input-path", help="Input Path, filesystem or URL")
    parser.add_argument("--input-glob", help="Input Glob")

    args = parser.parse_args()
    input_path = args.input_path if args.input_path else getenv("INPUT_PATH", "")
    input_glob = args.input_glob if args.input_glob else getenv("INPUT_GLOB", "")
    convert(Path(input_path), input_glob)


if __name__ == "__main__":
    main()
