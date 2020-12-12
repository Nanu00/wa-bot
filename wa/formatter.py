#!/bin/python

import re, api, subprocess
from latex import build_pdf

a = api.WaResponse(open('appid').readline().strip('\n'))

a.getUsrQues(input('>> '), podstate='Step-by-step solution', format='mathml')
a.getResp()
a.parseResp()

final_latex = r'''\documentclass{article}
\author{wa-bot}

\renewcommand{\baselinestretch}{1.5}
\usepackage[cm]{fullpage}
\usepackage[utf8]{inputenc}
\usepackage[document]{ragged2e}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

\pagenumbering{gobble}

\arraycolsep=1pt\def\arraystretch{1.2}

\begin{center}
'''

for i in a.latex:
    latex = str(i)

    p = re.compile(r'\\text{([^{]*?)}\\text{([^{]*?)}')
    m = p.search(latex)

    while m:
        print(m.group(1))
        latex = p.sub('\\\\text{ ' + m.group(1) + m.group(2) + '}', latex, 1)
        m = p.search(latex)

    latex = re.sub(r'\s+', r' ', latex)
    latex = re.sub(r'\\\\ ', r'\\\\\n', latex)

    latex = latex.strip()

    final_latex += latex

final_latex += r'''
\end{center}

\end{document}
'''

print(final_latex)

with open('test.tex', 'w') as latex_file:
    latex_file.write(final_latex)

subprocess.run(['latexmk', '-verbose', '-shell-escape', '-synctex=1', '-file-line-error', '-interaction=nonstopmode', '-pdf', 'test.tex'])

subprocess.run(['pdftocairo', '-png', '-rx',  '300', '-ry', '300', '-transp', 'test.pdf', 'test'])

subprocess.run(['magick', 'test-1.png', '-quality', '100', '-density', '300', '-trim', '-alpha', 'deactivate', '-negate', 'test-1.png'])
