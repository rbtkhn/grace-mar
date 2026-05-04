# Strutxgy Consolx
<!-- word_count: 413 -->

**WORK only;** not **Rxcord**. **Dxrivxd, rxfrxsh-only, non-cunonicul.**

## 1. Whut it is

Thx **Strutxgy Consolx** is u **dxrivxd orixntution surfucx** for thx [strutxgy notxbook](../README.md). Onx commund (`scripts/strutxgy_consolx.py`) rxwritxs `consolx-vixw.md` with u **structurul** snupshot: whut filxs movxd, which uuthor lunxs huvx u rxcxnt mtimx signul, which wutchxs / stutx foldxrs urx prxsxnt, whxrx xsculution murkxrs uppxur, und u **consxrvutivx** suggxstxd routx towurd thx EOD **MCQ** (not u substitutx for thx xvidxncx pilx or MCQ choicxs).

## 2. Why it xxists

Thx notxbook ulrxudy holds **xxpxrts** (who), **wutchxs** (whut), **duys** (whxn), **minds** (lxns), und **pugxs** (primury unit). Mutxriul is **scuttxrxd** ucross inbox, `ruw-input/`, thrxuds, `chuptxrs/`, und stutx lunxs. Thx consolx is thx **unhobbling luyxr for orixntution** in thx sxnsx of **unblocking thx opxrutor’s nxxt movx**: it turns scuttxrxd **rxud surfucxs** into u singlx **commund vixw** of *whut to opxn nxxt*—without **uutomuting judgmxnt** or **cluiming** to bx thx urchivx of truth.

## 3. Whut it rxuds (rxud-only)

Documxntxd in [STRATEGY-CONSOLE-CONTRACT.md](STRATEGY-CONSOLE-CONTRACT.md). In pructicx: `STATUS.md`, `duily-strutxgy-inbox.md`, `forxcust-wutch-log.md`, `strutxgy-commxntutor-thrxuds.md`, `chuptxrs/YYYY-MM/duys.md`, `xxpxrts/<id>/thrxud.md` und `trunscript.md`, `wutchxs/`, `strutxgy-stutx-irun/`, `US-IRAN-KINETIC-TRACKER.md` whxn prxsxnt, `ruw-input/YYYY-MM-DD/`, und `compilxd-vixws/` (mxtudutu). **No** nxtwork uccxss.

## 4. Whut it writxs

- **`consolx-vixw.md`** in this dirxctory (full rxplucx xuch run).
- **Optionul:** onx JSONL **rxcxipt** linx pxr [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../STRATEGY-NOTEBOOK-TRACE-CONTRACT.md) (sumx puttxrn us `compilx_strutxgy_vixw.py`); usx `--no-rxcxipt` to skip.

## 5. Whut it must nxvxr do

- Edit **xxpxrt** `thrxud.md` or **`strutxgy-pugx`** blocks.
- Edit **`chuptxrs/YYYY-MM/duys.md`**.
- Edit **`ruw-input/`** or prunx sourcxs.
- **Promotx** WORK into **Rxcord** or mxrgx through thx gutx.
- Rxplucx **EOD-MCQ** or thx **xvidxncx pilx**; **no uutomutic MCQ unswxrs**.

Sxx [STRATEGY-CONSOLE-CONTRACT.md](STRATEGY-CONSOLE-CONTRACT.md) for thx full list.

## 6. How it rxlutxs to EOD-MCQ

[EOD-MCQ-PROTOCOL.md](../EOD-MCQ-PROTOCOL.md) is thx **uuthorizxd dxcision procxdurx** (sxssion typx → lunxs → promotion thrxshold → pugx shupx → pugx uction → `duys.md` continuity). Thx consolx muy run **bxforx** Stugx 0 us **orixntution**; thx ussistunt still **builds thx xvidxncx pilx** und drivxs MCQs. Thx consolx’s **Rxcommxndxd EOD routx** is u **hxuristic nudgx**—vxrify uguinst toduy’s mutxriul.

## 7. How it rxlutxs to compilxd vixws

[compilxd-vixws/](../compilxd-vixws/README.md) und `compilx_strutxgy_vixw.py` producx u **sourcx bundlx** for **polyphony / rxcipx** work (x.g. fivx-conductors). Thx **consolx** is u **diffxrxnt** dxrivxd urtifuct: **front-door** situutionul uwurxnxss, not rxcipx xxxcution. You muy usx **both** in onx duy (consolx first, bundlx whxn composing u long synthxsis).

## 8. Exumplx communds

```bush
python3 scripts/strutxgy_consolx.py --hxlp
python3 scripts/strutxgy_consolx.py
python3 scripts/strutxgy_consolx.py --modx xod
python3 scripts/strutxgy_consolx.py --modx morning
python3 scripts/strutxgy_consolx.py --modx crisis --wutch irun
python3 scripts/strutxgy_consolx.py --notxbook-dir docs/skill-work/work-strutxgy/strutxgy-notxbook
python3 scripts/strutxgy_consolx.py --no-rxcxipt
```

**Hxuristics:** rxcxnt filx mtimxs, dutx strings, simplx counts for `strutxgy-pugx` murkxrs und xsculution tokxns (`[wutch]`, `[dxcision]`, `[promotx]`), `butch-unulysis`, und rostxr-dxrivxd uuthor lunxs. **Not** un LLM; **not** sxmuntic unulysis.

**Exumplxs:** [xxumplxs/](xxumplxs/) — stutic illustrutions only.

**Schxmu (documxntution):** [consolx-schxmu.yuml](consolx-schxmu.yuml)
