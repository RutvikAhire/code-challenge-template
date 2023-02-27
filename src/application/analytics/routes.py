"""
Empty
"""

import os
import json
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, send_file
from application import executor
from application.analytics.stats_utility import StatsUtilities


ANALYTICS = Blueprint('analytics', __name__)


@executor.job
def analytics_orchestrator_task(stats_object):
    """
    Statistics Calculation Background Task
    Params: stats_object --> stats object created in analytics_hub
    """
    StatsUtilities.analytics_orchestrator(self=stats_object)


@ANALYTICS.route('/analytics')
def analytics_hub():
    """
    Landing page for viewing analytics results
    """
    analytics_hub.root_directory = current_app.config['ROOT_DIR']
    analytics_hub.results_directory = f'{analytics_hub.root_directory}/results'
    analytics_hub.report_files = os.listdir(
        analytics_hub.results_directory)
    analytics_hub.report_files.sort()
    if len(analytics_hub.report_files) == 0:
        analytics_hub.result_json = {
            "YYYY": {
                "USC00000000": {
                    "avg_max_temperature": None,
                    "avg_min_temperature": None,
                    "total_accumulated_precipitation": None
                }
            }
        }
    else:
        analytics_hub.report_filename = f'{analytics_hub.report_files[-1]}'
        analytics_hub.latest_report_filepath = f'{analytics_hub.results_directory}/{analytics_hub.report_filename}'
        with open(analytics_hub.latest_report_filepath, mode='r') as infile:
            analytics_hub.result_json = json.load(infile)
    return render_template('analytics/analytics_hub.html', title='Analytics', report_json=analytics_hub.result_json)


@ANALYTICS.route('/analytics/generate_report')
def analytics_generate_report():
    """
    Manually trigger generation of new report based on current data in 'readings' table
    """
    analytics_hub.stats_object = StatsUtilities()
    analytics_orchestrator_task.submit(stats_object=analytics_hub.stats_object)
    flash('Calculating weather statistics', 'success')
    return redirect(url_for('analytics.analytics_hub'))


@ANALYTICS.route('/analytics/download_report')
def analytics_download_report():
    """
    Download latest weather statistics report based on current data in 'results' table
    """
    analytics_download_report.root_directory = current_app.config['ROOT_DIR']
    analytics_download_report.results_directory = f'{analytics_download_report.root_directory}/results'
    analytics_download_report.report_files = os.listdir(
        analytics_download_report.results_directory)
    analytics_download_report.report_files.sort()
    if len(analytics_hub.report_files) == 0:
        analytics_hub.result_json = {
            "YYYY": {
                "USC00000000": {
                    "avg_max_temperature": None,
                    "avg_min_temperature": None,
                    "total_accumulated_precipitation": None
                }
            }
        }
        analytics_download_report.latest_report_filepath = '#'
    else:
        analytics_download_report.report_filename = f'{analytics_download_report.report_files[-1]}'
        analytics_download_report.latest_report_filepath = f'{analytics_download_report.results_directory}/{analytics_download_report.report_filename}'
    return send_file(analytics_download_report.latest_report_filepath, as_attachment=True)
