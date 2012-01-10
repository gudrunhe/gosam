# vim: ts=3:sw=3:expandtab

import os
import re
try:
   import readline
except ImportError:
   readline = None

import atexit
import glob

class InteractiveShell:
   def __init__(self,
         prompt="? ",
         history_file=None,
         completer_delims=None,
         follow_set={}):

      if readline is not None:
         readline.parse_and_bind("tab: complete")

      if history_file is not None:
         self.init_history(os.path.expanduser(
            os.path.join("~", history_file)))
      else:
         self._histfile = None

      self.set_prompt(prompt)
      self._followset = follow_set

      if completer_delims is not None:
         self._delims = completer_delims
         if readline is not None:
            readline.set_completer_delims(completer_delims)
            readline.set_completer(self.completer_function)
         pat = ""
         for delim in self._delims:
            if delim in ["[", "\\", "]", "^", "-"]:
               pat += "\\" + delim
            else:
               pat += delim
         self._delim_pat = re.compile("[" + pat + "]")


   def completer_function(self, text, state):
      if state == 0:
         buf = readline.get_line_buffer()
         lt = len(text)
         lb = len(buf)
         pred = buf[0:lb-lt]

         parts = self._delim_pat.split(pred)

         follow_sel = ""
         for part in parts:
            spart = part.strip()
            if spart != "":
               follow_sel = spart
               break

         if follow_sel in self._followset:
            follow = self._followset[follow_sel]
         else:
            follow = []

         continuations = []
         for f in follow:
            if f == " file":
               continuations.extend(file_continuations(text))
               pass
            elif f.startswith(text):
               continuations.append(f)

         self._continuations_cache = continuations

      if state < len(self._continuations_cache):
         return self._continuations_cache[state]
      else:
         return None

   def set_prompt(self, prompt):
      self._prompt = prompt

   def get_prompt(self):
      return self._prompt

   def init_history(self, file_name):
      self._histfile = file_name
      if readline is not None:
         try:
            readline.read_history_file(self._histfile)
         except IOError:
            pass
      atexit.register(self.save_history)

   def save_history(self):
      if self._histfile is not None and readline is not None:
         readline.write_history_file(self._histfile)

   def run(self):
      exit_loop = False
      while not exit_loop:
         try:
            buf = ""
            line = raw_input(self._prompt)
            while line.rstrip().endswith("\\"):
               buf += line.rstrip()[:-1]
               line = raw_input("... ")
            buf += line
            exit_loop = not self.event(buf)
         except EOFError:
            print("")
            exit_loop = True
      self.onexit()

   def insert_text(self, *lines):
      buf = ""
      for line in lines:
         if line.rstrip().endswith("\\"):
            buf += line.rstrip()[:-1]
         else:
            buf += line
            result = self.event(buf)
            if not result:
               return False
            buf = ""
      return True

   def get_history(self, stub=""):
      if readline is None:
         return []

      l = readline.get_current_history_length()
      result = []
      for i in range(l):
         hist = readline.get_history_item(i)
         if hist is None:
            continue
         if hist.startswith(stub):
            result.append(hist)
      return result

   def event(self, line):
      return True

   def onexit(self):
      pass

def file_continuations(text):
   path, stub = os.path.split(
         os.path.expanduser(text))

   if len(path) == 0:
      actual_path = "."
   else:
      actual_path = path
      actual_path = os.path.expandvars(actual_path)

   result = []
   add_path = len(path) != 0
   for f in os.listdir(actual_path):
      if f.startswith(stub):
         actual_file = os.path.join(actual_path, f)
         if os.path.isdir(actual_file):
            suffix = os.sep
         else:
            suffix = " "


         if add_path:
            display = os.path.join(path, f + suffix)
         else:
            display = f + suffix
         result.append(display)

   #if len(result) == 0:
   #         result.append(text)
   return result

