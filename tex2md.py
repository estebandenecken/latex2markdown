# >---------------------------------------------------------------------< #
# LaTeX to Markdown 
# Esteban Denecken C.
# >---------------------------------------------------------------------< #
"""
This script reads a LaTeX text file, converts sections, equations, images and citations to Markdown, and writes the modified text to a new file

"""
# >---------------------------------------------------------------------< #
import re
import os
import tkinter as tk
from tkinter import filedialog

# >---------------------------------------------------------------------< #

def compact_number_list(numbers):
    """
    Given a list of integers, returns a compact string like '1-4, 8, 10-12'
    """
    numbers = sorted(set(numbers))
    if not numbers:
        return ""
    ranges = []
    start = prev = numbers[0]

    for n in numbers[1:]:
        if n == prev + 1:
            prev = n
        else:
            # Handle the previous range
            if prev == start:
                ranges.append(f"{start}")
            elif prev == start + 1:
                ranges.append(f"{start}, {prev}")
            else:
                ranges.append(f"{start}-{prev}")
            start = prev = n

    # Add the final range
    if prev == start:
        ranges.append(f"{start}")
    elif prev == start + 1:
        ranges.append(f"{start}, {prev}")
    else:
        ranges.append(f"{start}-{prev}")

    return ", ".join(ranges)

def latex_to_markdown(input_file, output_file):
    """
    Reads a LaTeX text file, converts sections, equations, images and citations to Markdown,
    and writes the modified text to a new file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # - - - Citations replacement - - - #
    # Dictionary to store citation keys and assigned numbers
    citation_numbers = {}
    next_number = 1

    # Function called for each \cite{...} match
    def replace_cite(match):
        nonlocal next_number
        cite_content = match.group(1)
        keys = [k.strip() for k in cite_content.split(',')]

        numbers = []
        for key in keys:
            if key not in citation_numbers:
                citation_numbers[key] = next_number
                next_number += 1
            numbers.append(citation_numbers[key])

        # Compact ranges like [1-3, 5]
        compact = compact_number_list(numbers)
        return f"[{compact}]"

    # Replace all \cite{...} occurrences
    text = re.sub(r'\\cite\{([^}]*)\}', replace_cite, text)
    # text = re.sub(r'\\cite\{(.*?)\}', r'<sub>\1</sub>', text)
    
    # - - - LaTeX sections replacements - - - #
    text = re.sub(r'\\section\{(.*?)\}', r'# \1', text)
    text = re.sub(r'\\subsection\{(.*?)\}', r'## \1', text)
    text = re.sub(r'\\subsubsection\{(.*?)\}', r'### \1', text)
    text = re.sub(r'\\section\*\{(.*?)\}', r'# \1', text)
    text = re.sub(r'\\subsection\*\{(.*?)\}', r'## \1', text)
    text = re.sub(r'\\subsubsection\*\{(.*?)\}', r'### \1', text)

    # - - - Equations replacements - - - #
    text = re.sub(r'\\begin\{equation\}', r'$$', text)
    text = re.sub(r'\\end\{equation\}', r'$$', text)
    text = re.sub(r'\\begin\{gather\}', r'$$', text)
    text = re.sub(r'\\end\{gather\}', r'$$', text)
    text = re.sub(r'\\begin\{align\}', r'$$', text)
    text = re.sub(r'\\end\{align\}', r'$$', text)
    text = re.sub(r'\\begin\{equation\*\}', r'$$', text)
    text = re.sub(r'\\end\{equation\*\}', r'$$', text)
    text = re.sub(r'\\begin\{gather\*\}', r'$$', text)
    text = re.sub(r'\\end\{gather\*\}', r'$$', text)
    text = re.sub(r'\\begin\{align\*\}', r'$$', text)
    text = re.sub(r'\\end\{align\*\}', r'$$', text)
    text = re.sub(r'\\begin\{alignat\*\}', r'$$', text)
    text = re.sub(r'\\end\{alignat\*\}', r'$$', text)

    # - - - Figures replacements - - - #
    text = re.sub(r'\\begin\{figure\}', r'', text)
    text = re.sub(r'\\end\{figure\}', r'', text)
    text = re.sub(r'\\includegraphics\[(.*?)\]\{([^}]*)\}', r'![Image](\2)', text)

    # - - - Other LaTeX replacements - - - #
    text = re.sub(r'\\label\{(.*?)\}', r'\\tag{\1}', text)
    text = re.sub(r'\{\\bf (.*?)\}', r'**\1**', text)
    text = re.sub(r'\{\\it (.*?)\}', r'*\1*', text)
    text = re.sub(r'\\reffig\{Fig(.*?)\}', r'Fig. \1', text)
    text = re.sub(r'\\reftab\{Tab(.*?)\}', r'Table \1', text)
    text = re.sub(r'\\caption\{(.*?)\}', r'\1', text)

    # - - - Append reference list - - - #
    references_md = "\n\n## References\n"
    for key, num in sorted(citation_numbers.items(), key=lambda x: x[1]):
        references_md += f"[{num}] {key}\n"

    text += references_md

    # - - - Write Markdown output - - - #
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Converted LaTeX to Markdown: '{input_file}' → '{output_file}'.")


# >---------------------------------------------------------------------< #

# LaTeX to Markdown conversion
if __name__ == "__main__":
    # Hide the root Tk window
    root = tk.Tk()
    root.withdraw()

    # Open file selection dialog
    input_file = filedialog.askopenfilename(
        title="Select LaTeX file",
        filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
    )

    if not input_file:
        print("No file selected. Exiting.")
        exit(0)

    # Generate output file name
    base, _ = os.path.splitext(input_file)
    output_file = base + ".md"

    latex_to_markdown(input_file, output_file)


# >---------------------------------------------------------------------< #
