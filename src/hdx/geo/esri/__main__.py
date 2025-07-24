import argparse
from logging import INFO, basicConfig
from os import getenv

from . import download
from .config import DEFAULT_EXTENSION
from .utils import generate_token

basicConfig(level=INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Download ESRI data.")
    parser.add_argument(
        "--url",
        help="ArcGIS URL, e.g. https://gis.example.org/server/rest/services",
    )
    parser.add_argument("--username", help="ArcGIS Username")
    parser.add_argument("--password", help="ARCGIS Password")
    parser.add_argument("--extension", help="Output Extension")
    parser.add_argument("--regex-url", help="Regex to filter URLs")
    parser.add_argument("--regex-layer", help="Regex to filter layers")

    args = parser.parse_args()
    url = args.url if args.url else getenv("URL", "")
    username = args.username if args.username else getenv("USERNAME", "")
    password = args.password if args.password else getenv("PASSWORD", "")
    extension = (
        args.extension
        if args.extension
        else getenv("EXTENSION", "")
        if getenv("EXTENSION")
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
