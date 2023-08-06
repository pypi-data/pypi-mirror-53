"""
 Project: coraline_eda
 Desctiption: Exploratory Data Analysis(EDA) Utilities
 Created by Jiranun J. at 2019/09/30 11:05 AM 
"""
import pandas as pd
import numpy as np
from os.path import join, splitext, exists
from os import mkdir
import pandas_profiling


def get_detected_column_types(df):
    """
    Get data type of each columns ('DATETIME', 'NUMERIC' or 'STRING')
    :param df: pandas dataframe
    :return: columns dict
    """
    col_dict = {}
    for c in df.columns:
        # Convert column to string
        col_data = df[c].map(str)
        col_data = col_data.replace("NaT", None)
        col_data = col_data.replace("NaN", None)

        # Check DATETIME
        try:
            # Check if it's able to convert column to datetime
            pd.to_datetime(col_data)
            col_dict[c] = 'DATETIME'
            continue
        except ValueError:
            pass

        # Check NUMERIC
        try:
            # Drop NaN rows
            series = df[c].dropna()

            # Check if it can be converted to numeric
            pd.to_numeric(series)

            if df[c].dtype == object:
                col_dict[c] = 'STRING'
            else:
                col_dict[c] = 'NUMERIC'
        except ValueError:
            # Otherwise, it's VARCHAR column
            col_dict[c] = "STRING"

    return col_dict


# def get_data_info(df):
#     """
#     Get data information from pandas dataframe
#     :param df: pandas dataframe
#     :return:
#     """
#     # Get numeric info from numeric columns
#     numeric_info = df.describe()
#     for c in df.colums:
#         row = {
#             'name': c
#         }
#         print(c)
#         print(sum(pd.isnull(df[c])))
#         print()
#     return numeric_info


def read_and_gen_report(file_path, file_name):
    """Read CSV/Excel file and generate report

    Parameters
    ----------
    file_path : str
        file path
    file_name : str
        file name

    Returns
    -------
    bool
        success or not
    """
    full_file_name = join(file_path, file_name)
    print(f"\nGenerating report for {full_file_name}")

    # Split name and extension
    _, file_extension = splitext(file_name)
    if file_extension == ".csv":
        print("  - Reading file")
        # Find out what the delimiter is
        f = open(full_file_name)
        first_line = f.readline()
        delimiter = ","
        for d in ['|', '\t', ';']:
            if d in first_line:
                delimiter = d
                break

        # read file
        df = pd.read_csv(full_file_name, delimiter=delimiter)
        print("  - Analyzing file")
    elif file_extension == ".xlsx":
        pass

    # Create Result folder if not exist
    result_folder = join(file_path, "EDA_reports")
    if not exists(result_folder):
        mkdir(result_folder)

    # Generate Profiling report
    profile = df.profile_report(title=f'{file_name} Profiling Report')
    output_file = f'{file_name.replace(".", "_")}_profiling_report.html'
    output_file = join(result_folder, output_file)
    print(f"  - Saving file at {output_file}")
    profile.to_file(output_file=output_file)

    return df


# def generate_reports_from_list(file_path, file_list):
#     """Generate EDA Report for every files

#     Parameters
#     ----------
#     file_path : str
#         full path of files
#     file_list : list
#         list of file names

#     Returns
#     -------
#     [type]
#         [description]
#     """
#     for file_name in file_list:
#         read_and_gen_report(file_path, file_name) 
#     return True


if __name__ == '__main__':
    read_and_gen_report("/Users/jiranun/Downloads/", "trafficindex.csv")

