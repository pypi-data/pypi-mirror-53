import os, sys, time
import logging
import yaml, boto3


def check_environ(env_var, init_value=None):
    exit = False
    if os.environ[env_var] is None:
        if init_value is None:
            print 'Please export [%s] in initial scripts, such as ~/.bashrc, ~/.profile ... etc.' % (var)
            exit = True
        else:
            os.environ[env_var] = init_value

    if exit:
        sys.exit(1)


def init_path(path):
    if not os.path.exists(path):
        print ('path: [%s] is not existing, create it.' % path)
        os.makedirs(path)


def load_config(path, use_userdata=True):
    ## 1. load main config
    config = None
    if use_userdata == True:
        path = '%s/%s' % (COPS_EC2_CONFIG_PATH, path)

    try:
        with open(path, 'r') as stream:
            config = yaml.load(stream)

    #except yaml.YAMLError as ex:
    #    print "Error occurs when load config in %s/%s" % (COPS_USERDATA, path)
    #    print ex
    except Exception as ex:
        print "Error occurs when load config in [%s]" % path
        print ex
        sys.exit(1)

    ## 2. Scan and handle 'include' element
    # @TODO: support recusive include
    base_path = os.path.dirname(path)
    print 'base_path: ' + base_path

    if 'include' in config:
        for include_file in config['include']:

            include_path = '%s/%s' % (base_path, include_file)

            with open(include_path, 'r') as stream:
                include_obj = yaml.load(stream)
            config.update(include_obj)

    ## 3. Transfer the 'cval' variables
    return config


def load_userdata(path):
    try:
        return open(path, 'r').read()
    except Exception as ex:
        print ex

def show_settings():
    print '\nSettings:'
    print '  COPS_HOME        : %s' % COPS_HOME
    print '  COPS_USERDATA    : %s' % COPS_USERDATA
    print '  AWS_DEFAULT_PROFILE: %s' % AWS_PROFILE
    print '  AWS_DEFAULT_REGION : %s' % AWS_REGION


AWS_PROFILE = os.environ['AWS_DEFAULT_PROFILE']
AWS_REGION = os.environ['AWS_DEFAULT_REGION']
COPS_HOME = os.environ['COPS_HOME']
COPS_USERDATA = '.'

check_environ('AWS_DEFAULT_PROFILE')
check_environ('AWS_DEFAULT_REGION')
check_environ('COPS_HOME')

COPS_REGION_DATA_PATH = COPS_USERDATA
COPS_IAM_CONFIG_PATH = COPS_USERDATA
COPS_EC2_CONFIG_PATH = COPS_USERDATA

if 'COPS_USERDATA' in os.environ:
  COPS_USERDATA = os.environ['COPS_USERDATA']
  COPS_REGION_DATA_PATH = '%s/%s' % (COPS_USERDATA, AWS_REGION)
  COPS_EC2_CONFIG_PATH = '%s/ec2' % (COPS_REGION_DATA_PATH)
  COPS_IAM_CONFIG_PATH = '%s/IAM' % (COPS_USERDATA)

init_path(COPS_USERDATA)
init_path(COPS_REGION_DATA_PATH)
init_path(COPS_EC2_CONFIG_PATH)
init_path(COPS_IAM_CONFIG_PATH)
