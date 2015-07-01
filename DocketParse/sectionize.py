# -*- coding: utf-8 -*-

import lxml.etree as etree
from parsimonious import Grammar
from parsimonious import NodeVisitor
import os
from datetime import datetime
import logging

# #SCHEMA
# schema = StringIO('''\
# <?xml version="1.0" encoding="utf-8"?>
# <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
#            elementFormDefault="qualified">
#   <xs:element name="docket">
#
#
#
#   </xs:element>
# </xs:schema>
# ''')

#Grammar
grammar_list = [
r"""
###
#  This grammar separates dockets into sections. It goes a little more into the
#  details of the case info section than necessary. It may be a good idea
#  later to take that out and move it to a separate sub-grammar and
#  sub-NodeVisitor.
###
docket = page+
page = header body? footer page_break?

header = ws* court_name new_line line docket_number line line line line caption
court_name = ~"COURT OF COMMON PLEAS OF PHILADELPHIA COUNTY"i
docket_number = content new_line?
caption = commonwealth_line line line defendant_line
commonwealth_line = ws* ~"Commonwealth of Pennsylvania"i ws* new_line
defendant_line = content new_line


body = ((section !start_of_footer)* section) /
       ((line !start_of_footer)* line) /
       (line body)
section = section_case_info /
          section_related_cases /
          section_status_info /
          section_calendar_events /
          section_confinement_info /
          section_defendant_info /
          section_case_participants /
          section_bail_info /
          section_charges /
          section_disposition_sentencing /
          section_commonwealth_info /
          section_entries /
          section_payment_plan /
          section_case_financial_info



section_case_info = (ws* ~"CASE INFORMATION"i new_line) section_body
section_related_cases = (ws* ~"RELATED CASES"i new_line) section_body
section_status_info = (ws* ~"STATUS INFORMATION"i new_line) section_body
section_calendar_events = (ws* ~"calendar events"i new_line)  section_body
section_confinement_info = (ws* ~"CONFINEMENT INFORMATION") section_body
section_defendant_info =  (ws* ~"defendant information"i new_line) section_body
section_case_participants = (ws* ~"case participants"i new_line) section_body
section_bail_info = (ws* ~"bail information"i new_line) section_body
section_charges = (ws* ~"charges"i new_line) section_body

section_disposition_sentencing = (ws* ~"disposition sentencing/penalties"i new_line) section_disposition_sentencing_body
section_disposition_sentencing_body = section_body

section_commonwealth_info =  (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) section_body
section_entries = (ws* ~"entries"i new_line)  section_body
section_payment_plan = (ws* ~"payment plan summary"i new_line) section_body
section_case_financial_info = (ws* ~"case financial information"i new_line) section_body

section_body = (line &end_of_section) / ((line !end_of_section)+ line)
#This revision is meant to deal with sections that have just the header on a
# page, followed by the footer, and no content in the section.
# section_body = (line !end_of_section)+ line

end_of_section = start_of_footer / next_section_header

next_section_header = (ws* ~"CASE INFORMATION"i new_line) /
                      (ws* ~"RELATED CASES"i new_line) /
                      (ws* ~"STATUS INFORMATION"i new_line) /
                      (ws* ~"calendar events"i new_line) /
                      (ws* ~"CONFINEMENT INFORMATION") /
                      (ws* ~"defendant information"i new_line) /
                      (ws* ~"case participants"i new_line) /
                      (ws* ~"bail information"i new_line) /
                      (ws* ~"charges"i new_line) /
                      (ws* ~"disposition sentencing/penalties"i new_line) /
                      (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) /
                      (ws* ~"entries"i new_line) /
                      (ws* ~"payment plan summary"i new_line) /
                      (ws* ~"case financial information"i new_line)



start_of_footer = (ws* ~"CPCMS 9082" content new_line)
footer = start_of_footer line+

line = content new_line?

content = single_content_char*
single_content_char =  ~"[a-z0-9+`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i


new_line = "\n"
page_break = "\f"
ws = " "
""",
r"""
###
#  This grammar separates dockets into sections. It goes a little more into the
#  details of the case info section than necessary. It may be a good idea
#  later to take that out and move it to a separate sub-grammar and
#  sub-NodeVisitor.
###
docket = page+
page = header body? footer page_break?

header = ws* court_name new_line line docket_number line line line line caption
court_name = ~"COURT OF COMMON PLEAS OF PHILADELPHIA COUNTY"i
docket_number = content new_line?
caption = commonwealth_line line line defendant_line
commonwealth_line = ws* ~"Commonwealth of Pennsylvania"i ws* new_line
defendant_line = content new_line


body = ((section !start_of_footer)* section) /
       ((line !start_of_footer)* line) /
       (line body)
section = section_case_info /
          section_related_cases /
          section_status_info /
          section_calendar_events /
          section_confinement_info /
          section_defendant_info /
          section_case_participants /
          section_bail_info /
          section_charges /
          section_disposition_sentencing /
          section_commonwealth_info /
          section_entries /
          section_payment_plan /
          section_case_financial_info



section_case_info = (ws* ~"CASE INFORMATION"i new_line) section_body

##  DEPRECATED because section details should really only be parsed in separate
##  sections
# section_case_info_body = judge_assigned content new_line section_body
# judge_assigned = ws* ~"judge assigned:"i ws* judge_name?
# judge_name =  (single_content_char !~"date filed"i)+ single_content_char

section_related_cases = (ws* ~"RELATED CASES"i new_line) section_body
section_status_info = (ws* ~"STATUS INFORMATION"i new_line) section_body
section_calendar_events = (ws* ~"calendar events"i new_line)  section_body
section_confinement_info = (ws* ~"CONFINEMENT INFORMATION") section_body
section_defendant_info =  (ws* ~"defendant information"i new_line) section_body
section_case_participants = (ws* ~"case participants"i new_line) section_body
section_bail_info = (ws* ~"bail information"i new_line) section_body
section_charges = (ws* ~"charges"i new_line) section_body

section_disposition_sentencing = (ws* ~"disposition sentencing/penalties"i new_line) section_disposition_sentencing_body
section_disposition_sentencing_body = section_body

section_commonwealth_info =  (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) section_body
section_entries = (ws* ~"entries"i new_line)  section_body
section_payment_plan = (ws* ~"payment plan summary"i new_line) section_body
section_case_financial_info = (ws* ~"case financial information"i new_line) section_body


section_body = (line !end_of_section)+ line

end_of_section = start_of_footer / next_section_header

next_section_header = (ws* ~"CASE INFORMATION"i new_line) /
                      (ws* ~"RELATED CASES"i new_line) /
                      (ws* ~"STATUS INFORMATION"i new_line) /
                      (ws* ~"calendar events"i new_line) /
                      (ws* ~"CONFINEMENT INFORMATION") /
                      (ws* ~"defendant information"i new_line) /
                      (ws* ~"case participants"i new_line) /
                      (ws* ~"bail information"i new_line) /
                      (ws* ~"charges"i new_line) /
                      (ws* ~"disposition sentencing/penalties"i new_line) /
                      (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) /
                      (ws* ~"entries"i new_line) /
                      (ws* ~"payment plan summary"i new_line) /
                      (ws* ~"case financial information"i new_line)



start_of_footer = (ws* ~"CPCMS 9082" content new_line)
footer = start_of_footer line+

line = content new_line?

content = single_content_char*
single_content_char =  ~"[a-z0-9+`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i


new_line = "\n"
page_break = "\f"
ws = " "
""",
r"""
###
#  This grammar separates dockets into sections. It goes a little more into the
#  details of the case info section than necessary. It may be a good idea
#  later to take that out and move it to a separate sub-grammar and
#  sub-NodeVisitor.
###
docket = page+
page = header body? footer page_break?

header = ws* court_name new_line line docket_number line line line line caption
court_name = ~"COURT OF COMMON PLEAS OF PHILADELPHIA COUNTY"i
docket_number = content new_line?
caption = commonwealth_line line line defendant_line
commonwealth_line = ws* ~"Commonwealth of Pennsylvania"i ws* new_line
defendant_line = content new_line


body = ((section !start_of_footer)* section) /
       ((line !start_of_footer)* line) /
       (line body)
section = section_case_info /
          section_related_cases /
          section_status_info /
          section_calendar_events /
          section_confinement_info /
          section_defendant_info /
          section_case_participants /
          section_bail_info /
          section_charges /
          section_disposition_sentencing /
          section_commonwealth_info /
          section_entries /
          section_payment_plan /
          section_case_financial_info



section_case_info = (ws* ~"CASE INFORMATION"i new_line) section_case_info_body
section_case_info_body = judge_assigned content new_line section_body
judge_assigned = ws* ~"judge assigned:"i ws* judge_name
judge_name =  (single_content_char !~"date filed"i)+ single_content_char

section_related_cases = (ws* ~"RELATED CASES"i new_line) section_body
section_status_info = (ws* ~"STATUS INFORMATION"i new_line) section_body
section_calendar_events = (ws* ~"calendar events"i new_line)  section_body
section_confinement_info = (ws* ~"CONFINEMENT INFORMATION") section_body
section_defendant_info =  (ws* ~"defendant information"i new_line) section_body
section_case_participants = (ws* ~"case participants"i new_line) section_body
section_bail_info = (ws* ~"bail information"i new_line) section_body
section_charges = (ws* ~"charges"i new_line) section_body

section_disposition_sentencing = (ws* ~"disposition sentencing/penalties"i new_line) section_disposition_sentencing_body
section_disposition_sentencing_body = section_body

section_commonwealth_info =  (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) section_body
section_entries = (ws* ~"entries"i new_line)  section_body
section_payment_plan = (ws* ~"payment plan summary"i new_line) section_body
section_case_financial_info = (ws* ~"case financial information"i new_line) section_body


section_body = (line !end_of_section)+ line

end_of_section = start_of_footer / next_section_header

next_section_header = (ws* ~"CASE INFORMATION"i new_line) /
                      (ws* ~"RELATED CASES"i new_line) /
                      (ws* ~"STATUS INFORMATION"i new_line) /
                      (ws* ~"calendar events"i new_line) /
                      (ws* ~"CONFINEMENT INFORMATION") /
                      (ws* ~"defendant information"i new_line) /
                      (ws* ~"case participants"i new_line) /
                      (ws* ~"bail information"i new_line) /
                      (ws* ~"charges"i new_line) /
                      (ws* ~"disposition sentencing/penalties"i new_line) /
                      (ws* ~"commonwealth information"i ws* ~"attorney information"i new_line) /
                      (ws* ~"entries"i new_line) /
                      (ws* ~"payment plan summary"i new_line) /
                      (ws* ~"case financial information"i new_line)



start_of_footer = (ws* ~"CPCMS 9082" content new_line)
footer = start_of_footer line+

line = content new_line?

content = single_content_char*
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i

#content = ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]*"i

new_line = "\n"
page_break = "\f"
ws = " "
"""
]

#NodeVisitor
class DocketVisitor(NodeVisitor):
  def generic_visit(self, node, vc):
    return self.stringify_list(vc)

  def visit_docket(self, node, vc):
    docket = " <docket> %s </docket> " % self.stringify_list(vc)
    return docket

  def visit_page(self, node, vc):
    page = " <page> %s </page> " % self.stringify_list(vc)
    return page

  def visit_header(self, node, vc):
    header = self.stringify_list(vc)
    return (" <header> %s </header> " % header)

  def visit_caption(self, node, vc):
#    print("visiting caption.")
    line = " <caption> %s </caption> " % self.stringify_list(vc)
    return line

  def visit_commonwealth_line(self, node, vc):
    line = " <state> %s </state> " % node.text
    return line

  def visit_defendant_line(self, node, vc):
#    print("visiting defendant line.")
    defendant = " <defendant> %s </defendant> " % self.stringify_list(vc)
    return defendant

  def visit_docket_number(self, node, vc):
    docket = self.stringify_list(vc)
#    print("visiting docket number.")
#    print(docket)
    try:
      index = docket.index(":")
#      print(index)
      docket = "%s <docket_number> %s </docket_number> " % (docket[0:index+1], docket[index+1:])
    except:
#      print("index not found.")
      docket = " <docket_number> % s</docket_number> " % docket
    return docket

  def visit_body(self, node, vc):
    body = " <body> %s </body> " % self.stringify_list(vc)
    return body

  def visit_footer(self, node, vc):
    footer = self.stringify_list(vc)
    footer = " <footer> %s </footer> " % footer
    return footer

  def visit_section(self, node, vc):
#    print("visiting section.")
    return self.stringify_list(vc)

# Methods related to the Case Information section
  def visit_section_case_info(self, node, vc):
#    print("visiting section case info")
    contents = self.stringify_list(vc)
    section_name = "Case_Information"
    contents = " <section name='%s'> %s </section> " % (section_name, contents)
    return contents

  def visit_section_case_info_body(self, node, vc):
#    print("Visiting Section case_info body.")
    contents = self.stringify_list(vc)
    return contents

  def visit_judge_assigned(self, node, vc):
#    print("visit_judge_assigned")
#    print(node.text)
    contents = self.stringify_list(vc)
    return ("<judge_assigned> %s </judge_assigned>" % contents)

  def visit_judge_name(self, node, vc):
#    print("visit_judge_name")
#    print(vc)
    contents = self.stringify_list(vc)
    return contents

#Methods for Related Cases section
  def visit_section_related_cases(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Related_Cases"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for status info section
  def visit_section_status_info(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Status_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for calendar events section
  def visit_section_calendar_events(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Calendar_Events"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for Confinement Info section
  def visit_section_confinement_info(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Confinement_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for defendant info section
  def visit_section_defendant_info(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Defendant_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for case participants section
  def visit_section_case_participants(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Case_Participants"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for Bail info section
  def visit_section_bail_info(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Bail_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods for charges section
  def visit_section_charges(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Charges"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods related to the Disposition Sentencing Section
  def visit_section_disposition_sentencing(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Disposition_Sentencing_Penalties"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods related to the Commonwealth Info Section
  def visit_section_commonwealth_info(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Commonwealth_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods related to the Entries Section
  def visit_section_entries(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Entries"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods related to the Payment Plan Section
  def visit_section_payment_plan(self, node, vc):
    contents = self.stringify_list(vc)
    section_name = "Payment_Plan"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Methods related to the Case Financial Information Section
  def visit_section_case_financial_info(self, node, vc):
#    print("Visiting section financial info.")
    contents = self.stringify_list(vc)
    section_name = "Financial_Information"
    return("<section name='%s'> %s </section>" % (section_name, contents))

#Terminals
  def visit_court_name(self, node, vc):
    return node.text

  def visit_section_header(self,node, vc):
    return node.text

  def visit_new_line(self, node, vc):
    return node.text

  def visit_content(self, node, vc):
    #return node.text
    return self.stringify_list(vc)

  def visit_single_content_char(self, node, vc):
    if node.text =="&":
      char = "&amp;"
    else:
      char = node.text
    return char

  #Helper method. Not for external use.
  def stringify_list(self, list):
    output = ""
    for element in list:
      output += element
    return output
# End of Class



def parse(path):
  """
  Parse a pdf docket into an xml document.
  This xml document will be of the form:
  <docket>
    <page>
      <caption> </caption>
      <body>
        <section name='a'> </section>
        <section name='b'> </section>
        ...
      </body>
      <footer> </footer>
    </page>
    <page>
      ...
    </page>
  </docket>
  ...

  This xml most closely resembles the original docket. (The caveat
  is that section names are removed from the text and turned into name
  attributes of the section xml elements).

  But some sections extend across pages, and this xml schema leves these
  sections separated from each other.


  TODO: Turn this into a real .xsd schema definition.
  """
  print("Starting parse {}".format(path)) #
  start = datetime.now() #
  docket_text = pdf_to_text(path)
  pdf2text_time = (datetime.now()-start).microseconds #
  start = datetime.now() #
  grammar = Grammar(grammar_list[0])
  create_grammar_time = (datetime.now()-start).microseconds #
  visitor = DocketVisitor()
  start = datetime.now() #
  root = grammar.parse(docket_text)
  parse_grammar_time = (datetime.now()-start).microseconds #
  start = datetime.now() #
  results = visitor.visit(root)
  node_visitor_time = (datetime.now()-start).microseconds #
  logging.info("{}, {}, {}, {}".format(pdf2text_time, create_grammar_time, parse_grammar_time, node_visitor_time))
  return results
  #return visitor.visit(root)


def stitch(xml_text):
  """
  Take a text that has been parsed into xml by this module's grammar and
  NodeVisitor, and then turn it into a xml text that looks like:

  <docket>
    <header> </header>
    <section> </section>
    <section> </section>
    ...
    <footer> </footer>
  </docket>
  """
  stitched_xml = etree.Element("docket")
  docket_xml = etree.XML(xml_text)
  #print(docket_xml.xpath("//header[1]")[0])
  stitched_xml.append(docket_xml.xpath("//header[1]")[0])

  sections = docket_xml.xpath("//section")
  combined_sections = []
  for section in sections:
    if len(combined_sections) != 0:
      #if the section last added to combined sections is the same kind of
      # section, then add the current section's text to the most recent
      # combined section's text.
      if section.xpath("@name") == combined_sections[-1].xpath("@name"):
        combined_sections[-1].text = "\n".join([combined_sections[-1].text.strip(), section.text.strip()])
      #else add the current section to the end of combined_sections
      else:
        combined_sections.append(section)
    else:
      combined_sections.append(section)


  [stitched_xml.append(section_node)  for section_node in combined_sections]

  return etree.tostring(stitched_xml, pretty_print=True)


#Helper functions
def pdf_to_text(path):
  """
  takes the path to a pdf and returns a UTF-8 encoded
  string of the pdf.
  """
  # PDF to text with:
  # >  pdftotext -layout -enc "UTF-8" [pdf file] [text file]
  assert path[-4:] == ".pdf"
  dest_file = path[:-4] + "_temp.txt"

  os.system('pdftotext -layout -enc "UTF-8" %s %s' % (path, dest_file))
  with open(dest_file, "r", encoding="utf-8") as f:
    docket_text = f.read()
  f.close()
  os.remove(dest_file)
  return docket_text