# agent-skills

สกิลสำหรับงานโค้ดและงานเขียน ให้ agent ทำงานตรงกับสิ่งที่เราต้องการ.

English: [README.md](./README.md)

repo นี้ตั้งใจเริ่มเล็กก่อน ตอนนี้มีสกิลห้าตัว:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - หยุดม้าท่านก่อนจะชนต้นไม้ เบรก agent ก่อนมันพุ่งใส่โค้ด ทั้งที่ยังไม่รู้ flow, data, contract, หรือ risk.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - หยุดคำว่า "เสร็จแล้ว" ถ้ายังไม่มีหลักฐานจริงมาวางบนโต๊ะ.
- **[council](./skills/engineering/council/SKILL.md)** - ให้ฝ่ายค้านมาช่วยรีวิวแบบ read-only จะได้ไม่หลงเชื่อโมเดลที่กำลังอวยงานตัวเอง.
- **[bug-hunter](./skills/engineering/bug-hunter/SKILL.md)** - ไล่บั๊กจนเจอต้นเหตุ พร้อมหลักฐาน ไม่เดาแล้วแก้ส่งๆ.
- **[write-like-me](./skills/writing/write-like-me/SKILL.md)** - เรียบเรียงความคิดเป็นบทความหรือโพสต์ ใช้คำง่ายและรักษาเสียงของเรา.

ไฟล์นี้เป็น summary เอาไว้อ่านภาพรวมและรสชาติพอ. กติกาจริงที่ agent ต้องทำตาม
อยู่ใน `SKILL.md` ของแต่ละสกิล อย่าเอา README ไปเถียงกับ source of truth.

แต่ละสกิลใช้เดี่ยวได้ ถ้าใช้ร่วมกันก็ใช้ flow และหลักฐานที่ยังตรงกับงานต่อได้
แล้วรวมผลไว้ในรายงานเดียว ไม่ต้องเริ่มพิธีใหม่ทุกครั้ง.

## Hold Your Horses

No code before the flow is clear.

ใช้ก่อนลงมือเมื่อ flow, data, contract, หรือ success criteria ยังไม่ชัด
หรือจะเปลี่ยนงานกว้างๆ/refactor ทั้งที่ขอบเขตกับผลกระทบยังไม่แน่.

มันบังคับ agent ให้:

- อ่านของจริง ไม่เดาจากกลิ่น.
- ถามเฉพาะคำถามที่ blocking.
- ไล่ path จริงผ่าน code, data, contracts, helpers, tests.
- frame risk, trim งาน, implement แคบๆ, แล้ว review diff.

ปรับความลึกตามสิ่งที่ยังไม่รู้และผลกระทบ ไม่ใช่นับไฟล์. ถ้า flow ชัดและงานจำกัด
ให้ใช้ทางสั้น: อ่าน ไล่ path ที่เปลี่ยน implement review diff แล้ว verify.
รายงาน `Changed`, `Verified`, และ `Unverified`; เพิ่มเหตุผลเรื่อง scope หรือทางเลือก
เมื่อมีประเด็นจริง. ถ้า data, contract, หรือ production risk ยังไม่ชัด ก็ต้องไล่ต่อ.

ใจความคือ: เข้าใจ flow ก่อน แล้วค่อยแตะ code. ไม่งั้นก็แค่พา bug ไปเดินเล่น.

## Prove It

No claim without proof.

ใช้ก่อน agent จะพูดว่า "เสร็จแล้ว", "แก้แล้ว", "ทดสอบแล้ว", "พร้อม ship",
หรือ "ปลอดภัย" ทั้งที่ proof ยังอ่อนหรือไม่ตรงกับสถานะงานที่กำลังอ้าง.

มันบังคับ agent ให้:

- จับ claim ให้ชัด อย่าให้คำพูดมันลื่น.
- หา proof ที่ตรง claim ที่สุด.
- ถามว่าถ้า claim ไม่จริง proof นี้จะพังไหม.
- ตรวจว่า proof ยังตรงกับ code, input, และ environment; ถ้าเปลี่ยนหรือหลักฐานไม่ครบก็ค่อยรันใหม่.
- บอกให้หมดว่าอะไรยังไม่ได้พิสูจน์ อย่าซ่อนใต้พรม.

หลักฐานที่ดีต้องแตะ behavior จริง เช่น repro, workflow, API call, targeted test,
หรือ manual check พร้อม input และ observed output.
ผล CI หรือ check เดิมใช้ต่อได้เมื่อดูผลจริงได้และสถานะที่เกี่ยวข้องยังตรงกัน.
อาการหาย ยืนยัน root cause และพร้อม release เป็นคนละ claim อย่าใช้หลักฐานหนึ่งแทนทุกข้อ.
แค่ "ดูโค้ดแล้วน่าจะได้" ไม่ใช่ proof มันคือดูดวง.

ใจความคือ: อย่า claim ถ้ายังพิสูจน์ไม่ได้. ไม่มีใบเสร็จ ก็อย่ามั่นหน้า.

## Council

No rubber stamps. Bring outside eyes.

ใช้เมื่ออยากได้ second opinion จากโมเดลนอกวง ไม่ใช่ให้โมเดลเดิมนั่งอวย diff ตัวเอง.

Council ส่ง review แบบ **read-only** ไปยัง Codex, Claude Code, หรือทั้งคู่:

- `council` หรือ `council both` - รัน Codex และ Claude แล้วแสดงผลข้างกัน.
- `council codex` / `council claude` - รันเฉพาะตัวที่เลือก.

กติการีวิวสั้นๆ:

- reviewer ต้องแยกกันคิด.
- finding ต้องมี evidence จริง.
- ถ้าเห็นไม่ตรงกันก็คืนความเห็นแยกกัน.

ถ้า CLI ใช้ไม่ได้ Council จะทำ manual review packet แทนการแกล้งบอกว่ารีวิวแล้ว.
ต้องได้ output จริง หรือ brief ที่พร้อม paste เอง ไม่ใช่ "เชื่อผมเถอะครับพี่".

ใจความคือ: เอามุมมองข้างนอกกลับมา แม้มันจะเห็นไม่ตรงกัน.

## Bug Hunter

Find the cause. Bring the evidence.

ใช้เมื่อ bug, อาการที่เกิดๆ หายๆ, หรือ performance regression ต้องหาสาเหตุก่อนเลือกวิธีแก้.

มันพา agent ให้:

- สร้าง feedback loop ที่จับอาการเดียวกับที่ผู้ใช้เจอ.
- ไล่ fail path แล้วทดลอง prediction ที่แยกสาเหตุคู่แข่งออกจากกัน.
- จด experiment ledger และตรวจคำอธิบายกับผลรันก่อนหน้า.
- แก้ใน scope ตรวจสถานการณ์เดิม แล้วเก็บกวาด temporary probes.

ตั้งสมมติฐานเพื่อช่วยสร้าง repro ได้ แต่ยังฟันธงไม่ได้จนกว่าจะทดลอง.
หักล้างไม่สำเร็จก็ยังไม่ใช่หลักฐานยืนยันสาเหตุ. อาการ flaky กับ performance
ต้องเทียบหลายรันภายใต้เงื่อนไขเดียวกัน ไม่ใช่เห็นผ่านครั้งเดียวแล้วประกาศชัยชนะ.

ใจความคือ: ตามรอยบั๊ก แล้วเอาหลักฐานมาวางให้เห็นว่าสาเหตุคืออะไร.

## Write Like Me

ความคิดของเรา ในคำที่เราใช้เองได้.

ใช้เขียนบทความ โพสต์ เปลี่ยนโน้ตไทยเป็นอังกฤษ หรือแก้ร่างที่อ่านแล้วไม่เหมือนเรา.

สกิลจะถามเอาประเด็นกับตัวอย่างจริงที่ยังขาด ดูงานเขียนเดิมถ้ามี แล้วใช้คำธรรมดา
และแกรมมาร์ที่ถูกต้อง ไม่แต่งประสบการณ์ให้ ไม่ขัดภาษาจนเสียงของเราหาย.
งานสั้นที่ข้อมูลครบแล้วก็เขียนได้เลย ไม่ต้องถามหรือวาง outline ทุกครั้ง.

ตัวอย่าง:

```text
ใช้ write-like-me เขียนโพสต์อังกฤษสั้นๆ จากโน้ตนี้
ใช้คำง่ายที่ฉันพูดเองได้ รักษาน้ำเสียงตรงๆ
ถ้าประเด็นหรือตัวอย่างยังขาด ให้ถามก่อน
```

## Install

installer จะ link published skills เข้า Codex กับ Claude Code และ copy เข้า Kiro.
ไม่ต้องก็อปมือให้เหนื่อย.

สำหรับ Claude Code:

```bash
./scripts/link-claude-skills.sh
```

สำหรับ Codex:

```bash
./scripts/link-codex-skills.sh
```

สำหรับ Kiro:

```bash
./scripts/link-kiro-skills.sh
```

ดูรายการ published skills:

```bash
./scripts/list-skills.sh
```

## Layout

published skills อยู่ใต้ `skills/`. แต่ละ skill มี `SKILL.md` และอาจมี
`agents/openai.yaml` สำหรับ metadata ของ Codex.

`.claude-plugin/plugin.json` คือ source of truth สำหรับ public bundle. installer และ
`list-skills.sh` ใช้ manifest นี้เป็นหลัก. อยาก publish อะไรก็ใส่ manifest ให้ถูก
อย่าแค่โยนไฟล์ไว้แล้วหวังว่าจักรวาลจะเข้าใจ.
