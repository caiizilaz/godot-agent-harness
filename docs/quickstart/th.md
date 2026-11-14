<!-- content-revision: 1; source: th -->
# เริ่มใช้ harness ของ SPACE8 LABS

ต้องมี Python 3.11+, Git, Godot ตาม tools/ci/godot-version.txt และ Node 22.18+ สำหรับตัวอย่าง TypeScript บน macOS/Linux; Windows ใช้ WSL ส่วน native ยังไม่ยืนยัน

รันจาก root ของ repo ตัวอย่างเต็มควรผ่าน Godot 6/6, TypeScript 3 tests และ tooling checks ตามผลปัจจุบัน คำสั่ง doctor ตรวจว่ามี executable แต่ไม่รันคำสั่งใน config ตรวจผล JSON ที่ path Evidence ทุกครั้ง

มือใหม่: เริ่มตัวอย่าง score แล้วเปลี่ยนกฎพร้อมเทสต์หนึ่งข้อ · Solo: ใช้ brief สั้นและ worktree ไม่ต้องเปิดหลาย agents · ทีม: ระบุ Owns/dependencies และให้ integrator รวมงาน hot files

```sh
python3 tools/harness.py inspect
python3 tools/harness.py doctor
python3 tools/harness.py check
# Generic example, no Godot required:
python3 tools/harness.py --config examples/typescript/harness.json check
# Existing compatibility entry points:
tools/test.sh test_score
tools/shot.sh main shots/main.png
```
