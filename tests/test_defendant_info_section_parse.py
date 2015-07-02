from lxml import etree
import io
import sectionize
import defendant_info_section_parse


class TestDefendantInfoSectionParse:

  def setup_method(self, method):
    self.docket = self.docket_to_test = "CP-51-CR-0000001-2011"
    self.birth_date = "07/24/1964"
    path = "tests/testDocs/testPDFs/%s.pdf" % self.docket_to_test
    text = sectionize.parse(path)
    sections = etree.XML(sectionize.stitch(text))
    self.section_text = sections.xpath("//section[@name='Defendant_Information']")[0].text.strip()
    with open("tests/testDocs/defendantSectionTexts/%s.txt" % self.docket_to_test, "w+") as f:
      f.write(self.section_text)
    f.close()

  def test_parse(self):
    section_parsed = defendant_info_section_parse.parse(self.section_text)
    parser = etree.XMLParser(remove_blank_text=True)
    file_object = io.StringIO(section_parsed.strip().replace("&","&amp;"))
    section_root = etree.parse(file_object, parser).getroot()

    #save parsed xml
    with open("tests/testDocs/defendantSectionTexts/section_%s.xml" % self.docket_to_test, "w+") as f:
      f.write(etree.tounicode(section_root, pretty_print=True))
    f.close()

    birth_date = section_root.xpath("//birth_date")[0].text.strip()
    assert birth_date == self.birth_date

