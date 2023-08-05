import click, os, sys, functools, subprocess, timeit, runpy
from .Intel import information

def is_project():
    try:
        with open(os.path.join(os.getcwd(), 'requirements.txt'), 'r') as project_file:
            PROJECT_MODULES = project_file.readlines()
            if len(PROJECT_MODULES):
                for module in PROJECT_MODULES:
                    if("reconframe" in module):
                        IS_PROJECT = True
                        break

    except:
        return {"IS_PROJECT": False, "PROJECT_MODULES": [], "PROJECT_DIR": lambda x: '' }

    PROJECT_DIR = lambda add: os.path.join(os.getcwd(), add)

    return {"IS_PROJECT": IS_PROJECT, "PROJECT_MODULES": PROJECT_MODULES, "PROJECT_DIR": PROJECT_DIR }

@click.group()
def cli():
    """reconframe v0.1.0 - by 0xcrypto <me@ivxenog.in>"""
    

@cli.command()
@click.option('--project', default=".", help='Project Name')
def init(project):
    """Initialize  a new reconframe project."""
    (not is_project()['IS_PROJECT']) or exit_cli("Project already exists!")

    currentdir = os.path.join(os.getcwd(), project)
    os.system('git clone --depth=1 https://github.com/0xcrypto/reconframe-project %s' % currentdir)
    os.system('cd %s; git remote remove origin' % currentdir)


@cli.command()
def install():
    """Install the requirements to the current project."""
    is_project()['IS_PROJECT'] or exit_cli("Not a reconframe project!")
    os.system('pip install -r requirements.txt')


@cli.command()
@click.argument('command')
def run(command):
    """Run an external command and parse its output as Information"""
    is_project()['IS_PROJECT'] or exit_cli("Not a reconframe project!")
    exit_cli(information(subprocess.check_output(command, shell=True)))


@cli.command()
def start():
    """Run the project's main strategy."""
    is_project()['IS_PROJECT'] or exit_cli("Not a reconframe project!")
    click.echo("Implementing strategies...")
    timer = timeit.Timer(execute)
    exit_cli("Time taken: %ss" % timer.timeit(1))


@cli.command()
def prepare():
    """Prepare the report."""
    print('prepare the report')


def exit_cli(message=""):
    click.echo(message)
    exit()


def execute():
    try:
        return runpy.run_path(is_project()['PROJECT_DIR']('main.py'), run_name='__main__')
    except FileNotFoundError:
        exit_cli("main.py not found!")
