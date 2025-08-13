# Flask Blog (MySQL/SQLite + SQLAlchemy) — Cover & Inline Image Uploads

ฟีเจอร์:
- สมัคร/เข้าสู่ระบบ (Flask-Login, password hash)
- โพสต์บล็อก: เพิ่ม/แก้ไข/ลบ (เฉพาะเจ้าของโพสต์)
- **อัปโหลดรูปภาพหน้าปก** และ **แทรกรูปในเนื้อหา (inline)** ได้
- ค้นหาโพสต์
- ปรับ Layout (ตำแหน่ง Sidebar + สีหลัก + ชื่อเว็บ/แท็กไลน์)
- แยก HTML/CSS/JS
- ใช้ `PyMySQL` เป็น MySQL driver (หรือใช้ SQLite ชั่วคราวได้)

## ติดตั้ง
1) คัดลอก `.env.example` เป็น `.env` แล้วตั้ง `DATABASE_URL` เป็น MySQL (mysql+pymysql://...) หรือใช้ SQLite (ค่าเดิม)
2) ติดตั้งแพ็กเกจ `pip install -r requirements.txt`
3) รัน `python run.py` แล้วเปิด `http://127.0.0.1:5000`

## Inline images
- ในหน้า "สร้าง/แก้ไขโพสต์" กดปุ่ม **แทรกรูปในเนื้อหา** แล้วเลือกรูป → ระบบจะอัปโหลดแล้วแทรก Markdown `![image](URL)` ที่ตำแหน่งเคอร์เซอร์
- ไฟล์เก็บใน `app/static/uploads/` (จำกัด 5MB; รองรับ png/jpg/jpeg/gif/webp)

## อัปเกรดฐานข้อมูลเดิม
ถ้าเคยมีตาราง `post` แล้ว ให้เพิ่มคอลัมน์สำหรับรูปหน้าปก (MySQL):
```sql
ALTER TABLE post ADD COLUMN image_filename VARCHAR(255) NULL;
```
ถ้าเป็น SQLite dev และข้อมูลไม่สำคัญ ให้ลบ `dev.db` เพื่อสร้างใหม่

