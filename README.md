## Recommended VSCode Extensions

- **Ruff** (`charliermarsh.ruff`) — Python linter and formatter
- **LaTeX Workshop** (`james-yu.latex-workshop`) — LaTeX editing, compilation, and preview

## Writing LaTeX in VSCode (like Overleaf)

You can write and compile LaTeX documents directly in VSCode.

### What to Install

1. **MiKTeX** — the LaTeX compiler for Windows. Download from [miktex.org](https://miktex.org/download). It auto-installs missing packages on first use.
2. **LaTeX Workshop** extension — install from the VSCode Extensions marketplace.

### How to Use

- Create a `.tex` file and start writing
- Press `Ctrl+Alt+B` to build (compile)
- Press `Ctrl+Alt+V` to open the PDF preview side by side
- `Ctrl+click` on the PDF jumps to the matching source line

### Example

```latex
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
```

Save the file and it will compile automatically.

## Part Name
`xc7a200tfbg676-1`

## How to Obtain Cell Usage
* Open synthesied design or report utilization
* Run the command to Tcl Console: `report_utilization -cells [get_cells]`