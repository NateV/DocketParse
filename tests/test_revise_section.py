from lxml import etree
from DocketParse.revise_section import revise_section, revise_directory, add_suffix
import shutil

def test_revise_section():
  tree = etree.parse("tests/testDocs/test_revise_dockets/CP-51-CR-0000001-2011_incomplete.xml")
  tree = revise_section(tree, "Case_Information","case_info_grammar")
  with open("tests/testDocs/test_revise_dockets/CP-51-CR-0000001-2011_complete.xml","w") as f:
    f.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))
  f.close()

  parsed_section = tree.getroot().xpath("/docket/section[@name='Case_Information']")[0]
  #print(etree.tostring(parsed_section))
  assert tree.getroot().xpath("/docket/section[@name='Case_Information']/case_info/date_filed/text()")[0].strip() == "01/03/2011"

def test_add_suffix():
  file_name = "something.xml"
  suffix = "_else"
  assert add_suffix(file_name, suffix) == "something_else.xml"

def test_revise_directory():
  src = "tests/testDocs/test_revise_dockets/CP-51-CR-0000001-2011_incomplete.xml"
  dest = "tests/testDocs/test_revise_dockets/directory_test/CP-51-CR-0000001-2011.xml"
  shutil.copy(src, dest)

  dest_dir = "tests/testDocs/test_revise_dockets/directory_test/"
  counter, successes = revise_directory(dest_dir, "Case_Information", "case_info_grammar")
  root = etree.parse(dest).getroot()
  assert root.xpath("/docket/section[@name='Case_Information']/case_info/date_filed/text()")[0].strip() == "01/03/2011"
  assert counter == 1
  assert successes == 1