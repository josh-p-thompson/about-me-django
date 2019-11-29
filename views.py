import requests
import markdown
import glob
from django.http import HttpResponse
from django.shortcuts import render
import os
from datetime import datetime

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
    print('---------- rendering Projects')
    context = {
        'title': 'projects',
        'path': 'projects', 
        'cards': github_projects(),
        'pages': pages(),
    }
    return render(request, 'projects.html', context)

def blog(request):
    print('---------- rendering Blog')
    context = {
        'title': 'blog',
        'path': 'blog', 
        'cards': [markdown_cards(file) for file in glob.glob('content/blog/*.md')],
        'pages': pages(),
    }
    return render(request, 'blog.html', context)

def pages(): 
    return [
        {'title': 'about', 'path': '/'}, 
        {'title': 'projects', 'path': 'projects'}, 
        {'title': 'blog', 'path': 'blog'}, 
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
    """
    calls github API to return a list of all repos 
    then loops through repos to extract repo name, url, description, updated time
    calls github API for each repo to get readme url and converts it to html
    returns list of repo dictionaries with extracted data
    """
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
            'repo_url': repo['html_url'], 
            'repo_description': repo['description'],
            'updated_at': datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
            'repo_readme': readme_to_html(repo_content['download_url']),
        })
    return repos