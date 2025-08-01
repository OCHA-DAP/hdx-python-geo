from pathlib import Path
from re import search
from subprocess import run
from urllib.parse import urlencode

from ..config import OBJECTID, data_dir
from .utils import client_get


def parse_fields(fields: list) -> tuple[str, str]:
    """Extract the OBJECTID and field names from a config."""
    objectid = next(x["name"] for x in fields if x["type"] == OBJECTID)
    field_names = ",".join(
        [x["name"] for x in fields if x["type"] != OBJECTID and not x.get("virtual")],
    )
    return objectid, field_names


def download_feature(
    url: str,
    extension: str,
    params: dict,
    response: dict,
    prefix: str = "",
) -> None:
    """Downloads a GeoJSON from a Feature Layer."""
    layer_name = response["name"]
    fields = response["fields"]
    objectid, field_names = parse_fields(fields)
    query = {
        **params,
        "orderByFields": objectid,
        "outFields": field_names,
        "where": "1=1",
    }
    query_url = f"{url}/query?{urlencode(query)}"
    output_file = data_dir / prefix / f"{layer_name}{extension}"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            *["gdal", "vector", "convert"],
            *["ESRIJSON:" + query_url, output_file],
            "--overwrite",
            "--lco=COMPRESSION=ZSTD",
        ],
        check=False,
    )


def download_layers(
    url: str,
    extension: str,
    params: dict,
    response: dict,
    regex: dict,
    prefix: str = "",
) -> None:
    """Downloads all GeoJSONs from a Feature Service."""
    for layer in response["layers"]:
        if layer["type"] == "Feature Layer" and search(regex["layer"], layer["name"]):
            feature_url = f"{url}/{layer['id']}"
            response = client_get(feature_url, params).json()
            download_feature(feature_url, extension, params, response, prefix)


def download_services(
    url: str,
    extension: str,
    params: dict,
    response: dict,
    regex: dict,
    prefix: str = "",
) -> None:
    """Downloads all GeoJSONs from Feature Services."""
    for service in response["services"]:
        if service["type"] == "FeatureServer" and search(regex["url"], service["name"]):
            service_name = service["name"].split("/")[-1]
            new_prefix = str(Path(prefix) / service_name)
            layers_url = f"{url}/{service_name}/FeatureServer"
            layers_r = client_get(layers_url, params).json()
            download_layers(layers_url, extension, params, layers_r, regex, new_prefix)
    for folder in response["folders"]:
        service_url = f"{url}/{folder['name']}"
        new_prefix = str(Path(prefix) / folder["name"])
        service_r = client_get(service_url, params).json()
        download_services(service_url, extension, params, service_r, regex, new_prefix)


def main(url: str, token: str, extension: str, regex: dict) -> None:
    """Download all GeoJSONs from the URL provided."""
    params = {"f": "json", "token": token}
    response = client_get(url, params).json()
    if "fields" in response:
        download_feature(url, extension, params, response)
    elif "layers" in response:
        download_layers(url, extension, params, response, regex)
    elif "services" in response:
        download_services(url, extension, params, response, regex)
