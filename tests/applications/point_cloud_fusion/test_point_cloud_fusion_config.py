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
Test module for config of
cars/applications/point_cloud_fusion/point_cloud_fusion.py
"""

import pytest

from cars.applications.point_cloud_fusion.mapping_to_terrain_tiles import (
    MappingToTerrainTiles,
)


@pytest.mark.unit_tests
def test_check_full_conf():
    """
    Test configuration check for point cloud fusion application
    """
    conf = {
        "method": "mapping_to_terrain_tiles",
        "save_points_cloud_as_laz": False,
        "save_points_cloud_as_csv": False,
        "save_points_cloud_by_pair": False,
    }
    _ = MappingToTerrainTiles(conf)