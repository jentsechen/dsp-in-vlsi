## To Do
 - Update report based on results of ADFP
 - Solve high fan-out problem
 - Try higher clock rate

## How to Run Design Verification
```bash
cd verification
python gen_test_case.py
```

## ADFP

### RTL Simulation

`01_run` must use `-sverilog` instead of `+v2k` for SystemVerilog files:
- Original: `vcs -f file.f -full64 -R +v2k -debug_access+all +define+RTL +notimingcheck`
- Updated:  `vcs -f file.f -full64 -R -sverilog -debug_access+all +define+RTL +notimingcheck`

Simulation results:

![tb_Sort8](./diagram/adfp/tb_Sort8.png)
![tb_SelectTopK](./diagram/adfp/tb_SelectTopK.png)

### Synthesis

Timing report:

![](./diagram/adfp/timing_report_0.png)
![](./diagram/adfp/timing_report_1.png)

Area report:

![](./diagram/adfp/area_report.png)