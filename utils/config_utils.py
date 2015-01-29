import sys
import yaml


def main_config(args):
	config_file = './config/.main.yml'

	try:
		with open(config_file, 'r') as file:
			config = yaml.safe_load(file)
	except IOError:
		sys.exit("Missing main config file: '{0}'".format(config_file))

	try:
		return config[args[0]], config_file
	except IndexError:
		sys.exit("Target system parameter is required: 'dev' or 'prod'")
	except KeyError:
		sys.exit("Target system parameter is not valid: 'dev' or 'prod'")


def job_config(args):
	try:
		config_file = './config/{0}.yml'.format(args[1])
	except IndexError:
		sys.exit("Job name is a required argument. Example: chicago_cta")

	try:
		with open(config_file, 'r') as file:
			config = yaml.safe_load(file)
	except IOError:
		sys.exit("Missing config file for job: '{0}'".format(config_file))

	return config, config_file
