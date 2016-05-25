#!/usr/bin/python

# Based on the standard directory and file names from the archives downloaded
# from https://data.gov.uk/dataset/prescribing-by-gp-practice-presentation-level
# 
# 
# For example, data files for April 2013 are:
# - "2013_04_April/T201304ADDR BNFT.CSV"    (Address Data)
# - "2013_04_April/T201304CHEM SUBS.CSV"    (Chemical Data)
# - "2013_04_April/T201304PDPI BNFT.CSV"    (Prescription Data)
# within the root_data_dir specified below
# 
# 
# Notes:
# - Year and month parameters are expected as integers. Years should be in range 2010-3000. Months are 1-indexed.
# 
# Extenions TODO:
# - Take head of each CSV before loading to ensure headers are included in address and chems data files
# - Validate file content: Ensure non-empty, correct number of columns, first/last line(s) in expected format
# - Identify files within the directory that do not match the filename format (i.e. misnamed or extra files)


import datetime as dt
import pandas as pd
import os.path


# Root path where extracted data resides
root_data_dir = './full_data/'


# Return a data frame containing address data for specified month
def load_address_data(year, month):
    address_data_filepath = get_address_data_filepath(year, month)
    
    addresses_col_names = ['Year-Month', 'PracticeCode', 'PracticeName', 'Addr1', 'Addr2', 'Addr3', 'Addr4', 'PostCode']
    addresses = pd.read_csv(address_data_filepath, names = addresses_col_names, index_col=False)
    addresses['Year-Month'] = pd.to_datetime(addresses['Year-Month'], format='%Y%m')
    return addresses

# Return a data frame containing chemicals data for specified month
def load_chems_data(year, month):
    chems_data_filepath = get_chems_data_filepath(year, month)

    chem_col_names = ['ChemCode','ChemName']
    chems = pd.read_csv(chems_data_filepath, names = chem_col_names, skiprows=1, index_col=False)
    return chems

# Return a data frame containing prescription data for specified month
def load_prescription_data(year, month):
    prescription_data_filepath = get_prescription_data_filepath(year, month)

    pxdata_col_names = ['SHA', 'PCT', 'PracticeCode', 'BNFCode', 'BNFName',
                  'LineCountDispensed', 'NetCost','ActualCost','QuantityDispensed', 'Year-Month']
    pxdata = pd.read_csv(prescription_data_filepath, names = pxdata_col_names, skiprows = 1, index_col=False)
    pxdata['Year-Month'] = pd.to_datetime(pxdata['Year-Month'], format='%Y%m')
    return pxdata


# Functions that return a filepath for the specified data for a given month
def get_address_data_filepath(year, month):
    return get_file_path_prefix(year, month) + "ADDR BNFT.CSV"

def get_chems_data_filepath(year, month):
    return get_file_path_prefix(year, month) + "CHEM SUBS.CSV"

def get_prescription_data_filepath(year, month):
    return get_file_path_prefix(year, month) + "PDPI BNFT.CSV"


# Functions that return multiple file paths, one per month, between two given months
def get_address_data_filepaths(year_from, month_from, year_to, month_to):
    prefixes = get_data_filepath_prefixes(year_from, month_from, year_to, month_to) 
    return [p + "ADDR BNFT.CSV" for p in prefixes]

def get_chems_data_filepaths(year_from, month_from, year_to, month_to):
    prefixes = get_data_filepath_prefixes(year_from, month_from, year_to, month_to) 
    return [p + "CHEM SUBS.CSV" for p in prefixes]


def get_prescription_data_filepaths(year_from, month_from, year_to, month_to):
    prefixes = get_data_filepath_prefixes(year_from, month_from, year_to, month_to) 
    return [p + "PDPI BNFT.CSV" for p in prefixes]


# Helper functions to generate the prefixes of filenames between two months
def get_data_filepath_prefixes(year_from, month_from, year_to, month_to):
    # Start date <= End date
    assert (year_from < year_to or (year_from == year_to and month_from <= month_to)), '"To" date must be before "from" date'

    filepaths = []
    current_year = year_from
    current_month = month_from

    while not (current_year == year_to and current_month == month_to + 1):
        filepaths.append(get_file_path_prefix(current_year, current_month))

        current_month += 1
        
        if current_month > 12:
            current_month = 1
            current_year += 1

    return filepaths


def get_file_path_prefix(year, month):
    validate_year(year)
    validate_month(month)
    
    data_dir = "{0}_{1:0>2}_{2}/".format(year, month, dt.datetime.strptime(str(month), '%m').strftime('%B'))

    return "{0}{1}T{2}{3:0>2}".format(root_data_dir, data_dir, year, month)


# Validate months and years
def validate_year(year):
    assert (year >= 2010 and year <= 3000), 'Year must be between 2010 and 3000 (inclusive)'

def validate_month(month):
    assert (month > 0 and month < 13), 'Months must be an integer between 1 and 12 (inclusive)'


# Validate file existence for each data source for a given month
def check_data(year_from, month_from, year_to, month_to):
    address_filepaths = get_address_data_filepaths(year_from, month_from, year_to, month_to)
    chems_filepaths = get_chems_data_filepaths(year_from, month_from, year_to, month_to)
    pxdata_filenames = get_prescription_data_filepaths(year_from, month_from, year_to, month_to)

    
    for i in range(0, len(address_filepaths)):
        file_check(address_filepaths[i])
        file_check(chems_filepaths[i])
        file_check(pxdata_filenames[i])


def file_check(filepath):
    if not os.path.isfile(filepath):
        print('WARNING: File not found - ' + filepath)

    return



