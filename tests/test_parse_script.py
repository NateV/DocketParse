

import DocketParse.parse_script as ps
import os
import shutil

def test_create_folders():
  destination = "tests/testDocs/test_three/"
  if os.path.exists(destination):
    shutil.rmtree(destination)
  assert not os.path.exists(destination + "complete/")
  ps.create_folders(destination)
  assert os.path.exists(destination + "complete/")


def test_parse_script_on_directory():
  source = "tests/testDocs/testPDFs/"
  destination = "tests/testDocs/test_four/"
  if os.path.exists(destination):
    shutil.rmtree(destination)
  logfile = "log.md"
  os.system("python DocketParse/parse_script.py -s {} -d {} -l {}".format(source, destination, logfile))