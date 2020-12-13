#!/bin/python

import re, api, subprocess
from latex import build_pdf

a = api.WaResponse(open('appid').readline().strip('\n'))

a.getUsrQues(input('>> '), podstate='Step-by-step solution', format='mathml')
a.getResp()
a.parseResp()

final_latex = r'''\documentclass{article}

\renewcommand{\baselinestretch}{1.5}
\usepackage[cm]{fullpage}
\usepackage[utf8]{inputenc}
\usepackage[document]{ragged2e}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{seqsplit}

\begin{document}

\pagenumbering{gobble}

\arraycolsep=1pt\def\arraystretch{1.2}

\begin{center}

'''

substitutions = {
        r'\\mathrm\{integral\}' : r'\\int',
        # r'\\text\{ right bracketing bar \}' : r'\\right|',
        # r'\\text\{ left bracketing bar \}' : r'\\left|',
        r'\\text\{ left bracketing bar \}' : r'|',
        r'\\text\{ right bracketing bar \}' : r'|',
}


for i in a.latex:
    latex = str(i)

    p = re.compile(r'\\text{([^{]*?)}\\text{([^{]*?)}')
    m = p.search(latex)

    while m:
        print(m.group(1))
        # latex = p.sub('\\\\text{' + m.group(1) + m.group(2) + '}', latex, 1)
        latex = p.sub('$' + m.group(1) + m.group(2) + '$', latex, 1)
        m = p.search(latex)

    latex = re.sub(r'\s+', r' ', latex)
    latex = re.sub(r'\\\\ ', r'\\\\\n', latex)
    latex = re.sub(r'''[^\|a-zA-Z\{\}\s%\./\-:;,0-9@=\\"'\(\)_~\$\!&\`\?+#\^<>\[\]\*]''', r'', latex)

    for j in substitutions:
        latex = re.sub(j, substitutions[j], latex)

    latex = latex.strip()

    final_latex += '\section{Solution ' + str(a.latex.index(i) + 1) + '}\n' + latex + '\n\n'

final_latex += r'''
\end{center}

\end{document}
'''

print(final_latex)

with open('test.tex', 'w') as latex_file:
    latex_file.write(final_latex)

subprocess.run(['latexmk', '-verbose', '-shell-escape', '-synctex=1', '-file-line-error', '-interaction=nonstopmode', '-pdf', 'test.tex'])
subprocess.run(['latexmk', '-c', '-pdf', 'test.tex'])
subprocess.run(['pdftocairo', '-png', '-rx',  '500', '-ry', '500', '-transp', 'test.pdf', 'test'])
subprocess.run(['magick', 'test-1.png', '-quality', '100', '-trim', '-alpha', 'deactivate', '-negate', 'test-1.png'])
