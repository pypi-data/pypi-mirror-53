===========
Django_Ops
===========

Django_Ops is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_ops" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_ops',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('ops/', include('django_ops.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server.

5. Visit http://127.0.0.1:8000/ops/.
