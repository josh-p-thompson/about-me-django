import glob
import os
from jinja2 import Template
import markdown

def generate_page_list(): 
    """
    determines pages to be created based on directories within content directory
    returns list of dictionaries, each representing an html page to be created
    """
    pages = []
    for directory in glob.glob("content/*"): 
        title = os.path.basename(directory)
        file_name = title + ".html"
        if title == 'index': 
            title = 'about'

        # each file within directory is associated with a card to be displayed on the page
        cards = [markdown_to_html(file) for file in glob.glob(directory + "/*.md")]
        pages.append(
            {
                'file_name': file_name, 
                'source': directory + "/", 
                'destination': 'docs/' + file_name, 
                'title': title, 
                'cards': cards,
            }
        )
    return sorted(pages, key = lambda page: page['title']) 

def markdown_to_html(file): 
    """
    imports card files and returns dictionary with top and bottom sections of card
    """
    md = markdown.Markdown(extensions=["markdown.extensions.meta", "markdown.extensions.attr_list", "markdown.extensions.extra"])
    data = open(file).read()
    html = md.convert(data)
    title = md.Meta["title"][0]
    if title == 'projects': 
        project_link = md.Meta["project_link"][0]
    else: 
        project_link = None
    card = {'top': html.split('<hr />')[0], 
            'bottom': html.split('<hr />')[1], 
            'meta': {
                'title': title, 
                'project_link': project_link,
                }
            }
    return card

def build(pages): 
    template = Template(open('templates/base.html').read())
    for page in pages: 
        print(f'generating page: {page}\n') 
        full_page = template.render(
            title = page['title'],
            file_name = page['file_name'],
            cards = page['cards'],
            pages=pages,
        )
        open(page['destination'], 'w+').write(full_page)