# airbag
Airbag is an effort to bring the convenience of debugging exceptions you find
in modern web frameworks to every python program.  The hope 

# Usage
Similar to pdb, you can wrap you script's execution in the shell.  That is:

python -m airbag yourscript.py

Any unhandled exceptions will be generate a crash report automatically which 
opens a browser.


# Install

pip install git+git://github.com/boyd/airbag.git@master
