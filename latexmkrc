# http://tex.stackexchange.com/questions/11710/specify-output-directory-when-using-latexmk
$pdflatex="pdflatex -interaction errorstopmode -shell-escape %O %S";
$out_dir = 'out';
$pdf_mode = 1;

@BIBINPUTS = ( ".", ".." );
$ENV{TEXINPUTS} .="${search_path_separator}media";
# @default_files = (
#  'pre-proposal.tex',
# );

$pdf_previewer = 'xdg-open %S';
