#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pandas_log` package."""

import pandas as pd

from pandas_log import *


def test_pipeline():
    with enable():
        df = pd.read_csv("../examples/pokemon.csv")

        (
            df.query("legendary==0")
            .query("type_1=='fire' or type_2=='fire'")
            .drop("legendary", axis=1)
            .nsmallest(1, "total")
            .reset_index(drop=True)
        )
    (
        df.query("legendary==0")
        .query("type_1=='fire' or type_2=='fire'")
        .drop("legendary", axis=1)
        .nsmallest(1, "total")
        .reset_index(drop=True)
    )


test_pipeline()
