from parsimonious import Grammar
from parsimonious import NodeVisitor
import os
from lxml import etree
import io

class CaseEventVisitor(NodeVisitor):

  # Nonterminals
  def generic_visit(self, node, vc):
    return self.stringify(vc)

  def visit_case_event(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event> %s </case_event> " % contents

  def visit_case_event_desc(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event_description> %s </case_event_description> " % contents

  def visit_date(self, node, vc):
    contents = self.stringify(vc)
    return " <date> %s </date> " % contents

 #  This is the very complicated version of this method
 #  def visit_sequence(self, node, vc):
#
#     def parse_details(details_list):
#       """
#       This nested function will parse the details of the sequence after
#       the parent method has done a bit of processing to clean up the details.
#       This is almost certainly _not_ the best way to do this, but jeez, I'm
#       tired and I've been stuck on this for frigging ever.
#       """
#
#       print("parsing the details.")
#       assert(details_list[0] == " <sequence_details>", details_list[0])
#       assert(details_list[-1] == "</sequence_details> ")
#       revised_details = []
#
#       details_grammar = r"""
#                         sequence_details = judge_line sequence_details /
#
#                         """
#
#       [print(detail) for detail in details_list]
#       return revised_details
#       #End of this nested function-in-a-method
#
#     contents = self.stringify(vc)
#     revised_contents = []
#     print("In sequence")
# #    print("<sequence>")
#     sequence_lines = contents.split("\n")
#     revised_contents.append(sequence_lines[0])
#     baseline_spaces = len(sequence_lines[0]) - len(sequence_lines[0].lstrip(" "))
#     for line in sequence_lines[1:]:
#       relative_spaces = len(line) - len(line.lstrip(" ")) - baseline_spaces
#       if relative_spaces == 0:
# #        print(line + " should be moved up to")
# #        print(revised_contents[0])
#         revised_contents[0] = revised_contents[0].replace("</sequence_description>", "%s </sequence_description>" % line.lstrip())
# #        print(revised_contents[0])
#       elif len(line) != 0:
#         revised_contents.append(line)
# #    [print(line) for line in revised_contents]
# #    print("</sequence>")
#
#     if len(revised_contents) > 3:
#       revised_contents[1:] = parse_details(revised_contents[1:])
#
#     revised_contents = self.stringify(revised_contents)
#     return " <sequence> %s </sequence> " % revised_contents

######## This is the simple version. ###########
  def visit_sequence(self, node, vc):
    contents = self.stringify(vc)
    return "<sequence_sequence>%s</sequence_sequence>" % contents
################################

  def visit_sequence_number(self, node, vc):
    contents = self.stringify(vc)
    return "<sequence_number>%s</sequence_number>" % contents

  def visit_sequence_description(self, node, vc):
    contents = self.stringify(vc)
    return " <sequence_description> %s </sequence_description> " % contents

  def visit_offense_disposition(self, node, vc):
    contents = self.stringify(vc)
    return " <offense_disposition> %s </offense_disposition> " % contents

  def visit_grade(self, node, vc):
    contents = self.stringify(vc)
    return " <offense_grade> %s </offense_grade >" % contents

  def visit_section(self, node, vc):
    contents = self.stringify(vc)
    return " <section> %s </section> " % contents

  def visit_sequence_details(self, node, vc):
    contents = self.stringify(vc)
#     lines = contents.split("\n")
#     print("visiting sequence details.")
#     [print("line: %s" % line) for line in lines]
    return " <sequence_details>\n%s\n</sequence_details> " % contents

  def visit_judge_name(self, node, vc):
    contents = self.stringify(vc)
    return "<judge_name> %s </judge_name>" % contents

  def visit_things_a_judge_did(self, node, vc):
    contents = self.stringify(vc)
    return "<things_a_judge_did> %s </things_a_judge_did>" % contents

  def visit_sentence_info(self, node, vc):
    contents = self.stringify(vc)
    return "<sentence_info> %s </sentence_info>" % contents

  def visit_program(self, node, vc):
    contents = self.stringify(vc)
    return "<program> %s </program>" % contents

  def visit_length_of_sentence(self, node, vc):
    contents = self.stringify(vc)
    return "<length_of_sentence> %s </length_of_sentence>" % contents

  def visit_sequence_description_continued(self, node, vc):
    contents = self.stringify(vc)
    return " <sequence_description_continued> %s </sequence_description_continued> " % contents

  def visit_extra_sentence_details(self, node, vc):
    contents = self.stringify(vc)
    return "<extra_sentence_details> %s </extra_sentence_details>" % contents

  #Terminals
  def visit_number(self, node, vc):
    return node.text

  def visit_single_content_char(self, node, vc):
    return node.text

  def visit_single_char_no_ws(self, node, vc):
    return node.text

  def visit_single_char_no_comma_or_ws(self, node, vc):
    return node.text

  def visit_new_line(self, node, vc):
    return node.text

  def visit_forward_slash(self, node, vc):
    return node.text

  def visit_ws(self, node, vc):
    return node.text

  def visit_single_letter_no_ws(self, node, vc):
    return node.text

  def visit_comma(self, node, vc):
    return node.text

  #Helpers
  def stringify(self, list):
    return "".join(list)

grammars = [
r"""
case_event = new_line case_event_desc_and_date sequences new_line?

case_event_desc_and_date = ws ws ws* case_event_desc ws ws ws+ date ws ws ws+ is_final new_line
case_event_desc = (word ws)+

date = number forward_slash number forward_slash number
is_final = (word ws word) / word

sequences = sequence+
sequence = sequence_start sequence_details?
sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* section new_line
sequence_number = number+
sequence_description = (word ws)+
offense_disposition = (word ws)+
grade = single_letter_no_ws+
section = single_content_char+


#### Imported form sequenceDetailsSection.py #######
sequence_details = !sequence_start sequence_description_continued? things_a_judge_did*


sequence_description_continued = (!name_line line)

things_a_judge_did = name_line sentence_info*
sentence_info = !name_line program_length_start extra_sentence_details?

name_line = ws+ judge_name ws ws ws ws+ date new_line
judge_name = word_no_comma comma ws word_no_comma
date = number forward_slash number forward_slash number

program_length_start = (ws ws+ no_further_penalty new_line) /
                       (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
program = word (ws word)*


extra_sentence_details = (!name_line !program_length_start line)*


length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                              (fraction ws word_or_numbers_or_fraction) /
                              (number ws word_or_numbers_or_fraction) /
                              (word)/
                              (number)/
                              (fraction)

fraction = number forward_slash number
# end of grammar Imported from sequenceDetailsSection.py


line = content new_line
content = single_content_char+
word = single_char_no_ws+
word_no_comma = single_char_no_comma_or_ws+

#Terminals
no_further_penalty = ~"No Further Penalty"i

number = ~"[0-9,\.]+"
single_letter_no_ws = ~"[a-z]"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_char_no_ws = ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
comma = ","
new_line = "\n"
forward_slash = "/"
ws = " "
""",
r"""
case_event = new_line case_event_desc_and_date sequences new_line?

case_event_desc_and_date = ws ws ws* case_event_desc ws ws ws+ date ws ws ws+ is_final new_line
case_event_desc = (word ws)+

date = number forward_slash number forward_slash number
is_final = (word ws word) / word

sequences = sequence+
sequence = (sequence_start sequence_desc_continued? sequence_details?)
sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* section new_line
sequence_number = number+
sequence_description = (word ws)+
offense_disposition = (word ws)+
grade = single_letter_no_ws+
section = single_content_char+
sequence_desc_continued = !sequence_start (word_no_comma ws?)+ new_line

# sequence_details = (!sequence_start line)+
#   OR
# sequence_details = (judge_date_credit_line line+) / (sequence_description_continued)
# judge_date_credit_line = ws+ word_no_comma ", " (word ws)+ ws ws ws+ line
# sequence_description_continued = (ws+ word new_line) / (ws+ (word ws)+ word new_line)
#ws+ (!sequence_start (word ws)+)+ new_line
#  OR
# sequence_details = (judge_and_date sequence_details) /
#                    (program_info sequence_details) /
#                    judge_and_date /
#                    program_info
# judge_and_date = "         Shreeves-Johns, Karen                                                     07/13/2011" new_line
# program_info = "            Probation                                                                Max of 3.00 Years                                   07/13/2011" new_line line line line line line
# IMPORTED FROM sequenceDetailsSection.py
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
# end of grammar Imported from sequenceDetailsSection.py


line = content new_line
content = single_content_char+
word = single_char_no_ws+
word_no_comma = single_char_no_comma_or_ws+

#Terminals
number = ~"[0-9,\.]+"
single_letter_no_ws = ~"[a-z]"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_char_no_ws = ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
forward_slash = "/"
ws = " "
""",
r"""
#Use this grammar when going back to the complex version of visit_sequence
case_event = new_line case_event_desc_and_date sequences new_line?

case_event_desc_and_date = ws ws ws* case_event_desc ws ws ws+ date ws ws ws+ is_final new_line
case_event_desc = (word ws)+

date = number forward_slash number forward_slash number
is_final = (word ws word) / word

sequences = sequence+
sequence = (sequence_start sequence_details) / sequence_start
sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* section new_line
sequence_number = number+
sequence_description = (word ws)+
offense_disposition = (word ws)+
grade = single_letter_no_ws+
section = single_content_char+


sequence_details = (!sequence_start line)+
# sequence_details = (judge_date_credit_line line+) / (sequence_description_continued)
# judge_date_credit_line = ws+ word_no_comma ", " (word ws)+ ws ws ws+ line
# sequence_description_continued = (ws+ word new_line) / (ws+ (word ws)+ word new_line)
#ws+ (!sequence_start (word ws)+)+ new_line


line = content new_line
content = single_content_char+
word = single_char_no_ws+
word_no_comma = single_char_no_comma_or_ws+

#Terminals
number = ~"[0-9,]+"
single_letter_no_ws = ~"[a-z]"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_char_no_ws = ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
forward_slash = "/"
ws = " "
""",
r"""
section = new_line case_event_and_date line+ new_line?

case_event_and_date = ws ws ws* (word ws)+ ws ws ws+ date ws ws ws+ is_final new_line
case_event = word+
word = single_char_no_ws+
date = number forward_slash number forward_slash number
is_final = (word ws word) / word



line = content new_line
content = single_content_char+
number = ~"[0-9,]+"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_char_no_ws = ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
forward_slash = "/"
ws = " "
"""
]

grammar = Grammar(grammars[0])



details_sections = [
r"""
   Trial                                                                      01/05/2012                                    Final Disposition
    1 / Criminal Attempt - Escape                                               Guilty Plea - Negotiated                        F3           18 § 901 §§ A
          Beloff, Adam                                                             01/05/2012
            No Further Penalty
""",
r"""
   Scheduling Conference                                                    05/17/2011                                    Final Disposition
    7 / Poss Instrument Of Crime W/Int                                        Guilty Plea - Negotiated                        M1           18 § 907 §§ A
       Hill, Glynnis                                                             05/17/2011
         Probation                                                                 Max of 5.00 Years                        07/13/2011
                                                                                   5 years
""",
r"""
   Pretrial Bring Back                                                        07/13/2011                                    Final Disposition
      1 / Manufacture, Delivery, or Possession With Intent to                   Guilty Plea - Negotiated                        F            35 § 780-113 §§ A30
      Manufacture or Deliver
         Shreeves-Johns, Karen                                                     07/13/2011
            Something                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
            Probation and fun                                                                Max of 3.00 Years                                   07/13/2011
                                                                                     3 years
                  Defendant is to pay imposed mandatory court costs.
                  To submit to random drug screens.
                  To pursue a prescribed secular course of study or vocational training.
                  Case relisted for status of compliance on 9/22/11 courtroom 605.
       Shreeves-Johns, Karen                                                     12/20/2011
""",
r"""
     Preliminary Hearing                                                      05/19/2011                                     Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                               35 § 780-113 §§ A30
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                               35 § 780-113 §§ A16
""",
r"""
     Preliminary Hearing                                                      05/19/2011                                     Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                               35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                               35 § 780-113 §§ A16
""",
r"""
     Information Filed                                                        06/03/2011                                     Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                               35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                               35 § 780-113 §§ A16
""",
r"""
   Lower Court Disposition                                                    03/02/2011                                    Not Final
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                     Guilty                                          M            75 § 3802 §§ A1*
    99,999 / False Identification To Law Enforcement                            Not Guilty                                      M3           18 § 4914 §§ A
    Officer

""",
r"""
   Information Filed                                                          06/02/2011                                    Not Final
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                          Added by Information                            M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                      Added by Information                            M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*
   99,999 / False Identification To Law Enforcement                               Disposed at Lower Court                         M3           18 § 4914 §§ A
   Officer

""",
r"""
     Trial                                                                      10/28/2011                                     Final Disposition
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                            Quashed                                         M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                      Quashed                                         M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*
      99,999 / False Identification To Law Enforcement                            Disposed at Lower Court                         M3           18 § 4914 §§ A
      Officer
""",
r"""
   Preliminary Hearing                                                        05/19/2011                                    Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                  F            35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                  M            35 § 780-113 §§ A16

""",
r"""
   Information Filed                                                          05/25/2011                                    Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                  F            35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                  M            35 § 780-113 §§ A16

""",
r"""
   Pretrial Bring Back                                                        07/13/2011                                    Final Disposition
      1 / Manufacture, Delivery, or Possession With Intent to                   Guilty Plea - Negotiated                        F            35 § 780-113 §§ A30
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
    2 / Int Poss Contr Subst By Per Not Reg                                   Nolle Prossed                                   M            35 § 780-113 §§ A16
       Shreeves-Johns, Karen                                                     07/13/2011
       Shreeves-Johns, Karen                                                     12/20/2011

""",
r"""
   Preliminary Hearing                                                      12/30/2010                                    Not Final
    1 / Rape Forcible Compulsion                                              Held for Court                                  F1           18 § 3121 §§ A1
    3 / Sexual Assault                                                        Held for Court                                  F2           18 § 3124.1
    4 / Unlawful Restraint/ Serious Bodily Injury                             Held for Court                                  M1           18 § 2902 §§ A1
    5 / Theft By Unlaw Taking-Movable Prop                                    Held for Court                                  M1           18 § 3921 §§ A
    6 / Receiving Stolen Property                                             Held for Court                                  M1           18 § 3925 §§ A
    7 / Poss Instrument Of Crime W/Int                                        Held for Court                                  M1           18 § 907 §§ A
    8 / Indecent Exposure                                                     Held for Court                                  M1           18 § 3127 §§ A
    11 / Recklessly Endangering Another Person                                Held for Court                                  M2           18 § 2705
    99,999 / Indec Asslt-W/O Cons Of Other                                    Held for Court                                  M2           18 § 3126 §§ A1
    99,999 / Robbery-Inflict Serious Bodily Injury                            Held for Court                                  F1           18 § 3701 §§ A1I
    99,999 / Simple Assault                                                   Held for Court                                  M2           18 § 2701 §§ A

""",
r"""
   Information Filed                                                        01/10/2011                                    Not Final
    1 / Rape Forcible Compulsion                                              Held for Court                                  F1           18 § 3121 §§ A1
    2 / Robbery-Threat Immed Ser Injury                                       Replacement by Information                      F1           18 § 3701 §§ A1II
    3 / Sexual Assault                                                        Held for Court                                  F2           18 § 3124.1
    4 / Unlawful Restraint/ Serious Bodily Injury                             Held for Court                                  M1           18 § 2902 §§ A1
    5 / Theft By Unlaw Taking-Movable Prop                                    Held for Court                                  M1           18 § 3921 §§ A
    6 / Receiving Stolen Property                                             Held for Court                                  M1           18 § 3925 §§ A
    7 / Poss Instrument Of Crime W/Int                                        Held for Court                                  M1           18 § 907 §§ A
    8 / Indecent Exposure                                                     Held for Court                                  M1           18 § 3127 §§ A
    9 / Ind Asslt Forcible Compulsion                                         Replacement by Information                      M2           18 § 3126 §§ A2
    10 / Simple Assault                                                       Replacement by Information                      M2           18 § 2701 §§ A3
    11 / Recklessly Endangering Another Person                                Held for Court                                  M2           18 § 2705
    12 / Rape Threat Of Forcible Compulsion                                   Added by Information                            F1           18 § 3121 §§ A2
    13 / Robbery-Commit Threat 1st/2nd Deg Fel                                Added by Information                            F1           18 § 3701 §§ A1III
    14 / Ind Asslt Threat Forcible Compulsion                                 Added by Information                            M2           18 § 3126 §§ A3
    99,999 / Indec Asslt-W/O Cons Of Other                                    Charge Changed                                  M2           18 § 3126 §§ A1
    Replaced by 18 § 3126 §§ A2, Ind Asslt Forcible Compulsion
    99,999 / Robbery-Inflict Serious Bodily Injury                            Charge Changed                                  F1           18 § 3701 §§ A1I
    Replaced by 18 § 3701 §§ A1II, Robbery-Threat Immed Ser Injury
    99,999 / Simple Assault                                       Charge Changed                                              M2           18 § 2701 §§ A
    Replaced by 18 § 2701 §§ A3, Simple Assault

""",
r"""
   Scheduling Conference                                                    05/17/2011                                    Final Disposition
    1 / Rape Forcible Compulsion                                              Guilty Plea - Negotiated                        F1           18 § 3121 §§ A1
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
         Confinement                                                               7 1/2 years to 15 years                             09/09/2011
               DEFENDANT FOUND NOT TO BE SEXUAL PREDITOR, LIFE TIME REGISTRATION WITH STATE
               POLICE; RESIDENCE, EMPLOYMENT, SCHOOL, PAY COURT COST & FINES, SENTENCE TO RUN
               CONSECUTIVE WITH ANY OTHER SENTENCE PRESENTLY SERVING
    2 / Robbery-Threat Immed Ser Injury                                       Nolle Prossed                                   F1           18 § 3701 §§ A1II
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    3 / Sexual Assault                                                        Nolle Prossed                                   F2           18 § 3124.1
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    4 / Unlawful Restraint/ Serious Bodily Injury                             Nolle Prossed                                   M1           18 § 2902 §§ A1
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    5 / Theft By Unlaw Taking-Movable Prop                                    Nolle Prossed                                   M1           18 § 3921 §§ A
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    6 / Receiving Stolen Property                                             Nolle Prossed                                   M1           18 § 3925 §§ A
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    7 / Poss Instrument Of Crime W/Int                                        Guilty Plea - Negotiated                        M1           18 § 907 §§ A
       Hill, Glynnis                                                             05/17/2011
         Probation                                                                 Max of 5.00 Years
                                                                                   5 years
       Hill, Glynnis                                                             09/09/2011
         Probation                                                                 Max of 5.00 Years                                   09/09/2011
                                                                                   5 years
    8 / Indecent Exposure                                                     Nolle Prossed                                   M1           18 § 3127 §§ A
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    9 / Ind Asslt Forcible Compulsion                                         Nolle Prossed                                   M2           18 § 3126 §§ A2
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    10 / Simple Assault                                                       Nolle Prossed                                   M2           18 § 2701 §§ A3
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    11 / Recklessly Endangering Another Person                                Nolle Prossed                                   M2           18 § 2705
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    12 / Rape Threat Of Forcible Compulsion                                   Nolle Prossed                                   F1           18 § 3121 §§ A2
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    13 / Robbery-Commit Threat 1st/2nd Deg Fel                                Nolle Prossed                                   F1           18 § 3701 §§ A1III
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    14 / Ind Asslt Threat Forcible Compulsion                                 Nolle Prossed                                   M2           18 § 3126 §§ A3
       Hill, Glynnis                                                             05/17/2011
       Hill, Glynnis                                                             09/09/2011
    99,999 / Indec Asslt-W/O Cons Of Other                                    Charge Changed                                  M2           18 § 3126 §§ A1
    Replaced by 18 § 3126 §§ A2, Ind Asslt Forcible Compulsion
      Hill, Glynnis                                                              05/17/2011
       Hill, Glynnis                                                             09/09/2011
      99,999 / Robbery-Inflict Serious Bodily Injury                            Charge Changed                                  F1           18 § 3701 §§ A1I
      Replaced by 18 § 3701 §§ A1II, Robbery-Threat Immed Ser Injury
        Hill, Glynnis                                                05/17/2011
        Hill, Glynnis                                                             09/09/2011
      99,999 / Simple Assault                                                   Charge Changed                                  M2           18 § 2701 §§ A
      Replaced by 18 § 2701 §§ A3, Simple Assault
        Hill, Glynnis                                                              05/17/2011
        Hill, Glynnis                                                              09/09/2011

""",
r"""
   Preliminary Hearing                                                        05/18/2011                                    Not Final
      1 / Criminal Attempt - Escape                                             Held for Court                                  F3           18 § 901 §§ A
      2 / Aggravated Assault                                                    Held for Court                                  F2           18 § 2702 §§ A
      3 / Simple Assault                                                        Held for Court                                  M2           18 § 2701 §§ A
      99,999 / Resist Arrest/Other Law Enforce                                  Dismissed - LOE                                 M2           18 § 5104

""",
r"""
   Information Filed                                                          06/02/2011                                    Not Final
    1 / Criminal Attempt - Escape                                               Held for Court                                  F3           18 § 901 §§ A
    2 / Aggravated Assault                                                      Held for Court                                  F2           18 § 2702 §§ A
    3 / Simple Assault                                                          Held for Court                                  M2           18 § 2701 §§ A
    99,999 / Resist Arrest/Other Law Enforce                                    Disposed at Lower Court                         M2           18 § 5104

""",
r"""
   Trial                                                                      01/05/2012                                    Final Disposition
    1 / Criminal Attempt - Escape                                               Guilty Plea - Negotiated                        F3           18 § 901 §§ A
          Beloff, Adam                                                             01/05/2012
            No Further Penalty
    2 / Aggravated Assault                                                      Guilty Plea - Negotiated                        F2           18 § 2702 §§ A
          Beloff, Adam                                                             01/05/2012
            Confinement                                                              Min of 3.00 Months                                  01/05/2012
                                                                                     Max of 23.00 Months
                                                                                     3 - 23 months
            Probation                                                                Min of 1.00 Years
                                                                                     Max of 1.00 Years
                                                                                     1 year
    3 / Simple Assault                                                          Nolle Prossed                                   M2           18 § 2701 §§ A
          Beloff, Adam                                                             01/05/2012
    99,999 / Resist Arrest/Other Law Enforce                                    Disposed at Lower Court                         M2           18 § 5104
          Beloff, Adam                                                             01/05/2012

""",
r"""
     Preliminary Hearing                                                      05/19/2011                                     Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                               35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                               35 § 780-113 §§ A16

""",
r"""
     Information Filed                                                        06/03/2011                                     Not Final
      1 / Manufacture, Delivery, or Possession With Intent to                   Held for Court                                               35 § 780-113 §§ A30
      Manufacture or Deliver
      2 / Int Poss Contr Subst By Per Not Reg                                   Held for Court                                               35 § 780-113 §§ A16
""",
r"""
   Lower Court Disposition                                                    02/07/2011                                    Not Final
      99,999 / DUI: Controlled Substance - Impaired Ability -                   Guilty                                          M            75 § 3802 §§ D2*
      1st Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                     Guilty                                          M            75 § 3802 §§ A1*

""",
r"""
   Information Filed                                                          06/02/2011                                    Not Final
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                          Added by Information                            M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                    Added by Information                            M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Controlled Substance - Impaired Ability -                     Disposed at Lower Court                         M            75 § 3802 §§ D2*
      1st Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*

""",
r"""
     Trial                                                                      12/06/2011                                     Final Disposition
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                            Nolle Prossed                                   M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                      Nolle Prossed                                   M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Controlled Substance - Impaired Ability -                     Disposed at Lower Court                         M            75 § 3802 §§ D2*
      1st Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*
"""]

file_name = "./DetailsCollection.xml"

try:
  os.remove(file_name)
except:
  pass

parser = etree.XMLParser(remove_blank_text=True)

for index in range(len(details_sections)):
  root = grammar.parse(details_sections[index].replace("&","&amp;"))
  print("Parsed text: %i" % index)
  visitor = CaseEventVisitor()
  parsed_text = io.StringIO(visitor.visit(root))
  xml_root = etree.parse(parsed_text, parser)
  with open(file_name, "a+") as f:
    f.write(etree.tostring(xml_root, pretty_print=True).decode('utf-8'))
    f.write("\n\n")
  f.close()