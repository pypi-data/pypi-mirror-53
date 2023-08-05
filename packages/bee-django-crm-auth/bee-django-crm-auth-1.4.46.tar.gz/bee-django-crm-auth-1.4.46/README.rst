==========
crm
==========

Quick start
-----------

1. Add "bee_django_crm" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'bee_django_crm.apps.CrmConfig',
    )

2. Include the crm URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    ...
    url(r'^crm/', include('bee_django_crm.urls')),

3.settings.py like this::

    USER_TABLE = ""

3. Run `python manage.py makemigrations`,`python manage.py migrate` to create the crm models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a crm (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/crm/ to participate in the crm.