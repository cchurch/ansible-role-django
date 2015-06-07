[![Build Status](http://img.shields.io/travis/cchurch/ansible-role-django.svg)](https://travis-ci.org/cchurch/ansible-role-django)
[![Galaxy](http://img.shields.io/badge/galaxy-cchurch.django-blue.svg)](https://galaxy.ansible.com/list#/roles/4069)

Django
======

Configure and update a Django project.

Role Variables
--------------

The following variables may be defined to customize this role:

- `django_app_path`: Directory containing Django project (required).
- `django_user`: User to become for running Django commands (default is
  `ansible_ssh_user`).
- `django_settings_templates`: List of templates to install with custom Django
  settings, default is `[]`.  Each item in the list should be a hash containing
  `src` and `dest` keys, and may also specify `owner`, `group`, `mode` and
  `backup` parameters.
- `django_settings`: Python path to the Django settings module for running
  Django commands, default is `omit`.
- `django_virtualenv`: Directory containing virtualenv for running Django
  commands, default is `omit`.
- `django_pre_commands`: List of extra django commands to run before the main
  commands, default is `[]`.
- `django_main_commands`: List of Django commands to run for normal project
  updates, default is `["syncdb", "migrate", "collectstatic"]`.
- `django_post_commands`: List of extra django commands to run after the main
  commands, default is `[]`.

Each item in a list of commands above may be specified as a string with only
the command name or as a hash with a `command` key and any other options
supported by the `django_manage` module, e.g.:

    - syncdb
    - command: migrate
      skip: yes
    - my_custom_command --noinput

Example Playbook
----------------

The following example playbook configures and updates a Django project:

    - hosts: all
      roles:
        - role: cchurch.django
          django_app_path: ~/src
          django_virtualenv: ~/env
          django_settings_templates:
            - src: ./templates/test.py.j2
              dest: ~/src/myproj/settings/test.py
          django_settings: myproj.settings.test
          django_pre_commands:
            - command: test
              failfast: yes
            - validate
          django_post_commands:
            - command: loaddata
              fixtures: defaults.json

License
-------

BSD

Author Information
------------------

Chris Church <chris@ninemoreminutes.com>
