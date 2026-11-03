from datetime import datetime

from tools.log_tokens import count_last_prompt, table_row


def typed(text):
    return {"type": "user", "origin": {"kind": "human"}, "message": {"content": [{"type": "text", "text": text}]}}


def reply(message_id, input_tokens, cache_write, cache_read, output_tokens):
    usage = {
        "input_tokens": input_tokens,
        "cache_creation_input_tokens": cache_write,
        "cache_read_input_tokens": cache_read,
        "output_tokens": output_tokens,
    }
    return {"type": "assistant", "message": {"id": message_id, "usage": usage}}


def tool_result():
    return {"type": "user", "message": {"content": [{"type": "tool_result", "content": "ok"}]}}


def test_counts_only_the_last_prompt():
    entries = [
        typed("first prompt"),
        reply("a", 10, 0, 0, 5),
        typed("second prompt"),
        reply("b", 2, 100, 1000, 50),
        tool_result(),  # Claude used a tool; this is not a new prompt
        reply("c", 3, 20, 1100, 30),
    ]

    result = count_last_prompt(entries)

    assert result["prompt"] == "second prompt"
    assert result["calls"] == 2
    assert result["input"] == (2 + 100 + 1000) + (3 + 20 + 1100)
    assert result["output"] == 50 + 30
    assert result["total"] == result["input"] + result["output"]


def test_one_api_call_saved_on_several_lines_is_counted_once():
    entries = [typed("hi"), reply("same", 1, 2, 3, 4), reply("same", 1, 2, 3, 4)]

    result = count_last_prompt(entries)

    assert result["calls"] == 1
    assert result["total"] == 10


def test_editor_notes_are_left_out_of_the_prompt():
    entry = typed("do task 2")
    entry["message"]["content"].insert(0, {"type": "text", "text": "<ide_opened_file>notes</ide_opened_file>"})

    assert count_last_prompt([entry])["prompt"] == "do task 2"


def test_no_typed_prompt_gives_none():
    assert count_last_prompt([tool_result()]) is None


def test_table_row_formats_numbers_and_cuts_long_prompts():
    result = {"prompt": "x" * 100, "calls": 3, "input": 12345, "output": 678, "total": 13023}

    row = table_row(result, datetime(2026, 11, 3, 14, 5))

    assert row == f"| 2026-11-03 14:05 | {'x' * 77}... | 3 | 12,345 | 678 | 13,023 |\n"
