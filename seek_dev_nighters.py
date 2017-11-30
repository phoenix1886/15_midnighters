import requests
import pytz
import datetime
from collections import Counter


def load_raw_data(page_number):
    params = {'page': str(page_number)}
    raw_data_request = requests.get(
        'http://devman.org/api/challenges/solution_attempts/', params)
    raw_data = raw_data_request.json()
    return raw_data


def load_solution_attempts(data_loader):
    solution_attempts = []
    num_of_pages = 10
    for page_number in range(1, num_of_pages+1):
        raw_data = data_loader(page_number)
        solution_attempts.extend(raw_data['records'])
    return solution_attempts


def is_midnight_attempt(attempt):
    local_timezone = pytz.timezone(attempt['timezone'])
    attempt_dt_utc = datetime.datetime.fromtimestamp(attempt['timestamp'],
                                                     pytz.utc)
    attempt_dt_loc = attempt_dt_utc.astimezone(local_timezone)
    local_time = attempt_dt_loc.time()

    lower_bound = datetime.time(0, 0, 0)
    upper_bound = datetime.time(5, 0, 0)

    return lower_bound <= local_time < upper_bound


def get_midnight_attempts_usernames(solution_attempts, filter_function):
    midnighters = [attempt['username'] for attempt in solution_attempts
                   if filter_function(attempt)]
    return midnighters


def calc_midnighters_top_list(midnight_attempts_usernames):
    midnight_attempts_counter = Counter(midnight_attempts_usernames)
    midnighters_top_list = sorted(midnight_attempts_counter.items(),
                                  key=lambda item: item[1],
                                  reverse=True)
    return midnighters_top_list


def print_to_console(midnighters_top_list):
    print('Midnighters Top List:')
    for index, (username, num_of_midnight_attempts) in enumerate(
            midnighters_top_list, 1):
        print('{}. {} made {} midnight attempts.'.format(
            index, username, num_of_midnight_attempts))


if __name__ == '__main__':
    data_loader = load_raw_data
    solution_attempts = load_solution_attempts(data_loader)
    midnight_attempts_usernames = get_midnight_attempts_usernames(
        solution_attempts, is_midnight_attempt)
    midnighters_top_list = calc_midnighters_top_list(
        midnight_attempts_usernames)
    print_to_console(midnighters_top_list)
