# -*- coding: utf-8 -*-

from DocketParse import sectionize
import lxml.etree as etree
import re

class TestSectionize:

  def setup_method(self, method):
    self.docket_to_parse = "CP-51-CR-0000025-2011"
    # "CP-51-CR-0005731-2011"
    self.this_dockets_number_of_sections = 14
    #"CP-51-CR-0000001-2011"


  def test_pdf_to_text(self):
    text = sectionize.pdf_to_text("tests/testDocs/testPDFs/%s.pdf" % self.docket_to_parse)
    isinstance(text, str)

  def test_parse(self):
    docket_xml_text = sectionize.parse("tests/testDocs/testPDFs/%s.pdf" % self.docket_to_parse)
    docket_xml = etree.XML(docket_xml_text)
    with open("tests/testDocs/sectionized_dockets/%s.xml" % self.docket_to_parse, "w+", encoding="utf-8") as f:
      f.write(etree.tostring(docket_xml, pretty_print=True).decode('utf-8'))
    f.close()
    docket_number = docket_xml.xpath("//docket_number/text()")[0].strip()
    print("Docket-number: " + docket_number)
    match = re.search('.*(%s).*' % self.docket_to_parse, docket_number)
    assert match.group(1) == self.docket_to_parse

  def test_stitch(self):
    raw_xml_text = sectionize.parse("tests/testDocs/testPDFs/%s.pdf" % self.docket_to_parse)
    stitched_text = sectionize.stitch(raw_xml_text)

    #So as I can check what I done.
    with open("tests/testDocs/sectionized_dockets/stitched_%s.xml" % self.docket_to_parse, "w+", encoding="utf-8") as f:
      f.write(stitched_text.decode(encoding='utf-8'))
    f.close()


    stitched_xml = etree.XML(stitched_text)
    sections = stitched_xml.xpath("//section")


    assert len(sections) == self.this_dockets_number_of_sections



  #A helper
  def validate_structured_text(self, text):
    xmlschema_doc = etree.parse(sectionize.schema)
    xml_schema = etree.XMLSchema(xmlschema_doc)
    xml_tree = etree.parse(StringIO(text))
    if xml_schema(xml_tree):
      return "Correctly structured."
    else:
      error = xml_schema.error_log.last_error
      return error

