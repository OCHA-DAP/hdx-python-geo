import argparse
from logging import INFO, basicConfig
from os import getenv

from ..config import DEFAULT_EXTENSION
from . import download
from .utils import generate_token

basicConfig(level=INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Download ESRI data.")
    parser.add_argument(
        "--arcgis-url",
        help="ArcGIS URL, e.g. https://gis.example.org/server/rest/services",
    )
    parser.add_argument("--arcgis-username", help="ArcGIS Username")
    parser.add_argument("--arcgis-password", help="ARCGIS Password")
    parser.add_argument("--output-extension", help="Output Extension")
    parser.add_argument("--regex-url", help="Regex to filter URLs")
    parser.add_argument("--regex-layer", help="Regex to filter layers")

    args = parser.parse_args()
    url = args.arcgis_url if args.arcgis_url else getenv("ARCGIS_URL", "")
    username = (
        args.arcgis_username if args.arcgis_username else getenv("ARCGIS_USERNAME", "")
    )
    password = (
        args.arcgis_password if args.arcgis_password else getenv("ARCGIS_PASSWORD", "")
    )
    extension = (
        args.output_extension
        if args.output_extension
        else getenv("OUTPUT_EXTENSION", "")
        if getenv("OUTPUT_EXTENSION")
        else DEFAULT_EXTENSION
    )
    regex_url = (
        args.regex_url
        if args.regex_url
        else getenv("REGEX_URL", "")
        if getenv("REGEX_URL")
        else ".*"
    )
    regex_layer = (
        args.regex_layer
        if args.regex_layer
        else getenv("REGEX_LAYER", "")
        if getenv("REGEX_LAYER")
        else ".*"
    )
    regex = {"url": regex_url, "layer": regex_layer}

    token = generate_token(url, username, password)
    download.main(url, token, extension, regex)


if __name__ == "__main__":
    main()
