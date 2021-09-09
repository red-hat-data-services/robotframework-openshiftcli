from typing import Any, Dict, List, Optional, Union

from OpenShiftCLI.outputformatter import OutputFormatter


class PlaintextFormatter(OutputFormatter):
    def format(self,
               output: Union[Dict[str, Any], List[Dict[str, Any]]],
               message: Optional[str] = "",
               type: Optional[str] = None) -> str:
        result = f"{message}:\n\n"
        if isinstance(output, List):
            result += "\n".join(self._format_one(item, type) for item in output)
        else:
            result += self._format_one(output, type)
        return result

    def _format_one(self, item: Dict[str, Any], type: Optional[str] = None) -> str:
        if type == "name":
            return f"{item['metadata']['name']}"
        elif type == "status":
            return (f"Name: {item['metadata']['name']}\n"
                    f"Status: {item['status']['phase']}\n")
        elif type == "wide":
            return (f"Name: {item['metadata']['name']}\n"
                    f"Status: {item['status']['phase']}\n"
                    f"Reason: {item['status']['reason'] if 'reason' in item['status'] else ''}\n"
                    f"Message: {item['status']['message'] if 'message' in item['status'] else ''}\n"
                    f"Conditions: {item['status']['conditions']}\n")
        else:
            return f"{item}"
