import sys
import yaml


def job_config(args):
	try:
		config_file = './config/{0}.yml'.format(args[0])
	except IndexError:
		sys.exit("Job name is a required argument. Example: chicago_cta")

	try:
		with open(config_file, 'r') as file:
			config = yaml.safe_load(file)
	except IOError:
		sys.exit("Missing config file for job: '{0}'".format(config_file))

	return config, config_file
