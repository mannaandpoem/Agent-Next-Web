from typing import List

from pydantic import Field

from app.agent.toolcall import ToolCallAgent
from app.prompt.swe import NEXT_STEP_TEMPLATE, SYSTEM_PROMPT
from app.tool import Bash, Finish, StrReplaceEditor, ToolCollection


class SWEAgent(ToolCallAgent):
    """An agent that implements the SWEAgent paradigm for executing code and natural conversations."""

    name: str = "SWEAgent"
    description: str = "an autonomous AI programmer that interacts directly with the computer to solve tasks."

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_TEMPLATE

    tool_collection: ToolCollection = ToolCollection(
        Bash(), StrReplaceEditor(), Finish()
    )
    special_tools: List[str] = Field(
        default_factory=lambda: [Finish.get_name().lower()]
    )

    max_steps: int = 30

    bash: Bash = Field(default_factory=Bash)
    working_dir: str = "."

    async def think(self) -> bool:
        """Process current state and decide next action"""
        # Update working directory
        self.working_dir = await self.bash.execute("pwd")
        self.next_step_prompt = self.next_step_prompt.format(
            current_dir=self.working_dir
        )

        return await super().think()
