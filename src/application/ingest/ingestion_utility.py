import pandas as pd
from datetime import datetime
import logging
import os
from flask import current_app
from sqlalchemy import insert
from application import db, executor
from application.data_model import Readings
from application.analytics.stats_utility import StatsUtilities


class IngestionUtility:
    root_directory = current_app.config["ROOT_DIR"]
    wx_data_directory = current_app.config["WX_DATA_DIR"]
    formatter = logging.Formatter("%(asctime)s: %(message)s")

    def __init__(self, ingestion_files=None, ingestion_type=None):
        self.ingestion_files = ingestion_files
        self.ingestion_type = ingestion_type
        # Set input parameters if ingestion not triggered via front end
        if self.ingestion_files is None:
            all_files = os.listdir(self.wx_data_directory)
            all_files.sort()
            for file in all_files:
                if ".txt" not in file:
                    all_files.remove(file)
            if len(all_files) == 0:
                raise Exception(
                    'No files found in "wx_data_files" directory. Upload single wx_data file or contact admin.'
                )
            else:
                self.ingestion_files = all_files
        if self.ingestion_type is None:
            self.ingestion_type = "Non-Frontend: ingestion_utility.py script execution"

        # Setup process logger
        self.log_folder_path = f"{self.root_directory}/logs"
        if not os.path.exists(self.log_folder_path):
            os.mkdir(self.log_folder_path)
        self.setup_datetime_str = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.log_file_path = (
            f"{self.log_folder_path}/ingestion_{self.setup_datetime_str}.log"
        )
        self.logger = logging.getLogger(self.setup_datetime_str)
        self.logger.setLevel(logging.INFO)
        self.file_handler = logging.FileHandler(self.log_file_path, mode="a")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.logger.info("=============== Logger setup complete ===============")
        self.logger.info(
            "Number of wx_data files to be processed: %s",
            f"{len(self.ingestion_files)}",
        )
        self.logger.info("Ingestion request endpoint: %s", f"{self.ingestion_type}")
        self.logger.info("Log file location: %s", f"{self.log_file_path}")
        self.logger.info("=============== ===================== ===============")

    def close_logger(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    @staticmethod
    @executor.job
    def analytics_orchestrator_task(stats_object):
        """
        Statistics Calculation Background Task
        Params: stats_object --> stats object created in analytics_hub
        """
        StatsUtilities.analytics_orchestrator(self=stats_object)

    def ingestor(self):
        try:
            process_start_time = datetime.now()
            self.logger.info("Process Start DateTime: %s", f"{process_start_time}")

            reading_id_list = db.session.query(Readings.reading_id).all()
            distinct_reading_id_list = list(set(reading_id_list))
            distinct_reading_id_dict = {}
            for item in distinct_reading_id_list:
                distinct_reading_id_dict[f"{item[0]}"] = None

            bulk_insert_list = []
            for file in self.ingestion_files:
                file_station_id = str(
                    file.split(f"{self.wx_data_directory}/")[0].split(".txt")[0]
                )
                self.logger.info(
                    "Processing wx_data file: %s", f"{file_station_id}.txt"
                )

                # Read file data into 'file_df' dataframe
                file_df = pd.read_csv(
                    filepath_or_buffer=f"{self.wx_data_directory}/{file_station_id}.txt",
                    sep="\t",
                    header=None,
                )
                row_counter = 0
                while row_counter < len(file_df):
                    row_data = file_df.iloc[row_counter].to_list()
                    record_reading_id = f"{file_station_id}{str(row_data[0])}"
                    # Check for duplicates
                    result = record_reading_id in distinct_reading_id_dict
                    if result == 0:
                        distinct_reading_id_dict[f"{record_reading_id}"] = None
                        record_year = int(str(row_data[0])[:4])
                        record_month = int(str(row_data[0])[4:6])
                        record_day = int(str(row_data[0])[6:8])
                        record_max_temperature = (
                            int(str(row_data[1]))
                            if str(row_data[1]) != "-9999"
                            else None
                        )
                        record_min_temperature = (
                            int(str(row_data[2]))
                            if str(row_data[2]) != "-9999"
                            else None
                        )
                        record_precipitation = (
                            int(str(row_data[3]))
                            if str(row_data[3]) != "-9999"
                            else None
                        )
                        record_dict = {
                            "reading_id": f"{record_reading_id}",
                            "station_id": file_station_id,
                            "year": record_year,
                            "month": record_month,
                            "day": record_day,
                            "max_temperature": round(record_max_temperature * 0.10, 4)
                            if record_max_temperature is not None
                            else record_max_temperature,
                            "min_temperature": round(record_min_temperature * 0.10, 4)
                            if record_min_temperature is not None
                            else record_min_temperature,
                            "precipitation": round(record_precipitation * 0.01, 4)
                            if record_precipitation is not None
                            else record_precipitation,
                        }
                        bulk_insert_list.append(record_dict)
                    row_counter = row_counter + 1
            self.logger.info(
                "Number of bulk insert records identified: %s",
                f"{len(bulk_insert_list)}",
            )
            if len(bulk_insert_list) > 0:
                self.logger.info("START: Bulk records insertion")
                db.session.execute(insert(Readings), bulk_insert_list)
                db.session.commit()
                self.logger.info("END: Bulk records insertion successful")

            process_end_time = datetime.now()
            self.logger.info("Process End DateTime: %s", f"{process_end_time}")
            total_process_time = process_end_time - process_start_time
            self.logger.info(
                "Total ingestion process time == %s", f"{total_process_time}"
            )

            # Initiate statistics calculation for newly ingested records
            if len(bulk_insert_list) > 0:
                self.logger.info(
                    "Initiated background task for weather statistics results computation for newly added records"
                )
                # Close logger
                IngestionUtility.close_logger(self=self)

                stats_object = StatsUtilities()
                IngestionUtility.analytics_orchestrator_task.submit(
                    stats_object=stats_object
                )

        except Exception as error:
            self.logger.info("%s", f"{error}")
