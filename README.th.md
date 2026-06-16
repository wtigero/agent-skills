# agent-skills

สกิลไว้คุม coding agents ไม่ให้รีบมั่วแล้วทำหน้ามั่น.

English: [README.md](./README.md)

repo นี้ตั้งใจเริ่มเล็กก่อน ตอนนี้ publish แล้วสามตัว:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - หยุดม้าท่านก่อนจะชนต้นไม้ เบรก agent ก่อนมันพุ่งใส่โค้ด ทั้งที่ยังไม่รู้ flow, data, contract, หรือ risk.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - หยุดคำว่า "เสร็จแล้ว" ถ้ายังไม่มีหลักฐานจริงมาวางบนโต๊ะ.
- **[council](./skills/engineering/council/SKILL.md)** - ให้ฝ่ายค้านมาช่วยรีวิวแบบ read-only จะได้ไม่หลงเชื่อโมเดลที่กำลังอวยงานตัวเอง.

ไฟล์นี้เป็น summary เอาไว้อ่านภาพรวมและรสชาติพอ. กติกาจริงที่ agent ต้องทำตาม
อยู่ใน `SKILL.md` ของแต่ละสกิล อย่าเอา README ไปเถียงกับ source of truth.

## Hold Your Horses

No code before the flow is clear.

ใช้ตอน request ยังเบลอ เสี่ยง แตะหลายไฟล์/data/contract หรือคันมืออยาก refactor
ทั้งที่ flow กับ success criteria ยังไม่ชัด.

มันบังคับ agent ให้:

- อ่านของจริง ไม่เดาจากกลิ่น.
- ถามเฉพาะคำถามที่ blocking.
- ไล่ path จริงผ่าน code, data, contracts, helpers, tests.
- frame risk, trim งาน, implement แคบๆ, แล้ว review diff.

ถ้าเป็น mechanical edit เล็กจริง ให้ใช้แค่ **Read it -> Implement it -> Review the diff**
แล้วรายงานเฉพาะ `Changed`, `Verified`, และ `Unverified`. แต่ถ้าแตะ behavior, data,
contracts, shared helpers, หรือ production risk แล้วทำเนียนย่อขั้นตอน อันนั้นไม่ใช่ไว
อันนั้นซุย.

ใจความคือ: เข้าใจ flow ก่อน แล้วค่อยแตะ code. ไม่งั้นก็แค่พา bug ไปเดินเล่น.

## Prove It

No claim without proof.

ใช้ก่อน agent จะพูดว่า "เสร็จแล้ว", "แก้แล้ว", "ทดสอบแล้ว", "พร้อม ship",
หรือ "ปลอดภัย" ทั้งที่ proof ยังอ่อนหรือไม่ได้รันใหม่.

มันบังคับ agent ให้:

- จับ claim ให้ชัด อย่าให้คำพูดมันลื่น.
- หา proof ที่ตรง claim ที่สุด.
- ถามว่าถ้า claim ไม่จริง proof นี้จะพังไหม.
- รัน proof สดรอบนี้.
- บอกให้หมดว่าอะไรยังไม่ได้พิสูจน์ อย่าซ่อนใต้พรม.

หลักฐานที่ดีต้องแตะ behavior จริง เช่น repro, workflow, API call, targeted test,
หรือ manual check พร้อม input และ observed output.
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

## Install

installer จะ link published skills จาก repo นี้เข้า skill directory ของแต่ละ agent.
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
