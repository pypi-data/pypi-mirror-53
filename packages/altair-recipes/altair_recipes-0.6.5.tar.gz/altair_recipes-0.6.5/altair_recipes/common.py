"""Mini-library for all the other modules."""
import altair as alt
from attr import attrs, attrib
from boltons.iterutils import remap
from functools import singledispatch
from numbers import Number
import numpy as np
import pandas as pd
import requests
from toolz.dicttoolz import keyfilter, valfilter

# collections


def choose_kwargs(from_, which):
    """Choose entries for a dictionary with key in `which` and not None value."""
    return keyfilter(lambda x: x in which, valfilter(lambda x: x is not None, from_))


def round_floats(a_dict, precision):
    """Find all the floats in `a_dict` (recursive) and round them to `precision`."""
    return remap(
        a_dict,
        lambda p, k, v: (k, round(v, precision)) if isinstance(v, float) else (k, v),
    )


def ndistinct(data, column):
    """Return number of distinct elements in data[column]."""
    return len(data[column].unique())


def col_cardinality(data, column, condition=None, default=1):
    """Return number of distinct elements in `data[column]` if `condition` is True (defaults to `column` being different from None), otherwise return `default`."""
    if condition is None:
        condition = column is not None
    return ndistinct(data, column) if condition else default


@singledispatch
def to_dataframe(data):
    """Convert altair.Data to pandas.DataFrame.

    Parameters
    ----------
    data : altair.Data
        The data source to be converted.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the same data as the `data` argument.

    """
    assert False, "Not implemented:" + str(type(data))


@to_dataframe.register(pd.DataFrame)
def _(data):
    return data


@to_dataframe.register(str)
def _(data):
    return pd.DataFrame(requests.get(data).json())


def default(*args):
    """Return the first not None of the arguments.

    Parameters
    ----------
    *args : Any
        Any number of arguments.

    Returns
    -------
    Any
        One of the arguments.

    """
    return next(x for x in args if x is not None)


def gather(data, key, value, columns):
    """Convert wide format data frame to long format.

    Do so while concatenating selected columns into one and using a new column
    to track their origin.

    Parameters
    ----------
    data : pandas DataFrame
        The data to operate on.
    key : str
        The name of the column tracking the origin of that record.
    value : type
        The name of the column holding all the values previously in a number of
        columns.
    columns : list of str
        The names of the columns to reduce to a single column.

    Returns
    -------
    pandas.DataFrame
        A data frame with a reduced number of columns but the same information.

    """
    return pd.melt(
        data,
        id_vars=[col for col in data.columns if col not in columns],
        value_vars=columns,
        var_name=key,
        value_name=value,
    )


# argument manip (may belong to signatures)
@attrs
class Column:
    col = attrib()

    def to_str(self, inst):
        """Convert a col specification to a col name and assign it to a given attribute.

        If it's an int, look at  inst['data'] positionally to find the col name, otherwise convert to str.
        Parameters
        ----------
        inst : any
            Instance to which attribute belongs.


        Returns
        -------
        str
            Column name
            """

        value = self.col
        if value is not None:
            value = (
                inst["data"].columns[value] if isinstance(value, Number) else str(value)
            )
        assert isinstance(value, str) or value is None
        return value


@attrs
class Columns:
    cols = attrib()

    def to_str(self, inst):
        """Convert a col set specification to a list of str.

        It first promotes value to a list if not Iterable, then applies to_column to each element and assigns result to attribute in inst. If value is None, it is construed as "all columns in inst['data']"

        Parameters
        ----------
        inst : any
            Instance to which attribute belongs.


        Returns
        -------
        list of str
            List of column names

        """

        value = self.cols
        value = (
            list(inst["data"].columns)
            if value is None
            else (
                [inst["data"].columns[value]]
                if isinstance(value, int)
                else (
                    [value]
                    if isinstance(value, str)
                    else list(
                        map(
                            lambda x: inst["data"].columns[x] if type(x) is int else x,
                            value,
                        )
                    )
                )
            )
        )
        for v in value:
            assert isinstance(v, str) or v is None
        return value


def init_cols(inst):
    for k, arg in inst.items():
        if isinstance(arg, (Column, Columns)):
            inst[k] = inst[k].to_str(inst)


# TODO: this doesn't cover multiscatterplot which is a multivariate viz but does
# require the data in wide format, this only converts to long (gather)
def multivariate_preprocess(data, columns, group_by):
    """Preprocess data for multivariate graphs.

    Converts to data frame, then turns to long format.

    Parameters
    ----------
    data : pandas.DataFrame
        The data to be processed.
    columns : list of str
        The columns that need to be gathered.
    group_by : str
        The column indicating which vaiable a record refers to (long format).

    Returns
    -------
    (pandas.DataFrame, str, str)
        A tuple with the data in long format, the name of the column indicating
        the variable and the name of of the column holding the values.

    """
    assert (
        type(columns) == str or len(columns) == 1 or group_by is None
    ), "Wide or long format but not both"
    if group_by is None:  # convert wide to long
        key = default(data.columns.name, "variable")
        value = "value"
        data = gather(data, key=key, value=value, columns=columns)
    else:
        key = group_by
        value = columns if type(columns) is str else columns[0]
    return data, key, value


# testing
def viz_reg_test(test_f):
    """Decorate recipe tests.

    Transforms a function into a regression test. Also saves chart in html for
    visual inspection in the test directory, named after the file and function
    of the test. If invoked with None as sole argument, the decorated function
    will just produce the chart, disabling the regression machinery, again for
    manual inspection.

    Parameters
    ----------
    test_f : function
        Simple chart-generating argumentless function, pytest-style

    Returns
    -------
    function
        The decorated function.

    """

    def fun(regtest):
        with alt.data_transformers.enable(consolidate_datasets=False):
            np.random.seed(seed=0)
            plot = test_f()
            if regtest is not None:
                regtest.write(
                    alt.Chart.from_dict(round_floats(plot.to_dict(), 13)).to_json()
                )
                plot.save(
                    test_f.__code__.co_filename + "_" + test_f.__qualname__ + ".html"
                )
            return plot

    test_f.__doc__ = (
        (
            test_f.__doc__
            or "Test for function {test_f}".format(test_f=test_f.__qualname__)
        )
        + """
    Parameters
    ----------
    Pass a single unnamed argument equal None to manually  execute outside regression testing. In that case it returns a chart.
    """
    )
    return fun


# constant luminosity and chroma scales

hue_scale_light = alt.Scale(type="linear", range=["#F271B8", "#00B4D7"])
hue_scale_dark = alt.Scale(type="linear", range=["#C10083", "#0080A7"])

# chart combinators


def layer(*layers, **kwargs):
    """Layer charts: a drop in replacement for altair.layer that does a deepcopy of the layers to avoid side-effects and lifts identical datasets one level down to top level."""
    layers = [l.copy() for l in layers]
    data = layers[0].data
    if all(map(lambda l: data.equals(l.data), layers)):
        layered = alt.layer(*layers, **kwargs, data=data)
        for l in layered.layer:
            del l._kwds["data"]
    else:
        layered = alt.layer(*layers, **kwargs)

    return layered
