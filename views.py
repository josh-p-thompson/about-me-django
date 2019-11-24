# import requests
import markdown
import glob
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    print('rendering about page')
    context = generate_context('about')
    return render(request, 'base.html', context)

def projects(request):
    print('rendering projects page')
    context = generate_context('projects')
    return render(request, 'base.html', context)

def blog(request):
    print('rendering blog page')
    context = generate_context('blog')
    return render(request, 'base.html', context)

def generate_context(title): 
    path = '/'
    if title != 'about': 
        path += title
    pages = [
        {'title': 'about', 'path': '/'}, 
        {'title': 'projects', 'path': '/projects'}, 
        {'title': 'blog', 'path': '/blog'}, 
    ]
    cards = [markdown_to_html(file) for file in glob.glob('content/' + title + "/*.md")]
    return {
        'title': title,
        'path': path,
        'cards': cards,
        'pages': pages,
    }

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