import yaml

from jinja2 import BaseLoader, Environment

from openshiftcli.templateloader import Jinja2Loader


class TemplateLoader(Jinja2Loader):
    def from_jinja2(self, src: str, data: str) -> str:
        template = Environment(loader=BaseLoader()).from_string(src)
        return template.render(yaml.safe_load(data))
