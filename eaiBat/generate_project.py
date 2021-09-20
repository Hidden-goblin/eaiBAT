# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import argparse
import pathlib
from os import makedirs
from shutil import copy2


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("destination", help="Where the project must be created")

    args = parser.parse_args()

    destination = pathlib.Path(args.destination)
    base_path = pathlib.Path(__file__).parent.absolute()

    if not destination.exists():
        makedirs(destination)

    # Create project subfolders
    makedirs(destination / "features/steps", exist_ok=True)
    makedirs(destination / "resources", exist_ok=True)
    makedirs(destination / "helpers", exist_ok=True)
    makedirs(destination / "documentation", exist_ok=True)

    # Copy files
    copy2(base_path / "resources/behave.txt", destination / "behave.ini")
    copy2(base_path / "resources/flake8.txt", destination / ".flake8")
    copy2(base_path / "resources/coveragerc.txt", destination / ".coveragerc")
    copy2(base_path / "resources/pytest.txt", destination / "pytest.ini")
    copy2(base_path / "resources/run.py", destination)
    copy2(base_path / "resources/Pipfile.txt", destination / "Pipfile")

    copy2(base_path / "resources/data_manager.py", destination / "helpers")
    copy2(base_path / "resources/data_holder.py", destination / "helpers")
    copy2(base_path / "resources/conversion_utils.txt", destination / "helpers/conversion_utils.py")

    copy2(base_path / "resources/environments.py", destination / "features")
    copy2(base_path / "resources/repository.csv", destination / "features")


if __name__ == '__main__':
    main()
