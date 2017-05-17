#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'xiaojieluo'
SITENAME = "llnhhy's Blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

# DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'misc'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

THEME = 'themes/abctheme'
#THEME_STATIC_DIR = 'themes/abctheme'
THEME_STATIC_PATHS = ['static']
CSS_FILE = 'style.css'

# 插件设置
PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap', 'googleplus_comments', 'render_math']
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# 主题设置
DESCRIPTION = "To be a Full Stack Engineer."
THEME_LINKS = (('Github','http://www.github.com/'),
                ('Linkedin','http://linkedin.com/'),)

DEFAULT_DATE_FORMAT = '%B %d %Y'

ABC_THEME = dict(
    copyright = '&copy; 2017 LuoXiaojie  Powered by <a href="http://1.1.1.1/" target="_blank">Pelican</a> Theme &copy; <a href="https://github.com/xiaojieluo" target="_blank">LuoXiaojie</a>',
)

GOOGLE_ANALYTICS = 'UA-92533917-2'

PAGE = (('Home', '/'),
        ('Archive', '/archives'),
        )

SITE = dict(
    # name = SITENAME,
    # url = 'http://www.llnhhy.com/', # 如果为空,则使用相对url
    title = SITENAME,
    # language = 'zh',
    description = 'llnhhy\'s Blog | Web | python | Code | Computer Sciences',
    copyright = '<p>I’m <strong><a href="/about">LuoXiaojie</a></strong>, a web developer who contributes open-source projects. You are reading my <a href="http://www.llnhhy.com">blog</a> powered by <a href="https://blog.getpelican.com/">Pelican</a> and <a href="https://github.com/xiaojieluo/abctheme_for_pelican.git">abctheme</a>. All articles are under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">CC BY-NC-ND 4.0</a>. Follow me on <a href="https://twitter.com/xiaojieluo">Twitter</a> for communicating, <a href="https://github.com/Xiaojieluo">GitHub</a> for code, and <a href="https://www.instagram.com/geekplux">Instagram</a> for daily.</p>'
)

TWITTER_NAME = 'xiaojieluo'

SOCIAL = dict(
    twitter = dict(name = 'luoxiaojie',description = SITE.get('description', None)),
    facebook = dict(name = 'xiaojieluo'),
)
