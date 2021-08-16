import base64
import os
import requests
import validators
import yaml

from typing import Iterator

from robot.api import Error

from OpenShiftCLI.dataloader import DataLoader


class YamlLoader(DataLoader):
    def load(self, path: str) -> Iterator:
        data = None
        if validators.url(path):
            data = self._get_data_from_url(path)
        else:
            data = self._get_data_from_file(path)
        if not data:
            raise Error(f"Data not found in {path}")
        return yaml.load_all(data, yaml.SafeLoader)

    def _get_data_from_url(self, path: str) -> bytes:
        req = requests.get(path, verify=False)
        if req.status_code != requests.codes.ok:
            raise Error(f"Content was not found. Verify url {path} is correct")
        try:
            req = req.json()
        except Error:
            raise Error(f"Error decoding JSON. Verify that the endpoint {path} returns a proper json response.")
        return base64.b64decode(req["content"])

    def _get_data_from_file(self, path: str) -> str:
        cwd = os.getcwd()
        with open(rf'{cwd}/{path}') as file:
            return file.read()
