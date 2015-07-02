from DocketParse import docket_parse
import os
import pytest
import logging

class TestDocketParse:

  @pytest.mark.order1
  def test_logging_setup(self):
    logger_file = "tests/testDocs/try_docket_parse/docket_parse_test.md"
    if os.path.exists(logger_file):
      os.remove(logger_file)
    docket_parse.start_logger("tests/testDocs/try_docket_parse/docket_parse_test.md")


  @pytest.mark.order2
  def test_pdf_directory_to_stitched_xml(self):
    logging.info("""
    ===========================
    Testing pdf_directory_to_stitched_xml
    ===========================
    """)
    directory = "tests/testDocs/try_docket_parse/pdfs/"
    destination = "tests/testDocs/try_docket_parse/stitched/"
    results = docket_parse.pdf_directory_to_stitched_xml(directory, destination)
    assert results["dockets"] == results["successes"]
    assert len(os.listdir(destination)) == results["dockets"] + 1 #.DS_Store is in there too.


  @pytest.mark.order3
  def test_stitched_xml_to_complete_xml(self):
    logging.info("""
    ===========================
    Testing stitched_xml_to_complete_xml
    ===========================
    """)
    directory = "tests/testDocs/try_docket_parse/stitched/"
    destination = "tests/testDocs/try_docket_parse/complete/"
    grammar_modules = [{"section_name": "Defendant_Information",
                        "module_name": "defendant_info_section_parse"},
                        {"section_name": "Disposition_Sentencing_Penalties",
                         "module_name": "disposition_section_parse"}]
    results = docket_parse.stitched_xml_to_complete_xml(directory, destination, grammar_modules)
    assert results["dockets"] == results["successes"]
    assert len(os.listdir(destination)) == results["dockets"] + 1 #.DS_Store is in there too.

