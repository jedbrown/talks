(TeX-add-style-hook
 "bp3-2020"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "standalone"
    "standalone10"
    "mathspec"
    "tikz"
    "pgfplots"))
 :latex)

