> Historical planning snapshot. Implementation outcome: [release readiness](../release-readiness.md).

# หลักฐานประกอบแผน

วันที่ตรวจ: 2026-11-14 · อ่าน local source; ไม่รับรองสถานะ deployment หรือประสิทธิภาพจาก README

## Snapshot

- Harness: `/Users/khongritjan-in/Downloads/godot-agent-harness` HEAD `0893df46e30af8b08c283d6ad53dd102929f77c4`
- TKR: `/Users/khongritjan-in/Downloads/TKR` HEAD `6152b29435d5231c130901d04ef2a74ef1f99202`
- HMP: `/Users/khongritjan-in/Downloads/HMP` HEAD `0dbfe9acaa749cb9c9c86758c040a017058924f6`
- SPACE8 LABS: `/Users/khongritjan-in/Downloads/space8labs`; project inventory ระบุว่าไม่ใช่ Git repository
- Working files อาจต่างจาก HEAD; หลักฐานนี้อ้างไฟล์ที่อ่านในเครื่อง ไม่ใช่ audit ประวัติ commit

## บทเรียนและสิ่งที่นำมาใช้

| หลักฐาน | สิ่งที่พบ | ผลต่อการออกแบบ |
|---|---|---|
| Harness `tests/run_tests.gd` | ค้น test suites จากไฟล์และเรียงชื่อ | รักษา autodiscovery ไม่เพิ่มจุดแก้ร่วมเพื่อ register tests |
| Harness/HMP `tools/test.sh` | retry import, log cap, summary output | เก็บแนวคิด แต่ต้องตรวจ exit code และ failure lifecycle |
| HMP `tools/test.sh` | เพิ่ม timing ผ่าน PTY; มี blocking read ก่อนตรวจ deadline รอบถัดไป | ใช้ monotonic timeout ที่ไม่ขึ้นกับว่าจะมี output และทดสอบ silent hang; ข้อนี้ยังเป็น static finding |
| TKR `tools/check.sh` | แบ่ง server/story/assets/security/client/e2e; เก็บ PIPESTATUS ของคำสั่ง | generic adapter มีที่มาจากงานหลาย runtime จริง; ไม่ต้องบังคับทุก check เป็น Godot |
| TKR `tools/check.sh` | เปิด server แล้วให้ client จริงทำ smoke flow | contract tests แยกฝั่งไม่แทน integration tests |
| TKR/HMP `tools/lint.sh` | เลือก changed files กับ lint ทั้งหมดได้ | targeted feedback ระหว่างพัฒนาและ full gate ก่อนรวม |
| TKR/HMP `AGENTS.md` | hot files, ownership, contract, screenshot evidence และ seeded logic | ทำเป็น workflow capabilities โดยไม่ยกข้อจำกัดเฉพาะเกมทั้งหมดมาตั้งเป็นกฎสากล |
| Harness `tools/agents/new-worktree.sh` | existing directory ไม่ตรวจ identity; branch อ่านด้วย regex | ต้อง validate ก่อน reuse และใช้ metadata ที่ parse ชัดเจน |
| Harness `tests/test_engine_version.gd` | เทียบ installed minor กับ pinned version prefix | exact-runtime checks แยกจาก minimum engine feature version |
| SPACE8 `src/data/work-projects.ts` | ids มี 3 รายการ, domain มี security/games, counts อยู่ใน strings | เพิ่ม developer-tools ใน data/template/filter และ derive counts |
| SPACE8 `src/templates/HomePage.astro`, `WorkPage.astro` | ใช้ WORK_SHOWCASE ร่วมกัน | ตรวจทั้ง homepage และ work page เมื่อเพิ่ม harness |
| SPACE8 `src/pages/{th,en,zh}` | มีสาม locale อยู่แล้ว | ต่อเว็บเดิม ไม่สร้างเว็บ/ระบบภาษาใหม่ซ้ำ |

## Reproduction: false success ใน harness (ยืนยันด้วยการรัน)

คัดลอกเฉพาะ `tools/test.sh` ไป temp directory และกำหนด GODOT เป็น fake executable:

```sh
#!/bin/sh
case " $* " in
  *" --import "*) exit 23 ;;
  *) printf '1/1 passed\n'; exit 42 ;;
esac
```

| Run | ควรได้ | ได้จริง |
|---|---|---|
| `bash tools/test.sh --import-only` | nonzero เพราะ import exit 23 | exit 0 |
| `bash tools/test.sh` | nonzero เพราะ import/suite ล้มเหลว | exit 0, `1/1 passed, 0 SCRIPT ERROR` |

ตำแหน่ง reproduction:
`/var/folders/y9/66qq2hg14h9dh_ls2yg5q3_c0000gn/T/harness-plan-repro-1ibxuoyn`

สาเหตุจาก source: import ไม่ใช้ exit status; suite pipeline status ถูกทิ้ง และผลสุดท้ายเทียบเฉพาะ passed/total
ไม่มีการแก้เกมหรือรัน Godot จริงในการทดลองนี้ จึงไม่ใช่ baseline ของ Godot suite

## สิ่งที่ยังไม่ยืนยัน

- จำนวน tests ปัจจุบันและ full-suite/lint baseline ทั้งสาม repo
- ผลประหยัดเวลา/token หรือความเหนือกว่าของ agent ใด
- สถานะเว็บที่ deploy จริง, ความพร้อม Windows native, engine อื่น
- เหตุการณ์ย้อนหลัง: comments/กฎยืนยันเจตนาของเครื่องมือ แต่ยังไม่ใช่ raw incident log
- รายละเอียด public case study ต้องแยกข้อเท็จจริงจากข้อมูลในเกมที่ยังไม่เปิดเผย
