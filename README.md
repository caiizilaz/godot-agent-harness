# Godot Agent Harness · SPACE8 LABS

Workflow จากบทเรียนการสร้าง **TKR — ลิขิตสามก๊ก** และ **HMP — KLAP CHAT: Reroll Protocol**:
แบ่งขอบเขตงาน ตรวจผลจริง และส่งต่อหลักฐาน โดยเริ่มจาก Godot และขยายผ่าน generic commands
ตัวเกมใน repo เป็นตัวอย่าง ไม่ใช่ source ของสองเกม

[เริ่มต้นภาษาไทย](docs/quickstart/th.md) · [English](docs/quickstart/en.md) · [简体中文](docs/quickstart/zh-Hans.md)

```sh
python3 tools/harness.py doctor
python3 tools/harness.py check
# Example without Godot:
python3 tools/harness.py --config examples/typescript/harness.json check
```

Python 3.11+, Git, pinned Godot (`tools/ci/godot-version.txt`), Node 22.18+ for the TypeScript example.
macOS is checked locally; Linux is covered by configured CI, not a claim of a completed remote run.
Windows: use WSL; native Windows is not supported by the POSIX runner.

| Use | Start here |
|---|---|
| First project | [Quickstart](docs/quickstart/th.md) |
| One developer/agent | [Solo workflow](docs/workflows/solo.th.md) |
| Small team | [Team workflow](docs/workflows/team.th.md) |
| Existing game | [Migration and rollback](docs/migration/th.md) |
| Different engine/runtime | [Adapter contract](docs/architecture/adapter-contract.md) |
| Something failed | [Troubleshooting](docs/troubleshooting/th.md) |

Core bounds process lifetime/logs and preserves failure status. The Godot adapter checks imports,
exact versions, test summaries and fresh captures. The generic adapter runs literal argv without a shell.
No AI subscription, cloud service, gstack install or plugin framework is required.
Agent roles follow capabilities, not provider names; one agent can hold multiple roles.

`tools/test.sh`, `tools/test.sh test_score`, and `tools/shot.sh main shots/main.png` remain supported.
`tools/agents/new-worktree.sh TASK-ID --offline` validates checkout identity before reuse.
`--skip-import` permits generic projects. Dirty files are preserved; hooks are not silently changed.

[Lessons from TKR/HMP](docs/case-studies/th.md) · [Measurement protocol](benchmarks/protocol.md) ·
[Release evidence and limits](docs/release-readiness.md)

Token/time savings are goals, not established percentages. Unity/Unreal adapters are not shipped.
MIT; engine reference attribution remains in `docs/engine-reference/godot/`.
