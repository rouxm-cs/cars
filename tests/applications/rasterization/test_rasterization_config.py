#!/usr/bin/env python
# coding: utf8
#
# Copyright (c) 2023 Centre National d'Etudes Spatiales (CNES).
#
# This file is part of CARS
# (see https://github.com/CNES/cars).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Test module for config of cars/applications/rasterization/simple_gaussian.py
"""

import json_checker

# Third party imports
import pytest

# CARS imports
from cars.applications.rasterization.simple_gaussian import SimpleGaussian


@pytest.mark.unit_tests
def test_check_full_conf():
    """
    Test configuration check for rasterization application
    with forbidden value for parameter resolution
    """
    conf = {
        "method": "simple_gaussian",
        "dsm_radius": 1,
        "sigma": None,
        "grid_points_division_factor": None,
        "resolution": 0.5,
        "dsm_no_data": -32768,
        "color_no_data": 0,
        "color_dtype": None,
        "msk_no_data": 255,
        "save_color": True,
        "save_stats": False,
        "save_mask": False,
        "save_classif": False,
        "save_dsm": True,
        "save_intervals": False,
        "save_confidence": False,
        "save_source_pc": False,
        "save_filling": False,
        "save_intermediate_data": False,
    }
    _ = SimpleGaussian(conf)


@pytest.mark.unit_tests
def test_check_conf_with_error():
    """
    Test configuration check for rasterization application
    with forbidden value for parameter resolution
    """
    conf = {
        "method": "simple_gaussian",
        "resolution": 0,  # should be > 0
    }
    with pytest.raises(json_checker.core.exceptions.DictCheckerError):
        _ = SimpleGaussian(conf)
