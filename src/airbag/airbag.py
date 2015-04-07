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


class ExceptionReporter(object):
  def __init__(self, exc_type, exc_value, tb):
    self.exc_type = exc_type
    self.exc_value = exc_value
    self.tb = tb

  def get_template_context(self):
    return {
      'exc_type' : self.exc_type.__class__.__name__,
      'exc_value' : self.exc_value,
      'frames_json' : json.dumps(dict(frames=self.get_traceback_frames()), indent=4),
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

  def _get_variables(self, tb_frame):
    var_strs = {}
    for name, value in tb_frame.f_locals.items():
      var_strs[str(name)] = str(value)[:10000]
    return var_strs

  def get_traceback_frames(self):
    frames = []
    tb = self.tb
    while tb is not None:
      frame = {
        'filename' : tb.tb_frame.f_code.co_filename,
        'func_name' : tb.tb_frame.f_code.co_name,
        'lineno' : tb.tb_lineno - 1,
        'variables' : self._get_variables(tb.tb_frame),
      }
      source_code =  self._get_source_code(frame , 7)

      if source_code is not None:
        frame.update(source_code)
        frames.append(frame)
      tb = tb.tb_next

    return frames


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
