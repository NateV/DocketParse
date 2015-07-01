from datetime import datetime
from sectionize import pdf_to_text, parse
import glob
import logging

def just_pdf2text():
  """
  Hmm. With 115 dockets, this finished in 3 seconds, for .026 seconds per docket.
  this suggests that the problem is not the pdf2text, but in text2stitched. :(
  """
  print("Testing time of pdf to text.")
  directory = "./testDocs/test_two/pdfs/*.pdf"
  iter = glob.iglob(directory)
  start = datetime.now()
  counter = 0
  for file in iter:
    pdf_to_text(file)
    counter += 1
  end = datetime.now()
  print("Finished.")
  duration = (end-start).seconds
  print("Processed {} dockets in {} seconds.".format(counter, duration))
  print("{} seconds per docket.".format(duration/counter))
  print("Thanks for playing our game.")

def just_parse():
  """"
  This is the slow one.  For 115 dockets, it took 80 seconds, or .76 seconds
  per docket.  This is the stumbling block in the whole thing.  Why is this
  method so slow?!
  """
  logging.basicConfig(filename="parse_timing.md", level=logging.DEBUG)
  logging.info("pdf2text_time, create_grammar_time, parse_grammar_time, node_visitor_time")
  print("Testing time of parse(), which includes pdf2text.")
  directory = "./testDocs/test_two/pdfs/*.pdf"
  iter = glob.iglob(directory)
  start = datetime.now()
  counter = 0
  for file in iter:
    parse(file)
    counter += 1
  end = datetime.now()
  print("Finished.")
  duration = (end-start).seconds
  print("Processed {} dockets in {} seconds.".format(counter, duration))
  print("{} seconds per docket.".format(duration/counter))
  print("Thanks for playing our game.")

just_parse()


