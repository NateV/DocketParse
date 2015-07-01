from docket_scrape import DocketScraper
from docket_scrape import DocketRecord
import re





class TestDocketScrape:

  def setup_method(self, method):
    self.directory = "./testDocs/testPDFs/"
    self.destination = "./testDocs/ScrapeOutput/"
    self.db_name = "scraped_info.db"
    self.scraper = DocketScraper(self.directory, self.destination, self.db_name)


  def test_get_list_of_dockets(self):
    dockets_list = self.scraper.get_list_of_dockets()
    pattern = re.compile(".*\.pdf")
    assert pattern.match(next(dockets_list))



#   def test_dockets_to_xml(self):
#     self.scraper.dockets_to_xml()


#   def test_scrape(self):
#     self.scraper.scrape()


class TestDocketRecord:

  def testCopy(self):
    record = DocketRecord()
    record.set_docket_number = "CP-30-CM-452520-2014"
    record.set_defendant_name = "Bill Smith"
    record.set_birth_date = "01/01/2015"
    record.set_sequence_description = "Ate a cow too fast"
    record.set_sequence_date = "06/24/5891"
    record.set_offense_disposition = "Guilty"
    record.set_program = "Dieting"
    record.set_period = "Max 7.00 years"
    other_record = record.copy()
    assert id(record) != id(other_record)