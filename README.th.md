# agent-skills

สกิลใช้งานจริงสำหรับ coding agents.

English: [README.md](./README.md)

repo นี้ตั้งใจเริ่มเล็กก่อน ตอนนี้มีสกิลที่ publish แล้วสามตัว:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - ชะลอ agent ไม่ให้รีบแตะโค้ดก่อนเข้าใจ flow, data, contract, และ risk.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - ห้ามอ้างว่างานเสร็จ แก้แล้ว ทดสอบแล้ว หรือปลอดภัย ถ้ายังไม่มีหลักฐานตรงกับ claim.
- **[council](./skills/engineering/council/SKILL.md)** - ขอรีวิวแบบ read-only จาก Codex, Claude Code, หรือทั้งคู่ เพื่อให้ได้สายตาจากโมเดลนอกวง.

ไฟล์นี้เป็น public summary ภาษาไทย. รายละเอียดที่ agent ต้องทำตามจริงอยู่ใน `SKILL.md`
ของแต่ละสกิล.

## Hold Your Horses

No code before the flow is clear.

ใช้เมื่อ request ยังคลุมเครือ เสี่ยง กระทบหลายไฟล์ เกี่ยวกับ data หรือ contract
หรือมีแรงล่อใจให้ refactor ทั้งที่ยังไม่เข้าใจ problem, flow, affected data,
contracts, หรือ success criteria ชัดพอ

ritual คือ:

1. **Read it** - อ่าน request และ artifact ที่ user ชี้มาให้ตรงจุด.
2. **Clarify intent** - ถามเฉพาะคำถามที่ blocking และหาเองจาก repo, runtime, docs, หรือ database ไม่ได้.
3. **Trace it** - ไล่ entry point, data, contracts, helpers, และ tests ตาม path จริง.
4. **Frame it** - ระบุ as-is flow, to-be flow, affected data/contracts, risk, และ open questions.
5. **Plan it** - แปลง to-be flow เป็นงานที่เปิด risk และ verification ให้เห็น.
6. **Trim it** - เหลือเฉพาะสิ่งที่ทำให้ to-be flow เป็นจริงโดยไม่เพิ่ม side effect ที่เลี่ยงได้.
7. **Implement it** - ทำเฉพาะงานที่ trim แล้ว เรียงตาม feedback ที่ได้เร็วและมีประโยชน์.
8. **Review the diff** - ตัด scope creep, test อ่อน, debug noise, และ complexity ที่ไม่คุ้มออก.

ถ้าเป็น mechanical edit เล็กมาก ให้ใช้แค่ **Read it -> Implement it -> Review the diff**
แล้วรายงานเฉพาะ `Changed`, `Verified`, และ `Unverified`. ห้ามย่อขั้นตอนนี้กับงานที่กระทบ
behavior, data, contracts, shared helpers, หรือ production risk.

ใจความคือ: เข้าใจ flow ก่อน แล้วค่อยแตะ code.

## Prove It

No claim without proof.

ใช้ก่อน agent จะบอกว่างานเสร็จแล้ว แก้แล้ว ทดสอบแล้ว validated แล้ว พร้อม ship
หรือปลอดภัย โดยเฉพาะเมื่อหลักฐานอาจอ่อน ไม่ตรง claim ไม่ได้รันใหม่ หรือเป็นแค่ความมั่นใจ

ritual คือ:

1. **Find the claim** - ระบุ claim ให้ชัดว่ากำลังอ้างอะไร.
2. **Find the proof** - หา evidence ที่ตรงกับ claim ที่สุด.
3. **Break the proof** - ถามว่าหลักฐานนี้จะ fail ไหมถ้า claim ไม่จริง.
4. **Run the proof** - รัน proof สดในรอบนี้ พร้อม command/result ที่ชัดเจน.
5. **Name what remains unproven** - บอกขอบเขตที่ยังพิสูจน์ไม่ได้.

หลักฐานที่ดีควรแตะ behavior จริง เช่น repro, workflow, API call, job, targeted test,
affected build/check, หรือ manual check พร้อม input, environment, และ observed output.

ใจความคือ: อย่า claim ถ้ายังพิสูจน์ไม่ได้.

## Council

No rubber stamps. Bring outside eyes.

ใช้เมื่ออยากได้ second opinion จากโมเดลนอกวง ไม่ใช่ให้โมเดลเดิมยืนยันงานตัวเอง

ritual คือ:

1. **Choose the scope** - เลือกว่าจะรีวิว git changes, files, หรือ pasted content.
2. **Summon outside reviewers** - ส่งรีวิวไป Codex, Claude Code, หรือทั้งคู่.
3. **Keep them blind** - อย่า feed คำตอบของ reviewer หนึ่งให้อีก reviewer.
4. **Demand evidence** - บังคับให้ finding อ้าง code, snippet, หรือ source จริง.
5. **Return the disagreement** - คืน output แยกกัน ไม่เกลี่ยให้เป็น consensus ปลอม.

Council ส่ง review แบบ **read-only** ไปยัง external agent CLI:

- `council` หรือ `council both` - รัน Codex และ Claude แล้วแสดงผลข้างกัน.
- `council codex` / `council claude` - รันเฉพาะตัวที่เลือก.

reviewer ทุกตัวต้องทำตัวเป็น auditor ข้างนอก: อ้าง code จริง, แยก correctness/security
ออกจาก style preference, tag severity, และไม่แก้ไฟล์. Codex `review` ใช้สำหรับรีวิว,
Codex `exec` ใช้ `--sandbox read-only`, และ Claude ใช้ `--permission-mode plan`.

ถ้า reviewer CLI ใช้ไม่ได้ Council จะเตรียม manual review packet แทนการแกล้งบอกว่ารีวิวแล้ว.
ผลลัพธ์ต้องเป็น reviewer output จริง หรือ brief ที่พร้อมเอาไป paste เอง ไม่ใช่ fake certainty.

ใจความคือ: เอามุมมองข้างนอกกลับมา แม้มันจะเห็นไม่ตรงกัน.

## Install

installer จะ link published skills จาก repo นี้เข้า skill directory ของแต่ละ agent.

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
`list-skills.sh` ใช้ manifest นี้เป็นหลัก.
