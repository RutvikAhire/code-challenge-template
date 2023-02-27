"""
Empty
"""

import json
from datetime import datetime
import logging
import os
from sqlalchemy import insert
from flask import current_app
from application import db
from application.data_model import Readings, Results


class StatsUtilities:
    """
    Empty
    """
    root_directory = current_app.config['ROOT_DIR']
    formatter = logging.Formatter('%(asctime)s: %(message)s')

    def __init__(self):
        self.years_list = None
        self.stations_list = None
        self.avg_max_temperature_var = None
        self.avg_min_temperature_var = None
        self.total_accumulated_precipitation_var = None
        self.stats_dict = None
        self.result_json = None
        self.bulk_insert_list = None

        # Setup process logger
        self.log_folder_path = f'{self.root_directory}/logs'
        if not os.path.exists(self.log_folder_path):
            os.mkdir(self.log_folder_path)
        self.setup_datetime_str = str(
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.log_file_path = f'{self.log_folder_path}/analytics_{self.setup_datetime_str}.log'
        self.logger = logging.getLogger(self.setup_datetime_str)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(self.log_file_path, mode='a')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.logger.info(
            '=============== Logger setup complete ===============')
        self.logger.info('Log file location: %s', f'{self.log_file_path}')
        self.logger.info(
            '=============== ===================== ===============')

    def close_logger(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def data_extractor(self):
        """
        Extracts list of distinct years and stations from 'readings' table
        -- Future Enhancement: Also check if year-station combination result already exists in 'results.id'
            -- We only calculate stat results for year-station combinations not in 'results.id'
        """
        # Extract distinct years list
        years_extract = db.session.query(Readings.year).distinct().all()
        self.years_list = []
        for year_tuple in years_extract:
            for year in year_tuple:
                self.years_list.append(year)
        self.years_list.sort()
        # Extract distinct stations list
        stations_extract = db.session.query(
            Readings.station_id).distinct().all()
        self.stations_list = []
        for station_tuple in stations_extract:
            for station in station_tuple:
                self.stations_list.append(station)
        self.stations_list.sort()
        return self.years_list, self.stations_list

    def avg_max_temperature_calculator(self, year, station):
        """
        Calcultates average maximum temperature per station per year
        """
        try:
            max_temperature_extract = db.session.query(Readings.max_temperature).filter_by(
                year=year, station_id=station).all()
            # ignoring missing data while calculating stats
            max_temperature_values = []
            for value in max_temperature_extract:
                if value[0] is not None:
                    max_temperature_values.append(value[0])
            result = round(sum(max_temperature_values) /
                           len(max_temperature_values), 4)
            self.avg_max_temperature_var = result
        except ZeroDivisionError:
            self.avg_max_temperature_var = None
        return self.avg_max_temperature_var

    def avg_min_temperature_calculator(self, year, station):
        """
        Calcultates average minimum temperature per station per year
        """
        try:
            min_temperature_extract = db.session.query(
                Readings.min_temperature).filter_by(year=year, station_id=station).all()
            # ignoring missing data while calculating stats
            min_temperature_values = []
            for value in min_temperature_extract:
                if value[0] is not None:
                    min_temperature_values.append(value[0])
            result = round(sum(min_temperature_values) /
                           len(min_temperature_values), 4)
            self.avg_min_temperature_var = result
        except ZeroDivisionError:
            self.avg_min_temperature_var = None
        return self.avg_min_temperature_var

    def total_accumulated_precipitation_calculator(self, year, station):
        """
        Calcultates total accumulated precipitation per station per year
        """
        try:
            precipitation_extract = db.session.query(
                Readings.precipitation).filter_by(year=year, station_id=station).all()
            # ignoring missing data while calculating stats
            precipitation_values = []
            for value in precipitation_extract:
                if value[0] is not None:
                    precipitation_values.append(value[0])
            result = round(sum(precipitation_values), 4)
            self.total_accumulated_precipitation_var = result
        except Exception:
            self.total_accumulated_precipitation_var = None
        return self.total_accumulated_precipitation_var

    def statistics_calculator(self):
        """
        Integrates
        'avg_max_temperature_calculator',
        'avg_min_temperature_calculator', and
        'total_accumulated_precipitation_calculator' functions to run within year>station loop
        """
        self.stats_dict = {}
        for year in self.years_list:
            self.logger.info(
                'Computing statistics for the year: %s', f'{year}')
            self.stats_dict[year] = {}
            for station in self.stations_list:
                self.stats_dict[year][station] = {}
                avg_max_temperature_calculator_op = StatsUtilities.avg_max_temperature_calculator(
                    self, year, station)
                self.stats_dict[year][station]['avg_max_temperature'] = avg_max_temperature_calculator_op
                avg_min_temperature_calculator_op = StatsUtilities.avg_min_temperature_calculator(
                    self, year, station)
                self.stats_dict[year][station]['avg_min_temperature'] = avg_min_temperature_calculator_op
                total_accumulated_precipitation_calculator_op = StatsUtilities.total_accumulated_precipitation_calculator(
                    self, year, station)
                self.stats_dict[year][station]['total_accumulated_precipitation'] = total_accumulated_precipitation_calculator_op
        return self.stats_dict

    def results_json_writer(self):
        """
        Writes weather statistics report to .json file
        """
        root_directory = current_app.config['ROOT_DIR']
        results_directory = f'{root_directory}/results'
        date_time_stamp = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        with open(file=f'{results_directory}/results_{date_time_stamp}.json', mode='w') as outfile:
            json.dump(self.stats_dict, outfile)
        with open(f'{results_directory}/results_{date_time_stamp}.json', mode='r') as infile:
            self.result_json = json.load(infile)
        return self.result_json

    def results_db_writer(self):
        """
        Writes weather statistics to 'results' table
        """
        result_id_list = db.session.query(Results.result_id).all()
        distinct_result_id_list = list(set(result_id_list))
        distinct_result_id_dict = {}
        for item in distinct_result_id_list:
            distinct_result_id_dict[f'{item[0]}'] = None
        self.bulk_insert_list = []
        result_json_years = self.result_json.keys()
        for year_key in result_json_years:
            result_json_stations = self.result_json[year_key].keys()
            for station_key in result_json_stations:
                record_result_id = f'{year_key}{station_key}'
                # Check for duplicates
                result = (
                    record_result_id in distinct_result_id_dict)
                if result == 0:
                    distinct_result_id_dict[f'{record_result_id}'] = None
                    record_dict = {
                        'result_id': f'{record_result_id}',
                        'year': int(year_key),
                        'station_id': station_key,
                        'avg_max_temperature': self.result_json[year_key][station_key]['avg_max_temperature'],
                        'avg_min_temperature': self.result_json[year_key][station_key]['avg_min_temperature'],
                        'total_accumulated_precipitation': self.result_json[year_key][station_key]['total_accumulated_precipitation']
                    }
                    self.bulk_insert_list.append(record_dict)
        if len(self.bulk_insert_list) > 0:
            self.logger.info('Number of new results identified: %s',
                             f'{len(self.bulk_insert_list)}')
            self.logger.info('START: Bulk insertion of results')
            # db.session.query(Results).delete()
            # db.session.commit()
            db.session.execute(insert(Results), self.bulk_insert_list)
            db.session.commit()
            self.logger.info('END: Bulk insertion of results')
        else:
            self.logger.info('Number of new results identified: 0')

    def analytics_orchestrator(self):
        """
        Defines the sequence of methods execution within 'StatsUtilities' module
        """
        process_start_time = datetime.now()
        self.logger.info('Process Start DateTime: %s',
                         f'{process_start_time}')
        self.logger.info('START: analytics_orchestrator')
        self.logger.info('RUN: analytics_orchestrator >> data_extractor')
        StatsUtilities.data_extractor(self)
        self.logger.info(
            'RUN: analytics_orchestrator >> statistics_calculator')
        StatsUtilities.statistics_calculator(self)
        self.logger.info('RUN: analytics_orchestrator >> results_json_writer')
        StatsUtilities.results_json_writer(self)
        self.logger.info('RUN: analytics_orchestrator >> results_db_writer')
        StatsUtilities.results_db_writer(self)
        self.logger.info('END: analytics_orchestrator')
        process_end_time = datetime.now()
        self.logger.info('Process End DateTime: %s',
                         f'{process_end_time}')
        total_process_time = process_end_time - process_start_time
        self.logger.info('Total ingestion process time == %s',
                         f'{total_process_time}')
        # Close logger
        StatsUtilities.close_logger(self=self)
