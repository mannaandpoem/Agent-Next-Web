from dataclasses import dataclass
from enum import Enum
from typing import Any, List
import subprocess
import os

from app.tool import BaseTool


class TemplateType(Enum):
    MINIMAL = "minimal"
    FULL = "full"


@dataclass
class DirectoryStructure:
    name: str
    description: str
    children: List[str] = None


class GetRepoTemplateTool(BaseTool):
    name: str = "get_repo_template"
    description: str = "Create a new Vite + React + TypeScript project with predefined structure"
    parameters: dict = {
        "type": "object",
        "properties": {
            "project_name": {
                "type": "string",
                "description": "Name of the project directory"
            },
            "path": {
                "type": "string",
                "description": "Path where to create the project"
            },
            "template_type": {
                "type": "string",
                "enum": ["minimal", "full"],
                "description": "Type of template structure to create"
            }
        },
        "required": ["project_name"]
    }

    def _get_base_structure(self) -> List[DirectoryStructure]:
        return [
            DirectoryStructure("src", "Source code directory", [
                "assets",
                "components",
                "hooks",
                "pages",
                "services",
                "store",
                "styles",
                "types",
                "utils"
            ]),
            DirectoryStructure("public", "Public assets directory"),
        ]

    def _get_full_structure(self) -> List[DirectoryStructure]:
        base = self._get_base_structure()
        base.extend([
            DirectoryStructure("src/layouts", "Layout components"),
            DirectoryStructure("src/constants", "Application constants"),
            DirectoryStructure("src/contexts", "React contexts"),
            DirectoryStructure("src/features", "Feature-based modules"),
            DirectoryStructure("src/i18n", "Internationalization"),
            DirectoryStructure("src/middlewares", "Redux middlewares"),
            DirectoryStructure("tests", "Test files"),
            DirectoryStructure("docs", "Documentation"),
        ])
        return base

    def _create_directory_structure(self, base_path: str, structure: List[DirectoryStructure]):
        for item in structure:
            dir_path = os.path.join(base_path, item.name)
            os.makedirs(dir_path, exist_ok=True)

            # Create index files for directories
            if item.children:
                with open(os.path.join(dir_path, 'index.ts'), 'w') as f:
                    f.write('// Export components from this directory\n')

                # Create directories for children
                for child in item.children:
                    child_path = os.path.join(dir_path, child)
                    os.makedirs(child_path, exist_ok=True)
                    with open(os.path.join(child_path, 'index.ts'), 'w') as f:
                        f.write('// Export components from this directory\n')

    async def execute(self, **kwargs) -> Any:
        project_name = kwargs.get("project_name")
        path = kwargs.get("path", ".")
        template_type = kwargs.get("template_type", "minimal")

        try:
            # Create project using Vite
            create_command = f"npm create vite@latest {project_name} -- --template react-ts"
            subprocess.run(create_command, shell=True, check=True, cwd=path)

            project_path = os.path.join(path, project_name)

            # Create directory structure
            structure = (
                self._get_full_structure()
                if template_type == TemplateType.FULL.value
                else self._get_base_structure()
            )
            self._create_directory_structure(project_path, structure)

            return f"Successfully created project: {project_name}\nPath: {project_path}\nProject structure: {structure}"

        except subprocess.CalledProcessError as e:
            return f"Error creating template: {str(e)}"
