"""
This module deals with the the following weather data APIs:
    - /api/weather
    - /api/weather/stats
"""

from flask import Blueprint
from sqlalchemy.exc import NoResultFound
from flask_restx import Api, Resource
from flask_restx import reqparse
from application.data_model import Readings, readings_schema, Results, results_schema

api_bp = Blueprint('api', __name__)
api = Api(api_bp, title='REST Explorer', description='Swagger UI demo for Colaberry Coding Test', contact='Rutvik Ahire',
          doc='/rest_explorer', default='Weather APIs', default_label='APIs for requesting weather related data', ordered=True)


def paginate_response(paginate_object, args):
    """
    Paginates JSON response
    Maximum records per page = 1000
    """
    if args['page'] is None:
        paginate_object.page = 1
        final_page = paginate_object.page
        final_output = paginate_object.items
    else:
        if int(args['page']) > paginate_object.pages:
            paginate_object.page = paginate_object.pages
            final_page = paginate_object.page
            final_output = paginate_object.items
        else:
            paginate_object.page = int(args['page'])
            final_page = paginate_object.page
            final_output = paginate_object.items
    return final_output, final_page


@api.route('/weather')
class ApiWeather(Resource):
    """
    This resource allows user to query 'Readings' table to fetch data with following query params:
        - date
        - station
        - page number
    """
    @api.doc('get-weather-records')
    @api.param('date', description='A date for which weather records need to be retrieved.', required=False, example='20230220')
    @api.param('station', description='A station for which weather records need to be retrieved.', required=False, example='USC00110072')
    @api.param('page', description='Page number of the paginated response to be retreived.', required=False, example='1')
    @api.response(200, description='Success')
    @api.response(204, description='No content')
    @api.response(400, description='Malformed request syntax')
    @api.response(404, description='Not found')
    def get(self):
        """
        API resource providing records from 'readings' table as response
        Can be filtered based on date and/or station
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'date', required=False, type=str, help='Required format: YYYYMMDD')
        parser.add_argument(
            'station', required=False, type=str, help='Required format: ABC12345678')
        parser.add_argument(
            'page', required=False, type=str, help='Required format: 1; Required condition: >0')
        args = parser.parse_args(strict=True)
        date = args['date']
        station = args['station']
        page = args['page']
        if date is not None and station is not None:
            if len(date) == 8 and len(station) == 11:
                q_year = int(date[:4])
                q_month = int(date[4:-2])
                q_day = int(date[-2:])
                q_station_id = station.upper()
                try:
                    readings = Readings.query.filter(
                        Readings.year == q_year, Readings.month == q_month, Readings.day == q_day, Readings.station_id == q_station_id
                    ).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=readings, args=args)
                    # Serialize the queryset
                    serialized_output = readings_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather",
                            "output_count": readings.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": readings.pages,
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given date and station could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "date": date,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        elif date is None and station is not None:
            if len(station) == 11:
                q_station_id = station.upper()
                try:
                    readings = Readings.query.filter(
                        Readings.station_id == q_station_id).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=readings, args=args)
                    # Serialize the queryset
                    serialized_output = readings_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather",
                            "output_count": readings.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": readings.pages,
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given station could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "date": date,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        elif date is not None and station is None:
            if len(date) == 8:
                q_year = int(date[:4])
                q_month = int(date[4:-2])
                q_day = int(date[-2:])
                try:
                    readings = Readings.query.filter(
                        Readings.year == q_year, Readings.month == q_month, Readings.day == q_day).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=readings, args=args)
                    # Serialize the queryset
                    serialized_output = readings_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather",
                            "output_count": readings.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": readings.pages,
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "date": date,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given date could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "date": date,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        else:
            readings = Readings.query.paginate(per_page=1000)
            paginate_response_op = paginate_response(
                paginate_object=readings, args=args)
            # Serialize the queryset
            serialized_output = readings_schema.dump(
                paginate_response_op[0])
            if len(serialized_output) != 0:
                response = {
                    "endpoint": "/weather",
                    "output_count": readings.total,
                    "current_page": paginate_response_op[1],
                    "total_pages": readings.pages,
                    "args": {
                        "date": date,
                        "station": station,
                        "page": page
                    },
                    "response": serialized_output
                }
                return response, 200
            else:
                response = {
                    "endpoint": "/weather",
                    "output_count": readings.total,
                    "current_page": paginate_response_op[1],
                    "total_pages": readings.pages,
                    "args": {
                        "date": date,
                        "station": station,
                        "page": page
                    },
                    "message": "There is no content to send for this request"
                }
                return response, 204


@api.route('/weather/stats')
class ApiWeatherStats(Resource):
    """
    This resource allows user to query 'Results' table to fetch data with following query params:
        - year
        - station
        - page number
    """
    @api.doc('get-weather-statistics')
    @api.param('year', description='A year for which weather records need to be retrieved.', required=False, example='2023')
    @api.param('station', description='A station for which weather records need to be retrieved.', required=False, example='USC00110072')
    @api.param('page', description='Page number of the paginated response to be retreived.', required=False, example='1')
    @api.response(200, description='Success')
    @api.response(204, description='No content')
    @api.response(400, description='Malformed request syntax')
    @api.response(404, description='Not found')
    def get(self):
        """
        API resource providing stats from 'results' table as response
        Can be filtered based on year and/or station
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            'year', required=False, type=str, help='Required format: 2023')
        parser.add_argument(
            'station', required=False, type=str, help='Required format: USC00110072')
        parser.add_argument(
            'page', required=False, type=str, help='Required format: 1; Required condition: >0')
        args = parser.parse_args(strict=True)
        year = args['year']
        station = args['station']
        page = args['page']
        if year is not None and station is not None:
            if len(year) == 4 and len(station) == 11:
                q_year = year
                q_station_id = station.upper()
                try:
                    results = Results.query.filter(
                        Results.year == q_year, Results.station_id == q_station_id
                    ).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=results, args=args)
                    # Serialize the queryset
                    serialized_output = results_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather/stats",
                            "output_count": results.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": results.pages,
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given year and station could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "year": year,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        elif year is None and station is not None:
            if len(station) == 11:
                q_station_id = station.upper()
                try:
                    results = Results.query.filter(
                        Results.station_id == q_station_id).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=results, args=args)
                    # Serialize the queryset
                    serialized_output = results_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather/stats",
                            "output_count": results.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": results.pages,
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given station could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "year": year,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        elif year is not None and station is None:
            if len(year) == 4:
                q_year = year
                try:
                    results = Results.query.filter(
                        Results.year == q_year).paginate(per_page=1000)
                    paginate_response_op = paginate_response(
                        paginate_object=results, args=args)
                    # Serialize the queryset
                    serialized_output = results_schema.dump(
                        paginate_response_op[0])
                    if len(serialized_output) != 0:
                        response = {
                            "endpoint": "/weather/stats",
                            "output_count": results.total,
                            "current_page": paginate_response_op[1],
                            "total_pages": results.pages,
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "response": serialized_output
                        }
                        return response, 200
                    else:
                        response = {
                            "endpoint": "/weather",
                            "args": {
                                "year": year,
                                "station": station,
                                "page": page
                            },
                            "message": "Records for given year could not be found"
                        }
                        return response, 404
                except NoResultFound:
                    return {"message": "Error: NoResultFound"}, 404
            else:
                response = {
                    "endpoint": "/weather",
                    "args": {
                        "year": year,
                        "station": station,
                        "page": page
                    },
                    "message": "The server cannot process the request due to malformed request syntax"
                }
                return response, 400
        else:
            results = Results.query.paginate(per_page=1000)
            paginate_response_op = paginate_response(
                paginate_object=results, args=args)
            # Serialize the queryset
            serialized_output = results_schema.dump(
                paginate_response_op[0])
            if len(serialized_output) != 0:
                response = {
                    "endpoint": "/weather",
                    "output_count": results.total,
                    "current_page": paginate_response_op[1],
                    "total_pages": results.pages,
                    "args": {
                        "year": year,
                        "station": station,
                        "page": page
                    },
                    "response": serialized_output
                }
                return response, 200
            else:
                response = {
                    "endpoint": "/weather",
                    "output_count": results.total,
                    "current_page": paginate_response_op[1],
                    "total_pages": results.pages,
                    "args": {
                        "year": year,
                        "station": station,
                        "page": page
                    },
                    "message": "There is no content to send for this request"
                }
                return response, 204
