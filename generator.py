import json
import copy
import os

from markdown import markdown
from jinja2 import Environment, FileSystemLoader


def open_json():
    json_path = 'config.json'
    with open(json_path, encoding='utf-8') as json_file:
        return json.load(json_file)


def get_jinja_template(filename, path):
    env = Environment(loader=FileSystemLoader(path),
                      auto_reload=True,
                      trim_blocks=True,
                      lstrip_blocks=True
                      )
    return env.get_template(filename)


def change_articles_paths(articles):
    articles_source = copy.deepcopy(articles)
    for article in articles_source:
        dir_path, file_path = article['source'].split('/')
        article['source'] = os.path.join(dir_path, file_path)
        article['source_html'] = os.path.join(dir_path, file_path.replace('.md', '.html'))
    return articles_source


def get_md_content(file_path):
    with open(file_path, encoding='utf-8') as md_file:
        return markdown(md_file.read())


def write_articles_content(articles, article_template, site_path):
    articles_path = 'articles'
    for article in articles:
        md_file_path = os.path.join(articles_path, article['source'])
        content = get_md_content(md_file_path)
        article_html = article_template.render(content=content, title=article['title'])
        check_site_dir(site_path, article['source_html'])
        article_html_path = os.path.join(site_path, article['source_html'])
        with open(article_html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(article_html)


def check_site_dir(root_path, file_path):
    dir_path = os.path.join(root_path, os.path.split(file_path)[0])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def write_index_content(html_path, html_content):
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)


def main():
    templates_path = 'templates'
    site_path = 'site'
    config = open_json()
    articles = config['articles']
    topics = config['topics']
    index_template = get_jinja_template('index.html', templates_path)
    article_template = get_jinja_template('article.html', templates_path)
    articles_with_html = change_articles_paths(articles)
    write_articles_content(articles_with_html, article_template, site_path)
    index_html = index_template.render(topics=topics, articles=articles_with_html)
    index_html_path = os.path.join(site_path, 'index.html')
    write_index_content(index_html_path, index_html)

if __name__ == '__main__':
    main()