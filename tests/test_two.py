import docket_parse
import logging
from datetime import datetime

print("Parsing dockets from pdfs.")
filename = "./testDocs/test_two/test_two_log.md"
docket_parse.start_logger(filename)

pdf2stitched_start = datetime.now()
directory = "./testDocs/test_two/pdfs/"
destination = "./testDocs/test_two/stitched/"
successes_and_total = docket_parse.pdf_directory_to_stitched_xml(directory, destination)
pdf2stitched_end = datetime.now()
pdf2stitch_time = pdf2stitched_end - pdf2stitched_start
logging.info(""""pdf2stitched complete.
Total time: {0}
Dockets per second: {1}""".format(pdf2stitch_time,
                                  successes_and_total["dockets"]/pdf2stitch_time.seconds))

stitch2complete_start = datetime.now()
directory = "./testDocs/test_two/stitched/"
destination = "./testDocs/test_two/complete/"
grammar_modules = [{"section_name": "Defendant_Information",
                    "module_name": "defendant_info_section_parse"},
                    {"section_name": "Disposition_Sentencing_Penalties",
                     "module_name": "disposition_section_parse"}]
successes_and_total = docket_parse.stitched_xml_to_complete_xml(directory, destination, grammar_modules)
stitch2complete_end = datetime.now()
stitch2complete_time = stitch2complete_end - stitch2complete_start
logging.info("""stitch2complete completed.
Total time: {0}
Dockets per second: {1}""".format(stitch2complete_time,
                                  successes_and_total["dockets"]/stitch2complete_time.seconds))

print("End.")
# Ugh. I ran this on 115 dockets and pdf2stitch runs at 1.32 dockets/second
# for a total running time of 1m 27s.
# stitch2complete is much faster, at 10 dockets a second.
#
# If pdf2stitch has to be that slow, running it on 14000 dockets would take
# 5 hours!!  Even stitch2complete will take 23 minutes!