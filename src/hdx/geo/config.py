from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

OBJECTID = "esriFieldTypeOID"
DEFAULT_EXTENSION = ".parquet"

ATTEMPT = int(getenv("ATTEMPT", "5"))
TIMEOUT = int(getenv("TIMEOUT", "60"))
WAIT = int(getenv("WAIT", "10"))

cwd = Path(__file__).parent
data_dir = cwd / "../../../data"
data_dir.mkdir(parents=True, exist_ok=True)
