import os
import utils
import click


@click.command()
@click.option('--name', prompt='Project name', default='machine-learning-project')
def init(name):
    """Creating the dir structure for a Machine Learning project with MLflow"""
    print("Creating directories....")
    utils.create_dirs()
    print("Creating files....")
    utils.create_files(name)

    current_dir = os.getcwd()
    full_dir = current_dir + '/src/models/'

    utils.create_file('model.py', name, full_dir)
    utils.create_file('train.py', name, current_dir + '/src/')
    utils.create_file('settings.py', name, current_dir + '/src/')

    utils.write_file('', full_dir + '__init__.py')
    utils.write_file('', current_dir + '/src/data/__init__.py')
    utils.write_file('', current_dir + '/src/data/data_preparation.py')
    utils.write_file('', current_dir + '/src/__init__.py')
    utils.create_docker_file()
    print("Done!")
