# agent-skills

สกิลไว้คุม coding agents ไม่ให้รีบมั่วแล้วทำหน้ามั่น.

English: [README.md](./README.md)

repo นี้ตั้งใจเริ่มเล็ก ไม่ได้สะสมสกิลไว้โชว์จำนวน ตอนนี้ publish แล้วสามตัว:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - เบรก agent ก่อนมันพุ่งใส่โค้ด ทั้งที่ยังไม่รู้ flow, data, contract, หรือ risk.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - หยุดคำว่า "เสร็จแล้ว" ถ้ายังไม่มีใบเสร็จจริงมาวางบนโต๊ะ.
- **[council](./skills/engineering/council/SKILL.md)** - ลากสายตานอกวงมาช่วยรีวิวแบบ read-only จะได้ไม่หลงเชื่อโมเดลที่กำลังอวยงานตัวเอง.

ไฟล์นี้เป็น public summary ภาษาไทย อ่านเอารสและภาพรวมพอ. กติกาจริงที่ agent
ต้องทำตามอยู่ใน `SKILL.md` ของแต่ละสกิล อย่าเอาไฟล์นี้ไปเถียงกับ source of truth.

## Hold Your Horses

No code before the flow is clear.

ใช้ตอน request ยังเบลอ เสี่ยง กระทบหลายไฟล์ แตะ data/contract หรือมีอาการคันมือ
อยาก refactor ทั้งที่ยังไม่เข้าใจ problem, flow, affected data, contracts,
หรือ success criteria ให้ชัดก่อน

ritual คือ:

1. **Read it** - อ่าน request กับของจริงที่ user ชี้มา อย่าเดาจากกลิ่น.
2. **Clarify intent** - ถามเฉพาะคำถามที่ blocking และขุดเองจาก repo, runtime, docs, หรือ database ไม่ได้.
3. **Trace it** - ไล่ path จริง: entry point, data, contracts, helpers, tests.
4. **Frame it** - เขียนให้เห็น as-is, to-be, data/contracts ที่โดน, risk, และคำถามค้าง.
5. **Plan it** - แตกงานให้เห็น risk กับวิธีพิสูจน์ ไม่ใช่ list งานเท่ๆ ไว้หลอกตัวเอง.
6. **Trim it** - ตัดของฟุ่มเฟือย เหลือแค่สิ่งที่ทำให้ flow ใหม่จริงโดยไม่พาเรื่องงอก.
7. **Implement it** - ทำเฉพาะที่ trim แล้ว เอา feedback เร็วก่อน.
8. **Review the diff** - ไล่เก็บ scope creep, test อ่อน, debug ขยะ, และ complexity ที่ไม่คุ้ม.

ถ้าเป็น mechanical edit เล็กจริง ให้ใช้แค่ **Read it -> Implement it -> Review the diff**
แล้วรายงานเฉพาะ `Changed`, `Verified`, และ `Unverified`. แต่ถ้าแตะ behavior, data,
contracts, shared helpers, หรือ production risk แล้วทำเนียนย่อขั้นตอน อันนั้นไม่ใช่ไว
อันนั้นซุย.

ใจความคือ: เข้าใจ flow ก่อน แล้วค่อยแตะ code. ไม่งั้นก็แค่พา bug ไปเดินเล่น.

## Prove It

No claim without proof.

ใช้ก่อน agent จะพูดคำอันตรายพวก "เสร็จแล้ว", "แก้แล้ว", "ทดสอบแล้ว",
"validated แล้ว", "พร้อม ship", หรือ "ปลอดภัย" โดยเฉพาะเวลาหลักฐานยังอ่อน
ไม่ตรง claim ไม่ได้รันใหม่ หรือเป็นแค่ความมั่นใจลอยๆ

ritual คือ:

1. **Find the claim** - จับให้ได้ว่ากำลังอ้างอะไร อย่าให้คำพูดมันลื่น.
2. **Find the proof** - หา evidence ที่ตรง claim ที่สุด ไม่ใช่ proof ข้างๆ คูๆ.
3. **Break the proof** - ถามว่าถ้า claim ไม่จริง proof นี้จะพังไหม.
4. **Run the proof** - รัน proof สดรอบนี้ พร้อม command/result ชัดๆ.
5. **Name what remains unproven** - บอกให้หมดว่าอะไรยังไม่ได้พิสูจน์ อย่าซ่อนใต้พรม.

หลักฐานที่ดีต้องแตะ behavior จริง เช่น repro, workflow, API call, job, targeted test,
affected build/check, หรือ manual check พร้อม input, environment, และ observed output.
แค่ "ดูโค้ดแล้วน่าจะได้" ไม่ใช่ proof มันคือดูดวง.

ใจความคือ: อย่า claim ถ้ายังพิสูจน์ไม่ได้. ไม่มีใบเสร็จ ก็อย่ามั่นหน้า.

## Council

No rubber stamps. Bring outside eyes.

ใช้เมื่ออยากได้ second opinion จากโมเดลนอกวง ไม่ใช่ให้โมเดลเดิมนั่งอวย diff ตัวเอง
แล้วทำเหมือนนั่นคือ review

ritual คือ:

1. **Choose the scope** - เลือกให้ชัดว่าจะรีวิว git changes, files, หรือ pasted content.
2. **Summon outside reviewers** - เรียก Codex, Claude Code, หรือทั้งคู่มาเป็นกรรมการนอกวง.
3. **Keep them blind** - อย่าเอาคำตอบคนหนึ่งไปป้อนอีกคน เดี๋ยวได้เสียงสะท้อน ไม่ใช่ review.
4. **Demand evidence** - finding ต้องอ้าง code, snippet, หรือ source จริง ไม่ใช่ความรู้สึก.
5. **Return the disagreement** - คืน output แยกกัน อย่าเกลี่ยให้ดูสามัคคีปลอมๆ.

Council ส่ง review แบบ **read-only** ไปยัง external agent CLI:

- `council` หรือ `council both` - รัน Codex และ Claude แล้วแสดงผลข้างกัน.
- `council codex` / `council claude` - รันเฉพาะตัวที่เลือก.

reviewer ทุกตัวต้องทำตัวเป็น auditor ข้างนอก: อ้าง code จริง, แยก correctness/security
ออกจาก style preference, tag severity, และไม่แก้ไฟล์. Codex `review` ใช้สำหรับรีวิว,
Codex `exec` ใช้ `--sandbox read-only`, และ Claude ใช้ `--permission-mode plan`.

ถ้า reviewer CLI ใช้ไม่ได้ Council จะเตรียม manual review packet แทนการแกล้งบอกว่ารีวิวแล้ว.
ผลลัพธ์ต้องเป็น reviewer output จริง หรือ brief ที่พร้อมเอาไป paste เอง ไม่ใช่ fake certainty
แบบ "เชื่อผมเถอะครับพี่".

ใจความคือ: เอามุมมองข้างนอกกลับมา แม้มันจะเห็นไม่ตรงกัน. โดยเฉพาะตอนที่เรากำลังอินกับงานตัวเองเกินไป.

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
