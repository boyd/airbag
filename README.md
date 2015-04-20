# airbag
Python exception module to help debug crashes in a web browser.

# Usage
Similar to pdb, you can wrap you script's execution in the shell.  That is:

python -m airbag yourscript.py

Any unhandled exceptions will be generate a crash report automatically which 
opens a browser.
