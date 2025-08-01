from pathlib import Path
from subprocess import run


def main(input_path: Path, output_path: Path) -> None:
    """Use GDAL to convert files to Parquet.

    Once GDAL 3.12 is available later in 2025, the following options should be added.
    --lco=COMPRESSION_LEVEL=15
    --lco=USE_PARQUET_GEO_TYPES=YES

    If you are generating a clipping layer with large geometries you want to query one
    at a time from the cloud, split into individual row groups.
    --lco=ROW_GROUP_SIZE=1

    Although there is a PyPI package for GDAL, it is not recommended. The Python
    bindings are just a light wrapper over the native CLI, and it consumes more memory
    than using subprocess.
    """
    run(
        [
            *["gdal", "vector", "convert"],
            *[input_path, output_path],
            "--overwrite",
            "--lco=COMPRESSION=ZSTD",
            "--lco=GEOMETRY_NAME=geometry",
        ],
        check=False,
    )
