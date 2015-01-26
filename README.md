## Project Structure

I'm pretty sure I'm the only person that will ever use this thing, so apologies in advance about the short documentation.

* `config/`: Directory containing a config file, written in YAML, for each job you want to process. Then name of the file corresponds to the job name command line argument when executing one of the main scripts.
* `gtfs/in/`: Directory for CSV files received from a GTFS feed.
* `gtfs/out/`: Directory for CSV files that have been prepared by the script: `prepare_gtfs_files.py`.
* `sql/`: Directory for SQL files:
    * A create tables script for each GTFS feed
    * A routes query extracting the desired production data from staging
    * A stops query extracting the desired production data from staging
* `tpl/`: Directory for template files. For example, SQL query strings that need to be merged with other data before being usable.
* `utils/`: A Python package for some basic utilities shared by the main scripts.
* `prepare_gtfs_files.py`: A script that takes GTFS feed files from `gtfs/in/` and prepares them for import into staging tables. Prepared files are output into the `gtfs/out/` directory.
* `populate_staging_data.py`: A script that imports data from prepared GTFS feed files (`gtfs/out/`) into the staging tables.
* `populate_production_data.py`: A script that performs expensive queries against staging tables to build final output for the production database.
