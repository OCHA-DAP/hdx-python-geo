from pathlib import Path

from duckdb import connect


def main(input_path: Path, output_path: Path) -> None:
    """Use DuckDB to convert files to Parquet.

    While this function performs the quickest, it does not read or write GeoParquet
    metadata to files, limiting compatibility with other readers.

    One downside to DuckDB for GeoParquet is that it doesn't automatically detect the
    actively used geometry column, which is often named either 'geometry' or 'geom'.

    Also, it does not automatically create covering bounding boxes, and if they are
    manually created, this isn't added to the Parquet metadata.

    Overall recommended to use GDAL for the above reasons.
    """
    with connect() as con:
        con.sql("LOAD spatial;")
        result = con.sql(f"""
            SELECT column_name
            FROM (DESCRIBE '{input_path}')
            WHERE column_type = 'GEOMETRY'
        """).fetchone()
        geometry_name = result[0] if result else "geometry"
        con.sql(f"""
            SET preserve_insertion_order=false;
            COPY (
                SELECT
                    *,
                    STRUCT_PACK(
                        xmin := ST_XMin({geometry_name}),
                        ymin := ST_YMin({geometry_name}),
                        xmax := ST_XMax({geometry_name}),
                        ymax := ST_YMax({geometry_name})
                    ) as bbox
                    RENAME ({geometry_name} TO geometry)
                FROM {input_path}
            )
            TO '{output_path}'
            WITH (
                COMPRESSION zstd,
                COMPRESSION_LEVEL 15,
                ROW_GROUP_SIZE_BYTES '128mb'
            );
        """)
