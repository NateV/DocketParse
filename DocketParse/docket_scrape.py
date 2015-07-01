from parsimonious import Grammar
from parsimonious import NodeVisitor
from lxml import etree
import os
import glob
import re
import io
from collections import OrderedDict

import sectionize
import defendant_info_section_parse
import disposition_section_parse

class DocketRecord:
  """
  A bean for holding the info I want to scrape from dockets.
  """

  def __init__(self):
    self.docket_number = ""
    self.defendant_name = ""
    self.birth_date = ""
    self.sequence_description = ""
    self.sequence_date = ""
    self.offense_disposition = ""
    self.program = ""
    self.period = ""
    self.judge_name = ""


  def set_docket_number(self, docket_number): self.docket_number = docket_number
  def set_defendant_name(self, name): self.defendant_name = name
  def set_birth_date(self, date): self.birth_date = date
  def set_sequence_description(self, desc): self.sequence_description = desc
  def set_sequence_date(self, date): self.sequence_date = date
  def set_offense_disposition(self, dispo): self.offense_disposition = dispo
  def set_program(self, program): self.program = program
  def set_period(self, period): self.period = period
  def set_judge_name(self, name): self.judge_name = name

  def set_all(self, record):
    """ Sets all the variables that are keys in the record """
    self.docket_number = record["docket_number"] if "docket_number" in record else ""
    self.defendant_name = record["defendant_name"] if "defendant_name" in record else ""
    self.birth_date = record["birth_date"] if "birth_date" in record else ""
    self.sequence_description = record["sequence_description"] if "sequence_description" in record else ""
    self.sequence_date = record["sequence_date"] if "sequence_date" in record else ""
    self.offense_disposition = record["offense_disposition"] if "offense_disposition" in record else ""
    self.program = record["program"] if "program" in record else ""
    self.period = record["period"] if "period" in record else ""
    self.judge_name = record["judge_name"] if "judge_name" in record else ""

  def get_docket_number(self): return self.docket_number
  def get_defendant_name(self): return self.defendant_name
  def get_birth_date(self): return self.birth_date
  def get_sequence_description(self): return self.sequence_description
  def get_sequence_date(self): return self.sequence_date
  def get_offense_disposition(self): return self.offense_disposition
  def get_program(self): return self.program
  def get_period(self): return self.period
  def get_judge_name(self): return self.judge_name

  def get_all(self):
    """ Returns a dict of all the info in the object. """
    all = OrderedDict()
    all["docket_number"] = self.docket_number
    all["defendant_name"] = self.defendant_name
    all["birth_date"] = self.birth_date
    all["sequence_description"] = self.sequence_description
    all["sequence_date"] = self.sequence_date
    all["offense_disposition"] = self.offense_disposition
    all["program"] = self.program
    all["judge_name"] = self.judge_name
    all["period"] = self.period
    return all

  def copy(self):
    new_record = DocketRecord()
    new_record.set_all(self.get_all())
    return new_record

  def print_nicely(self):
    return """
               ---------
               Docket: {0},
               Defendant: {1},
               Birth: {2},
               Sequence Description: {3},
               Sequence Date: {4},
               Offense Disposition: {5},
               Program: {6},
               Judge: {7},
               Period: {8}
               ---------
           """.format(*self.get_all().values())

class DocketScraper:

  def __init__(self, pdf_directory, destination, db_name):
    self.pdf_directory = pdf_directory
    self.destination = destination
    self.db_name = db_name
    self.log_name = "log.md"
    if os.path.exists(self.destination + self.log_name):
      os.remove(self.destination + self.log_name)

  def log(self, message):
    message = message + "\n"
    with open(self.destination + self.log_name, "ab+") as f:
      f.write(message.encode("utf-8"))
    f.close()

  def get_list_of_dockets(self):
    """
    Input: a directory
    Output: an iterator of the files in the director.
    TODO: Make the glob pattern more restrictive. Right now it just assumes
          that all pdfs in the directory are dockets.
    """
    #path = directory + '[A-Z]{2}-[0-9]{2}-[A-Z]{2}-[0-9]{7}-[0-9]{4}\.pdf'
    path = self.pdf_directory + "*.pdf"
    files_iterator = glob.iglob(path)
    return files_iterator
    #[{"name":os.path.split(file)[1] ,"rel_path":file} for file in files]

  def save_stitched_sections(self, docket_name, sections):
    """
    Input: The name of a docket and the text of the docket parsed into xml
           and then stitched together (pages removed and sections that
           extended across multiple pages combined.
    Effect: Save the parsed and stitched xml docket to the destination directory.
    """
    file_name = "%s_stitched.xml" % docket_name
    with open(self.destination + file_name, "w+") as f:
      f.write(sections.encode('utf-8'))
    f.close()

  def one_docket_to_xml(self, docket_path):
    """
    Input: The relative path to one docket.
    Output: The xml of the parsed docket.
    """
    text = self.one_docket_pdf_to_text(docket_path)
    pages = self.one_docket_text_to_pages(text)
    stitched = self.one_docket_pages_to_stitched_sections(stitched)




  def dockets_to_xml(self):
    """
    Goes through all the dockets in the directory of dockets and parses all
    those dockets using the section grammars.
    Input: Nothing.
    Inside: Parses all the dockets in the directory to xml, including parsing
            the sections.
            Saves all the dockets and creates a log.
    Output: A hash of the successes and failures.
    """
    successes_and_failures = {"dockets": 0,
                              "successes": 0,
                              "failures": 0}

    for docket_path in self.get_list_of_dockets():
      successes_and_failures["dockets"] += 1
      docket_name = os.path.split(docket_path)[1]
      try:
        file_name = "%s_complete.xml" % docket_name
        with open(self.destination + file_name) as f:
          f.write(self.one_docket_to_xml(docket_path))
        f.close()
        successes_and_failures["successes"] += 1
      except:
        successes_and_failures["falures"] += 1
        print("Failure with %s" % docket_name)



#   def scrape(self):
#     """
#     Input: 1) a directory with docket pdfs in it and
#            2) a directory for parsed dockets to be saved to
#            3) name of a database in the destination where scraped info
#               should be saved.
#     Inside: 1) parses dockets in the directory,
#             2) saves parsed dockets as xml in the destination
#             3) adds info to a database
#             4) Logs to the destination
#     Output: A list of saved records.
#     """
#     records_to_save = []
#     dockets_iterator = self.get_list_of_dockets()
#     dockets_iterator_counter = 0
#     #Set up database. Do this later.
#
#     for docket_name in dockets_iterator:
#       self.log("###Parsing: %s" % docket_name)
#       dockets_iterator_counter += 1
#       parent_docket = DocketRecord()
#
#       docket_path = docket_name
#
#       print("\n\n\n\n\nParsing: %s " % docket_path)
#
#       #Pull information from the sectionized docket
#       try:
#         sections = sectionize.parse(docket_path)
#         stitched_sections = sectionize.stitch(sections).decode("utf-8")
#         self.save_stitched_sections(docket_name, stitched_sections)
#       except:
#         self.log("\n\nDocket **%s** did not parse\n\n" % docket_name)
#
#       parser = etree.XMLParser(remove_blank_text=True)
#
#       stitched_file_object = io.StringIO(stitched_sections.strip().replace("&","&amp;"))
#       stitched_etree = etree.parse(stitched_file_object, parser).getroot()
#
#       try:
#         parent_docket.set_docket_number(stitched_etree.xpath("//docket_number/text()")[0].strip())
#         print("docket_number: %s" % parent_docket.get_docket_number())
#       except:
#         self.log("Could not find docket number.")
#
#       try:
#         parent_docket.set_defendant_name(stitched_etree.xpath("//defendant/text()")[0].strip())
#         print("defendant_name: %s" % parent_docket.get_defendant_name())
#       except:
#         self.log("Could not find defendant name.")
#
#
#       #Process additional sections of the docket that are not parsed in
#       # sectionize.py
#       #1) Get the birth date from the Defendant Info Section
#       try:
#         defendant_info_section = stitched_etree.xpath("//section[@name='Defendant_Information']")[0].text.strip()
#       except:
#         self.log("Could not find defendant information section.")
#
#       try:
#         defendant_info_parsed_text = defendant_info_section_parse.parse(defendant_info_section)
#       except:
#         self.log("Could not parse defendant information section.")
#
#       defendant_info_parsed_object = io.StringIO(defendant_info_parsed_text.strip().replace("&","&amp;"))
#       defendant_info_parsed_xml = etree.parse(defendant_info_parsed_object, parser).getroot()
#
#       try:
#         parent_docket.set_birth_date(defendant_info_parsed_xml.xpath("//birth_date/text()")[0].strip())
#         print("Birth date: %s" % parent_docket.get_birth_date())
#       except:
#         self.log("Could not find the birth date.")
#
#       #2) Get the guilty info, if any, from the Disposition Section
#
#       #  a) Parse the disposition section
#       print("---Parsing disposition section---")
#       try:
#         disposition_section = stitched_etree.xpath("//section[@name='Disposition_Sentencing_Penalties']")[0].text.strip()
#       except:
#         self.log("Could not find Disposition section.")
#
#       try:
#         disposition_parsed_text = disposition_section_parse.parse(disposition_section)
#       except:
#         self.log("Could not parse disposition section.")
#
#       disposition_parsed_object = io.StringIO(disposition_parsed_text.strip().replace("&","&amp;"))
#       disposition_parsed_xml = etree.parse(disposition_parsed_object, parser).getroot()
#
#       #  b) Get all the sequences that involve guilty dispositions
#       #TODO: The issue here is that I only want sequence entries where
#
#       try:
#         guilty_sequences = disposition_parsed_xml.xpath("//sequence[contains(./offense_disposition, 'Guilty') and (judge_action/sentence_info/length_of_sentence)]")
#         print("---Docket has %d sequences with guilty dispositions---" % len(guilty_sequences))
#       except:
#         self.log("Could not find guilty sequences.")
#
#       #  c) For each sequence with a guilty disposition, create a docket record.
#       #     N.B. We are assuming here that only the first judge action is the
#       #     important one.
#       #     I'm making this assumption because people may violate the terms of
#       #     their sentence and go back to the judge for changes to the terms,
#       #     but only the original sentence is important for the research
#       #     I want to do here.
#       #
#       #     So there will only be one record per sequence, even though there
#       #     may be multiple judge actions.
#
#       for sequence in guilty_sequences:
#
#         temp_record = DocketRecord()
#
#         #Docket Number
#         temp_record.set_docket_number(parent_docket.get_docket_number())
#
#         #Defendant's Name
#         temp_record.set_defendant_name(parent_docket.get_defendant_name())
#
#         #Defendant's Birth Date
#         temp_record.set_birth_date(parent_docket.get_birth_date())
#
#         #Sequence Description and continuation, if any
#         try:
#           description = sequence.xpath("./sequence_description")[0].text.strip()
#           description_cont = " ".join([description_continued.text.strip() for description_continued in sequence.xpath(".//sequence_description")])
#           description += " " + description_cont
#           print("Sequence_description: %s " % description)
#           temp_record.set_sequence_description(description)
#         except:
#           self.log("Could not find sequence description.")
#
#         #Disposition
#         try:
#           disposition = sequence.xpath("./offense_disposition")[0].text.strip()
#           temp_record.set_offense_disposition(disposition)
#           print("Disposition: %s" % disposition)
#         except:
#           self.log("Could not find the offense disposition.")
#
#         #Get the first judge action for convenience
#         #N.B. This should be the first judge action that involved sentencing the defendant.
#         try:
#           first_judge_action = sequence.xpath("//judge_action[sentence_info/length_of_sentence]")[0]
#           print("First Judge Action:")
#           print(etree.tostring(first_judge_action))
#
#           #Date of the action.
#           try:
#             temp_record.set_sequence_date(first_judge_action.xpath("./date")[0].text.strip())
#             print("Action date: %s" % temp_record.get_sequence_date())
#           except:
#             self.log("Could not find the date.")
#
#           #Name of judge on original sentence
#           try:
#             temp_record.set_judge_name(first_judge_action.xpath("./judge_name")[0].text.strip())
#             print("Judge name: %s" % temp_record.get_judge_name())
#           except:
#             self.log("Could not find the judge's name.")
#
#           #Length of original sentence
#           try:
#             temp_record.set_period(first_judge_action.xpath("./sentence_info/length_of_sentence/min_length/time")[0].text.strip() + " " + \
#                                    first_judge_action.xpath("./sentence_info/length_of_sentence/min_length/unit")[0].text.strip())
#             print("Min length of sentence: %s" % temp_record.get_period())
#           except:
#             self.log("Could not find the sentence length.")
#
#           #Program for original sentence
#           try:
#             temp_record.set_program(first_judge_action.xpath("./sentence_info/program")[0].text.strip())
#             print("Program: %s" % temp_record.get_program())
#           except:
#             self.log("Could not find program.")
#         except:
#           self.log("Could not find the first judge action.")
#
#         records_to_save.append(temp_record)
#
#     #END OF LOOP THROUGH DOCKETS_ITERATOR
#
#     print("\n\n==============\nRecords to save:")
#     [print("\n" + str(record.print_nicely()) + "\n") for record in records_to_save]
#     [self.log("\n" + str(record.print_nicely()) + "\n") for record in records_to_save]
#     num_records_parsed = len(records_to_save)
#     num_records_failed = dockets_iterator_counter - num_records_parsed
#     self.log("""
#                 ##Dockets tested: %s
#                 ##Dockets parsed: %s
#                 ##Dockets failed: %s
#                 ##Success ratio: %s
#              """ % (dockets_iterator_counter, num_records_parsed, \
#                     num_records_failed, \
#                     num_records_parsed/dockets_iterator_counter))
#     return records_to_save