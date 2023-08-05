from .make_predicate import make_predicate
from .bot import Bot
from random import random
import json


def make_bot(script, variables, handlers, logger_format=None,):
    """

    bot:
        username: sds
        password: ...

    max_per_day:
        likes:                  50
        follow:                 20
        unfollow:               10
        ...

    delay:
        like:                   10
        usual:                  2
        ...

    """

    # if not 'bot' in script:
    #     raise Exception('no bot in script')

    data = script['bot'] if 'bot' in script else {}

    def get(var):
        if var in variables:
            return variables[var]
        elif var in data:
            return data[var]
        else:
            return None

    def get_from_script(var):
        if var in variables:
            return variables[var]
        elif var in script:
            return data[var]
        else:
            return None

    
    bot = Bot(
        settings_path=get('settings_path'),
        settings=get('settings') or None,
        username=get('username') or error(Exception('username necessary')),
        password=get('password') or error(Exception('password necessary')),
        latitude=get('latitude') or 0,
        longitude=get('longitude') or 0,
        max_per_day={key: value for key, value in (get_from_script('max_per_day') or {}).items()},
        # filter_predicates= [make_predicate(script['filter'], bot)] if 'filter' in script else [], # TODO should not take bot as arg
        delay={key: value for key,value in (get_from_script('delay') or {}).items()},
        disable_logging=script.get('disable_logging') or False,
        log_level=script.get('log_level') or 'INFO',
        script_name=get_from_script('name') or 'not named script',
        proxy=get_from_script('proxy') or None,
        handlers=handlers,
        logger_format=logger_format,
    )

    if not bot.latitude or not bot.longitude:
        bot.logger.warning(
            'no latitude and longitude in script, geotag searches will probably fail')

    return bot


def error(exception):
    raise exception
