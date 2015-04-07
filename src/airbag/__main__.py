import bdb
import os.path
import sys

from .airbag import enable

class AirbagRunner(bdb.Bdb):
  def _runscript(self, filename):
    # The script has to run in __main__ namespace (or imports from
    # __main__ will break).
    #
    # So we clear up the __main__ and set several special variables
    # (this gets rid of pdb's globals and cleans old variables on restarts).
    import __main__
    __main__.__dict__.clear()
    __main__.__dict__.update({"__name__"    : "__main__",
                              "__file__"    : filename,
                              "__builtins__": __builtins__,
                             })
    cmd = 'execfile(%r)' % filename
    self.run(cmd)


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
