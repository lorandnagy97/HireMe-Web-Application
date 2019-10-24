import os
import yaml


basedir = os.path.abspath(os.path.dirname(__file__))


CONFIG_FILE = 'vars.yml'


def validate_deploy_env(env):
    """
    Validates that the environment is one of the three
    which we are expecting
    :param env: value os os.environ["ENV"]
    :return: bool, true if env is valid
    """
    if 'prod' not in env and \
            'test' not in env and \
            'local' not in env:
        sys.stderr.write("ERROR: Deployment Environment Must"
                         " Be One Of The Following:\n"
                         "'prod'\n"
                         "'test'\n"
                         "'local'\n")
        sys.exit(1)
    return 0


def get_deploy_env():
    """
    Reads ENV variable to figure out which environment deployment
    is occuring in.
    :return: value of ENV environment variable, string
    """
    try:
        deploy_env = os.environ["ENV"]
        validate_deploy_env(deploy_env)
        return deploy_env
    except (KeyError, TypeError) as missing_env_error:
        sys.stderr.write("ERROR: Deployment Environment Not Specified,"
                         " Please Define Var: %s\n" % missing_env_error)
        sys.exit(1)


def get_configurations(config_file):
    """
    Reads the configuration yml and assigns
    values to a dictionary
    :param config_file: file name of config yml
    :return: dictionary of configuration values
    """
    config_listings = yaml.full_load(
        open(config_file, 'r')
    )
    config_environment = get_deploy_env()
    configs = config_listings[config_environment]
    configs['deploy_env'] = config_environment
    return configs


def determine_db_type(vars):
    """
    Determines whether postgres or mysql
    database is in use
    :param vars: configuration options
    :return: url of database, or nothing if
    invalid configuration options
    """
    if 'postgres' in vars['db_type']:
        # Postgres Support
        return
    if 'mysql' in vars['db_type']:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
                                  vars['db_username'] + ':' + \
                                  vars['db_password'] + '@' + \
                                  vars['db_host'] + '/' + \
                                  vars['db_database'] or \
                                  'sqlite:///' + \
                                  os.path.join(basedir, 'app.db')
        return SQLALCHEMY_DATABASE_URI
    return



class Config(object):
    """
    Config object to be used throughout
    the application.
    """
    VARS = get_configurations(CONFIG_FILE)
    SECRET_KEY = VARS.get('secret_key', 'random_key_to_use')
    SQLALCHEMY_DATABASE_URI = determine_db_type(VARS)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'fi']