import requests
import markdown
import glob
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    print('---------- rendering About')
    context = {
        'title': 'about',
        'path': '/', 
        'cards': [markdown_cards(file) for file in glob.glob('content/about/*.md')],
        'pages': pages(),
    }
    return render(request, 'base.html', context)

def projects(request):
    print('rendering projects page')
    context = generate_context('projects')
    return render(request, 'base.html', context)

def pages(): 
    return [
        {'title': 'about', 'path': '/'}, 
        {'title': 'projects', 'path': '/projects'}, 
    ]

def markdown_cards(file): 
    """
    imports card files and returns dictionary with top and bottom sections of card
    """
    md = markdown.Markdown(extensions=["markdown.extensions.meta", "markdown.extensions.attr_list", "markdown.extensions.extra"])
    data = open(file).read()
    html = md.convert(data)
    title = md.Meta["title"][0]
    card = {'top': html.split('<hr />')[0], 
            'bottom': html.split('<hr />')[1], 
            'meta': {
                'title': title, 
                }
            }
    return card

def readme_to_html(url): 
    md = markdown.Markdown(extensions=["markdown.extensions.meta", "markdown.extensions.attr_list", "markdown.extensions.extra"])
    data = requests.get(url).text
    return md.convert(data)

def github_projects(): 
    base_url = 'https://api.github.com'
    repos_url = '/users/josh-p-thompson/repos'
    params = {'affiliation': ['owner'], 'sort': 'updated'}
    
    response = requests.get(base_url + repos_url, params=params)
    repos_json = response.json()
    repos = []
    for repo in repos_json: 
        response = requests.get(base_url + f"/repos/josh-p-thompson/{repo['name']}/readme")
        repo_content = response.json()
        repos.append({
            'repo_name': repo['name'], 
            'repo_url': repo['url'], 
            'repo_description': repo['description'],
            'created_at': repo['created_at'], 
            'updated_at': repo['updated_at'],
            'repo_readme': readme_to_html(repo_content['download_url']),
        })
    return repos

print(github_projects())
