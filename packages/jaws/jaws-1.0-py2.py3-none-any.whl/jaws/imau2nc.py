import os
import sys

import numpy as np
import pandas as pd
import xarray as xr

try:
    from jaws import common, sunposition, clearsky, tilt_angle, fsds_adjust
except ImportError:
    import common, sunposition, clearsky, tilt_angle, fsds_adjust


def init_dataframe(args, input_file, sub_type):
    """Initialize dataframe with data from input file; convert temperature and pressure to SI units"""
    check_na = -9999

    df, columns = common.load_dataframe(sub_type, input_file, 0)
    df.replace(check_na, np.nan, inplace=True)

    if sub_type == 'imau/ant':
        temperature_vars = ['temp_cnr1', 'ta',
                            'tsn1a', 'tsn2a', 'tsn3a', 'tsn4a', 'tsn5a',
                            'tsn1b', 'tsn2b', 'tsn3b', 'tsn4b', 'tsn5b',
                            'temp_logger']
        pressure_vars = ['pa']

    elif sub_type == 'imau/grl':
        temperature_vars = ['temp_cnr1', 'ta2', 'ta6',
                            'tsn1', 'tsn2', 'tsn3', 'tsn4', 'tsn5',
                            'datalogger']
        pressure_vars = ['pa']

    if not args.celsius:
        df.loc[:, temperature_vars] += common.freezing_point_temp  # Convert units to Kelvin

    if not args.mb:
        df.loc[:, pressure_vars] *= common.pascal_per_millibar  # Convert units to millibar/hPa

    df = df.where((pd.notnull(df)), common.get_fillvalue(args))

    return df, temperature_vars, pressure_vars


def get_station(args, input_file, stations):
    """Get latitude, longitude and name for each station"""
    filename = os.path.basename(input_file)
    name = filename[:9]
    try:
        lat, lon, new_name = common.parse_station(args, stations[name])
    except KeyError as err:
        print('KeyError: {}'.format(err))
        print('HINT: This KeyError can occur when JAWS is asked to process station that is not in its database. '
              'Please inform the JAWS maintainers by opening an issue at https://github.com/jaws/jaws/issues.')
        sys.exit(1)

    return lat, lon, new_name


def get_time_and_sza(args, dataframe, longitude, latitude, sub_type):
    """Calculate additional time related variables"""
    seconds_in_30min = 30*60
    seconds_in_15min = 15*60
    dtime_1970, tz = common.time_common(args.tz)
    num_rows = dataframe['year'].size

    month, day, minutes, time, time_bounds, sza, az = ([0] * num_rows for _ in range(7))

    hour = (dataframe['hour_mult_100']/100).astype(int)
    temp_dtime = pd.to_datetime(dataframe['year']*1000 + dataframe['day_of_year'].astype(int), format='%Y%j')

    dataframe['hour'] = hour
    dataframe['dtime'] = temp_dtime

    dataframe['dtime'] = pd.to_datetime(dataframe.dtime)
    dataframe['dtime'] = [tz.localize(i.replace(tzinfo=None)) for i in dataframe['dtime']]
    dataframe['dtime'] += pd.to_timedelta(dataframe.hour, unit='h')

    if sub_type == 'imau/ant':
        # Each timestamp is average of previous and current hour values i.e. value at hour=5 is average of hour=4 and 5
        # Our 'time' variable will represent values at half-hour i.e. 4.5 in above case, so subtract 30 minutes from all
        time = (dataframe['dtime'] - dtime_1970) / np.timedelta64(1, 's') - seconds_in_30min
        time_bounds = [(i-seconds_in_30min, i+seconds_in_30min) for i in time]
    elif sub_type == 'imau/grl':
        minutes = (((dataframe['hour_mult_100']/100) % 1) * 100).astype(int)
        dataframe['minutes'] = minutes
        dataframe['dtime'] += pd.to_timedelta(dataframe.minutes, unit='m')

        # Each timestamp is average of previous and current half-hour values i.e. value at hr=5 is average of 4.5 and 5
        # Our 'time' variable will represent values at half of 30 min i.e. 4.75, so subtract 15 minutes from all
        time = (dataframe['dtime'] - dtime_1970) / np.timedelta64(1, 's') - seconds_in_15min
        time_bounds = [(i-seconds_in_15min, i+seconds_in_15min) for i in time]

    month = pd.DatetimeIndex(dataframe['dtime']).month.values
    day = pd.DatetimeIndex(dataframe['dtime']).day.values
    dates = list(pd.DatetimeIndex(dataframe['dtime']).date)
    dates = [int(d.strftime("%Y%m%d")) for d in dates]
    first_date = min(dates)
    last_date = max(dates)

    for idx in range(num_rows):
        solar_angles = sunposition.sunpos(dataframe['dtime'][idx], latitude, longitude, 0)
        az[idx] = solar_angles[0]
        sza[idx] = solar_angles[1]

    return month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date


def imau2nc(args, input_file, output_file, stations):
    """Main function to convert IMAU ascii file to netCDF"""
    with open(input_file) as stream:
        line = stream.readline()
        var_count = len(line.split(','))

    errmsg = 'Unknown sub-type of IMAU network. Antarctic stations have 31 columns while Greenland stations have 35. ' \
             'Your dataset has {} columns.'.format(var_count)
    if var_count == 31:
        sub_type = 'imau/ant'
    elif var_count == 35:
        sub_type = 'imau/grl'
    else:
        raise RuntimeError(errmsg)

    df, temperature_vars, pressure_vars = init_dataframe(args, input_file, sub_type)
    ds = xr.Dataset.from_dataframe(df)
    ds = ds.drop('time')

    common.log(args, 2, 'Retrieving latitude, longitude and station name')
    latitude, longitude, station_name = get_station(args, input_file, stations)

    common.log(args, 3, 'Calculating time and sza')
    month, day, hour, minutes, time, time_bounds, sza, az, first_date, last_date = get_time_and_sza(
        args, df, longitude, latitude, sub_type)

    ds['month'] = 'time', month
    ds['day'] = 'time', day
    ds['hour'] = 'time', hour
    ds['minutes'] = 'time', minutes
    ds['time'] = 'time', time
    ds['time_bounds'] = ('time', 'nbnd'), time_bounds
    ds['sza'] = 'time', sza
    ds['az'] = 'time', az
    ds['station_name'] = tuple(), station_name
    ds['latitude'] = tuple(), latitude
    ds['longitude'] = tuple(), longitude

    rigb_vars = []
    if args.rigb:
        ds, rigb_vars = common.call_rigb(
            args, station_name, first_date, last_date, ds, latitude, longitude, rigb_vars)

    comp_level = args.dfl_lvl

    common.load_dataset_attributes(sub_type, ds, args, rigb_vars=rigb_vars, temperature_vars=temperature_vars,
                                   pressure_vars=pressure_vars)
    encoding = common.get_encoding(sub_type, common.get_fillvalue(args), comp_level, args)

    common.write_data(args, ds, output_file, encoding)
