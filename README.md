# prescad
Openscad without the spaghetti

Prescad is a 'language' which allows you to write openscad scripts in a coherent, maintainable way. I put 'language' in quotes beacuse it's really a preprocessor with the soul of a Perl script, but it works well in practice.

To use prescad, first write your .prescad file, then run prescad.py passing it the name of your file as an argument, and it will output a valid .scad file which you can then run openscad on.

The format of a .prescad file starts with beginning of the file will be copied verbatim into the beginning of the .scad file. That's where you should put all scalar constant assignments and reused modules. After that follows the fixed string !PRESCAD! followed by the meat of the prescad script.

The final part of a .prescad file consists of one command per line. Each line except the last one follows the format:

variable = expression

Expression can be anything which results in a mesh. Expressions can refer to previously assigned variables, and variables can be overwritten. When a variable has been assigned repeatedly, the most recent assignment is the one which is used.

Blank lines can also be included, and comments can be included by using // which comments out everything on the line after them. Leading and trailing whitespace gets trimmed.

It's very very important that variable names not be substrings of anything which might appear in an expression, including and especially other variable names.

The very last line of the script is simply an expression which is the output of the script as a whole.
