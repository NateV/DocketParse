from parsimonious import Grammar
from parsimonious import NodeVisitor
import re
import pytest


grammars = [
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

  ####Imported from dispositionDetailsSection.py ###########
  case_event = new_line? case_event_desc_and_date sequences new_line?

  case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final new_line
  case_event_desc = (word ws)+

  date = number forward_slash number forward_slash number
  is_final = (word ws word) / word

  sequences = sequence+
  sequence = sequence_start sequence_details?
  sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* code_section new_line
  sequence_number = number+ &ws
  sequence_description = (word ws)+
  offense_disposition = (word ws)+
  code_section = single_content_char+


    #### Imported from sequenceDetailsSection.py #######
    sequence_details = !sequence_start sequence_description_continued* things_a_judge_did*

    # The complexity of the following rule is necessary because I need to
    # distinguish lines that carry over from the sequence description, which
    # could be just words without commas: "intent to distribute"
    # or which can contain commas, as in
    # "    Replaced by 18 § 2701 §§ A3, Simple Assault"
    # I identify names by [words] comma [words], as in "Smith, John"
    # In order to distinguish them, I'm assuming that a judge won't have more
    # than two last names before the comma, and a sequence_description_continued line will
    # have at least three words before any comma.
    # N.B. If this turns out to be wrong, a couple other ideas might work:
    # 1) Treat the "Replaced by" lines as an entirely separate optional line,
    #    characterized by the presence of section symbols
    # 2) Create a dictionary of judges' names, and explicitly check their names.
    sequence_description_continued = (ws+ !number !name_line word_no_comma new_line) /
                                     (ws+ !number !name_line word_no_comma ws word_no_comma new_line) /
                                     (ws+ !number !name_line word_no_comma ws word_no_comma  ws content new_line) /
                                     (ws+ !number !name_line word_no_comma comma ws word_no_comma ws word_no_comma (ws !date word_no_comma)* new_line)


    things_a_judge_did = name_line sentence_info*
    sentence_info = !name_line program_length_start extra_sentence_details?

    name_line = ws+ judge_name ws ws ws ws+ date new_line
    judge_name = word_no_comma (ws word_no_comma)? comma ws word_no_comma (ws word_no_comma)? (ws word_no_comma)?

    program_length_start = (ws ws+ no_further_penalty new_line) /
                           (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
    program = word (ws word)*

    extra_sentence_details = (!name_line !program_length_start !sequence_start line)*


    length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
    word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                  (fraction ws word_or_numbers_or_fraction) /
                                  (number ws word_or_numbers_or_fraction) /
                                  (word)/
                                  (number)/
                                  (fraction)

    fraction = number forward_slash number
  ####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = (" LINKED SENTENCES:" new_line) /
                  (ws* "The following Judge Ordered Conditions are imposed:" new_line)

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+

##Terminals
grade = ~"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

  ####Imported from dispositionDetailsSection.py ###########
  case_event = new_line? case_event_desc_and_date sequences new_line?

  case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final new_line
  case_event_desc = (word ws)+

  date = number forward_slash number forward_slash number
  is_final = (word ws word) / word

  sequences = sequence+
  sequence = sequence_start sequence_details?
  sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* code_section new_line
  sequence_number = number+ &ws
  sequence_description = (word ws)+
  offense_disposition = (word ws)+
  code_section = single_content_char+


    #### Imported from sequenceDetailsSection.py #######
    sequence_details = !sequence_start sequence_description_continued* things_a_judge_did*

    # The complexity of the following rule is necessary because I need to
    # distinguish lines that carry over from the sequence description, which
    # could be just words without commas: "intent to distribute"
    # or which can contain commas, as in
    # "    Replaced by 18 § 2701 §§ A3, Simple Assault"
    # I identify names by [words] comma [words], as in "Smith, John"
    # In order to distinguish them, I'm assuming that a judge won't have more
    # than two last names before the comma, and a sequence_description_continued line will
    # have at least three words before any comma.
    # N.B. If this turns out to be wrong, a couple other ideas might work:
    # 1) Treat the "Replaced by" lines as an entirely separate optional line,
    #    characterized by the presence of section symbols
    # 2) Create a dictionary of judges' names, and explicitly check their names.
    sequence_description_continued = (ws+ !number !name_line word_no_comma new_line) /
                                     (ws+ !number !name_line word_no_comma ws word_no_comma new_line) /
                                     (ws+ !number !name_line word_no_comma ws word_no_comma  ws content new_line) /
                                     (ws+ !number !name_line word_no_comma comma ws word_no_comma ws word_no_comma ws word_no_comma ws content new_line)


    things_a_judge_did = name_line sentence_info*
    sentence_info = !name_line program_length_start extra_sentence_details?

    name_line = ws+ judge_name ws ws ws ws+ date new_line
    judge_name = word_no_comma (ws word_no_comma)? comma ws word_no_comma (ws word_no_comma)?

    program_length_start = (ws ws+ no_further_penalty new_line) /
                           (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
    program = word (ws word)*

    extra_sentence_details = (!name_line !program_length_start !sequence_start line)*


    length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
    word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                  (fraction ws word_or_numbers_or_fraction) /
                                  (number ws word_or_numbers_or_fraction) /
                                  (word)/
                                  (number)/
                                  (fraction)

    fraction = number forward_slash number
  ####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = (" LINKED SENTENCES:" new_line) /
                  (ws* "The following Judge Ordered Conditions are imposed:" new_line)

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+

##Terminals
grade = ~"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

  ####Imported from dispositionDetailsSection.py ###########
  case_event = new_line? case_event_desc_and_date sequences new_line?

  case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final new_line
  case_event_desc = (word ws)+

  date = number forward_slash number forward_slash number
  is_final = (word ws word) / word

  sequences = sequence+
  sequence = sequence_start sequence_details?
  sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* code_section new_line
  sequence_number = number+ &ws
  sequence_description = (word ws)+
  offense_disposition = (word ws)+
  code_section = single_content_char+


    #### Imported from sequenceDetailsSection.py #######
    sequence_details = !sequence_start sequence_description_continued* things_a_judge_did*

    # The complexity of the following rule is necessary because I need to
    # distinguish lines that carry over from the sequence description, which
    # could be just words without commas: "intent to distribute"
    # or which can contain commas, as in
    # "    Replaced by 18 § 2701 §§ A3, Simple Assault"
    # I identify names by [words] comma [words], as in "Smith, John"
    # In order to distinguish them, I'm assuming that a judge won't have more
    # than two last names before the comma, and a sequence_description_continued line will
    # have at least three words before any comma.
    # N.B. If this turns out to be wrong, a couple other ideas might work:
    # 1) Treat the "Replaced by" lines as an entirely separate optional line,
    #    characterized by the presence of section symbols
    # 2) Create a dictionary of judges' names, and explicitly check their names.
    sequence_description_continued = (ws+ !name_line word_no_comma new_line) /
                                     (ws+ !name_line word_no_comma ws word_no_comma new_line) /
                                     (ws+ !name_line word_no_comma ws word_no_comma  ws content new_line) /
                                     (ws+ !name_line word_no_comma comma ws word_no_comma ws word_no_comma ws content new_line)


    things_a_judge_did = name_line sentence_info*
    sentence_info = !name_line program_length_start extra_sentence_details?

    name_line = ws+ judge_name ws ws ws ws+ date new_line
    judge_name = word_no_comma (ws word_no_comma)? comma ws word_no_comma (ws word_no_comma)?

    program_length_start = (ws ws+ no_further_penalty new_line) /
                           (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
    program = word (ws word)*

    extra_sentence_details = (!name_line !program_length_start !sequence_start line)*


    length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
    word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                  (fraction ws word_or_numbers_or_fraction) /
                                  (number ws word_or_numbers_or_fraction) /
                                  (word)/
                                  (number)/
                                  (fraction)

    fraction = number forward_slash number
  ####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+

##Terminals
grade = ~"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

  ####Imported from dispositionDetailsSection.py ###########
  case_event = new_line? case_event_desc_and_date sequences new_line?

  case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final new_line
  case_event_desc = (word ws)+

  date = number forward_slash number forward_slash number
  is_final = (word ws word) / word

  sequences = sequence+
  sequence = sequence_start sequence_details?
  sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* code_section new_line
  sequence_number = number+ &ws
  sequence_description = (word ws)+
  offense_disposition = (word ws)+
  code_section = single_content_char+


    #### Imported form sequenceDetailsSection.py #######
    sequence_details = !sequence_start sequence_description_continued? things_a_judge_did*


    sequence_description_continued = ws+ !name_line word_no_comma (ws content)? new_line

    things_a_judge_did = name_line sentence_info*
    sentence_info = !name_line program_length_start extra_sentence_details?

    name_line = ws+ judge_name ws ws ws ws+ date new_line
    judge_name = "Wright Padilla, Nina N."
    #judge_name = word_no_comma (ws word_no_comma)? comma ws word_no_comma (ws word_no_comma)?

    program_length_start = (ws ws+ no_further_penalty new_line) /
                           (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
    program = word (ws word)*

    extra_sentence_details = (!name_line !program_length_start !sequence_start line)*


    length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
    word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                  (fraction ws word_or_numbers_or_fraction) /
                                  (number ws word_or_numbers_or_fraction) /
                                  (word)/
                                  (number)/
                                  (fraction)

    fraction = number forward_slash number
  ####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+

##Terminals
grade = ~"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer? new_line


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line single_content_char_no_ws content new_line

disposition_details = ws ws+ !start_of_footer case_event+

  ####Imported from dispositionDetailsSection.py ###########
  case_event = new_line? case_event_desc_and_date sequences new_line?

  case_event_desc_and_date = ws* case_event_desc ws ws+ date ws ws ws+ is_final new_line
  case_event_desc = (word ws)+

  date = number forward_slash number forward_slash number
  is_final = (word ws word) / word

  sequences = sequence+
  sequence = sequence_start sequence_details?
  sequence_start = ws+ sequence_number ws forward_slash ws sequence_description ws ws ws ws+ offense_disposition ws ws ws+ grade? ws* code_section new_line
  sequence_number = number+ &ws
  sequence_description = (word ws)+
  offense_disposition = (word ws)+
  code_section = single_content_char+


    #### Imported form sequenceDetailsSection.py #######
    sequence_details = !sequence_start sequence_description_continued? things_a_judge_did*


    sequence_description_continued = ws+ !name_line content_no_comma new_line

    things_a_judge_did = name_line sentence_info*
    sentence_info = !name_line program_length_start extra_sentence_details?

    name_line = ws+ judge_name ws ws ws ws+ date new_line
    judge_name = word_no_comma comma ws word_no_comma

    program_length_start = (ws ws+ no_further_penalty new_line) /
                           (ws ws+ program ws ws+ length_of_sentence (ws ws+ date)? new_line)
    program = word (ws word)*

    extra_sentence_details = (!name_line !program_length_start !sequence_start line)*


    length_of_sentence = word_or_numbers_or_fraction &(ws / new_line)
    word_or_numbers_or_fraction = (word ws word_or_numbers_or_fraction) /
                                  (fraction ws word_or_numbers_or_fraction) /
                                  (number ws word_or_numbers_or_fraction) /
                                  (word)/
                                  (number)/
                                  (fraction)

    fraction = number forward_slash number
  ####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = ~"LINKED SENTENCES:"i new_line

word_no_comma = single_char_no_comma_or_ws+
word = single_content_char_no_ws+

##Terminals
grade = ~"[a-z0-9]"i+
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
content_no_comma = single_content_char_no_comma+
content_no_ws = single_content_char_no_ws+
number = ~"[0-9,\.]+"
forward_slash = "/"
single_content_char_no_comma =  ~"[a-z0-9`\ \"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
# This version of the grammar parses the disposition section only into
# disposition subsections, which have a disposition type and disposition
# details.
#
# This grammar requires further processing of the disposition details to
# get any useful information out of the disposition details.
#
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line line

disposition_details = (ws ws+ !start_of_footer line)+

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

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

section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line line

disposition_details = ws ws+ !start_of_footer case_event+

####Imported from dispositionDetailsSection.py ###########
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
####End Imported From dispositionDetailsSection.py

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

word_no_comma = single_char_no_comma_or_ws+

##Terminals
no_further_penalty = ~"No Further Penalty"i
single_char_no_comma_or_ws = ~"[a-z0-9`\"=_\.\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
line = content new_line?
content = single_content_char+
number = ~"[0-9,]+"
word = ~"[a-zA-Z]+"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_letter_no_ws = ~"[a-z]"i
comma = ","
new_line = "\n"
ws = " "
""",
r"""
# This version of the grammar parses the disposition section only into
# disposition subsections, which have a disposition type and disposition
# details.
#
# This grammar requires further processing of the disposition details to
# get any useful information out of the disposition details.
#
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer?


disposition_subsection = (disposition_type disposition_details) / (heading new_line*)
disposition_type = !ws !first_heading_line line

disposition_details = (ws ws+ !start_of_footer line)+

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line


footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

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
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer


disposition_subsection = (disposition_type case_event+ new_line*) / (heading new_line*)
disposition_type = !ws line

heading = first_heading_line line line line line line
first_heading_line = ~"Disposition"i new_line

case_event = case_event_line sequence+
case_event_line = ws ws line

sequence = sequence_description judge_date* sentence_program_info? new_line?
sequence_description = ((ws ws ws ws ws ws number ws forward_slash ws line) (ws ws ws ws ws ws seq_desc_continued)* ) /
                       ((ws ws ws ws number ws forward_slash ws line) (ws ws ws ws seq_desc_continued)*)
seq_desc_continued = !ws line

#judge_date = ws ws ws ws ws ws ws ws ws ws line
judge_date = ws ws ws ws ws ws+ judge_name ws ws ws+ date new_line
judge_name = word ~", " word
date = number forward_slash number forward_slash number

sentence_program_info = (ws ws ws ws ws ws ws ws ws ws* line)+

footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
word = ~"[a-zA-Z]*"
forward_slash = "/"
single_content_char_no_ws =  ~"[a-z0-9`\"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
""",
r"""
section_disposition_sentencing_body = ws* new_line? disposition_subsection+ new_line? footer


disposition_subsection = (disposition_type case_event+ new_line*) / (heading new_line*)
disposition_type = !ws line

heading = line line line line line line

case_event = case_event_line sequence+
case_event_line = ws ws line

sequence = sequence_description judge_date? program_type*
sequence_description = (ws ws ws ws number ws forward_slash ws line) (ws ws ws ws !number line)*

judge_date = ws ws ws ws ws ws ws ws ws ws line

program_type = ws ws ws ws ws ws ws ws ws ws ws ws ws* line

footer = start_of_footer line+
start_of_footer = " LINKED SENTENCES:" new_line

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
forward_slash = "/"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
""",
r"""
section_disposition_sentencing_body = new_line? heading disposition_subsection+
heading = line line line line line line

disposition_subsection = disposition_line case_event+

disposition_line = !ws line
case_event = ws+ line

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
""",
r"""
section_disposition_sentencing_body = new_line? heading disposition_subsection+
heading = line line line line line line

disposition_subsection = line+

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
""",
r"""
section_disposition_sentencing_body = new_line? heading
heading = line line line line line line
line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
""",
r"""
section_disposition_sentencing_body = new_line? heading disposition_subsection*
heading = line line line line line line
disposition_subsection = content new_line case_event+
case_event = ws ws content new_line sequence_description+
sequence_description = ws ws ws ws number ws "/" ws content new_line (ws* !number content new_line)*

line = content new_line?
content = single_content_char+
number = ~"[0-9,]*"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
new_line = "\n"
multi_ws = ws ws
ws = " "
"""]


# CURRENT VERSION
class DispositionVisitor(NodeVisitor):

  #Non-terminal methods
  def generic_visit(self, node, vc):
    return self.stringify(vc)

  def visit_section_disposition_sentencing_body(self, node, vc):
    contents = self.stringify(vc).replace("><", "> <")
    return " <disposition_sentencing_body> %s </disposition_sentencing_body> " % contents

  def visit_disposition_subsection(self, node, vc):
    contents = self.stringify(vc)
    return " <disposition_subsection> %s </disposition_subsection> " % contents

  def visit_disposition_type(self, node, vc):
    contents = self.stringify(vc)
    return " <disposition_type> %s </disposition_type> " % contents.strip()

  def visit_case_event(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event> %s </case_event> " % contents

  def visit_case_event_desc(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event_desc> %s </case_event_desc> " % contents

  def visit_code_section(self, node, vc):
    contents = self.stringify(vc)
    return " <code_section> %s </code_section> " % contents

  def visit_case_event_desc_and_date(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event_desc_and_date> %s </case_event_desc_and_date> " % contents

  def visit_case_event_line(self, node, vc):
    contents = self.stringify(vc)
    return " <case_event_type> %s </case_event_type> " % contents

  def visit_date(self, node, vc):
    contents = self.stringify(vc)
    return " <date> %s </date> " % contents

  def visit_is_final(self, node, vc):
    contents = self.stringify(vc)
    return " <finality> %s </finality> " % contents

  def visit_sequence(self, node, vc):
    contents = self.stringify(vc)
    contents = contents.replace(" / ", " ")
    return " <sequence> %s </sequence> " % contents

  def visit_sequence_description(self, node, vc):
    contents = self.stringify(vc)
    return " <sequence_description> %s </sequence_description> " % contents

  def visit_sequence_description_continued(self, node, vc):
    contents = self.stringify(vc)
    return " <sequence_description_continued> %s </sequence_description_continued> " % contents.strip()

  def visit_sequence_number(self, node, vc):
    contents = self.stringify(vc)
    return " <sequence_num> %s </sequence_num> " % contents

  def visit_things_a_judge_did(self, node, vc):
    contents = self.stringify(vc)
    return " <judge_action> %s </judge_action> " % contents

#   Traditional version
#   def visit_sentence_info(self, node, vc):
#     contents = self.stringify(vc)
#     return " <sentence_info> %s </sentence_info> " % contents

  #   Version for identifying sentence maxes and mins
  def visit_sentence_info(self, node, vc):
#    print("visit_sentence_info")
    min_pattern = re.compile(r".* min of (?P<time>[0-9\./]*) (?P<units>\w+).*", flags=re.IGNORECASE|re.DOTALL)
    max_pattern = re.compile(r".* max of (?P<time>[0-9\./]*) (?P<units>\w+).*", flags=re.IGNORECASE|re.DOTALL)
    range_pattern = re.compile(r".*?(?P<min_time>(?:[0-9\.\/]+(?:\s|$))+)(?P<min_unit>\w+ )?(?:to|-) (?P<max_time>(?:[0-9\.\/]+(?:\s|$))+)(?P<max_unit>\w+).*", flags=re.IGNORECASE|re.DOTALL)
    single_term_pattern = re.compile(r".* \s{5,}(?P<time>[0-9\./]+)\s(?P<unit>\w+)$.*", flags=re.IGNORECASE|re.DOTALL)
    temp_string = node.text
#    print(temp_string)
    min_length = None
    max_length = None
    min_length_match = re.match(min_pattern, node.text)
    max_length_match = re.match(max_pattern, node.text)
    range = re.match(range_pattern, node.text)
    single_term = re.match(single_term_pattern, node.text)

    if min_length_match is not None:
      #print("Min-length is %s number of %s" % (min_length.group('time'), min_length.group('units')))
      min_length = "<min_length> <time> %s </time> <unit> %s </unit> </min_length>" % (min_length_match.group('time'),min_length_match.group('units'))
      if max_length_match is None:
        max_length = "<max_length> <time> %s </time> <unit> %s </unit> </max_length>" % (min_length_match.group('time'),min_length_match.group('units'))

    #else:
      #print("Min length not found.")

    if max_length_match is not None:
#      print("Max-length is %s number of %s" % (max_length_match.group('time'), max_length_match.group('units')))
      max_length = "<max_length> <time> %s </time> <unit> %s </unit> </max_length>" % (max_length_match.group('time'),max_length_match.group('units'))
      if min_length_match is None:
        min_length = "<min_length> <time> %s </time> <unit> %s </unit> </min_length>" % (max_length_match.group('time'),max_length_match.group('units'))

    #else:
      #print("Max length not found")

    if range is not None:
      #print(range.groups())
      #print("Range from %s to %s %s" % (range.group('min_time'), range.group('max_time'),range.group('max_unit')))
      if range.group('min_unit') is not None:
        min_length = "<min_length> <time> %s </time> <unit> %s </unit> </min_length>" % (range.group('min_time'), range.group('min_unit'))
      else:
        min_length = "<min_length> <time> %s </time> <unit> %s </unit> </min_length>" % (range.group('min_time'), range.group('max_unit'))
      max_length = "<max_length> <time> %s </time> <unit> %s </unit> </max_length>" % (range.group('max_time'),range.group('max_unit'))
#     else:
#       print("Range not found.")

    if single_term is not None:
#      print("Single term is %s %s" % (single_term.group('time'), single_term.group('unit')))
      min_length = "<min_length> <time> %s </time> <unit> %s </unit> </min_length>" % (single_term.group('time'), single_term.group('unit'))
      max_length = "<max_length> <time> %s </time> <unit> %s </unit> </max_length>" % (single_term.group('time'), single_term.group('unit'))
#     else:
#       print("Single terms not found.")

    contents = self.stringify(vc)
    if min_length is not None and max_length is not None:
      contents = re.sub(r"(<length_of_sentence>)(.*)(</length_of_sentence>)", r"\1" + min_length + max_length + r"\3", contents)

#     print("New Contents:")
#     print(contents)
#     print("Finished with visit_sentence_info.")
    return " <sentence_info> %s </sentence_info> " % contents

  def visit_judge_name(self, node, vc):
    contents = self.stringify(vc)
    return " <judge_name> %s </judge_name> " % contents

  def visit_offense_disposition(self, node, vc):
    contents = self.stringify(vc)
    return " <offense_disposition> %s </offense_disposition> " % contents

  def visit_sentence_program_info(self, node, vc):
    contents = self.stringify(vc)
    return " <sentence_program_information> %s </sentence_program_information> " % contents

  def visit_program(self, node, vc):
    contents = self.stringify(vc)
    return " <program> %s </program> " % contents

  def visit_length_of_sentence(self, node, vc):
    contents = self.stringify(vc)
    return " <length_of_sentence> %s </length_of_sentence> " % contents

  def visit_extra_sentence_details(self, node, vc):
    contents = self.stringify(vc).replace("\n","...")
    return " <extra_sentence_details> %s </extra_sentence_details> " % contents

  def visit_footer(self, node, vc):
    contents = self.stringify(vc)
    return " <footer> %s </footer> " % contents

  #Terminal methods
  def visit_grade(self, node, vc):
    return " <grade> %s </grade> " % node.text

  def visit_single_char_no_comma_or_ws(self, node, vc):
    return node.text

  def visit_single_content_char_no_ws(self, node, vc):
    return node.text

  def visit_single_content_char(self, node, vc):
    return node.text

  def visit_single_content_char_no_comma(self, node, vc):
    return node.text

  def visit_number(self, node, vc):
    return node.text

  def visit_forward_slash(self, node, vc):
    return node.text

  def visit_new_line(self, node, vc):
    return node.text

  def visit_ws(self, node, vc):
    return node.text

  def visit_comma(self, node, vc):
    return node.text

  #Helpers
  def stringify(self, content):
    return "".join(content)


# OLD VERSION
# class DispositionVisitor(NodeVisitor):
#
#   #Non-terminal methods
#   def generic_visit(self, node, vc):
#     return self.stringify(vc)
#
#   def visit_heading(self, node, vc):
#     contents = self.stringify(vc).replace("><", "> <")
#     return " <heading> %s </heading> " % contents
#
#   def visit_section_disposition_sentencing_body(self, node, vc):
#     contents = self.stringify(vc).replace("><", "> <")
#     return " <disposition_sentencing_body> %s </disposition_sentencing_body> " % contents
#
#   def visit_disposition_subsection(self, node, vc):
#     contents = self.stringify(vc)
#     return " <disposition_subsection> %s </disposition_subsection> " % contents
#
#   def visit_disposition_type(self, node, vc):
#     contents = self.stringify(vc)
#     return " <disposition_type> %s </disposition_type> " % contents.strip()
#
#   def visit_disposition_details(self, node, vc):
#     contents = self.stringify(vc)
#     return " <disposition_details> %s </disposition_details> \n" % contents
#
#   def visit_case_event(self, node, vc):
#     contents = self.stringify(vc)
#     return " <case_event> %s </case_event> " % contents
#
#   def visit_case_event_line(self, node, vc):
#     contents = self.stringify(vc)
#     return " <case_event_type> %s </case_event_type> " % contents
#
#   def visit_sequence(self, node, vc):
#     contents = self.stringify(vc)
#     return " <sequence> %s </sequence> " % contents
#
#   def visit_sequence_description(self, node, vc):
#     contents = self.stringify(vc)
#     return " <sequence_description> %s </sequence_description> " % contents
#
#   def visit_seq_desc_continued(self, node, vc):
#     contents = self.stringify(vc)
#     return " <sequence_description_continued> %s </sequence_description_continued> " % contents
#
#   def visit_judge_date(self, node, vc):
#     contents = self.stringify(vc)
#     return " <judge_date> %s </judge_date> " % contents
#
#   def visit_sentence_program_info(self, node, vc):
#     contents = self.stringify(vc)
#     return " <sentence_program_information> %s </sentence_program_information> " % contents
#
#   def visit_footer(self, node, vc):
#     contents = self.stringify(vc)
#     return " <footer> %s </footer> " % contents
#
#   #Terminal methods
#   def visit_single_content_char(self, node, vc):
#     return node.text
#
#   def visit_word(self, node, vc):
#     return node.text
#
#   def visit_number(self, node, vc):
#     return node.text
#
#   def visit_forward_slash(self, node, vc):
#     return " %s " % node.text
#
#   def visit_new_line(self, node, vc):
#     return node.text
#
#   def visit_ws(self, node, vc):
#     return node.text
#
#   def stringify(self, content):
#     return "".join(content)




def parse(section_text):
  clean_section_text = clean_headers(section_text)
#   print("====")
#   print(clean_section_text)
#   print("====")
#   print("----")
#   print(temp_text)
#   print("-----")
  grammar = Grammar(grammars[0])
  visitor = DispositionVisitor()
  root = grammar.parse(clean_section_text)
  reconstituted_xml = visitor.visit(root)
  return reconstituted_xml


temp_text = r"""
Lower Court Proceeding (generic)
  Lower Court Disposition                                                    03/02/2011                                    Not Final
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                     Guilty                                          M            75 § 3802 §§ A1*
    99,999 / False Identification To Law Enforcement                            Not Guilty                                      M3           18 § 4914 §§ A
    Officer
Proceed to Court
  Information Filed                                                          06/02/2011                                    Not Final
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                          Added by Information                            M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                      Added by Information                            M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*
   99,999 / False Identification To Law Enforcement                               Disposed at Lower Court                         M3           18 § 4914 §§ A
   Officer
Quashed
    Trial                                                                      10/28/2011                                     Final Disposition
      1 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                            Quashed                                         M            75 § 3802 §§ A1*
      2 / DUI: Controlled Substance - Impaired Ability - 1st                      Quashed                                         M            75 § 3802 §§ D2*
      Offense
      99,999 / DUI: Gen Imp/Inc of Driving Safely - 1st Off                       Disposed at Lower Court                         M            75 § 3802 §§ A1*
      99,999 / False Identification To Law Enforcement                            Disposed at Lower Court                         M3           18 § 4914 §§ A
      Officer
"""

def clean_headers(section_text):
  """
  Takes a section text and removes all the header sections except the first.
  """
  cleaned = ["\n"]
  section_lines = section_text.split('\n')
  header_start_line = re.compile("^Disposition", flags=re.IGNORECASE)
  header_counter = 0
  for line in section_lines:
#     print("Searching: %s" % line)
#     print(header_start_line.search(line))
#     print("header_counter = %i" % header_counter)
    if (header_start_line.search(line) is not None):
      header_counter = 1
      if len(cleaned) == 0:  # <-- For keeping one copy of the header
        cleaned.append(line)
    else:
      if header_counter == 5:
        if len(cleaned) == 5:
          cleaned.append(line)
        header_counter = 0
      elif (header_counter > 0) and (header_counter < 5):
        if len(cleaned) < 6:
          cleaned.append(line)
        header_counter +=1
      else:
        cleaned.append(line)
  cleaned_string = "\n".join(cleaned[7:]).replace("\n\n","\n")
  #print("Type: %s" % type(cleaned_string))
  #return temp_text
  return cleaned_string + "\n"
