<!-- content-revision: 1; source: th -->
# นำไปใช้กับโปรเจกต์เดิม

เริ่มบน branch/worktree แยก บันทึกผลตรวจเดิมก่อนเปลี่ยน อย่าคัดลอก AGENTS.md ทับกฎของโปรเจกต์

สร้าง harness.json ใน root ของโปรเจกต์เอง ใช้ schema จาก examples/typescript/harness.json เปลี่ยน argv เป็นคำสั่ง test/lint/build ที่ใช้อยู่ และ cwd เป็น path ภายในโปรเจกต์ เรียก tools/harness.py จาก checkout ของ harness ด้วย --config /absolute/project/harness.json

Dry-run: ใช้ inspect แล้ว doctor ก่อน check ซึ่งจะรันคำสั่งจริง ไม่ต้องย้ายไฟล์เกมหรือแก้คำสั่งเดิม Rollback: ลบเฉพาะ harness.json ที่เพิ่ม และกลับไปรันคำสั่งเดิม ห้ามลบไฟล์อื่นหรือ cache ของผู้ใช้
