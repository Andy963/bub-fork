from __future__ import annotations

from dataclasses import dataclass

import pytest
from republic import ToolContext

import bub.builtin.tools as builtin_tools
from bub.builtin.tools import tape_search


@dataclass(frozen=True)
class _FakeEntry:
    date: str
    payload: object


class _FakeTapes:
    def __init__(self, entries: list[_FakeEntry]) -> None:
        self._entries = entries
        self._store = object()

    async def search(self, _query: object) -> list[_FakeEntry]:
        return list(self._entries)


class _FakeAgent:
    def __init__(self, entries: list[_FakeEntry]) -> None:
        self.tapes = _FakeTapes(entries)


@pytest.mark.asyncio
async def test_tape_search_counts_shown_matches_and_reports_filtered_entries(monkeypatch) -> None:
    entries = [
        _FakeEntry(date="2026-01-01T00:00:00Z", payload={"content": "ok"}),
        _FakeEntry(date="2026-01-01T00:00:01Z", payload={"content": "[tape.search]: 1 matches"}),
    ]
    fake_agent = _FakeAgent(entries)
    monkeypatch.setattr(builtin_tools, "_get_agent", lambda _context: fake_agent)

    context = ToolContext(tape="tape", run_id="run", state={})
    output = await tape_search.run(query="x", context=context)

    first_line = output.splitlines()[0]
    assert first_line == "[tape.search]: 1 matches (1 filtered)"
    assert "[tape.search]:" not in "\n".join(output.splitlines()[1:])


@pytest.mark.asyncio
async def test_tape_search_does_not_show_filtered_suffix_when_nothing_filtered(monkeypatch) -> None:
    entries = [
        _FakeEntry(date="2026-01-01T00:00:00Z", payload={"content": "a"}),
        _FakeEntry(date="2026-01-01T00:00:01Z", payload={"content": "b"}),
    ]
    fake_agent = _FakeAgent(entries)
    monkeypatch.setattr(builtin_tools, "_get_agent", lambda _context: fake_agent)

    context = ToolContext(tape="tape", run_id="run", state={})
    output = await tape_search.run(query="x", context=context)

    assert output.splitlines()[0] == "[tape.search]: 2 matches"
