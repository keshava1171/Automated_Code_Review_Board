"""
diff_agent.py - Module 1: Diff Agent
Summarizes what the code change does and the files touched using Semantic Kernel & tools.
"""
from typing import Dict, Any
from models import ChangeState
from tools import parse_git_diff, extract_touched_components

class DiffAgent:
    def __init__(self, kernel=None):
        self.kernel = kernel
        self.agent_name = "DiffAgent"

    def review(self, state: ChangeState) -> Dict[str, Any]:
        """
        Executes Tool 1 (parse_git_diff) and Tool 2 (extract_touched_components)
        to extract modified files, line counts, and new classes/functions.
        """
        # Call Tool 1
        diff_info = parse_git_diff(state.raw_diff)
        state.files_touched = diff_info["files"]
        state.log_step(self.agent_name, "parse_git_diff", {
            "files": state.files_touched,
            "added_lines": diff_info["total_added"],
            "removed_lines": diff_info["total_removed"]
        })

        # Call Tool 2
        components = extract_touched_components(diff_info["file_chunks"])
        state.log_step(self.agent_name, "extract_touched_components", {
            "detected_components": components
        })

        # Generate summary
        summary = (
            f"PR touches {len(state.files_touched)} file(s): {', '.join(state.files_touched)}. "
            f"Additions: +{diff_info['total_added']} lines, Deletions: -{diff_info['total_removed']} lines. "
            f"Identified components: {', '.join(components) if components else 'None'}."
        )
        state.summary_of_changes = summary
        return {
            "diff_info": diff_info,
            "components": components,
            "summary": summary
        }
