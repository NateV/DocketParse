import DocketParse.sectionize as sectionize
from DocketParse.grammar_modules import disposition_section_parse
from lxml import etree
import re
import pytest
import io

class TestDispositionSectionParse:

  def setup_method(self, method):
    self.docket_to_test = "CP-51-CR-0000025-2011"
    self.first_guilty_program = "Confinement"
    self.first_guilty_program_length = '1'
    # "CP-51-CR-0005730-2011" :)
    # "CP-51-CR-0005729-2011"
    # "CP-51-CR-0005728-2011"
    # "CP-51-CR-0000001-2011"
    # "CP-51-CR-0005727-2011"
    # "CP-51-CR-0005731-2011"
    # "CP-51-CR-0000101-2011"
    # "CP-51-CR-0005727-2011"
    # "CP-51-CR-0000018-2011"
    path = "./testDocs/testPDFs/%s.pdf" % self.docket_to_test
    text = sectionize.parse(path)
    sections = etree.XML(sectionize.stitch(text))
    self.section_text = sections.xpath("//section[@name='Disposition_Sentencing_Penalties']")[0].text.strip()
    with open("./testDocs/dispositionSectionTexts/%s.txt" % self.docket_to_test, "w+") as f:
      f.write(self.section_text)
    f.close()

  def test_parse(self):
#     print("-----")
#     print(self.section_text)
#     print("-----")
    section_parsed = disposition_section_parse.parse(self.section_text)
    parser = etree.XMLParser(remove_blank_text=True)
    file_object = io.StringIO(section_parsed.strip().replace("&","&amp;"))
    section_root = etree.parse(file_object, parser).getroot()

    #save parsed xml
    with open("./testDocs/dispositionSectionTexts/section_%s.xml" % self.docket_to_test, "w+") as f:
      f.write(etree.tounicode(section_root, pretty_print=True))
    f.close()

#   collect a lot of disposition subsections.
#     with open("./testDocs/dispositionDetailsCollection.py", "a+") as f:
#        for details in section_root.xpath("//disposition_details"):
#          f.write("r\"\"\"\n #" + self.docket_to_test + "\n" + details.text + "\n\"\"\",\n")
#     f.close()
    first_program = section_root.xpath("//sequence[judge_action/sentence_info/program]/judge_action/sentence_info/program")[0].text.strip()
    assert first_program == self.first_guilty_program
    first_program_length = section_root.xpath("//sequence[judge_action/sentence_info/program]/judge_action/sentence_info/length_of_sentence/min_length/time")[0].text.strip()
    assert first_program_length == self.first_guilty_program_length

  def test_clean_headers(self):
    headers_cleaned = disposition_section_parse.clean_headers(self.section_text)

    with open("./testDocs/dispositionSectionTexts/section_%s_noheaders.txt" % self.docket_to_test, "w+") as f:
      f.write(headers_cleaned)
    f.close()

    #assert len(headers_cleaned.split('\n'))== (len(self.section_text.split('\n')) - 0)
