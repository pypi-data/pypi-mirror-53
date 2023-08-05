#!/usr/bin/env python3

from QUBEKit.utils.helpers import pretty_print, unpickle, COLOURS

from datetime import datetime
from functools import wraps, partial
import logging
import os
from time import time


def timer_func(orig_func):
    """
    Prints the runtime of a function when applied as a decorator (@timer_func).
    Currently only used for debugging.
    """

    @wraps(orig_func)
    def wrapper(*args, **kwargs):

        t1 = time()
        result = orig_func(*args, **kwargs)
        t2 = time() - t1

        print(f'{orig_func.__qualname__} ran in: {t2} seconds.')

        return result
    return wrapper


def timer_logger(orig_func):
    """
    Logs the various timings of a function in a dated and numbered file.
    Writes the start time, function / method qualname and docstring when function / method starts.
    Then outputs the runtime and time when function / method finishes.
    """

    # TODO Currently only logs when the decorated class is passed molecule.
    #  Need a better way of getting log file beyond just getting it from the molecule object.

    @wraps(orig_func)
    def wrapper(*args, **kwargs):

        # All this does is check if the decorated function has a molecule attribute;
        # if it does, the function must therefore have a home path which can be used to write to the log file.
        if len(args) >= 1 and hasattr(args[0], 'molecule'):
            if getattr(args[0].molecule, 'home') is None:
                return orig_func(*args, **kwargs)
            log_file_path = os.path.join(args[0].molecule.home, 'QUBEKit_log.txt')
        else:
            if not os.path.exists('../QUBEKit_log.txt'):
                return orig_func(*args, **kwargs)
            log_file_path = '../QUBEKit_log.txt'

        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t1 = time()

        with open(log_file_path, 'a+') as log_file:
            log_file.write(f'{orig_func.__qualname__} began at {start_time}.\n\n    ')
            log_file.write(f'Docstring for {orig_func.__qualname__}:\n    {orig_func.__doc__}\n\n')

            time_taken = time() - t1

            mins, secs = divmod(time_taken, 60)
            hours, mins = divmod(mins, 60)

            secs, remain = str(float(secs)).split('.')

            time_taken = f'{int(hours):02d}h:{int(mins):02d}m:{int(secs):02d}s.{remain[:5]}'
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            log_file.write(f'{orig_func.__qualname__} finished in {time_taken} at {end_time}.\n\n')
            # Add some separation space between function / method logs.
            log_file.write(f'{"-" * 50}\n\n')

        return orig_func(*args, **kwargs)
    return wrapper


def for_all_methods(decorator):
    """
    Applies a decorator to all methods of a class (includes sub-classes and init; it is literally all callables).
    This class decorator is applied using '@for_all_methods(timer_func)' for example.
    """

    @wraps(decorator)
    def decorate(cls):
        # Examine all class attributes.
        for attr in cls.__dict__:
            # Check if each class attribute is a callable method.
            if callable(getattr(cls, attr)):
                # Set the callables to be decorated.
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def logger_format(log_file):
    """
    Creates logging object to be returned.
    Contains proper formatting and locations for logging exceptions.
    This isn't a decorator itself but is only used by exception_logger so it makes sense for it to be here.
    """

    logger = logging.getLogger('Exception Logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)

    # Format the log message
    fmt = '\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def exception_logger(func):
    """
    Decorator which logs exceptions to QUBEKit_log.txt file if one occurs.
    Do not apply this decorator to a function / method unless a log file will exist in the working dir;
    doing so will just raise the exception as normal.

    On any Exception, the Ligand class objects which are taken from the pickle file are printed to the log file,
    then the full stack trace is printed to the log file as well.

    Currently, only Execute.run is decorated like this, as it will always have a log file.
    Decorating other functions this way is possible and won't break anything, but it is pointless.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # Any BaseException is logged; KeyboardInterrupt and SystemExit must still be raised (see below)
        except BaseException as exc:

            home = getattr(args[0].molecule, 'home', None)
            state = getattr(args[0].molecule, 'state', None)

            if home is None or state is None:
                raise

            mol = unpickle()[state]
            if getattr(args[0].molecule, 'verbose'):
                pretty_print(mol, to_file=True, finished=False)

            log_file = os.path.join(home, 'QUBEKit_log.txt')
            logger = logger_format(log_file)

            logger.exception(f'\nAn exception occurred with: {func.__qualname__}\n')
            print(f'{COLOURS.red}\n\nAn exception occurred with: {func.__qualname__}{COLOURS.end}\n'
                  f'Exception: {exc}\nView the log file for details.')

            if isinstance(exc, SystemExit) or isinstance(exc, KeyboardInterrupt):
                raise

            # Re-raises the exception if it's not a bulk run.
            # Even if the exception is not raised, it is still logged.
            if len(args) >= 1 and hasattr(args[0], 'molecule'):
                if not hasattr(args[0].molecule, 'bulk_run'):
                    raise
                if args[0].molecule.bulk_run is None:
                    raise

    return wrapper


class ExceptionLogger:
    """Alternate implementation of exception logger functions above"""

    def __init__(self, func):

        self.func = func
        self.log_file = None

    def __get__(self, instance, owner):
        """Allows decoration of functions and methods"""
        return partial(self.__call__, instance)

    def __call__(self, *args, **kwargs):

        try:
            return self.func(*args, **kwargs)
        # Any BaseException is logged; KeyboardInterrupt and SystemExit must still be raised (see below)
        except Exception as exc:

            home = getattr(args[0].molecule, 'home', None)
            state = getattr(args[0].molecule, 'state', None)

            if home is None or state is None:
                raise

            mol = unpickle()[state]
            pretty_print(mol, to_file=True, finished=False)

            self.log_file = os.path.join(home, 'QUBEKit_log.txt')
            logger = self.logger_format()

            logger.exception(f'\nAn exception occurred with: {self.func.__qualname__}\n')
            print(f'\n\nAn exception occurred with: {self.func.__qualname__}\n'
                  f'Exception: {exc}\nView the log file for details.'.upper())

            # Re-raises the exception if it's not a bulk run.
            # Even if the exception is not raised, it is still logged.
            if len(args) >= 1 and hasattr(args[0], 'molecule'):
                if not hasattr(args[0].molecule, 'bulk_run'):
                    raise
                if args[0].molecule.bulk_run is None:
                    raise

    def logger_format(self):

        logger = logging.getLogger('Exception Logger')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file)

        # Format the log message
        fmt = '\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger
