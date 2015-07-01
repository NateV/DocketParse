
from parsimonious import Grammar
from parsimonious import NodeVisitor


grammars = [
r"""
#Nonterminals
defendant_information = new_line? birth_info line*

birth_info = "Date Of Birth:" ws+ birth_date ws+ "City/State/Zip:" location new_line
birth_date = number forward_slash number forward_slash number
location = single_content_char+

line = single_content_char* new_line

#terminals
number = ~"[0-9,\.]+"
single_content_char =  ~"[a-z0-9`\ \"=_\.,\-\(\)\'\$\?\*%;:#&\[\]/@§]"i
forward_slash = "/"
ws = " "
new_line = "\n"
"""
]

class DefendantInfoVisitor(NodeVisitor):
  #Nonterminals
  def generic_visit(self, node, vc):
    return self.stringify(vc)

  def visit_defendant_information(self, node, vc):
    contents = self.stringify(vc)
    return " <defendant_information> %s </defendant_information> " % contents

  def visit_birth_date(self, node, vc):
    contents = self.stringify(vc)
    return " <birth_date> %s </birth_date> " % contents

  def visit_location(self, node, vc):
    contents = self.stringify(vc)
    return " <location> %s </location> " % contents

  def visit_line(self, node, vc):
    contents = self.stringify(vc)
    return " <extra_info> %s </extra_info> " % contents

  #Terminals
  def visit_number(self, node, vc):
    return node.text

  def visit_single_content_char(self,node, vc):
    return node.text

  def visit_forward_slash(self, node, vc):
    return node.text

  def visit_ws(self, node, vc):
    return node.text

  def visit_new_line(self, node, vc):
    return node.text

  #Helpers
  def stringify(self, list):
    return "".join(list)


def parse(section_text):
  section_text += "\n"
  grammar = Grammar(grammars[0])
  visitor = DefendantInfoVisitor()
  root = grammar.parse(section_text)
  section_xml = visitor.visit(root)
  return section_xml