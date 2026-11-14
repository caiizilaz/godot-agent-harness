> Historical planning snapshot. Implementation outcome: [release readiness](../release-readiness.md).

# SPACE8 LABS — แผน overhaul harness

วันที่ 14 พฤศจิกายน 2026 · สถานะ: แผนส่งต่อสำหรับ integrator ยังไม่ใช่ implementation

## เป้าหมายที่ผู้ใช้ยืนยัน

- Harness ใช้ได้กับหลายเกม; เกมใน repo เป็นตัวอย่างเท่านั้น
- เผยแพร่บทเรียนจาก TKR (ลิขิตสามก๊ก) และ HMP (KLAP CHAT: Reroll Protocol) ในนาม SPACE8 LABS
- ช่วยให้งานดีขึ้น ลดเวลาและ token พร้อมเชื่อมให้คนรู้จักสองเกม
- รองรับมือใหม่ นักพัฒนา solo และทีมเล็กผ่าน workflow เดียวที่เปิดรายละเอียดตามระดับ
- ไทยเป็นภาษาหลัก มีอังกฤษและจีนตัวย่อ; รองรับการขยายออกจาก Godot
- บทบาท agents ปรับตามความสามารถและเครื่องมือที่มี ไม่ผูกกับผู้ให้บริการถาวร

## ขอบเขตรุ่นแรกที่เสนอ

ทำแกนกลางพร้อม Godot adapter และ generic command adapter ที่ทดลองกับ Node/TypeScript ได้จริง
ยังไม่ประกาศรองรับ Unity/Unreal จนมี fixture และการตรวจครบวงจรบนเครื่องที่ติดตั้ง engine นั้น
เก็บชื่อ repository เดิมระหว่าง migration; ไม่ตั้งชื่อแบรนด์ผลิตภัณฑ์ใหม่โดยพลการ
ไม่มี hosted orchestration, dashboard, marketplace หรือการเรียก paid API ในรุ่นแรก
เครื่องมือในเครื่องยังใช้ได้โดยไม่ผูกบัญชี AI; gstack และเครื่องมือเสริมเป็น optional integration

## หลักฐานและข้อจำกัด

ดู EVIDENCE.th.md สำหรับแหล่งข้อมูลและ reproduction
อ่านโค้ดเครื่องมือและกฎของโปรเจกต์โดยตรง ไม่เปิดบอร์ด งานที่ได้รับมอบหมายให้คนอื่น หรือรายงาน archive
ยังไม่มี baseline เกมจริงหรือผล benchmark token; ตัวเลขใน README เดิมไม่ใช่ผลตรวจปัจจุบัน
ทดสอบ runner ด้วย fake executable ใน temp directory พบ false success สองกรณี

## สถาปัตยกรรมที่เสนอ

1. Core: อ่าน configuration, ตรวจ tool readiness, รัน subprocess, จำกัดเวลา/log, เก็บผลตรวจ
2. Workflow: brief, ownership, dependency, worktree, handoff, integration evidence
3. Adapters: Godot import/test/capture; generic commands สำหรับ test/lint/build ของ stack อื่น
4. Agent profiles: ความสามารถที่ต้องมี เครื่องมือที่ต้องใช้ และหลักฐานส่งมอบ ไม่บังคับชื่อ model
5. Examples: Godot ขนาดเล็กและ TypeScript deterministic logic ที่ไม่คัดลอก IP เกม
6. Docs/site: เอกสารภาษาไทยและคำแปล; case studies และหน้า portfolio บนเว็บเดิม

เสนอใช้ Python 3.11+ standard library สำหรับ core เพราะ repo ใช้ Python อยู่แล้ว และลด dependency install
คง shell entry points เดิมเป็น compatibility wrappers ในช่วง migration
generic adapter รับ executable และ argv เป็น array ไม่ส่ง command string เข้า shell โดยปริยาย
configuration ถือเป็นโค้ดที่เจ้าของ repo เชื่อถือ: การ inspect/doctor ต้องไม่รันคำสั่งใน config
ทุก task path ต้องอยู่ใต้ project root; ปฏิเสธ path traversal และ symlink ที่ออกนอกขอบเขต ownership

### Contract สำหรับ adapter (ข้อเสนอให้ล็อกในงานแรก)

- ระบุ schema_version, adapter id, project root และ capabilities ที่รองรับ
- operation รับ root, argv, timeout, log budget และ artifact directory
- ผลมี status: passed/failed/skipped, exit code หรือ null, reason, duration, log/artifact paths
- missing tool, timeout, log cap, signal, parse failure และ error หลัง summary ต้องเป็น failed
- skipped ต้องมีเหตุผล และไม่ทำให้ required check ผ่าน
- จำนวน test ที่อ่านไม่ได้ให้เป็น null; ห้ามรายงานเป็น 0 หรืออ้างว่าผ่านทั้งหมด
- ใช้ monotonic clock สำหรับ timeout; wall-clock ใช้ได้เฉพาะ metadata ไม่ใช่ผลเทสต์ deterministic
- รุ่น schema ที่ไม่รู้จักต้องปฏิเสธอย่างชัดเจน

### Workflow และการเลือก agents

Owner ระบุผลลัพธ์ → planner เขียน brief → implementer ทำใน worktree → ตรวจหลักฐาน → integrator รวมงาน
หนึ่ง agent รับหลายบทบาทได้; solo ไม่ต้องสร้างบอร์ดและรายงานซ้ำซ้อนกับทุกการแก้เล็กน้อย
ทีมเปิดใช้ ownership/dependency checks และให้ integrator คนเดียวดูแล hot files
ค่าเริ่มต้นแนะนำจากบทเรียนเดิม: logic ใช้ผู้ทำ contract tests ได้; visual ใช้ผู้ตรวจภาพได้;
integration ใช้ผู้เข้าใจ diff, dependency และตรวจครบระบบได้ ไม่อ้างว่า model ใดเก่งที่สุดถาวร
ใช้หลาย agents เมื่อขอบเขตแยกกันจริงและประหยัดกว่าต้นทุนอ่านบริบท/ส่งต่องาน

### การลด token โดยไม่ลดคุณภาพ

- brief มีเฉพาะเป้าหมาย, source pointers, contract, Owns, acceptance และ dependencies
- canonical rules แหล่งเดียว; profile อ้างอิงแทนการคัดลอกกฎทั้งชุด
- doctor และ check แสดงสรุปสั้น พร้อม path ของ log; เปิดรายละเอียดเมื่อจำเป็น
- targeted checks ระหว่างแก้; full required checks ก่อน integration
- เก็บ baseline ตาม revision/environment; ไม่ใช้ผลเก่ากับ diff ที่เปลี่ยนแล้ว
- จำกัดขอบเขต automated retries และรายงานเหตุผลเมื่อหยุด

## ลำดับส่งมอบ

| ชุด | งาน | ขึ้นกับ | Gate |
|---|---|---|---|
| A | ล็อก scope/contract และนำแผนเข้า repo โดย integrator | ไม่มี | ownership และ branch ของทุกงานชัด |
| B | ซ่อม runner และเพิ่ม regression fixtures | A | กรณี failure ไม่คืน success |
| C | core runner + generic adapter | B | fixture รันได้โดยไม่ติดตั้ง Godot |
| D | Godot adapter + wrappers | C | ตัวอย่างเดิมยังทดสอบและจับภาพได้ |
| E | workflow/profile/worktree validation | A, C | solo และ team task เดินจบได้ |
| F | ตัวอย่าง + docs ไทย/อังกฤษ/จีน | D, E | clean setup ทำตัวอย่างแรกจบได้ |
| G | portfolio/case study SPACE8 LABS | A; ใช้ผล F ประกอบ final copy | สามภาษา/filters/links/QA ผ่าน |
| H | pilot, benchmark และ migration rehearsal | F, G | หลักฐานพร้อมเผยแพร่โดยไม่มีคำกล่าวอ้างเกินผล |

ทำ B ก่อน refactor ใหญ่ เพื่อให้เครื่องมือตรวจงานน่าเชื่อถือ จากนั้นทำ C/D ทีละชั้น
F และ G เตรียมโครงเนื้อหาได้ระหว่างพัฒนา แต่ระบุ capabilities ตามสิ่งที่ผ่าน gate แล้วเท่านั้น

## Verification และ migration

- ก่อนแก้โค้ด: บันทึก revision, engine/runtime, test count และ lint result ใน worktree งานนั้น
- Regression: import nonzero, suite nonzero หลังข้อความผ่าน, timeout แบบเงียบ, log flood,
  child process ค้าง, runtime error หลัง summary, zero tests, missing binary, malformed config
- Worktree: existing correct checkout, wrong repo/branch, stale base, dirty files, path มีช่องว่าง,
  invalid task id, offline mode และ retry หลังสร้างไม่สำเร็จ
- Adapters: generic fixture ไม่ต้องใช้ Godot; Godot fixture ตรวจ import/test/capture จริง
- CI เริ่มจาก macOS/Linux; Windows native เป็นสถานะยังไม่ยืนยันจนมี job จริง ส่วน WSL ระบุแยก
- เก็บ shell commands เดิมไว้จนเอกสาร migration และ integration checks ผ่าน
- ใช้ additive migration; ไม่ย้ายฉาก/asset หรือโฟลเดอร์เกมทั้งหมดพร้อม refactor core
- ทดสอบ adoption บนสำเนาโปรเจกต์: dry-run แสดง diff, ไม่เขียนทับ config/กฎเดิมเงียบ ๆ
- Rollback: ปิด config ใหม่และกลับ wrapper version เดิมได้; ไม่ต้องเปลี่ยนเกมเพื่อถอน harness

## ภาษาและเว็บ SPACE8 LABS

ไทยเป็น canonical editorial source; English และ zh-Hans ใช้ content ids/command examples ชุดเดียวกัน
แยก public localization ออกจาก machine-readable schema; config keys และ identifiers เป็นอังกฤษ
เพิ่ม locale parity check และ translation revision เพื่อจับข้อความที่ตามหลังต้นฉบับ
ใช้เว็บ Astro เดิม: เพิ่ม work item, developer-tools category, filter และ case study สามภาษา
จำนวนรายการใน filters คำนวณจากข้อมูล ไม่เพิ่ม hardcoded 4 ทับ hardcoded 3
ตรวจ homepage ซึ่งใช้ข้อมูลผลงานชุดเดียวกัน รวมทั้ง metadata, alternate links และ sitemap
Case study: ปัญหาจากเกม → วิธีทำงาน → ตัวอย่างหลักฐาน → ข้อจำกัด → ทดลอง harness → รู้จักสองเกม
ตัวอย่างและภาพต้องเป็นสิ่งที่นำมาเผยแพร่ได้; ไม่คัดลอกเนื้อหาเกมส่วนตัวทั้งหมดเข้า open-source repo
ไม่ใส่เปอร์เซ็นต์ประหยัด token หรือสถานะ engine support ที่ยังไม่ผ่านการทดลอง
ชื่อผลิตภัณฑ์ใช้ชื่อเดิมพร้อม SPACE8 LABS attribution จนมีการตัดสินใจเรื่องชื่อใหม่

## Benchmark ที่เสนอ (ยังไม่ได้รัน)

ใช้สามประเภทงาน: เปลี่ยนกฎ deterministic, แก้ bug import/runtime, ทำงานข้าม client/server contract
เปรียบเทียบ workflow เดิมกับใหม่บน revision เริ่มต้นเดียวกัน ใช้ acceptance tests ชุดเดียวกัน
ทำอย่างน้อยสาม repetitions ต่อประเภท/วิธี สลับลำดับวิธี ใช้ session ใหม่และบันทึก cache state
คง agent/model/settings เท่ากันในคู่เปรียบเทียบ; หากเปลี่ยนให้แยกชุดผล
รายงาน median/range, completion rate, regression, รอบแก้, เวลาคน และ wall time
เก็บ input/output/cached tokens เมื่อ provider เปิดเผย; missing เป็น null ไม่ประมาณว่าเท่ากับศูนย์
แยกเวลา setup ครั้งแรกออกจากงานถัดไป; รวม failed runs และต้นทุน handoff/review ในรายงาน
รุ่นใหม่ต้องไม่ลด acceptance quality หรือมี unhandled regression จึงจะพิจารณาผลด้านต้นทุน
ไม่ตั้งเป้าลดเป็นเปอร์เซ็นต์ก่อนเห็น baseline; ใช้ผลทดลองเล็กเป็น pilot ไม่อ้าง general superiority

## ขอบเขตการตัดสินใจและการส่งต่อ

แผนนี้ไม่แก้กฎปัจจุบันใน AGENTS.md โดยอัตโนมัติ
integrator ต้องรับผิดชอบ shared files/board และออก task IDs จริงตามพื้นที่ว่างในบอร์ด
BRIEFS.th.md ใช้ proposal IDs เพื่อไม่ชนกับงานที่ยังไม่อ่าน; ไม่ใช่งาน ready ที่สั่ง agents ได้ทันที
ก่อนลงมือแต่ละ task ให้ materialize brief พร้อม exact Owns และ branch ใน repo ที่เกี่ยวข้อง
งานเว็บยังต้องเตรียมและตรวจ local result ก่อนขั้นเผยแพร่; รอบนี้ไม่มี external release
ชื่อใหม่และ engine ตัวที่สามยังเปิดไว้ แต่ไม่ขวาง B–F
