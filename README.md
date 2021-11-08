# Django cheat-sheet

Welcome in my django cheat-sheet app, which only purpose is to give beginner django developers insight how basic concepts can be done with django. Some topics that are covered:

* Urls, models, view, templates --> (Model - View - Controller)
* Authentication and Authorization
* Forms
* Admin panel

Most of the views are implemented as class based and function based.
 
Note that this project is still under construction, so I will be polishing it and adding more features over time. Feel free to open any pull requests or issues. 

## How to start django project?

1. Create virtual environment. In my case I'm using  virtualenvwrapper 
    - cmd: ``mkvirtualenv <project_name>``
    - docs: https://virtualenvwrapper.readthedocs.io/en/latest/
    - tutorial: https://www.geeksforgeeks.org/using-mkvirtualenv-to-create-new-virtual-environment-python/

2. Install Django
    - cmd: ``python -m pip install Django``
    
3. Initialize Django project
    - cmd: ``django-admin startproject tmp_project``
    - note: This command will create django project named tmp_project on current path in your terminal. Make sure, you are staying in the place where you wan't to gather django applications
    
4. Create first django application
    - cmd: ``python manage.py startapp tmp_app``
    - docs: https://docs.djangoproject.com/en/3.2/ref/applications/

5. (Optional) init git repo and create initial commit
    - cmd: ``git init``
    - cmd2: ``git add .``
    - cmd3: ``git commit -m "Initial commit"``
