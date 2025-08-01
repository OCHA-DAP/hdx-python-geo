from pathlib import Path

from geopandas import read_file, read_parquet


def main(input_path: Path, output_path: Path) -> None:
    """Use GeoPandas to convert files to Parquet.

    GeoPandas has all the necessary options to implement best practices in GeoParquet.

    However, because it loads all data into memory first, unlike GDAL or DuckDB which
    operate on disk, it is only recommended for small files.
    """
    if input_path.suffix == ".parquet":
        gdf = read_parquet(input_path)
    else:
        gdf = read_file(input_path, use_arrow=True)
    gdf.to_parquet(
        output_path,
        compression="zstd",
        compression_level=15,
        row_group_size=50000,
        schema_version="1.1.0",
        write_covering_bbox=True,
    )
