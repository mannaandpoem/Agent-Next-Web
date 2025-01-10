from typing import List

from pydantic import Field

from app.agent.toolcall import ToolCallAgent
from app.prompt.midwit import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import (
    AttemptCompletionClientRequest,
    ListFiles,
    SearchFile,
    StrReplaceEditor,
    Terminal,
    Tool,
)


class MidwitAgent(ToolCallAgent):
    """An agent that implements the MidwitAgent paradigm for executing code and natural conversations."""

    name: str = "MidwitAgent"
    description: str = "a brilliant and meticulous engineer assigned to help the user with any query they have."

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    tools: List[Tool] = [
        Terminal,
        StrReplaceEditor,
        SearchFile,
        ListFiles,
        AttemptCompletionClientRequest,
    ]
    special_tool_commands: List[str] = Field(
        default_factory=lambda: [AttemptCompletionClientRequest.name]
    )

    max_steps: int = 30
