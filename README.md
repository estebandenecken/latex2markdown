# LaTeX to Markdown translator
> tex2md

A lightweight Python script that converts LaTeX `.tex` files to Markdown `.md`, handling sections, equations, figures, citations, and common formatting commands.

## Features

- **Section headings** — converts `\section`, `\subsection`, and `\subsubsection` (including starred variants) to the corresponding `#`, `##`, and `###` Markdown headings.
- **Math equations** — wraps `equation`, `gather`, `align`, `alignat` environments (and their starred forms) in `$$...$$` display math blocks.
- **Figures** — strips `\begin{figure}` / `\end{figure}` wrappers and converts `\includegraphics` to `![Image](path)` syntax.
- **Citations** — replaces `\cite{key}` calls with sequential numeric references `[1]`, `[2]`, etc., compacting consecutive numbers into ranges like `[1-4, 8]`, and appends a numbered reference list at the end of the document.
- **Text formatting** — converts `{\bf ...}` to `**bold**` and `{\it ...}` to `*italic*`.
- **Labels & captions** — converts `\label{...}` to `\tag{...}` and strips the `\caption{}` wrapper, keeping the caption text.
- **GUI file picker** — launches a Tkinter dialog so you can select any `.tex` file without touching the command line.

----
## Usage

### GUI mode (default)

Run the script directly; a file-picker dialog will open:

```bash
python tex2md.py
```

Select a `.tex` file and the converted `.md` file will be written to the same directory with the same base name.

### Programmatic / scripted use

Import and call `latex_to_markdown` directly:

```python
from tex2md import latex_to_markdown

latex_to_markdown("paper.tex", "paper.md")
```

----
## Supported LaTeX constructs

| LaTeX | Markdown output |
|---|---|
| `\section{Title}` | `# Title` |
| `\subsection{Title}` | `## Title` |
| `\subsubsection{Title}` | `### Title` |
| `\begin{equation}` … `\end{equation}` | `$$` … `$$` |
| `\begin{align}` … `\end{align}` | `$$` … `$$` |
| `\includegraphics[…]{path}` | `![Image](path)` |
| `\cite{key1, key2}` | `[1, 2]` |
| `{\bf text}` | `**text**` |
| `{\it text}` | `*text*` |
| `\label{id}` | `\tag{id}` |
| `\caption{text}` | `text` |

----
## Limitations

- Nested or multi-line LaTeX commands may not convert correctly — the script uses single-pass regex substitutions.
- The bibliography list is populated with citation keys only; actual reference metadata (authors, title, journal, etc.) is not resolved. You will need to fill in the details manually or from your `.bib` file.
- Complex table environments (`tabular`, `longtable`, etc.) are not converted.
- Custom macros and user-defined commands are not expanded.

----