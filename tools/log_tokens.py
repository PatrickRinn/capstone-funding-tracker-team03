"""Log how many tokens each prompt to Claude Code used.

Claude Code runs this after every answer (a "Stop" hook, set up in
.claude/settings.json). It reads the chat's transcript file, finds the last
prompt you typed, adds up the exact token counts Anthropic sent back for
every reply to it, and adds one row to token_log.md.

Why the input number is big: to answer one prompt, Claude often calls the
API many times (once per tool it uses), and each call re-reads the whole
chat so far. Most of that re-reading is cached, which is cheaper.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "token_log.md"
HEADER = (
    "# Token log\n\n"
    "One row per prompt. Input = everything Claude read (including cached chat history). "
    "Output = everything Claude wrote (including tool calls and thinking).\n\n"
    "| Time | Prompt | API calls | Input tokens | Output tokens | Total tokens |\n"
    "| --- | --- | --- | --- | --- | --- |\n"
)


def is_typed_prompt(entry):
    """True if this transcript line is a prompt a person typed."""
    return entry.get("type") == "user" and entry.get("origin", {}).get("kind") == "human"


def prompt_text(entry):
    """The words the person typed, without editor notes like <ide_opened_file>."""
    content = entry["message"]["content"]
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        text = block.get("text", "")
        if block.get("type") == "text" and not text.startswith("<"):
            parts.append(text)
    return " ".join(parts)


def count_last_prompt(entries):
    """Add up the tokens for the last typed prompt and Claude's answer to it.

    Returns a dict, or None if there is no typed prompt yet.
    """
    last = None
    for i, entry in enumerate(entries):
        if is_typed_prompt(entry):
            last = i
    if last is None:
        return None

    # One API call can be saved as several lines (one per text or tool block),
    # all with the same message id and the same usage. Count each call once.
    usage_by_call = {}
    for entry in entries[last + 1:]:
        message = entry.get("message", {})
        if entry.get("type") == "assistant" and "usage" in message:
            usage_by_call[message["id"]] = message["usage"]

    input_tokens = 0
    output_tokens = 0
    for usage in usage_by_call.values():
        input_tokens += usage.get("input_tokens", 0)
        input_tokens += usage.get("cache_creation_input_tokens", 0)
        input_tokens += usage.get("cache_read_input_tokens", 0)
        output_tokens += usage.get("output_tokens", 0)

    return {
        "prompt": prompt_text(entries[last]),
        "calls": len(usage_by_call),
        "input": input_tokens,
        "output": output_tokens,
        "total": input_tokens + output_tokens,
    }


def table_row(result, when):
    """One Markdown table row. Long prompts are cut to 80 characters."""
    prompt = " ".join(result["prompt"].split()).replace("|", "/")
    if len(prompt) > 80:
        prompt = prompt[:77] + "..."
    return (
        f"| {when:%Y-%m-%d %H:%M} | {prompt} | {result['calls']} "
        f"| {result['input']:,} | {result['output']:,} | {result['total']:,} |\n"
    )


def main():
    hook_input = json.load(sys.stdin)
    with open(hook_input["transcript_path"], encoding="utf-8") as file:
        entries = [json.loads(line) for line in file if line.strip()]

    result = count_last_prompt(entries)
    if result is None:
        return

    if not LOG_FILE.exists():
        LOG_FILE.write_text(HEADER, encoding="utf-8")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(table_row(result, datetime.now()))


if __name__ == "__main__":
    main()
