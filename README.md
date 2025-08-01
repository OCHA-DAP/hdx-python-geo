# HDX Python Geo

A collection of tools to perform common geospartial operations.

## Development

Initialize your python environment with [uv](https://docs.astral.sh/uv/).

```shell
uv sync
```

This tools accepts configuration either in the form of command line arguments or environment variables. Command line arguments will take precedence over environment variables. Make a copy of `.env.example` and fill in the values as needed.

### ESRI Downloader

Command:

```shell
uv run task esri --arcgis-url https://gis.example.org/server/rest/services
```

A bulk downloader of ESRI Feature Service layers. For any provided URL, it will crawl through all available services and layers, saving a local copy in any GDAL supported format given with a provided file extension (Using GeoParquet by default if no extension is provided). Finally, to avoid downloading layers you don't need, you can set a regex to match the Feature Service URL or the layer name.

### GeoParquet Converter

Command:

```shell
uv run task parquet --input-path /my/input/path
```

Converts files to GeoParquet based on current [best practices](https://github.com/opengeospatial/geoparquet/blob/main/format-specs/distributing-geoparquet.md).
