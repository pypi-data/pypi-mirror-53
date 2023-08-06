# -*- coding: utf-8 -*-
import time
import base64
import re
from functools import wraps
import logging
from datetime import datetime, timedelta
import dateutil.parser

def dehexify(data):
    """
    A URL and Hexadecimal Decoding Library.

    Credit: Larry Dewey
    """

    hexen = {
        '\x1c': ',',  # Replacing Device Control 1 with a comma.
        '\x11': '\n',  # Replacing Device Control 2 with a new line.
        '\x12': ' ',  # Space
        '\x22': '"',  # Double Quotes
        '\x23': '#',  # Number Symbol
        '\x27': '\'',  # Single Quote
        '\x28': '(',  # Open Parenthesis
        '\x29': ')',  # Close Parenthesis
        '\x2b': '+',  # Plus Symbol
        '\x2d': '-',  # Hyphen Symbol
        '\x2e': '.',  # Period, dot, or full stop.
        '\x2f': '/',  # Forward Slash or divide symbol.
        '\x7c': '|',  # Vertical bar or pipe.
    }

    uri = {
        '%11': ',',  # Replacing Device Control 1 with a comma.
        '%12': '\n',  # Replacing Device Control 2 with a new line.
        '%20': ' ',  # Space
        '%22': '"',  # Double Quotes
        '%23': '#',  # Number Symbol
        '%27': '\'',  # Single Quote
        '%28': '(',  # Open Parenthesis
        '%29': ')',  # Close Parenthesis
        '%2B': '+',  # Plus Symbol
        '%2D': '-',  # Hyphen Symbol
        '%2E': '.',  # Period, dot, or full stop.
        '%2F': '/',  # Forward Slash or divide symbol.
        '%3A': ':',  # Colon
        '%7C': '|',  # Vertical bar or pipe.
    }

    for (enc, dec) in hexen.items():
        data = data.replace(enc, dec)

    for (enc, dec) in uri.items():
        data = data.replace(enc, dec)

    return data


def timethis(func):
    """
    Decorator that reports the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

def tob64(s):
    if type(s) is str:
        return base64.b64encode(s.encode('utf-8')).decode()

def fromb64(s):
    if type(s) is str:
        return base64.b64decode(s.encode('utf-8')).encode()

def timerange_gettimes(time_range):
    t=time_range
    now=datetime.now()
    times=tuple()

    if t is 'LAST_MINUTE' :
        times=(now-timedelta(seconds=60), now)
        
    elif t is 'LAST_10_MINUTES':
        times=(now-timedelta(minutes=10), now)

    elif t is 'LAST_30_MINUTES':
        times=(now-timedelta(minutes=30), now)

    elif t is 'LAST_HOUR':
        times=(now-timedelta(minutes=60), now)

    elif t is 'CURRENT_DAY':
        times=(now.replace(hour=0, minute=0, second=0), now.replace(hour=23, minute=59, second=59))

    elif t is 'PREVIOUS_DAY':
        yesterday=now-timedelta(hours=24)
        times=(yesterday.replace(hour=0, minute=0, second=0), yesterday.replace(hour=23, minute=59, second=59))

    elif t is 'LAST_24_HOURS':
        times=(now-timedelta(hours=24), now)

    elif t is 'LAST_2_DAYS':
        times=(now-timedelta(days=2), now)

    elif t is 'LAST_3_DAYS':
        times=(now-timedelta(days=3), now)

    else :
        raise NotImplementedError("Timerange "+t+" is not supported yet")
    
    return(times[0].isoformat(), times[1].isoformat())
    
    """ #TODO Support other time ranges
    elif t is 'CURRENT_WEEK':
        pass
    elif t is 'PREVIOUS_WEEK':
        pass
    elif t is 'CURRENT_MONTH':
        pass
    elif t is 'PREVIOUS_MONTH':
        pass
    elif t is 'CURRENT_QUARTER':
        pass
    elif t is 'PREVIOUS_QUARTER':
        pass
    elif t is 'CURRENT_YEAR':
        pass
    elif t is 'PREVIOUS_YEAR':
        pass"""

def divide_times(first, last, time=0, slots=0, delta=0, min_slots=0):
    """"
        Divide the time range based on another time, a delta or on a number of slots
        Return list of tuple 
    """

    #parse the dates
    t1=convert_to_time_obj(first) if not isinstance(first, datetime) else first
    t2=convert_to_time_obj(last) if not isinstance(last, datetime) else last
    
    duration=t2-t1

    if slots==0 :
        if delta==0 :
            if time==0 :
                raise AttributeError('Either time, slots or delta must be specified')
            else :
                div=convert_to_time_obj(time)-t1

        elif(isinstance(delta, timedelta)):
            div = delta
        elif isinstance(delta, str):
            div = parse_timedelta(delta)
        else:
            raise AttributeError('delta Must be timedelta or str object')

        
        slots=int(duration.total_seconds()/div.total_seconds())

    slots+=min_slots
    timeSlot=timedelta(seconds=duration.total_seconds()/slots)

    #print(locals())

    times=list()

    for i in range(slots):
        times.append( (t1, t1+timeSlot) )
        t1+=timeSlot

    return(times)

def regex_match(regex, string):
    if re.search(regex, string):
        return True
    else:
        return False

def format_esm_time(esm_time):
    """Converts time object to ESM time string.
    
    Arguments:
        time_obj {[type]} -- [description]
    Returns:
        time string in format: 2019-04-08T19:35:02.971Z
    """
    _esm_out_time_fmt = '%m/%d/%Y %H:%M:%S'
    _esm_in_time_fmt = '%Y-%m-%dT%H:%M:%S.000Z'
    if isinstance(esm_time, str):
        esm_time = convert_to_time_obj(esm_time)#, _esm_out_time_fmt)
    return datetime.strftime(esm_time, _esm_in_time_fmt)

def convert_to_time_obj(time_str):
    """
    Converts given timestamp string to datetime object
    
    Args:
        time_str: timestamp in format 'YYYY/MM/DD HH:MM:SS',
                         'MM/DD/YYYY HH:MM:SS', or 'DD/MM/YYYY HH:MM:SS'
                         
    Returns:
        datetime object or None if no format matches
    """
    return dateutil.parser.parse(time_str)

def parse_query_result(columns, rows):
    """
    For input :
        columns = ['key1','name','password']
        rows = [
            ['67','bob','b08b'],
            ['68','mike','kaas'],
            ['69','jean','p992'],
        ]
    Returns :
    [
        {key1=67, name=bob, password=b08b},
        {...},
        {},
    ]

    """
    events=list()
    for row in rows :
        event=dict()
        for i in range(len(columns)):
            event.update({columns[i]['name']:row['values'][i]})

        events.append(event)

    return(events)


def format_fields_for_query(fields):
    """
    ['field1','name','user']

    Returns :
    [
        {'name':'field1'},
        {...},
        {},
    ]
    """
    return([{'name':value} for value in list(fields)])




def parse_timedelta(time_str):
    """
    Parse a time string e.g. (2h13m) into a timedelta object.

    Modified from virhilo's answer at https://stackoverflow.com/a/4628148/851699

    :param time_str: A string identifying a duration.  (eg. 2h13m)
    :return datetime.timedelta: A datetime.timedelta object
    """
    regex = re.compile(r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
    parts = regex.match(time_str)
    assert parts is not None, "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(time_str)
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)
