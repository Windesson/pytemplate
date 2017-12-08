from jinja2 import FileSystemLoader, Environment, StrictUndefined
import yaml
import os
import argparse
import imp

"""
A python2 program to emulate Ansible's template module
"""

BASE_DIR = os.path.dirname(__file__)
DEFAULT_TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DEFAULT_CUSTOM_FILTER_DIR = os.path.join(BASE_DIR, 'filter_plugins')
DEFAULT_VARS_DIR = os.path.join(BASE_DIR, 'host_vars')


def cli_mode():
    """ Entry point via cli """

    args = parse_args()
    jinja_file_name = args.template
    yaml_file_list = args.yamls

    rendered_file = get_rendered_template(
        jinja_file_name, yaml_file_list
    )
    print rendered_file


def module_mode(jinja_file_name, yaml_file_list):
    """ Entry point via module call"""
    rendered_file = get_rendered_template(
        jinja_file_name, yaml_file_list
    )
    return rendered_file


def get_rendered_template(jinja_file_name, yaml_file_list):
    data = parse_yaml_files(yaml_file_list)
    env = load_environment()
    t = env.get_template(jinja_file_name)
    rendered_file = t.render(**data)
    return rendered_file


def parse_yaml_files(yaml_file_list):
    """ Function to open yaml files and parse into dictionary """
    variables = {}
    for filename in yaml_file_list:
        raw_data = open(os.path.join(DEFAULT_VARS_DIR, filename)).read()
        variables.update(yaml.load(raw_data))
    return variables


def parse_args():
    """ Function to parse and validate user input """
    arg_parser = argparse.ArgumentParser(
        description="Emulate Ansible's Template module"
    )

    arg_parser.add_argument(
        'template',
        help='Jinja2 filaname in ./templates (required)'
    )

    arg_parser.add_argument(
        'yamls',
        nargs='*',
        help='YAML filename(s) in ./host_vars (required)'
    )

    args = arg_parser.parse_args()
    return args


def load_environment():
    """ Set up JINJA2 ENV"""
    env = Environment(
        loader=FileSystemLoader(DEFAULT_TEMPLATE_DIR),
        undefined=StrictUndefined  # Force variable to be defined
    )

    load_custom_filter(env)
    return env


def load_custom_filter(env):
    """ Import custom jinja2 filter from default dir filter_plugins """
    if os.path.exists(DEFAULT_CUSTOM_FILTER_DIR):
        for filename in os.listdir(DEFAULT_CUSTOM_FILTER_DIR):
            try:
                if filename.endswith(".py"):
                    new_module = os.path.join(
                        DEFAULT_CUSTOM_FILTER_DIR, filename
                    )
                    temp = imp.load_source(
                        filename.replace('.py', ''), new_module
                    )
                    OBJFilter = temp.FilterModule()
                    for k, v in OBJFilter.filters().iteritems():
                        env.filters[k] = v
            except Exception as e:
                print e
                pass


if __name__ == '__main__':
    cli_mode()
