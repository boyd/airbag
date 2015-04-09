import os.path
import sys

from .airbag import enable, AirbagRunner


def main():
  if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
    print "usage: airbag.py scriptfile [arg] ..."
    sys.exit(2)

  mainpyfile = sys.argv[1] # Get script filename
  if not os.path.exists(mainpyfile):
    print 'Error:', mainpyfile, 'does not exist'
    sys.exit(1)

  del sys.argv[0]  # Hide "airbag" from argument list

  enable()

  airbag = AirbagRunner()
  airbag._runscript(mainpyfile)


# When invoked as main program, invoke the debugger on a script
if __name__ == '__main__':
  main()
