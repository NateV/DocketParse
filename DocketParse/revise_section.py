from lxml import etree
from pytest import set_trace
from DocketParse import grammar_modules
from glob import iglob
import os

def revise_section(docket_tree, section_name, section_module):
  """
  Method is used for plucking an unparsed section out of a parsed docket.
  This is useful when dockets have already been completely parsed with certain
  sections, but you'd like to parse another section but avoid parsing
  everything from the pdfs again.

  Input: the etree of the incompletely parsed docket,
         the name of the section to be revised,
         the name of the module to parse the section.
  Output: An etree now with the revised section parsed.
  """
  __import__("DocketParse.grammar_modules." + section_module)
  module = getattr(grammar_modules, section_module)


  root = docket_tree.getroot()
  docket_num = root.xpath("/docket/header/docket_number/text()")
  section_to_parse = root.xpath("/docket/section[@name='{}']/text()".format(section_name))[0]
  print("Section_to_parse:")
  print(section_to_parse)
  try:
    #set_trace()
    parsed_section = module.parse(section_to_parse)
  except:
    raise Exception("Could not parse section {} for {}.".format(section_name, docket_num))

  root.xpath("/docket/section[@name='{}']".format(section_name))[0].text = ""
  root.xpath("/docket/section[@name='{}']".format(section_name))[0].append(etree.fromstring(parsed_section))
  return docket_tree

def add_suffix(file, suffix):
  split_file = os.path.splitext(file)
  return "{}{}{}".format(split_file[0], suffix, split_file[1])



def revise_directory(dir_path, section_name, section_module, suffix=""):
  """
  Processes an entire directory of dockets that have an unparsed section to
  parse.
  Input: 1) path to a directory with dockets that have a section needing to be
            parsed.
         2) Name of section to be parsed and replaced.
         3) Name of grammar module
         4) Suffix. Optional.  Suffix is added to the revised dockets, so if
            you want to keep old and new versions, add a suffix to prevent the
            new version from overwriting the old one.
  """
  iterator = iglob("{}*.xml".format(dir_path))
  counter = 0
  successes = 0
  for file in iterator:
    print("Revising {}".format(file))
    try:
      tree = revise_section(etree.parse(file), section_name, section_module)
      successes += 1
      new_file = add_suffix(file, suffix)
      with open(new_file, "w") as f:
        f.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))
      f.close()
    except:
      print("{} failed revision.".format(file))
    counter += 1
  return (counter, successes)
















#End
