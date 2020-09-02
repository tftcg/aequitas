import os
import glob
import re
from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET 
#import json
#from collections import Counter
from collections import OrderedDict

# Global
TOP_OUTPUT_DIR ='docs'

# Returns nothing
def mkdirp(directory):
    # TODO: if os.path.isfile(directory)
    if( not os.path.isdir(directory) ):
        os.makedirs(directory)

# Returns the inner xml of an Element; i.e. <a>Text <b>bob</b>. </a> would return 'Text <b>bob</b>. '
# https://stackoverflow.com/questions/3443831/python-and-elementtree-return-inner-xml-excluding-parent-element
def inner_xml(element):
    return (element.text or '') + ''.join(ET.tostring(e).decode() for e in element)

# Returns the text to output
def prepare_text(node):
    text = inner_xml(node)
    newtext = text.replace('[[', '').replace(']]', '').strip()
    newtext = re.sub(r'(.)\n(.)', r'\1<br/>\2', newtext)
    newtext = newtext.replace('<a href="http', '<a class="external" href="http')

    return newtext


# Load FAQ Template
faq_template_file = open('templates/faq.jinja2','r')
faq_template_text = faq_template_file.read()
faq_template = Environment(loader=FileSystemLoader("templates/")).from_string(faq_template_text)


def generate_faq(faq_dir, faq_template):
    faq_glob = os.path.join(faq_dir, '**', '*.xml')

    for file in glob.glob(faq_glob, recursive=True):
        filename = os.path.splitext(file)[0][len(faq_dir)+1:]
        faq_tree = ET.parse(file)
        faq_node=faq_tree.getroot()
        write_faq(faq_node, faq_template, filename)

def write_faq(faq_node, faq_template, filename):
        page = faq_template.render(faq_node=faq_node, f_prepare_text=prepare_text)
        #page = leaf_template.render(f_safe_name=safe_name, f_prepare_text=prepare_text, entries=found_entries, faq_name=leaf_name, f_source_label=source_label, parent_stack=parent_stack, tag_node=tag_node, filename=filename[len(TOP_OUTPUT_DIR)+1:], pretty_path=pretty_path, f_build_image_path=build_image_path, faq_db=faq_db )

        f = open('docs/roundups/' + filename + '.html', "w")
        f.write(page)
        f.close()

generate_faq('../aequitas-faq/faqxml-official', faq_template)
generate_faq('../aequitas-faq/faqxml-roundups', faq_template)
generate_faq('../aequitas-faq/faqxml-unofficial', faq_template)