from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as matialvarezs_time_sleep_models
from . import errors as matialvarezs_time_sleep_errors
from . import settings
import os, time, random
from matialvarezs_request_handler import utils as matialvarezs_request_handler_utils

random_string = "807HB9Z5JUOtagFolqf71Ff9sLFq54Ch"



"""
def parse_model_attributes(**kwargs):
	attributes = {}
	
	return attributes

def create_model(**kwargs):

	for key, value in parse_model_attributes(**kwargs).items():
		kwargs[key] = value
	return h_utils.db_create(matialvarezs_time_sleep_models.Model, **kwargs)

def get_model(**kwargs):
	return h_utils.db_get(matialvarezs_time_sleep_models.Model, **kwargs)

def get_or_none_model(**kwargs):
	return h_utils.db_get_or_none(matialvarezs_time_sleep_models.Model, **kwargs)

def filter_model(**kwargs):
	return h_utils.db_filter(matialvarezs_time_sleep_models.Model, **kwargs)

def q_model(q, **otions):
	return h_utils.db_q(matialvarezs_time_sleep_models.Model, q)

def delete_model(entry, **options):
	return h_utils.db_delete(entry)

def update_model(entry, **kwargs):
	attributes = {}
	for key, value in parse_model_attributes(**kwargs).items():
		attributes[key] = value
	return h_utils.db_update(entry, **attributes)
"""


def get_delay_schedule(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = list()
    if total_time_sleep == 0:
        delay_schedule.append(0)

    # print("total time sleep", total_time_sleep)
    if total_time_sleep > 0:
        if options.get('time_in_minutes', False) is True:
            total_time_sleep = total_time_sleep * 60

        while True:
            random_time = random.randint(lower_boundary, upper_boundary)
            # print("antes de append sum(delay_schedule) + random_time",sum(delay_schedule) + random_time)
            if sum(delay_schedule) + random_time > total_time_sleep:
                continue
            else:
                # print("agrego numero")
                delay_schedule.append(random_time)
            # if sum(delay_schedule) + random_time > total_time_sleep:
            #     continue
            # print("despues de append sum(delay_schedule) + random_time", sum(delay_schedule) + random_time)
            if sum(delay_schedule) == total_time_sleep:
                break

    if options.get("debug", False):
        print("total time sleep", total_time_sleep)
        print(delay_schedule)
    return delay_schedule


def time_sleep(total_time_sleep, **options):
    delay_schedule = get_delay_schedule(total_time_sleep, **options)  # list()
    # if options.get('time_in_minutes',False) is True:
    #     total_time_sleep = total_time_sleep*60
    # while sum(delay_schedule) < total_time_sleep:
    #     delay_schedule.append(random.randint(1, 10))

    print(delay_schedule)
    for delay in delay_schedule:
        time.sleep(delay)


def should_stop(**kwargs):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = kwargs.get('url',settings.URL_SHOULD_STOP_TIME_SLEEP)
    method = kwargs.get('method',"GET")
    data = kwargs.get('data',{})
    results = {}
    if method == "GET":
    #results = requests.get(headers=headers, url=url).json()
        results = matialvarezs_request_handler_utils.send_get_and_get_response(url,headers=headers).json()
    if method == "POST":
        results = matialvarezs_request_handler_utils.send_post_and_get_response(url, headers=headers,data=data,convert_data_to_json=True).json()
    # print("results:",results,results['stop'])
    return eval(results['stop'])


def time_sleep_with_stop_url(total_time_sleep, lower_boundary=1, upper_boundary=10, **options):
    delay_schedule = get_delay_schedule(total_time_sleep, lower_boundary, upper_boundary, **options)
    # delay_schedule = list()
    # if options.get('time_in_minutes', False) is True:
    #     total_time_sleep = total_time_sleep * 60
    #
    # while sum(delay_schedule) < total_time_sleep:
    #     delay_schedule.append(random.randint(lower_boundary, upper_boundary))
    # if options.get("debug", False):
    #     print("total time sleep", total_time_sleep)
    #     print(delay_schedule)
    for delay in delay_schedule:
        # print("should_stop(url)",should_stop(url))
        # print("current delay",delay)
        # stop_sleep = False
        stop_sleep = should_stop(**options)
        # print("stop_sleep",stop_sleep, type(stop_sleep))
        if stop_sleep:
            # print("DETENCION DESDE URL")
            return None
        else:
            # print("ESPERO EL TIEMPO TIME-SLEEP")
            time.sleep(delay)
    return delay_schedule
