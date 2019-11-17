[![Build Status](http://img.shields.io/travis/cchurch/ansible-role-django.svg)](https://travis-ci.org/cchurch/ansible-role-django)
[![Galaxy](http://img.shields.io/badge/galaxy-cchurch.django-blue.svg)](https://galaxy.ansible.com/cchurch/django/)

Django
======

Configure and update a Django project. Requires Ansible 2.4 or later.

Requirements
------------

When `become` is used (i.e. `django_user` does not equal `ansible_user` or
`ansible_ssh_user`), the necessary OS package(s) to support `become_method`
(e.g. `sudo`) must be installed before using this role.

The Django project must be made available on the target host prior to running
this role (via SCM checkout, rsync, etc.). The
[cchurch.scm](https://galaxy.ansible.com/cchurch/scm) role may
be useful to checkout a Django project from git/hg/svn.

The OS and Python package dependencies for the project, include Django itself,
must be installed prior to running this role. The
[cchurch.virtualenv](https://galaxy.ansible.com/cchurch/virtualenv) role may
be useful to install packages and create a virtualenv for running Django.

Role Variables
--------------

The following variables may be defined to customize this role:

- `django_app_path`: Directory containing Django project (required).
- `django_user`: User to become for running Django commands (default is
  `ansible_user` or `ansible_ssh_user`).
- `django_directories`: List of directories to be be created to support the
  Django project (for log files, uploaded media, etc.); default is `[]`. Each
  item in the list may be a single string specifying the directory name or a
  hash containing `path`, `owner`, `group` and `mode` keys.
- `django_settings_templates`: List of templates to install with custom Django
  settings, default is `[]`.  Each item in the list should be a hash containing
  `src` and `dest` keys, and may also specify `owner`, `group`, `mode`, `backup`
  and `force` parameters. Parent directories will be created if needed before
  installing settings files; `dir_owner`, `dir_group` and `dir_mode` keys may
  be set to specify ownership and permission options for the parent
  directories that differ from the settings files.
- `django_settings`: Python dotted path to the Django settings module for
  running Django commands (e.g. `proj.settings`); default is `omit`.
- `django_virtualenv`: Directory containing virtualenv to be activated before
  running Django commands; default is `omit`.
- `django_pre_commands`: List of extra Django commands to run before the main
  commands; default is `[]`.
- `django_main_commands`: List of Django commands to run for normal project
  updates; default is `[{command: "migrate", run_once: true}, "collectstatic"]`.
- `django_post_commands`: List of extra django commands to run after the main
  commands; default is `[]`.
- `django_run_once_host`: Hostname to use for running Django commands that
  specify `run_once`; default is `"{{ ansible_play_hosts_all[0] }}"` to target
  the first host specified in the play.

Each item in a list of commands above may be specified as a string with only
the command name or as a hash with a `command` key and any other options
supported by the [`django_manage`](https://docs.ansible.com/ansible/latest/modules/django_manage_module.html)
module, e.g.:

    - check
    - command: migrate
      skip: yes
      run_once: yes
      run_once_host: worker
    - command: collectstatic
      link: yes
    - command: my_custom_command --noinput
      changed_when: '"created" in result.stdout'

Each item may specify a `changed_when` conditional expression that will be
evaluated to determine if the command made any changes; the `result` variable
will be made available to the expression and contain the result from that
particular `django_manage` module invocation.

Each item may also specify `run_once` option, which causes the task to only run
on one host instead of all hosts targeted by the play. The item may also
specify `run_once_host` to override the default hostname specified via
`django_run_once_host`.

The following variable may be defined for the play or role invocation (but will
not work if defined as an inventory group or host variable):

- `django_notify_on_updated`: Handler name to notify when any changes were made
  while updating the Django project. The default is `"django updated"`; it is
  generally recommended for custom handlers to listen for `"django updated"`
  instead of changing the notification name.

This role can run Django management commands as another user, specified by
`django_user`, and will use the `become_method` specified for the
host/play/task to switch to this user. You may need to define
`allow_world_readable_tmpfiles` in your `ansible.cfg` (which still will
generate a warning instead of an error) or use another approach to support one
unprivileged user becoming another unprivileged user.

Example Playbook
----------------

The following example playbook configures and updates a Django project,
notifying a custom handler when anything was changed:

    - hosts: all
      vars:
        django_app_path: ~/src
        django_virtualenv: ~/env
        django_settings_templates:
          - src: local_settings.py.j2
            dest: ~/src/myproj/local_settings.py
        django_settings: myproj.settings
        django_pre_commands:
          - command: test
            failfast: yes
          - validate
        django_post_commands:
          - command: loaddata
            fixtures: defaults.json
      roles:
        - role: cchurch.django
      handlers:
        - name: django project updated
          debug:
            msg: "Django project in {{ django_app_path }} was updated!"
          listen: django updated

License
-------

BSD

Author Information
------------------

Chris Church ([cchurch](https://github.com/cchurch))
