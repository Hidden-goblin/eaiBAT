from json import load
from pathlib import Path
from dpath.util import merge
from logging import getLogger

log = getLogger(__name__)


# Update the default value in order to match your needs
def build_dataset(base_path: str = "resources/pages"):
    """Build a single dictionary from a collection of json files"""
    try:
        path = Path(base_path)
        merged_json = {}
        for filepath in path.glob("**/*.json"):
            log.debug(f"Processing {filepath}")
            with open(filepath, "r") as file:
                merge(merged_json, load(file))
        return merged_json
    except Exception as exception:
        log.error(exception)
        raise Exception(exception) from exception
