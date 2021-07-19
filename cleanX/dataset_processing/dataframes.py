# -*- coding: utf-8 -*-
"""
clean X : Library for cleaning radiological data used in machine learning
applications
module dataframes: processing of datasetss related to images
This module can be implemented by functions,
or can be implemented with classes
"""

import os

from abc import ABC
from collections.abc import Iterable
from pathlib import Path

import pandas as pd


class GuesserError(TypeError):
    pass


class ColumnsSource(ABC):

    def to_dataframe(self):
        raise NotImplementedError()


class CSVSource(ColumnsSource):

    def __init__(self, csv, **pd_args):
        self.csv = csv
        self.pd_args = pd_args or {}

    def to_dataframe(self):
        return pd.read_csv(self.csv, **self.pd_args)


class JSONSource(ColumnsSource):

    def __init__(self, json, **pd_args):
        self.json = json
        self.pd_args = pd_args or {}

    def to_dataframe(self):
        return pd.read_json(self.json, **self.pd_args)


class DFSource(ColumnsSource):

    def __init__(self, df):
        self.df = df

    def to_dataframe(self):
        return self.df


class MultiSource(ColumnsSource):

    def __init__(self, *sources):
        self.sources = sources

    def to_dataframe(self):
        return pd.concat(s.to_dataframe() for s in self.sources)


def string_source(raw_src):
    ext = os.path.splitext(raw_src)[1]
    if isinstance(ext, bytes):
        ext = ext.decode()
    ext = ext.lower()
    if ext == '.csv':
        return CSVSource(raw_src)
    elif ext == '.json':
        return JSONSource(raw_src)

    raise GuesserError('Cannot guess source of {}'.format(raw_src))


class MLSetup:
    """
    This class allows configuration of the train and test datasets
    organized into a pandas dataframe
    to be checked for problems, and creates reports, which can be
    put in multiple output options.
    """

    known_sources = {
        str: string_source,
        bytes: string_source,
        Path: string_source,
        pd.DataFrame: lambda _: DFSource,
    }

    def __init__(self, train_src, test_src):
        # TODO: Implement
        self.train_src = self.guess_source(train_src)
        self.test_src = self.guess_source(test_src)

    # def train_maker():

    def guess_source(self, raw_src):
        guesser = self.known_sources.get(type(raw_src))
        if guesser:
            return guesser(raw_src)
        if isinstance(raw_src, Iterable):
            return MultiSource(self.guess_source(src) for src in raw_src)
        elif isinstance(raw_src, ColumnsSource):
            return raw_src

    def metadata(self):
        return (
            self.train_src.to_dataframe().columns,
            self.test_src.to_dataframe().columns,
        )

    def concat_dataframe(self):
        return pd.concat((
            self.train_src.to_dataframe(),
            self.test_src.to_dataframe(),
        ))

    def duplicated(self):
        return self.concat_dataframe().duplicated()

    def duplicates(self):
        return (
            self.train_src.to_dataframe().duplicated().sum(),
            self.test_src.to_dataframe().duplicated().sum(),
        )

    def pics_in_both_groups(self, unique_id):
        train_df = self.train_src.to_dataframe()
        test_df = self.test_src.to_dataframe()
        return train_df.merge(test_df, on=unique_id, how='inner')

    # def bad_bias(self):

    # def knowledge(self):
    #     train_df = self.train_src.to_dataframe()
    #     test_df = self.test_src.to_dataframe()
    #     both_df = [test_df, train_df]
    #     for df in both_df:
    #         names = df.columns
            
    def generate_report(
        self,
        duplicates=True,
        leakage=True,
        bias=True,
        understand=True,
    ):
        return Report(
        self,
        duplicates,
        leakage,
        bias,
        understand,
    )

class Report:
    def __init__(
        self, 
        mlsetup, 
        duplicates=True,
        leakage=True,
        bias=True,
        understand=True,
    ):
        self.mlsetup = mlsetup
        self.sections = {}
        if duplicates:
            self.report_duplicates()
        if leakage:
            self.report_leakage()
        if bias:
            self.report_bias()
        if understand:
            self.report_understand()

    def report_duplicates(self):
        train_dupes, test_dupes = self.mlsetup.duplicates() 
        self.sections['Duplicates'] = {
            'Train Duplicates Count': train_dupes,
            'Test Duplicates Count': test_dupes,
        }

    def report_leakage(self, unique_id):
        train_df = self.train_src.to_dataframe()
        test_df = self.test_src.to_dataframe()
        leaked =  train_df.merge(test_df, on=unique_id, how='inner')
        self.sections['Leakage'] = {
           'Leaked entries': leaked,
        }
    
    def report_bias(self, sensitive_list):
        ###
        #
        help = 'help'
        self.sections['Value Count'] = {
           'Value counts of categorty 1': help,
        } 
        
    def report_understand(self):
        train_df = self.train_src.to_dataframe()
        test_df = self.test_src.to_dataframe()
        train_columns = train_df.columns
        test_columns = test_df.columns
        columns = train_columns + test_columns
        train_rows = len(train_df)
        test_rows = len(test_df)
        rows = train_rows + test_rows
        train_nulls = train_df[test_df.isnull()].count()
        test_nulls = test_df[test_df.isnull()].count()
        nulls = train_nulls + test_nulls
        train_dtypes = train_df.dtypes
        test_dtypes = test_df.dtypes
        datatypes = train_dtypes + test_dtypes
        train_description = train_df.describe()
        test_description = test_df.describe()
        description = train_description + test_description
        self.sections['Knowledge'] = {
           'Columns': columns,
           'Train columns': train_columns,
           'Test columns': test_columns, 
           'Rows': rows,
           'Train rows': train_rows,
           'Test rows': test_rows,   
           'Nulls': nulls,
           'Train nulls': train_nulls,
           'Test nulls': test_nulls, 
           'Datatypes': datatypes,
           'Train datatypes': train_dtypes,
           'Test datatypes': test_dtypes, 
           'Descriptions': description,
           'Train description': train_description,
           'Test description': test_description, 
        }     

    # method that generates data
    # method that prints to terminal
    # method that prints to json
    # method that generates an email message
    # method that controls verbosity

# to run on dataframes
def check_paths_for_group_leakage(train_df, test_df, unique_id):
    """
    Finds train samples that have been accidentally leaked into test
    samples

    :param train_df: Pandas :code:`DataFrame` containing information about
                     train assets.
    :type train_df: :pd:`DataFrame`
    :param test_df: Pandas :code:`DataFrame` containing information about
                    train assets.
    :type test_df: :pd:`DataFrame`

    :return: duplications of any image into both sets as a new
             :code:`DataFrame`
    :rtype: :pd:`DataFrame`
    """
    pics_in_both_groups = train_df.merge(test_df, on=unique_id, how='inner')
    return pics_in_both_groups


def see_part_potential_bias(df, label, sensitive_column_list):
    """
    This function gives you a tabulated :code:`DataFrame` of sensitive columns
    e.g. gender, race, or whichever you think are relevant,
    in terms of a labels (put in the label column name).
    You may discover all your pathologically labeled sample are of one ethnic
    group, gender or other category in your :code:`DataFrame`. Remember some
    early neural nets for chest X-rays were less accurate in women and the
    fact that there were fewer X-rays of women in the datasets they built on
    did not help

    :param df: :code:`DataFrame` including sample IDs, labels, and sensitive
               columns
    :type df: :pd:`DataFrame`
    :param label: The name of the column with the labels
    :type label: string
    :param sensitive_column_list: List names sensitive columns on
                                  :code:`DataFrame`
    :type sensitive_column_list: list

    :return: tab_fight_bias2, a neatly sorted :code:`DataFrame`
    :rtype: :pd:`DataFrame`
    """

    label_and_sensitive = [label]+sensitive_column_list
    tab_fight_bias = pd.DataFrame(
        df[label_and_sensitive].value_counts()
    )
    tab_fight_bias2 = tab_fight_bias.groupby(label_and_sensitive).sum()
    tab_fight_bias2 = tab_fight_bias2.rename(columns={0: 'sums'})
    return tab_fight_bias2


def understand_df(df):
    """
    Takes a :code:`DataFrame` (if you have a :code:`DataFrame` for images)
    and prints information including length, data types, nulls and number
    of duplicated rows

    :param df: :code:`DataFrame` you are interested in getting features of.
    :type df: :pd:`DataFrame`

    :return: Prints out information on :code:`DataFrame`.
    :rtype: NoneType
    """
    print("The DataFrame has", len(df.columns), "columns, named", df.columns)
    print("")
    print("The DataFrame has", len(df), "rows")
    print("")
    print("The types of data:\n", df.dtypes)
    print("")
    print("In terms of nulls, the DataFrame has: \n", df[df.isnull()].count())
    print("")
    print(
        "Number of duplicated rows in the data is ",
        df.duplicated().sum(),
        ".",
    )
    print("")
    print("Numeric qualities of numeric data: \n", df.describe())


def show_duplicates(df):
    """
    Takes a :code:`DataFrame` (if you have a :code:`DataFrame` for images)
    and prints duplicated rows
    """
    if df.duplicated().any():
        print(
            "This DataFrame table has",
            df.duplicated().sum(),
            " duplicated rows"
        )
        print("They are: \n", df[df.duplicated()])
    else:
        print("There are no duplicated rows")
