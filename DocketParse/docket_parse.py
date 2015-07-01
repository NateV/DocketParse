import DocketParse.sectionize
# import defendant_info_section_parse
# import disposition_section_parse
import pytest
import DocketParse.grammar_modules

import importlib
from lxml import etree
import os
import glob
import logging

def start_logger(file_name, custom_level=logging.DEBUG):
  """
  Must call this method before pdf_directory_to_stitched_xml and
  stitched_xml_to_complete_xml, so that those methods can use the logger
  that this method starts.

  There's something unattractive about using logger in a stateful way, but
  that seems to be how it is designed to work, so...
  """
  logging.basicConfig(filename=file_name, level=custom_level)

def docket_name_from_path(path):
  """
  Input: The path of a criminal docket. i.e. "texts/CP-51-CR-00000001-2011.txt"
  Output: The docket's name, i.e. "CP-51-000000001-2011"
  Note: If the path has extra info ("CP-51-CR-00000001-2011_modified.txt"),
        the docket's name will have the extra text too, in this case "_modified"
  """
  return os.path.split(path)[1][:-4]

def save_file(dest, file_name_format, docket_name, text):
  """
  Input: 1) The path for saving a file with % for interpolation,
         2) The end of the file, including format,
         3) The name of the docket,
         4) The text to save
  Output: Nothing, but the method saves the file.
  Ex. save_file("%s../sectionized_texts/" % destination,
                "%s_paginated.xml",
                docket_name_from_path(docket_pdf),
                paginated_text)
  """
  #print("Saving %s" % dest + (file_name_format % docket_name))
  with open(dest + (file_name_format.format(docket_name)), "w+") as f:
    f.write(text)
  f.close()

def log_successes_and_failures(successes_and_failures, which_method):
  logging.info("""
##Successes and failures for {3}:
| Successes | Failures | Total |
|-----------|----------|-------|
| {0} | {1} | {2} |
""".format(successes_and_failures["successes"],
           successes_and_failures["dockets"] - successes_and_failures["successes"],
           successes_and_failures["dockets"]),
           which_method)
  logging.info("    Success ratio: **{}**\n".format(successes_and_failures["successes"]/successes_and_failures["dockets"]))

def pdf_directory_to_stitched_xml(directory, destination):
  """
  Input: 1) A directory of pdf files that are criminal record dockets.
         2) A directory for the stitched xml files to be saved in.
  Inside: Uses Sectionize.parse and Sectionize.stitch to
          a) Turn the pdfs to text
          b) Turn the text to xml
          c) Stitch the xml text together.
  Output: a log of the success and failure of the procedure.
  """
  successes_and_failures = {"dockets": 0,
                            "successes": 0}
  path = directory + "*.pdf"
  files_iterator = glob.iglob(path)
  for docket_pdf in files_iterator:
    logging.info("  *Parsing %s*\n" % docket_name_from_path(docket_pdf))
    successes_and_failures["dockets"] += 1
    try:
      paginated = sectionize.parse(docket_pdf) # PDF to raw text, then to xml
                                               # that includes the pages of
                                               # the original pdf.
      #  Commented because I don't want to save all of them.  But
      #  it could be useful to turn back on for debugging at some point.
      #save_file("%s../sectionized_texts/" % destination, "%s_paginated.xml",docket_name_from_path(docket_pdf), paginated)
      #
      try:
        stitched = sectionize.stitch(paginated).decode('utf-8').replace("&","&amp;")
        save_file(destination, "%s_stitched.xml",docket_name_from_path(docket_pdf), stitched)
        successes_and_failures["successes"] += 1
      except:
        logging.warning("Sectionize.stitch failed for %s" % docket_name_from_path(docket_pdf))
        save_file("%s../sectionized_texts/" % destination, "%s_paginated.xml",docket_name_from_path(docket_pdf), paginated)
    except:
      logging.warning("Sectionize.parse failed for %s" % docket_name_from_path(docket_pdf))
  log_successes_and_failures(successes_and_failures, "pdf2stitched")
  return successes_and_failures

def stitched_xml_to_complete_xml(directory, destination, section_grammars):
  """
  Input: 1) A directory of xml files of the form [docket_name]_stitched.xml
         2) A destination directory
         3) TODO: Sections grammars. A list of dicts of the form
            {section_name: string, grammar_module_for_the_section: string}
  Inside: Parses particular sections using section grammar modules.
          (these modules have a grammar and NodeVisitor for parsing a
           particular section of a docket)
          Saves the files as [docket_name]_complete.xml
  Output: A log of the success and failure of the procedure.
  """
  successes_and_failures = {"dockets": 0,
                            "successes": 0}
  path = directory + "*_stitched.xml"
  files_iterator = glob.iglob(path)
  for stitched_xml_file in files_iterator:
    #   SUMMARY
    #I. open the stitched xml with lxml directly as an etree
    #II. Parse each section that needs to be parsed.
    #  A. Grab the raw section from the stitched xml.
    #  B. Try to parse the raw section.
    #  C. Replace the parsed section with the raw section's text.
    #III. Save the complete file.

    successes_and_failures["dockets"] += 1
    logging.info("  *Now Parsing: %s*\n" % docket_name_from_path(stitched_xml_file.replace("_stitched","")))
    #I. open the stitched xml with lxml directly as an etree

    stitched_etree = etree.parse(stitched_xml_file)

    #II. Parse each section that needs to be parsed.
    try:
      for section_grammar in section_grammars:
        __import__("grammar_modules." + section_grammar["module_name"])
        module = getattr(grammar_modules, section_grammar["module_name"])

        try:
          #  A. Grab the raw section from the stitched xml.
          section = stitched_etree.xpath("//section[@name='%s']" % section_grammar["section_name"])[0].text.strip()
          #  B. Try to parse the raw section.

          try:
            parsed_text = module.parse(section)
            #  C. Replace the parsed section with the raw section's text.
            try:
              parsed_xml = etree.fromstring(parsed_text)
              stitched_etree.xpath("//section[@name='%s']" % section_grammar["section_name"])[0].text = ""
              stitched_etree.xpath("//section[@name='%s']" % section_grammar["section_name"])[0].append(parsed_xml)
            except Exception as e:
              logging.warning("Failed at replacing etree node.")
              logging.warning(e)
              raise Exception("etree_error", section_grammar["section_name"])
          except Exception as e:
            if "etree_error" in e.args:
              raise e
            else:
              logging.warning("Could not parse %s section." % section_grammar["section_name"])
              save_file("{}../failed_sections/".format(destination), "{}_failed.txt",docket_name_from_path(stitched_xml_file), section)
              raise Exception("parsing_error", section_grammar["section_name"])
        except Exception as e:
          if "etree_error" in e.args or "parsing_error" in e.args:
            raise e
          else:
            logging.warning("Could not find %s section." % section_grammar["section_name"])
            raise Exception("finding_section_error", section_grammar["section_name"])
    except Exception as e:
      logging.warning("Failed parsing section grammars.")
      logging.warning(e.args)
    else:
      successes_and_failures["successes"] += 1
      #III. Save the complete file.
      output_text = etree.tostring(stitched_etree, pretty_print=True)
      os.remove(stitched_xml_file)
      save_file(destination, "%s_complete.xml", docket_name_from_path(stitched_xml_file), output_text.decode('utf-8'))
  log_successes_and_failures(successes_and_failures, "stitched_sections2complete_xml")
  return successes_and_failures