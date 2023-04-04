# A retry decorator

from email.mime.text import MIMEText
import traceback
import smtplib
import functools
import logging
import time
import requests
from functools import wraps


def retry(max_tries=3, delay_seconds=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    print(f"Retrying ... attepmts: {tries}")
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)
        return wrapper_retry
    return decorator_retry


@retry(max_tries=5, delay_seconds=2)
def call_dummy_api():
    response = requests.get("https://jsonplaceholders.typicode.com/todos/1")
    return response

# res = call_dummy_api()
# print(res.text)


# Memoize decorator
def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return wrapper


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


# Time started and elapsed decorator


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper


# Logging function calls

logging.basicConfig(level=logging.INFO)


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished executing {func.__name__}")
        return result
    return wrapper


@log_execution
def extract_data(source):
    # extract data from source
    data = ...

    return data


@log_execution
def transform_data(data):
    # transform data
    transformed_data = ...

    return transformed_data


@log_execution
def load_data(data, target):
    # load data into target
    ...


def main():
    # extract data
    source = ...
    data = extract_data(source)

    # transform data
    transformed_data = transform_data(data)

    # load data
    target = ...
    load_data(transformed_data, target)

# INFO:root:Executing extract_data
# INFO:root:Finished executing extract_data
# INFO:root:Executing transform_data
# INFO:root:Finished executing transform_data
# INFO:root:Executing load_data
# INFO:root:Finished executing load_data

# mixing


@log_execution
@timing_decorator
def my_function(x, y):
    time.sleep(1)
    return x + y


# Notify when fails


def email_on_failure(sender_email, password, recipient_email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # format the error message and traceback
                err_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"

                # create the email message
                message = MIMEText(err_msg)
                message['Subject'] = f"{func.__name__} failed"
                message['From'] = sender_email
                message['To'] = recipient_email

                # send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, password)
                    smtp.sendmail(sender_email, recipient_email,
                                  message.as_string())

                # re-raise the exception
                raise

        return wrapper

    return decorator


@email_on_failure(sender_email='your_email@gmail.com', password='your_password', recipient_email='recipient_email@gmail.com')
def my_function():
    # code that might fail
    ...
