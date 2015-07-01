from parsimonious import Grammar
from parsimonious import NodeVisitor

class DetailsVisitor(NodeVisitor):
  def generic_visit(self, node, vc):
    return self.stringify(vc)

  def visit_sequence_description_continued(self, node, vc):
    contents = self.stringify(vc)
    return "<seq_desc_cont> %s </seq_desc_cont>" % contents

  def visit_sequence_details(self, node, vc):
    contents = self.stringify(vc)
    return "<sequence_details> %s </sequence_details>" % contents

  def visit_things_a_judge_did(self, node, vc):
    contents = self.stringify(vc)
    return "<things_judge_did> %s </things_judge_did>" % contents

  def visit_name_line(self, node, vc):
    contents = self.stringify(vc)
    return "<name_line> %s </name_line>" % contents

  def visit_judge_name(self, node, vc):
    contents = self.stringify(vc)
    return "<judge_name> %s </judge_name>" % contents

  def visit_sentence_info(self, node, vc):
    contents = self.stringify(vc)
    return "<sentence_info> %s </sentence_info>" % contents

  def visit_sentence_length_start(self, node, vc):
    contents = self.stringify(vc)
    return "<sentence_length_start> %s </sentence_length_start>" % contents

  def visit_length_of_sentence(self, node, vc):
    contents = self.stringify(vc)
    return "<length_of_sentence> %s </length_of_sentence>" % contents

  def visit_program_length_start(self, node, vc):
    contents = self.stringify(vc)
    return "<program_length_start> %s </program_length_start>" % contents

  def visit_program(self, node, vc):
    contents = self.stringify(vc)
    return "<program> %s </program>" % contents

  def visit_extra_sentence_details(self, node, vc):
    contents = self.stringify(vc)
    return "<extra_sentence_details> %s </extra_sentence_details>" % contents

  #terminals

  def visit_number(self, node, vc):
    return node.text

  def visit_word(self, node, vc):
    return node.text

  def visit_single_content_char(self, node, vc):
    return node.text

  def visit_single_char_no_ws(self, node, vc):
    return node.text

  def visit_new_line(self, node, vc):
    return node.text

  def visit_forward_slash(self, node, vc):
    return node.text

  def visit_ws(self, node, vc):
    return node.text

  def visit_single_letter_no_ws(self, node, vc):
    return node.text

  #Helpers
  def stringify(self, list):
    return "".join(list)

grammars = [
r"""
#WORKS!!
sequence_details = new_line sequence_description_continued? things_a_judge_did*

sequence_description_continued = (!name_line line)

things_a_judge_did = name_line sentence_info?
sentence_info = !name_line program_length_start extra_sentence_details? # start here :)

name_line = ws+ judge_name ws ws ws ws+ date new_line
judge_name = word "," ws word
date = number forward_slash number forward_slash number

program_length_start = ws ws+ program ws ws+ length_of_sentence ws ws+ date new_line
program = word (ws word)*


extra_sentence_details = (!name_line !program_length_start line)*


length_of_sentence = word_or_numbers_or_fraction &ws
word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                              (fraction ws word_or_numbers_or_fraction) /
                              (number ws word_or_numbers_or_fraction) /
                              (word)/
                              (number)/
                              (fraction)

fraction = number forward_slash number




line = content new_line?
content = single_content_char+
number = ~"[0-9,\.]+"
word = ~"[a-zA-Z\-]+"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
""",
r"""
program_length_start = ws ws+ word (ws word)* ws ws ws+ length_of_sentence ws ws ws+ date new_line

length_of_sentence = (word ws word_or_numbers_or_fraction) /
                              (fraction ws word_or_numbers_or_fraction) /
                              (number ws word_or_numbers_or_fraction) /
                              (word)/
                              (number)/
                              (fraction)
date = number forward_slash number forward_slash number
fraction = number forward_slash number

line = content new_line?
content = single_content_char+
number = ~"[0-9,\.]+"
word = ~"[a-zA-Z\-]+"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
""",
r"""
word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                              (number ws word_or_numbers_or_fraction) /
                              (fraction ws word_or_numbers_or_fraction) /
                              (word new_line)/
                              (number new_line)/
                              (fraction new_line)


fraction = number forward_slash number
number = ~"[0-9,\.]*"
forward_slash = "/"
word = ~"[a-zA-Z\-]*"

new_line = "\n"
ws = " "
""",
r"""
program_length_start = ws ws+ word (ws word)? ws ws ws+ (word_or_numbers_or_fraction ws)+ ws ws+ date new_line
#ws ws+ (word ws)+ ws ws+ (word_or_numbers_or_fraction ws) ws ws+ date new_line

word_or_numbers_or_fraction = word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                              (number ws word_or_numbers_or_fraction) /
                              (fraction ws word_or_numbers_or_fraction) /
                              (word new_line)/
                              (number new_line)/
                              (fraction new_line)
date = number forward_slash number forward_slash number
fraction = number forward_slash number

line = content new_line?
content = single_content_char+
number = ~"[0-9,\.]*"
word = ~"[a-zA-Z\-]*"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
""",
r"""
sequence_details = new_line sequence_description_continued? things_a_judge_did*

sequence_description_continued = (!name_line line)

things_a_judge_did = name_line sentence_info
sentence_info = (!name_line program_length_start)? (!name_line !program_length_start line)* # start here :)

program_length_start = ws ws+ (word ws)+ ws ws+ (word_or_numbers ws?) ws ws+ date new_line
word_or_numbers_or_slash = word / number / slash

name_line = ws+ judge_name ws ws ws ws+ date new_line
judge_name = word "," ws word
date = number forward_slash number forward_slash number

line = content new_line?
content = single_content_char+
number = ~"[0-9,\.]*"
word = ~"[a-zA-Z\-]*"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
""",
r"""
sequence_details = new_line line+

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
word = ~"[a-zA-Z]*"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
""",
r"""
sequence_details = new_line line+

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
word = ~"[a-zA-Z]*"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
ws = " "
"""
]

texts = [
"""
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
            Probation and fun                                                                 Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
          Confinement                                                              Min of 11.00 Months 15.00 Days                      12/20/2011
""",
"""
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
             Probation                                                                Max of 3.00 Years                                   07/13/2011
       Shreeves-Johns, Karen                                                     12/20/2011
""",
"""
      Manufacture or Deliver
""",
"""
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
            Probation                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
          Confinement                                                              Min of 11.00 Months 15.00 Days                      12/20/2011
                                                                                   Max of 23.00 Months
                                                                                   11 1/2 - 23 months
               Defendant eligible for work release.
          Probation                                                                 Max of 3.00 Years                                  12/20/2011
                                                                                    3 years
               All conditions previously imposed to remain.
""",
"""         Confinement and fun                                                              7 1/2 years to 15 years                             09/09/2011
""",
"""7 1/2 years to 15 years
""",
"""         Confinement                                                               7 1/2 years to 15 years                             09/09/2011
""",
"""
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
         Confinement                                                               7 1/2 years to 15 years                             09/09/2011
               DEFENDANT FOUND NOT TO BE SEXUAL PREDITOR, LIFE TIME REGISTRATION WITH STATE
               POLICE; RESIDENCE, EMPLOYMENT, SCHOOL, PAY COURT COST &amp; FINES, SENTENCE TO RUN
               CONSECUTIVE WITH ANY OTHER SENTENCE PRESENTLY SERVING
""",
"""
       Shreeves-Johns, Karen                                                     07/13/2011
       Shreeves-Johns, Karen                                                     12/20/2011
""",
"""
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
            Probation                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
          Confinement                                                              Min of 11.00 Months 15.00 Days                      12/20/2011
                                                                                   Max of 23.00 Months
                                                                                   11 1/2 - 23 months
               Defendant eligible for work release.
          Probation                                                                 Max of 3.00 Years                                  12/20/2011
                                                                                    3 years
               All conditions previously imposed to remain.
""",
"""
         Shreeves-Johns, Karen                                                     07/13/2011
""",
"""
         Shreeves-Johns, Karen                                                     07/13/2011
            Probation                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
          Confinement                                                              Min of 11.00 Months 15.00 Days                      12/20/2011
                                                                                   Max of 23.00 Months
                                                                                   11 1/2 - 23 months
               Defendant eligible for work release.
          Probation                                                                 Max of 3.00 Years                                  12/20/2011
                                                                                    3 years
               All conditions previously imposed to remain.
""",
"""
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
            Probation                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
          Confinement                                                              Min of 11.00 Months 15.00 Days                      12/20/2011
                                                                                   Max of 23.00 Months
                                                                                   11 1/2 - 23 months
               Defendant eligible for work release.
          Probation                                                                 Max of 3.00 Years                                  12/20/2011
                                                                                    3 years
               All conditions previously imposed to remain.
"""
]

grammar = Grammar(grammars[0])
root = grammar.parse(texts[0])
print("parsed.")
visitor = DetailsVisitor()
print(visitor.visit(root))
