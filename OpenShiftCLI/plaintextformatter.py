from .outputformatter import OutputFormatter
from typing import List


class PlaintextFormatter(OutputFormatter):
    def format(self, message: str, objects: List, type: str) -> str:
        if type == "name":
            return message + "\n".join(f"{object.metadata.name}" for object in objects)
        elif type == "status":
            return "\n".join(f"{message}:\n"
                             f"Name: {object.metadata.name}\n"
                             f"Status: {object.status.phase}" for object in objects)
        elif type == "wide":
            return "\n".join(f"{message}:\n"
                             f"Name: {object.metadata.name}\n"
                             f"Status: {object.status.phase}\n"
                             f"Reason: {object.status.reason}\n"
                             f"Message: {object.status.message}\n"
                             f"Conditions: {object.status.conditions}\n" for object in objects)
