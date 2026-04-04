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


## Compressing a Directory

**Linux/macOS** (`compress.sh`):
```bash
bash compress.sh <source_dir> <output_name>
# e.g. bash compress.sh hw1_sorter/design hw1
# produces hw1.tar.gz
```

**Windows PowerShell** (`compress.ps1`):
```powershell
powershell -ExecutionPolicy Bypass -File .\compress.ps1 -Source <source_dir> -OutputName <output_name>
# e.g. powershell -ExecutionPolicy Bypass -File .\compress.ps1 -Source .\hw1_sorter\design -OutputName hw1
# produces hw1.zip
```

## Vivado Usage
- Part name: `xc7a200tfbg676-1`
- Cell usage: open synthesized design, then run in Tcl Console: `report_utilization -cells [get_cells]`