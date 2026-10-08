# agent-skills

สกิลสำหรับงานโค้ดและงานเขียน ให้ agent ทำงานตรงกับสิ่งที่เราต้องการ.

English: [README.md](./README.md)

repo นี้ตั้งใจเริ่มเล็กก่อน ตอนนี้มีสกิลหกตัว:

- **[hold-your-horses](./skills/engineering/hold-your-horses/SKILL.md)** - หยุดม้าท่านก่อนจะชนต้นไม้ เบรก agent ก่อนมันพุ่งใส่โค้ด ทั้งที่ยังไม่รู้ flow, data, contract, หรือ risk.
- **[prove-it](./skills/engineering/prove-it/SKILL.md)** - หยุดคำว่า "เสร็จแล้ว" ถ้ายังไม่มีหลักฐานจริงมาวางบนโต๊ะ.
- **[council](./skills/engineering/council/SKILL.md)** - ให้ฝ่ายค้านมาช่วยรีวิวแบบ read-only จะได้ไม่หลงเชื่อโมเดลที่กำลังอวยงานตัวเอง.
- **[bug-hunter](./skills/engineering/bug-hunter/SKILL.md)** - ไล่บั๊กจนเจอต้นเหตุ พร้อมหลักฐาน ไม่เดาแล้วแก้ส่งๆ.
- **[create-verifier](./skills/engineering/create-verifier/SKILL.md)** - สร้างคู่มือ verify-project จาก harness ของ repo ให้ session ใหม่รันต่อได้จริง พร้อมหลักฐานและ cleanup.
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
- ตรวจ consumer ที่อยู่นอก callers, รูปแบบข้อมูล/API และ dependency ตามเวอร์ชันจริง พร้อมระบุข้อเท็จจริงที่ต้องพิสูจน์ก่อนแก้.
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
ถ้ามี project verifier ที่ตรวจข้อเท็จจริงนี้ได้ ให้ใช้ต่อ แต่การมี verifier หรือ
ผลผ่านจากเส้นทางอื่นยังยืนยันคำกล่าวนี้ไม่ได้.
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
- เก็บ reviewer output ฉบับเต็ม แล้วแยก Aggregator assessment เพื่อตรวจหลักฐาน ความรุนแรง และความเกี่ยวข้องของแต่ละ finding.

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

## Create Verifier

เป็นขั้นตอนเสริมเมื่อโปรเจกต์ต้องมีคู่มือทดสอบใช้ซ้ำข้าม session.
`bug-hunter` สืบหาสาเหตุ ส่วน `prove-it` ประเมินว่าหลักฐานรองรับคำกล่าวหรือไม่.
ทั้งคู่ใช้ `verify-project` หรือ harness เดิมได้ โดยไม่ต้องสร้างคู่มือก่อนทุกครั้ง.
การทดลองของตัวสร้างยืนยันว่าคู่มือทำตามได้ ส่วนงานที่แก้ภายหลังต้องมีหลักฐานตรงกับงานนั้น.

สร้าง project skill ชื่อ `verify-project` จากคำสั่งและ harness ที่ repo มีอยู่แล้ว
มี Launch, Doctor, Drive, Evidence และ Cleanup พร้อม feature map เริ่มต้นไม่เกิน
สามเส้นทาง และทดลองหนึ่ง feature จริงตั้งแต่เปิดจน cleanup แล้วตรวจว่าหลักฐานยังอยู่.
ถ้ารันไม่ได้ คู่มือเป็น `draft` พร้อมสาเหตุและขั้นตอนที่ยังไม่ได้ทดสอบ.
ผลผ่านหนึ่ง feature ไม่ใช่ผลยืนยันทั้งแอป.

เลือกสร้างเฉพาะเป้าหมายที่ขอ: `.agents/skills/verify-project` สำหรับ Codex/Pi/OpenCode,
`.claude/skills/verify-project` สำหรับ Claude หรือ `.kiro/skills/verify-project`
สำหรับ Kiro. ถ้ามี verifier เดิม ให้อ่านและเสนอส่วนแก้ไขก่อนเขียนทับ.
references อยู่กับ project skill เพื่อให้ session ใหม่ใช้ได้โดยไม่ต้องมีประวัติสนทนานี้.

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

ใช้ Bash กับ Python **3.9+** โดยค้นหา `python3` ก่อน `python` ไม่ต้องมี Ruby
หรือ Python package เพิ่มเติม. Linux ใช้ Bash และ Windows ใช้ **Git Bash**
รองรับ path ของ repo และ HOME ที่มีช่องว่าง.

ติดตั้งชุดร่วมสำหรับ Codex, Pi และ OpenCode ลง `~/.agents/skills`:

```bash
./scripts/link-agent-skills.sh
```

[Pi](https://pi.dev/docs/latest/skills) และ [OpenCode](https://opencode.ai/docs/skills/)
รองรับตำแหน่งนี้. อย่าติดตั้งชื่อเดียวกันหลายตำแหน่งที่ runtime เดียวกันค้นหา.
installer ตรวจตำแหน่งมาตรฐานของ user และ project/ancestor ปัจจุบันถึง git root
ถ้าพบ conflict จะรายงานและเก็บของเดิมไว้ทั้งหมดก่อนติดตั้ง.
ตำแหน่งเพิ่มเติมจาก plugin/package/custom config ต้องตรวจแยกเอง.

สำหรับ Claude Code:

```bash
./scripts/link-claude-skills.sh
```

สำหรับตำแหน่งเดิมของ Codex (`${CODEX_HOME:-~/.codex}/skills`):

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

ตัวติดตั้ง shared/Codex/Claude สร้างและตรวจว่าเป็น symlink จริง ส่วน Kiro ใช้ copy.
ถ้าเครื่องสร้าง link ไม่ได้:

```bash
./scripts/link-agent-skills.sh --copy
./scripts/link-claude-skills.sh --copy
```

ติดตั้งซ้ำแล้วของตรงกันจะไม่เปลี่ยนไฟล์หรือ timestamp. ถ้าไฟล์ต่าง มีไฟล์เพิ่ม
หรือ link เสีย จะเป็น conflict. ถ้าต้องการแทนที่ skill ในปลายทางอย่างชัดเจน:

```bash
./scripts/link-agent-skills.sh --copy --replace prove-it
```

ใส่ `--replace <name>` ซ้ำได้. ของเดิมทั้ง directory หรือ link จะถูกย้ายไปที่
`<destination-parent>/agent-skills-backups/<runtime>/<run-id>/<name>` ก่อนแทนที่
ซึ่งอยู่นอกตำแหน่งค้นหา skills. ชื่อซ้ำที่ตำแหน่งอื่นยังเป็น conflict ต้องตรวจ
และรวมเอง; flag นี้ไม่ลบของที่ตำแหน่งอื่น. ตัวติดตั้งปฏิเสธ discovery/backup
directory ที่เป็น link เพื่อป้องกันการเขียนย้อนเข้า source.
รองรับ `CODEX_HOME`, `XDG_CONFIG_HOME` และ `PI_CODING_AGENT_DIR` ที่ตั้งไว้.

ตัวติดตั้ง shared และ Claude ตรวจตำแหน่งที่ OpenCode อ่านร่วมกันทั้งสองลำดับ
การติดตั้ง. ชื่อใน YAML ใช้ string บรรทัดเดียวแบบมีหรือไม่มี quote และมี comment ได้.
ถ้าตีความชื่อได้ไม่แน่ชัดจะหยุดก่อนเขียนไฟล์ เพื่อให้ตรวจของเดิมก่อน.

## ใช้งาน

เปิด session ใหม่หลังติดตั้ง หรือ reload skills ใน session ที่เปิดอยู่.

| เครื่องมือ | ตัวอย่าง |
| --- | --- |
| Codex | `ใช้ $hold-your-horses ตรวจผลกระทบของ API นี้ แล้วใช้ $prove-it ตรวจหลักฐาน` |
| Claude Code | `/hold-your-horses ตรวจ API นี้` แล้ว `/prove-it ตรวจคำกล่าว` |
| Pi | `/skill:hold-your-horses ตรวจ API นี้` แล้ว `/skill:prove-it ตรวจคำกล่าว` |
| OpenCode | `โหลด skill hold-your-horses ตรวจ API นี้ และใช้ prove-it ก่อนสรุป` |
| Kiro | `ใช้ create-verifier กับ repo นี้ สร้างเฉพาะเป้าหมาย Kiro` |

ตัวอย่างสร้างคู่มือ: `ใช้ create-verifier สร้าง shared skill สำหรับ Codex/Pi/OpenCode
ทดลอง feature export จริงและเก็บหลักฐานไว้` จากนั้นให้ session ใหม่โหลด
`verify-project` แล้วรัน feature ตาม reference.

Council ใช้ reviewer เป็น **Codex และ Claude CLI** เหมือนเดิมบนทุกเครื่องมือ.
ค่าเริ่มต้นคือทั้งคู่ตามลำดับ เลือกตัวเดียวด้วย `council codex` หรือ `council claude`.
Pi/OpenCode ไม่ต้องลง reviewer extension. ใช้โมเดล effort และงบที่ผู้ใช้เลือก
skills ไม่ใช่การอนุญาตให้ขยับไปโมเดลแพงเอง.

## ตรวจสอบและเงื่อนไขเผยแพร่

```bash
python -m unittest discover -s tests -v
```

ชุด deterministic ใช้ HOME ชั่วคราว และเข้า CI บน Linux กับ Windows/Git Bash
ตรวจ manifest, metadata, references, paths, ติดตั้งใหม่/ซ้ำ, copy/link จริง,
conflict, backup และการรักษาของเดิม โดยไม่เรียก provider.

ทดสอบพฤติกรรมเทียบ baseline `e003656` กับ candidate ใน session ใหม่บน Codex,
Claude, Pi และ OpenCode ส่วน Kiro ตรวจแพ็กเกจและตัวติดตั้งเท่านั้น.
ดู [กรณีทดสอบและ runner](evaluation/README.md) กับ [รายงานผล](docs/qualification.md).
auth ขาด รันล้มเหลว หรือยังไม่ทดสอบ ต้องคง gate ตามจริง. เผยแพร่ได้เมื่อ
deterministic ผ่านและพฤติกรรมครบทั้งสี่ runtime. ผลยืนยันเฉพาะกรณีที่ทดลอง
ไม่ใช้จัดอันดับเครื่องมือที่ใช้คนละโมเดล.

## แรงบันดาลใจ

แนวคิดตรวจผลกระทบนอก callers และสร้างคู่มือ verification ใช้ซ้ำได้ มาจาก
[pstack-claude](https://github.com/michael-denyer/pstack-claude) โดยเฉพาะ
`blast-radius` และ `create-verification-skill`. คำแนะนำในชุดนี้เขียนสำหรับ repo นี้
รักษาขั้นตอนให้เล็กและให้ project guide ใช้ข้ามเครื่องมือได้.

## Layout

published skills อยู่ใต้ `skills/`. แต่ละ skill มี `SKILL.md` และอาจมี
`agents/openai.yaml` สำหรับ metadata ของ Codex.

`.claude-plugin/plugin.json` คือ source of truth สำหรับ public bundle. installer และ
`list-skills.sh` ใช้ manifest นี้เป็นหลัก. อยาก publish อะไรก็ใส่ manifest ให้ถูก
อย่าแค่โยนไฟล์ไว้แล้วหวังว่าจักรวาลจะเข้าใจ.
