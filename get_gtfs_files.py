import os
import sys
import shutil
from io import BytesIO
from zipfile import ZipFile
import requests

from utils.config_utils import job_config


CONFIG, _ = job_config(sys.argv[1:])
WORKING_DIR = "./gtfs/working"
INPUT_DIR = "./gtfs/in"


def download_gtfs_feed(file_url, target_dir):
	response = requests.get(file_url)
	zip_file = ZipFile(BytesIO(response.content))
	zip_file.extractall(target_dir)


def move_gtfs_files(gtfs_config, src_dir, dst_dir):
	for k in gtfs_config:
		src_file = src_dir + "/{0}.txt".format(k)
		dst_file = dst_dir + "/{0}".format(gtfs_config[k]['file'])
		shutil.move(src_file, dst_file)
	for file in os.listdir(src_dir):
		os.remove(src_dir + "/{0}".format(file))


def main():
	download_gtfs_feed(CONFIG['feed_url'], WORKING_DIR)
	move_gtfs_files(CONFIG['gtfs'], WORKING_DIR, INPUT_DIR)


if __name__ == '__main__':
	main()
