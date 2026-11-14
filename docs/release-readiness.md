# Local release readiness — 2026-11-14

## Delivered

- P01: owner-authorized umbrella brief, preserved plan/evidence and strict adapter schema v1.
- P02: no false success from failed imports, nonzero suite exits or SCRIPT ERROR after summary.
- P03: bounded POSIX process runner, literal argv, strict configuration, read-only inspect/doctor, generic adapter.
- P04: exact Godot version, import output checks, test summary checks, fresh capture, compatibility wrappers.
- P05: worktree identity/base validation, preserved dirty files, optional dependency/ownership validator, portable roles.
- P06: deterministic TypeScript example; four documentation topics in Thai/English/zh-Hans, parity checks, adoption/rollback test.
- P07: 13 website source/evidence files applied to SPACE8 LABS after preimage validation; three case-study routes and developer-tools filter.
- P08: reproducible tool-correctness pilot and published protocol/results. End-to-end agent productivity measurements remain unavailable (see limits).

## Observed checks

| Check | Result |
|---|---|
| Existing baseline | Godot 6/6; lint passed |
| Final Godot suite | 9/9 after integrating main 10cbf2c |
| Python tooling suite | 32/32 |
| TypeScript rule suite | 3/3 |
| Pinned GDScript lint | passed |
| Localization | 4 topics × 3 locales; revisions/snippets agree |
| Native capture | fresh PNG produced and visually inspected; centered title and combo x1.4 |
| Tool pilot | before 3/9 accepted; after 9/9 accepted; synthetic failure cases |
| Website original checkout | Astro build + static verification passed; 38 pages |
| Website browser | 42/42 responsive/theme/filter checks; keyboard activation; reduced-motion canvas unpainted |
| Visual evidence | Thai desktop and Thai/Chinese mobile inspected; sample lead contrast ≥9.29:1 |

Final harness check evidence originally written to `/var/folders/y9/66qq2hg14h9dh_ls2yg5q3_c0000gn/T/space8-harness-58365a8a/`.
Portable summaries are in this document, benchmark JSON and website-patch/files/docs/qa-evidence/harness/browser-results.json.
Godot screenshot: `shots/CX-OVERHAUL.png` (not committed). Additional screenshots are local task artifacts.

## Limits and remaining external work

- No push, shared-branch merge, external preview or production deployment was performed.
- Linux/macOS CI jobs are configured; no remote Actions run is claimed. Local verification was on macOS.
- Native Windows and Unity/Unreal adapters are not implemented or advertised. WSL is the documented Windows route.
- The pilot validates runner correctness/overhead only. It uses a fake executable and cannot demonstrate agent token savings.
- Input/output tokens and human effort are null, not zero. No cross-model paid benchmark was authorized or run.
- Translation parity is automated; professional native-language editorial review is not claimed.
- Browser checks cover the changed pages, not a fresh full-site accessibility certification.
- Existing site styles changed concurrently; those changes were retained and the merged result rebuilt/rechecked.

## Review / rollback

Review the local branch and report before integration. Keep the original shell commands available via wrappers.
For an adopted project, remove only its added harness.json to return to its original commands.
The website patch is idempotent and rejects changed preimages. Prior website source files were backed up locally
under `/var/folders/y9/66qq2hg14h9dh_ls2yg5q3_c0000gn/T/space8-site-backup-rnpzud_6`.

## Integration preflight

Latest upstream main `10cbf2c` has been integrated locally. Its tower-defense kickoff,
board/briefs, decisions and three repository-document checks were preserved. README conflicts
were resolved without dropping the reusable-harness positioning. Full checks passed again:
Godot 9/9, tooling 32/32, TypeScript 3/3, pinned lint and locale parity.
Publication remains a separate action under the repository and website release instructions.
