

# TODO:

# Define a stylesheet for the site
# Fix the list css
# Put logo on lhs
# Make it a link back to main page
# Steal style from faq site with regards to spacing etc
# Generate a site that has each of the faqs listed on it. Or hand write it given it'll be pretty basic.

import os
import glob
import re
from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET 
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
    output_dir = os.path.join('docs', 'roundups', re.sub(r'faqxml-', '', os.path.basename(faq_dir)))
    mkdirp(output_dir)

    for file in glob.glob(faq_glob, recursive=True):
        filename = os.path.splitext(file)[0][len(faq_dir)+1:]
        faq_tree = ET.parse(file)
        faq_node=faq_tree.getroot()
        write_faq(faq_node, faq_template, output_dir, filename)

def write_faq(faq_node, faq_template, output_dir, filename):
    path = os.path.join(output_dir, filename) + '.html'

    page = faq_template.render(faq_node=faq_node, f_prepare_text=prepare_text, filename=filename, path=path[5:])
    #page = leaf_template.render(f_safe_name=safe_name, f_prepare_text=prepare_text, entries=found_entries, faq_name=leaf_name, f_source_label=source_label, parent_stack=parent_stack, tag_node=tag_node, filename=filename[len(TOP_OUTPUT_DIR)+1:], pretty_path=pretty_path, f_build_image_path=build_image_path, faq_db=faq_db )

    page = re.sub('<tftcg-note>', '<div class="tftcg-note">', page)
    page = re.sub('</tftcg-note>', '</div>', page)

    f = open( path, 'w' )
    f.write(page)
    f.close()

generate_faq('../aequitas-faq/faqxml-wotc-faqs', faq_template)
generate_faq('../aequitas-faq/faqxml-wotc-roundups', faq_template)
generate_faq('../aequitas-faq/faqxml-aequitas-roundups', faq_template)
generate_faq('../aequitas-draft-faq/faqxml-aequitas-roundups', faq_template)
