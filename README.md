# HDX Python Geo

A collection of tools to perform common geospartial operations.

## Development

Initialize your python environment with `uv`.

```shell
uv sync
```

This tools accepts configuration either in the form of command line arguments or environment variables. Command line arguments will take precedence over environment variables. Make a copy of `.env.example` and fill in the values as needed. To see a list of all available arguments:

```shell
uv run task app --help
```

## Usage

With environment variables:

```shell
uv run task app
```

or

```shell
docker compose up
```

With command line arguments:

```shell
uv run task app --url https://gis.example.org/server/rest/services
```

### ESRI Downloader

Currently, this toolbox has one tool, a bulk downloader of ESRI Feature Service layers. For any provided URL, it will crawl through all available services and layers, saving a local copy in any GDAL supported format given with a provided file extension (Using GeoPackage by default if no extension is provided). Finally, to avoid downloading layers you don't need, you can set a regex to match the Feature Service URL or the layer name.
