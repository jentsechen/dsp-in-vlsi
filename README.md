## ADFP Flow (RTL Sim / Synthesis / Gate-Level Sim)

See [adfp_flow.md](adfp_flow.md) for the full workflow guide.

---

## Recommended VSCode Extensions
- **Ruff** (`charliermarsh.ruff`) — Python linter and formatter
- **LaTeX Workshop** (`james-yu.latex-workshop`) — LaTeX editing, compilation, and preview
- **Verilog-HDL/SystemVerilog** (`mshr-h.veriloghdl`) — Verilog/SystemVerilog syntax, linting, and formatting via Verible

## Writing LaTeX in VSCode

### What to Install
1. **MiKTeX** — the LaTeX compiler for Windows. Download from [miktex.org](https://miktex.org/download). It auto-installs missing packages on first use.
2. **LaTeX Workshop** extension — install from the VSCode Extensions marketplace.

### How to Use

- Create a `.tex` file and start writing
- Press `Ctrl+Alt+B` to build (compile)
- Press `Ctrl+Alt+V` to open the PDF preview side by side
- `Ctrl+click` on the PDF jumps to the matching source line


## Tools

### Compress

**Linux/macOS** (`tools/compress.sh`):
```bash
bash tools/compress.sh <source_dir> <output_name>
# e.g. bash tools/compress.sh hw1_sorter/design tmp/hw1
# produces tmp/hw1.tar.gz
```

**Windows PowerShell** (`tools/compress.ps1`):
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\compress.ps1 -Source <source_dir> -OutputName <output_name>
# e.g. powershell -ExecutionPolicy Bypass -File .\tools\compress.ps1 -Source .\hw1_sorter\design -OutputName tmp\hw1
# produces tmp\hw1.zip
```

### Run Scripts on ADFP Server

```bash
cb && bash run.sh rtl_sim <folder>
cb && bash run.sh syn     <folder>
cb && bash run.sh gl_sim  <folder>
# e.g. cb && bash run.sh rtl_sim hw3
# e.g. cb && bash run.sh syn     hw3
# e.g. cb && bash run.sh gl_sim  hw3
```

Requires `<folder>.zip` and the unzipped `<folder>/` to be in the same directory.
If the zip is newer than the folder, the folder is removed and re-unzipped automatically.

## Vivado Usage
- Part name: `xc7a200tfbg676-1`
- Cell usage
    - open synthesized design, then run in Tcl Console: `report_utilization -cells [get_cells]`