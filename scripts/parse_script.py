#!/usr/bin/env python

import getopt
import sys
import logging
import os
from datetime import datetime
import yaml

from DocketParse import docket_parse

def create_folders(dest_path):
  """
  Input: Destination path
  Inside: Creates directories in the destination that will be needed for the
          parsing.
  """
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)

  dirs = ["complete/", "failed_sections/", "stitched/"]
  for dir in dirs:
    if not os.path.exists(dest_path + dir):
      os.makedirs(dest_path + dir)




def run():
  # Set up parameters and directories

  usage_string = "user$ parse_script.py -s <source_path> -d <destination_path> [-l <logfile_path>]"

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:d:l:")
  except:
    print("Options error")
    print(usage_string)
    sys.exit(2)

  print("opts:")
  print(opts)

  for opt, arg in opts:
    if opt=="-h":
      print("""
      Usage:
      {}

      Script parses dockets in a given source directory, transforming them
      from pdfs to xml. The xml tree identifies sections of the docket and
      parses certain sections in more detail.

      Options:
      -h:   Help. This message.
      -s:   Path of the source directory, where the docket pdfs are.
      -d:   Path of the destination directory, where parsed documents and
            logs will be created.
      -l:   Path of logging file.
      """.format(usage_string))
    if opt=="-s":
      source_path = arg
    if opt=="-d":
      assert arg[-1] == "/", "Directory name should end with '/'"
      destination_path = arg
    if opt=="-l":
      logfile_path = arg

  create_folders(destination_path)
  docket_parse.start_logger(logfile_path)

  #PDF2Stitch
  pdf2stitched_start = datetime.now()
  stitched_destination = destination_path + "stitched/"
  successes_and_total = docket_parse.pdf_directory_to_stitched_xml(source_path, stitched_destination)
  pdf2stitched_end = datetime.now()
  pdf2stitch_time = pdf2stitched_end - pdf2stitched_start
  logging.info(""""pdf2stitched complete.
Total time: {0}
Dockets per second: {1}""".format(pdf2stitch_time,
                                  successes_and_total["dockets"]/pdf2stitch_time.seconds))

  #Stitch2CompleteParses
  stitch2complete_start = datetime.now()
  grammar_modules = [{"section_name": "Case_Information",
                      "module_name": "case_info_grammar"},
                     {"section_name": "Defendant_Information",
                      "module_name": "defendant_info_section_parse"},
                     {"section_name": "Disposition_Sentencing_Penalties",
                      "module_name": "disposition_section_parse"}]
  successes_and_total = docket_parse.stitched_xml_to_complete_xml(stitched_destination, destination_path + "complete/", grammar_modules)
  stitch2complete_end = datetime.now()
  stitch2complete_time = stitch2complete_end - stitch2complete_start
  logging.info("""stitch2complete completed.
Total time: {0}
Dockets per microsecond: {1}""".format(stitch2complete_time,
                                  successes_and_total["dockets"]/stitch2complete_time.microseconds))

  print("End.")

if __name__=="__main__":
  run()

