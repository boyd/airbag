import bdb
import json
import os
import pprint
import sys
import time
import tempfile
import traceback
import webbrowser


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
HTML_FILE_PATH = os.path.join(ROOT_PATH, "airbag.html")
JS_FILE_PATH = os.path.join(ROOT_PATH, "airbag.js")


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

class ExceptionReporter(object):
  def __init__(self, exc_type, exc_value, tb):
    self.exc_type = exc_type
    self.exc_value = exc_value
    self.tb = tb

  def get_template_context(self):
    crash_data = dict(
      frames=self.get_traceback_frames(),
      environ=self.get_environ(),
    )
    return {
      'exc_type': self.exc_type.__class__.__name__,
      'exc_value': self.exc_value,
      'handlebar_data': json.dumps(crash_data, indent=4),
    }

  def render_html(self):
    template = open(HTML_FILE_PATH).read()
    ctx = self.get_template_context()
    ctx["inline_airbag_javascript"] = open(JS_FILE_PATH).read()
    return template % ctx 

  def _get_source_code(self, frame, max_lines):
    try:
      with open(frame['filename'], 'rb') as f:
        source = f.read().splitlines()
    except (OSError, IOError):
      return None

    lower_bound = max(0, frame['lineno'] - max_lines)
    upper_bound = frame['lineno'] + max_lines

    return {
      'start_lineno' : lower_bound,
      'source_context' : source[lower_bound:upper_bound],
    }

  def _get_renderable_dict(self, dictionary):
    renderable_dict = {}
    for name, value in dictionary.items():
      renderable_dict [str(name)] = str(value)[:10000]
    return renderable_dict

  def is_airbag_reset_point(self, tb_frame):
      return isinstance(tb_frame.f_locals.get('self'), AirbagRunner)

  def get_traceback_frames(self):
    frames = []
    tb = self.tb
    while tb is not None:
      frame = {
        'filename': tb.tb_frame.f_code.co_filename,
        'func_name': tb.tb_frame.f_code.co_name,
        'lineno': tb.tb_lineno - 1,
        'variables': self._get_renderable_dict(tb.tb_frame.f_locals)
      }

      source_code =  self._get_source_code(frame , 7)

      if source_code is not None:
        frame.update(source_code)
        frames.append(frame)

      if self.is_airbag_reset_point(tb.tb_frame):
        frames = []

      tb = tb.tb_next

    return frames

  def get_environ(self):
    return self._get_renderable_dict(os.environ)


def generate_crash_report(exctype=None, value=None, tb=None):
  if (exctype==None and value==None, tb==None):
    (exc_type, exc_value, exc_traceback) = sys.exc_info()

  reporter = ExceptionReporter(exctype, value, tb)
  report_file = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False)
  report_file.write(reporter.render_html())
  report_file.flush()

  webbrowser.open_new_tab('file://' + report_file.name)
  sys.__excepthook__(exctype, value, tb)


def enable():
  sys.excepthook = generate_crash_report
