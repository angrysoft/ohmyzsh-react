#!/usr/bin/python3

from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict, Any
from os import path, mkdir

component_template="""{imports}


{props}
{state}

class {name} extends {component_type}<{name}Props> {{
    render(): ReactNode {{
        return(
            <div></div>
        );
    }}
}}


{exports}
"""

class ReactHelpers:
    def __init__(self, command:AbstractCommand) -> None:
        command.execute()

class AbstractCommand(ABC):
    def __init__(self, args:Namespace) -> None:
        self.args = args

    @abstractmethod
    def execute(self) -> None:
        pass


class CreateComponentCommand(AbstractCommand):
    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self.component_type = "Component"

    def execute(self) -> None:
        _path:str = self.get_argument("path")
        if not path.exists(_path):
            raise FileExistsError("path")
        
        self.path:str = path.join(_path, self.get_argument("name"))
        mkdir(path.join(self.path))
        self.create_style()
        self.create_component()

    def get_argument(self, name:str) -> str:
        result = getattr(self.args, name)
        return result[0]
    
    def create_style(self):
        with open(path.join(self.path, "style.css"), "w") as style_file:
            style_file.write(f'/* Component {self.get_argument("name")} styles */')
    
    def create_component(self):
        with open(path.join(self.path, "index.tsx"), "w") as comp_file:
            _name = self.get_argument("name").title()
            comp_file.write(component_template.format(
                name=_name,
                imports=self.get_imports(),
                props=self.get_props(_name),
                state=self.get_state(_name),
                component_type=self.component_type,
                exports=self.get_exports(_name)))
    
    def get_imports(self):
        return "import {{ {component_type}, ReactNode }} from \"react\";" \
               "\nimport \"./style.css\";".format(component_type=self.component_type)
    
    def get_exports(self, name:str):
        return f"export default {name};"
    
    def get_props(self, name:str):
        return f"type {name}Props = {{}};"
    
    def get_state(self, name:str):
        return ""


class DummyCommand(AbstractCommand):
    
    def execute(self) -> None:
        print("Command not found")


if __name__ == "__main__":
    parser = ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("action", choices=['create_component', 'create_pure_component'])
    parser.add_argument("-p", "--path", type=str, nargs=1, default=['./'], help="Path to component")
    parser.add_argument("-n", "--name", type=str, nargs=1, required=True, help="Name of Component")

    args = parser.parse_args()
    actions:Dict[str, Any] = {
        "create_component": CreateComponentCommand
    }
    app = ReactHelpers(actions.get(args.action, DummyCommand)(args))
