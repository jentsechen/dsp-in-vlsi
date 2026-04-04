# ADFP RTL Simulation, Synthesis, and Gate-Level Simulation

## Prerequisites

- Get your ADFP account and password from TA
- Connect to NTU VPN before accessing the workstation
- Write all code locally on your PC — you cannot download files from ADFP, only upload
- Run `cb` in the terminal after connecting to initialize the environment

---

## Folder Structure

```
lab0/
├── 00_TESTBED/    # your testbench
├── 01_RTL/        # your design + file.f + 01_run
├── 02_SYN/        # syn.tcl + syn.sdc
└── 03_GATESIM/    # gate-level sim file.f + 01_run
```

---

## File Preparation

### 00_TESTBED
- Place your testbench here (e.g. `HW3_tb.v`)
- Add the following to dump waveform:
  ```verilog
  initial begin
      $fsdbDumpfile("your_design.fsdb");
      $fsdbDumpvars(0, "+mda");
  end
  ```

### 01_RTL
- Place your design file here (e.g. `HW3.v`)
- Edit `file.f` to list all files used in simulation:
  ```
  ../00_TESTBED/HW3_tb.v
  HW3.v
  ```

### 02_SYN
- Edit `syn.tcl` — only change:
  - `set DESIGN "YourModuleName"`
  - `analyze -format sverilog "../01_RTL/YourFile.sv"` (use `-format sverilog` for `.sv` files)
  - Do **not** modify the target library
- Edit `syn.sdc` — only change the cycle time (`set cycle 20.0`)
  - Do **not** modify anything else in the SDC
- Clock name in your module must match the SDC: name it `clk`

### 03_GATESIM
- Edit `file.f`:
  ```
  ../00_TESTBED/HW3_tb.v
  ../02_SYN/Netlist/HW3_syn.v
  -v /share1/tech/ADFP/Executable_Package/Collaterals/IP/stdcell/N16ADFP_StdCell/VERILOG/N16ADFP_StdCell.v
  ```
  - Keep the `-v` stdcell line — do not delete it

---

## RTL Simulation

```bash
cd lab0/01_RTL
chmod +x 01_run
./01_run
```

After simulation, a `.fsdb` waveform file is generated in the same folder.

---

## Synthesis

```bash
cd ../02_SYN
chmod +x 01_syn
./01_syn
```

- After synthesis completes, type `exit` in the dc_shell prompt
- Outputs:
  - `Report/check_design.txt`, `Report/check_timing.txt`
  - `Report/YourDesign_syn.timing`, `Report/YourDesign_syn.area`
  - `Netlist/YourDesign_syn.v` — used for gate-level simulation

---

## Gate-Level Simulation

```bash
cd ../03_GATESIM
chmod +x 01_run
./01_run
```

After simulation, a `.fsdb` waveform file is generated.

---

## Viewing Waveforms (nWave)

```bash
nWave &
```

1. **File → Open** — select your `.fsdb` file
2. Click the `.fsdb` file twice to load it
3. In the signal panel, select the signals you want to view → click **Apply**
4. **File → Save Signal** (Shift+S) to save signal layout as `signal.rc`
5. **File → Restore Signal** (R) to reload a saved layout

---

## Common Mistakes

| Issue | Fix |
|---|---|
| `analyze -format verilog` on `.sv` file | Change to `-format sverilog` |
| Compound reset condition in `always_ff` | Split into `if (!rst_n)` then `else if (sync_cond)` |
| Clock name mismatch | Rename clock port in your module to `clk` |
| Missing stdcell `-v` line in `03_GATESIM/file.f` | Keep the `-v /share1/tech/...` line |