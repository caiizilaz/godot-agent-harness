<!-- content-revision: 1; source: th -->
# บทเรียนจาก TKR และ HMP

TKR ใช้ Godot client กับ TypeScript server ส่วน HMP ใช้ Godot และ headless tests ทั้งสองเป็นงานเกมของ SPACE8 LABS ที่เป็นที่มาของ workflow นี้

บทเรียนที่นำมาใช้: แยก logic ให้ตรวจได้, contract ชัดเจน, ไม่ให้หลายงานแก้ hot files พร้อมกัน, ตรวจภาพจริงเมื่อผลกระทบถึงผู้เล่น และเก็บ log ที่มีขอบเขต

รุ่นนี้แยก process runner ออกจาก Godot และมี generic command adapter ไม่อ้างว่ารองรับ Unity/Unreal แล้ว และยังไม่มีหลักฐานประหยัด token แบบ end-to-end อ่าน benchmarks/protocol.md และ results.json สำหรับข้อจำกัด
