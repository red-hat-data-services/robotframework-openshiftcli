import json
import yaml

from typing import Any, Dict, List

from OpenShiftCLI.dataparser import JsonParser
from OpenShiftCLI.dataparser import YamlParser


class DataParser(YamlParser, JsonParser):
    def from_json(self, data: str) -> List[Dict[str, Any]]:
        object = json.loads(data)
        if isinstance(object, List):
            return object
        else:
            list = []
            list.append(object.copy())
            return list

    def from_yaml(self, data: str) -> List[Dict[str, Any]]:
        return list(yaml.load_all(data, yaml.SafeLoader))
