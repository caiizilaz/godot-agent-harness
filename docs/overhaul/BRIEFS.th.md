> Historical planning snapshot. Implementation outcome: [release readiness](../release-readiness.md).

# ร่างชุดงานส่งต่อ integrator

Proposal IDs ด้านล่างยังไม่ใช่ task IDs บนบอร์ด ไม่เริ่ม implementation จน integrator ออก brief จริง
ทุก task ใช้หนึ่ง worktree/branch, บันทึก baseline ก่อนแก้, ไม่ push/merge และส่ง report ไม่เกิน 30 บรรทัด
แต่ละรายการมี proposed ownership; integrator ต้องตรวจชนกับงานที่มีอยู่และล็อก exact file list ก่อนมอบหมาย
เมื่อเกิด shared-file change ให้ integrator ทำตาม integration notes ไม่ให้ worker ขยาย Owns เอง

## P01 — ล็อก contract และขอบเขตรุ่นแรก

**ผู้รับ:** integrator · **Depends:** ไม่มี

**Context:** รองรับหลาย runtime โดยรักษาคำสั่งเดิม และแยก public product intent จากกฎเฉพาะสองเกม

**Do:** นำ PLAN/EVIDENCE เข้า docs ตามตำแหน่งที่ integrator เลือก; ล็อก schema/version semantics;
ออก task IDs และ branches จริง; กำหนด core runtime Python 3.11+ และ optional integrations

**Proposed Owns:** `docs/overhaul/PLAN.th.md`, `docs/overhaul/EVIDENCE.th.md`,
`docs/architecture/adapter-contract.md`, task briefs/board และ agent rules โดย integrator เท่านั้น

**Done when:** required/optional checks, failed/skipped semantics, timeout/process cleanup,
schema field types และ path policy มี contract ตัวอย่าง valid/invalid; ทุก worker มี Owns ไม่ชนกัน

**Out of scope:** เปลี่ยนชื่อผลิตภัณฑ์หรือประกาศรองรับ engine ที่ยังไม่มี fixture

## P02 — ปิดช่อง false success ของ runner

**ผู้รับ:** logic/test implementer · **Depends:** P01

**Context:** reproduction ใน EVIDENCE แสดง exit 0 เมื่อ fake import/suite จบด้วย nonzero

**Do:** เขียน regression test ก่อน; ตรวจ exit code ทุกขั้น, script errors และผล summary;
จัด timeout/log cap ให้หยุด process ที่เกี่ยวข้องและคืน failed; validate configuration limits

**Proposed Owns:** `tools/test.sh`, `tools/tests/test_test_runner.py`, `tools/tests/fixtures/fake_godot.py`
และ report ของ task ที่ integrator กำหนด

**Done when:** fake import exit 23, suite exit 42 หลัง summary, missing executable, silent timeout,
log flood, SCRIPT ERROR หลัง summary, missing summary และ zero-test run ไม่ผ่าน;
happy path ผ่าน; import-only ไม่เรียก suite; test cleanup ไม่เหลือ child process;
Godot suite และ lint ใน worktree ผ่านโดยไม่ลด tests เดิม

**Out of scope:** refactor test discovery, ย้ายฉากเกม, เปลี่ยน runner ให้ใช้ core ใหม่ทั้งชุด

## P03 — core runner และ generic command adapter

**ผู้รับ:** logic/test implementer · **Depends:** P01, P02

**Contract:** ใช้ exact schema จาก P01; เขียน contract tests ก่อน producer

**Proposed Owns:** new `tools/harness/core.py`, `tools/harness/config.py`,
`tools/harness/adapters/command.py`, `tools/tests/test_harness_core.py`,
`tools/tests/test_command_adapter.py`, `tools/tests/fixtures/command_project/` และ task report

**Do:** config inspection, doctor, subprocess argv, monotonic timeout, capped logs,
structured result และ short summary; ไม่มี network/install/paid calls โดยอัตโนมัติ

**Done when:** generic fixture รันได้โดยไม่ติดตั้ง Godot; required skipped ไม่ผ่าน;
invalid schema/path/command ถูกปฏิเสธก่อนรัน; argv มีช่องว่างและ shell metacharacters ถูกส่งตามตัวอักษร;
interrupt/timeout เก็บเหตุผลและ cleanup; logs มีขอบเขตและตรวจ full failure lifecycle

**Integration notes:** integrator เพิ่ม CLI entry point และ CI job; fixture files ต้องแจกแจง exact list ใน brief จริง

## P04 — Godot adapter และ compatibility

**ผู้รับ:** logic/test implementer · **Depends:** P03

**Proposed Owns:** new `tools/harness/adapters/godot.py`, `tools/tests/test_godot_adapter.py`
และ task report

**Do:** import/test/capture operations ตาม P01; ตรวจ exact installed runtime แยกจาก feature minimum;
fixture รองรับ asset import, missing outputs และ engine crashes; capture ต้องตรวจ artifact ของ run นี้

**Done when:** headless suite จริงผ่าน; fake failures จาก P02 ยังไม่ผ่าน;
capture ที่ไม่มี display เป็น skipped พร้อมเหตุผลและไม่ผ่าน required visual gate;
ภาพใหม่มีหลักฐาน inspection ไม่ใช้ไฟล์เก่ามาสวมว่าจับภาพสำเร็จ

**Integration notes:** integrator เปลี่ยน `tools/test.sh`, `tools/shot.sh`, version checks และ CI ให้เรียก core;
คง invocation/exit semantics เดิมที่ถูกต้อง; ไม่แก้ P02 พร้อมกัน

## P05 — workflow, worktree และ agent profiles

**ผู้รับ:** logic/test implementer + integrator สำหรับ shared rules · **Depends:** P01, P03

**Proposed Owns:** `tools/agents/new-worktree.sh`, new `tools/tests/test_worktree.py`,
`docs/workflows/solo.th.md`, `docs/workflows/team.th.md` และ task report

**Do:** ตรวจ task id, branch, repository identity และ destination ก่อน reuse;
รองรับการเริ่มซ้ำหลัง interrupted setup; ให้การ fetch/network เป็นพฤติกรรมชัดเจนและมี offline path

**Done when:** temporary Git repos ทดสอบ correct/wrong worktree, dirty/untracked preservation,
path มีช่องว่าง, invalid brief, conflicting ownership และ dependency mismatch;
ไม่ mutate hooks/config ก่อน preconditions ผ่าน; คนใช้ agent เดียวทำ flow จบโดยไม่เปิดหลาย agents

**Integration notes:** integrator จัด canonical rules/profile pointers, templates และ board validation;
capability checklist ใช้ชื่อบทบาท ไม่ล็อกผู้ให้บริการ; generated instructions ไม่เขียนทับของผู้ใช้เงียบ ๆ

## P06 — ตัวอย่างข้าม runtime และคู่มือสามภาษา

**ผู้รับ:** implementer สำหรับ examples; documentation/localization reviewer สำหรับ copy · **Depends:** P04, P05

**Proposed Owns:** new `examples/typescript/`, `docs/quickstart/{th,en,zh-Hans}.md`,
`docs/migration/{th,en,zh-Hans}.md`, `docs/troubleshooting/{th,en,zh-Hans}.md`,
`tools/docs/check_locales.py` และ task report

**Do:** ตัวอย่าง deterministic logic + contract; ปรับตัวอย่าง Godot ผ่านงานแยกหากต้องแก้ hot files;
สามเส้นทาง onboarding มือใหม่/solo/team; command snippets แหล่งเดียว;
เพิ่ม version/revision markers ให้ตรวจคำแปลล้าสมัยได้

**Done when:** clean fixture ทำงานแรกจบได้ทั้ง Godot และ TypeScript;
ทุกภาษามี setup, run, expected result, failure recovery; locale check ผ่าน;
existing-project migration dry-run ไม่แก้เกม; rollback ผ่าน; ไม่คัดลอก asset/เนื้อหา IP ส่วนตัว

**Integration notes:** exact example file list และ supported runtime versions ต้องล็อกก่อนเริ่ม;
README/CI updates โดย integrator; ภาพที่แก้ต้องมี screenshot และ inspection

## P07 — เพิ่มผลงาน harness ในเว็บ SPACE8 LABS

**ผู้รับ:** web/content implementer ตามกฎ repo เว็บ · **Depends:** P01; final claims รอ P06/P08

**Proposed Owns:** `src/data/work-projects.ts`, `src/templates/WorkPage.astro`,
`src/templates/HomePage.astro`, `src/scripts/site-ui.ts`, new localized case-study routes,
`scripts/verify-build.mjs` และหลักฐาน QA ตามกฎเว็บ

**Do:** เพิ่ม developer-tools domain และ derive filter counts; เพิ่ม harness item ทั้งสาม locale;
เชื่อม case study ไป TKR/HMP/repo; metadata และ alternate links ตาม pattern เว็บเดิม

**Done when:** item/filters/counts และ link targets ถูกต้องทั้งสามภาษา;
keyboard, mobile reflow, themes และ locale switching ผ่าน;
`npm run build`, `npm test` และ browser QA ผ่าน;
ไม่มี fabricated metrics/engine support และไม่มี placeholder ภายในใน public output

**Integration notes:** repo เว็บใน inventory ไม่ใช่ Git repository จึงตรวจวิธีจัด version/workspace ก่อนแก้;
asset ใหม่ใช้ original editable vectors และ provenance ตามกฎเว็บ;
เตรียม local preview ให้ตรวจรับก่อน release ตาม policy ของ repo; task นี้ไม่รวม deploy

## P08 — pilot และ release evidence

**ผู้รับ:** verifier/documentation · **Depends:** P06, P07

**Proposed Owns:** new `benchmarks/protocol.md`, `benchmarks/results.json`,
`docs/case-studies/tkr-hmp.{th,en,zh-Hans}.md`, `docs/release-readiness.md` และ task report

**Do:** รัน pilot ตาม PLAN บนสำเนา fixture; เปรียบเทียบ workflow เดิม/ใหม่;
จัด publishable evidence โดยไม่เผย raw private game logs; ตรวจข้อมูลตาม locale

**Done when:** บันทึก failed runs, setup cost, review/handoff cost, model/environment และ missing tokens;
ไม่มี acceptance regression; capability matrix แยก verified/experimental/planned;
case study ทุก claim มีแหล่งหลักฐาน; migration และ rollback มีผลตรวจจริง

**Out of scope:** ใช้เงินกับ paid eval โดยไม่ได้รับอนุญาต หรือเปลี่ยนชื่อ/เผยแพร่ production อัตโนมัติ

## การส่งต่อครั้งแรก

Integrator นำ P01 เข้า repo แล้วออก brief จริงสำหรับ P02 ก่อน
P02 ไม่ต้องรอการตัดสินใจชื่อใหม่หรือ engine ตัวที่สาม
แผนนี้ไม่แตะ board และไม่มอบหมายงานให้ agents อื่นโดยอัตโนมัติ
