import itertools
from contextlib import suppress
from functools import wraps
from inspect import signature

import pandas as pd
import pandas_flavor as pf

from pandas_log import patched_logs_functions, settings
from pandas_log.timer import Timer


def get_pandas_func(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Get original pandas method

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: Original pandas method
    """

    return getattr(pd.DataFrame, f"{prefix}{func.__name__}")


def get_signature_repr(fn, args, include_defaults=False):
    """ Get the signature for the original pandas method with actual values

        :param fn: The pandas method
        :param args: The arguments used when it was applied
        :return: string representation of the signature for the applied pandas method
    """

    def _get_orig_func_params():
        return [
            param_value if include_defaults else param_name
            for param_name, param_value in signature(
                get_pandas_func(fn)
            ).parameters.items()
            if param_name not in ("kwargs", "self")
        ]

    def _get_param_value(param_with_default, arg_value):
        res = str(param_with_default)
        if arg_value:
            param_name = res.split("=")[0]
            res = f"{param_name}={arg_value}"
        return res

    zip_func = itertools.zip_longest if include_defaults else zip
    orig_func_params = _get_orig_func_params()
    args_vals = ", ".join(
        _get_param_value(param_with_default, arg_value)
        for param_with_default, arg_value in zip_func(orig_func_params, args)
    )
    return f"{fn.__name__}({args_vals}):"


def get_patch_log_func(func, prefix=settings.PATCHED_LOG_METHOD_PREFIX):
    """ Get return relevant log function.
        For example: for .query pandas' method as input one will get ._log_query method
        from patched_functions

        :param func: The pandas method we applied and going to calculate stats
        :return: a function which calculate statistic for the applied pandas method
    """

    res = None
    with suppress(AttributeError):
        res = getattr(patched_logs_functions, f"{prefix}{func.__name__}")
    return res


def restore_pandas_func_copy(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Restore the original pandas method instead of overridden one

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, func.replace(prefix, ""), original_method)


def keep_pandas_func_copy(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Saved copy of the pandas method before it overridden

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, f"{prefix}{func}", original_method)


def create_overide_pandas_func(func, silent):
    """ Create overridden pandas method dynamically

        :param func: pandas method name to be overridden
        :param silent: Whether additional the statistics get printed
        :return: the same function with additional logging capabilities
    """

    def _log_func_stats(
        exec_time, fn, fn_args, fn_kwargs, input_df, output_df, silent
    ):
        """ Calculate relevant statistics for this pandas method and
            save an attribute (step_logs) which saves history of teh applied methods

            :param exec_time: the time it took a function to run in a human friendly way
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param fn_kwargs: The original pandas method kwargs
            :param input_df: the DataFrame before applying function fn
            :param output_df: the DataFrame after applying function fn
            :param silent: Whether additional the statistics get printed
            :return: None
        """
        from pandas_log.dataframe_logger import DataFrameLogger

        dl = DataFrameLogger(**locals())
        dl.calc_step_stats()

    def _overide_dataframe_method(fn):
        """ Decorator function that Create overridden pandas method with
            additional logging using DataFrameLogger

            Note: if we extracting _overide_dataframe_method outside we need to implement decorator like here
                  https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
            :param fn: pandas original method to be overridden
            :return: the overridden pandas method
        """

        @pf.register_dataframe_method
        @wraps(fn)
        def wrapped(*args, **kwargs):
            with Timer() as t:
                output_df = get_pandas_func(fn)(*args, **kwargs)

            _log_func_stats(
                exec_time=t.humanized_exec_time,
                fn=fn,
                fn_args=args[1:],
                fn_kwargs=kwargs,
                input_df=args[0],
                output_df=output_df,
                silent=silent,
            )

            return output_df

        return wrapped

    return exec(
        f"@_overide_dataframe_method\ndef {func}(df, *args, **kwargs): pass"
    )


if __name__ == "__main__":
    pass
