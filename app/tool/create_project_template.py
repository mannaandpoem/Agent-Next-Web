from dataclasses import dataclass
from enum import Enum
from typing import Any, List
import subprocess
import os

from app.tool import BaseTool
from app.tool.show_repo_structure import ShowRepoStructureTool


class TemplateType(Enum):
    MINIMAL = "minimal"
    BASIC = "basic"


class CreateProjectTemplateTool(BaseTool):
    name: str = "create_project_template"
    description: str = "Create a minimal React TypeScript project template with predefined structure"
    parameters: dict = {
        "type": "object",
        "properties": {
            "project_name": {
                "type": "string",
                "description": "Name of your new project",
                "examples": ["my-react-app"]
            },
            "path": {
                "type": "string",
                "description": "Where to create the project (defaults to current directory)",
                "default": ".",
                "examples": ["./projects", "/path/to/workspace"]
            },
            "template_type": {
                "type": "string",
                "enum": ["minimal", "basic"],
                "description": """
                Template structure type:
                - minimal: Bare minimum setup (just src and public)
                - basic: Essential directories for small to medium projects
                """,
                "default": "minimal"
            }
        },
        "required": ["project_name"]
    }

    async def execute(self, **kwargs) -> Any:
        project_name = kwargs.get("project_name")
        path = kwargs.get("path", ".")
        template_type = kwargs.get("template_type", "minimal")

        try:
            # Use create-vite with the minimal template
            create_command = "npm create vite@latest {project_name} -- --template react-ts"
            subprocess.run(create_command.format(project_name=project_name),
                           shell=True, check=True, cwd=path)

            project_path = os.path.join(path, project_name)
            project_path = os.path.abspath(project_path)

            # Define minimal directory structure
            base_dirs = ["src"]

            if template_type == TemplateType.BASIC.value:
                base_dirs.extend([
                    "src/components",
                    "src/styles",
                    "src/utils",
                    "public"
                ])

            # Create directories
            for dir_path in base_dirs:
                os.makedirs(os.path.join(project_path, dir_path), exist_ok=True)

            # # Install additional dependencies
            # subprocess.run('npm install', shell=True, check=True, cwd=project_path)

            # Show created structure
            show_tool = ShowRepoStructureTool()
            structure = await show_tool.execute(path=project_path)

            return f"""
Template Created: {project_name}
Location: {project_path}

Structure:
{structure}

Template Rules:
1. Main entry point is src/main.tsx - DO NOT MODIFY
2. Global styles in src/index.css - DO NOT MODIFY
3. App logic goes in src/App.tsx - MODIFY THIS
4. Create new components in src/components/
5. Modify vite.config.js only if absolutely necessary

Development Flow:
1. cd {project_path}
2. Start by implementing your logic in App.tsx

Note: The application won't run properly unless you maintain the core files structure and entry points. 
You need to write a complete application logic in this template.
"""

        except subprocess.CalledProcessError as e:
            return f"❌ Error creating project template: {str(e)}"
