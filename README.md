Simple PyTemplate
------------
Simple PyTemplate is a script build in Python 2.7 to emulate Ansible's template module.


Getting Started
---------------------
Move to local directory containing template source code

From the python console, run:

    > python2
    >>import template
    >>newtemplate = template.module_mode('vlans.j2', ('common.yml','n0-access-a.yml'))
    >>print str(newtemplate)

    hostname n0-access-a
    interface vlan 100
        description data vlan
        ip 192.168.1.1
        mask 24


From the terminal, run:

    >python template.py -h
    usage: template.py [-h] template [yamls [yamls ...]]

    Emulate Ansible's Template module

    positional arguments:
      template    Jinja2 filaname in ./templates (required)
      yamls       YAML filename(s) in ./host_vars (required)

    optional arguments:
      -h, --help  show this help message and exit


    >python2 template.py vlans.j2 common.yml n0-access-a.yml

    hostname n0-access-a
    interface vlan 100
        description data vlan
        ip 192.168.1.1
        mask 24


