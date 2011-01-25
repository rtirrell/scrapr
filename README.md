# scrapr

## Overview
This project demonstrates the right and proper use of Django, python-twitter, jQuery, and Google's javascript visualization library.

## Requirements
* django (any recent version should do, but we've only tested 1.2 and 1.3).
* sqlite3 (strictly optional, but the admin requires it, and the admin is one of Django's great features)
* python-twitter

## Install
Probably easiest is to use pip to install the libraries.
Then:
    mkdir db
    touch db/development.db
    python manage.py syncdb
    python manage.py runserver
    python -c 'import webbrowser; webbrowser.open("http://localhost:8000/app/")'
