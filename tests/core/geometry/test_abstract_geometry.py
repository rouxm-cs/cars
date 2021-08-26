#!/usr/bin/env python
# coding: utf8
#
# Copyright (c) 2020 Centre National d'Etudes Spatiales (CNES).
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
Test module for cars.core.geometry
"""
import numpy as np
import pytest

import cars.core.constants as cst

from ...helpers import absolute_data_path
from .dummy_abstract_classes import (  # noqa; pylint: disable=unused-import
    NoMethodClass,
)

from cars.core.geometry import (  # noqa;  isort:skip; pylint: disable=wrong-import-order
    AbstractGeometry,
)


@pytest.fixture
def epipolar_coords():
    """
    inputs for the test_matches_to_sensor_coords and
    test_sensor_position_from_grid tests
    """
    left_epipolar_coords = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [2.0, 0.0],
            [3.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
            [2.0, 1.0],
            [3.0, 1.0],
            [0.0, 2.0],
            [1.0, 2.0],
            [2.0, 2.0],
            [3.0, 2.0],
        ]
    )

    right_epipolar_coords = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [2.0, 0.0],
            [3.0, 0.0],
            [4.0, 1.0],
            [6.0, 1.0],
            [8.0, 1.0],
            [10.0, 1.0],
            [8.0, 2.0],
            [10.0, 2.0],
            [12.0, 2.0],
            [14.0, 2.0],
        ]
    )

    out_dict = {
        "left": left_epipolar_coords,
        "right": right_epipolar_coords,
    }

    return out_dict


@pytest.fixture
def ref_sensor_coords():
    """
    expected results for the test_matches_to_sensor_coords,
    test_disp_to_sensor_coords and test_sensor_position_from_grid tests
    """
    left_sensor_coords = np.array(
        [
            [-5737.38623047, -1539.64440918],
            [-5738.12719727, -1539.61027832],
            [-5738.86816406, -1539.57614746],
            [-5739.60913086, -1539.5420166],
            [-5735.42036133, -1540.38536784],
            [-5736.16132867, -1540.35123711],
            [-5736.90229601, -1540.31710639],
            [-5737.64326335, -1540.28297567],
            [-5733.45449219, -1541.1263265],
            [-5734.19546007, -1541.09219591],
            [-5734.93642795, -1541.05806532],
            [-5735.67739583, -1541.02393473],
        ]
    )
    right_sensor_coords = np.array(
        [
            [-5737.38623047, -1539.64440918],
            [-5738.12719727, -1539.61027832],
            [-5738.86816406, -1539.57614746],
            [-5739.60913086, -1539.5420166],
            [-5738.38423069, -1540.24884494],
            [-5739.86616536, -1540.1805835],
            [-5741.34810004, -1540.11232205],
            [-5742.83003472, -1540.0440606],
            [-5739.38223524, -1540.85328179],
            [-5740.86417101, -1540.78502062],
            [-5742.34610677, -1540.71675944],
            [-5743.82804253, -1540.64849826],
        ]
    )

    out_dict = {
        "left": left_sensor_coords,
        "right": right_sensor_coords,
    }
    return out_dict


@pytest.mark.unit_tests
def test_missing_abstract_methods():
    """
    Test cars geometry abstract class
    """
    with pytest.raises(Exception) as error:
        AbstractGeometry(  # pylint: disable=abstract-class-instantiated
            "NoMethodClass"
        )
    assert (
        str(error.value) == "Can't instantiate abstract class"
        " NoMethodClass with abstract methods check_products_consistency, "
        "conf_schema, generate_epipolar_grids, triangulate"
    )


@pytest.mark.unit_tests
def test_wrong_class_name():
    """
    Test cars geometry abstract class
    """
    with pytest.raises(KeyError) as error:
        AbstractGeometry("test")  # pylint: disable=abstract-class-instantiated
    assert str(error.value) == "'No geometry loader named test registered'"


@pytest.mark.unit_tests
def test_sensor_position_from_grid(
    epipolar_coords, ref_sensor_coords
):  # pylint: disable=redefined-outer-name
    """
    Test sensor_position_from_grid
    """
    grid = absolute_data_path("input/abstract_geometry_input/grid.tif")

    coords = AbstractGeometry.sensor_position_from_grid(
        grid, epipolar_coords["left"]
    )
    assert np.allclose(ref_sensor_coords["left"], coords)

    coords = AbstractGeometry.sensor_position_from_grid(
        grid, epipolar_coords["right"]
    )
    assert np.allclose(ref_sensor_coords["right"], coords)


@pytest.mark.unit_tests
def test_disp_to_sensor_coords(
    ref_sensor_coords,
):  # pylint: disable=redefined-outer-name
    """
    Test matching_data_to_sensor_coords with the cst.DISP_MODE
    """
    grid1 = absolute_data_path("input/abstract_geometry_input/grid.tif")
    grid2 = absolute_data_path("input/abstract_geometry_input/grid.tif")

    nb_row = 3
    nb_col = 4
    disp_map = np.arange(nb_row * nb_col)
    disp_map = disp_map.reshape((nb_row, nb_col))
    disp_msk = np.full((nb_row, nb_col), fill_value=255)
    disp_msk[0, :] = 0

    (
        sensor_pos_left,
        sensor_pos_right,
    ) = AbstractGeometry.matches_to_sensor_coords(
        grid1, grid2, disp_map, cst.DISP_MODE, matches_msk=disp_msk
    )

    ref_sensor_pos_left_x = np.copy(ref_sensor_coords["left"][:, 0])
    ref_sensor_pos_left_y = np.copy(ref_sensor_coords["left"][:, 1])
    ref_sensor_pos_left_x = ref_sensor_pos_left_x.reshape((nb_row, nb_col))
    ref_sensor_pos_left_y = ref_sensor_pos_left_y.reshape((nb_row, nb_col))
    ref_sensor_pos_left_x[np.where(disp_msk != 255)] = np.nan
    ref_sensor_pos_left_y[np.where(disp_msk != 255)] = np.nan

    assert np.allclose(
        sensor_pos_left[:, :, 0], ref_sensor_pos_left_x, equal_nan=True
    )
    assert np.allclose(
        sensor_pos_left[:, :, 1], ref_sensor_pos_left_y, equal_nan=True
    )

    ref_sensor_pos_right_x = np.copy(ref_sensor_coords["right"][:, 0])
    ref_sensor_pos_right_y = np.copy(ref_sensor_coords["right"][:, 1])
    ref_sensor_pos_right_x = ref_sensor_pos_right_x.reshape((nb_row, nb_col))
    ref_sensor_pos_right_y = ref_sensor_pos_right_y.reshape((nb_row, nb_col))
    ref_sensor_pos_right_x[np.where(disp_msk != 255)] = np.nan
    ref_sensor_pos_right_y[np.where(disp_msk != 255)] = np.nan

    assert np.allclose(
        sensor_pos_right[:, :, 0], ref_sensor_pos_right_x, equal_nan=True
    )
    assert np.allclose(
        sensor_pos_right[:, :, 1], ref_sensor_pos_right_y, equal_nan=True
    )

    # test with a cropped disparity map
    ul_corner_crop = (1, 2)
    disp_map = disp_map[ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col]
    disp_msk = disp_msk[ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col]

    (
        sensor_pos_left,
        sensor_pos_right,
    ) = AbstractGeometry.matches_to_sensor_coords(
        grid1,
        grid2,
        disp_map,
        cst.DISP_MODE,
        matches_msk=disp_msk,
        ul_matches_shift=ul_corner_crop,
    )

    ref_sensor_pos_left_x = ref_sensor_pos_left_x[
        ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col
    ]
    ref_sensor_pos_left_y = ref_sensor_pos_left_y[
        ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col
    ]

    assert np.allclose(
        sensor_pos_left[:, :, 0], ref_sensor_pos_left_x, equal_nan=True
    )
    assert np.allclose(
        sensor_pos_left[:, :, 1], ref_sensor_pos_left_y, equal_nan=True
    )

    ref_sensor_pos_right_x = ref_sensor_pos_right_x[
        ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col
    ]
    ref_sensor_pos_right_y = ref_sensor_pos_right_y[
        ul_corner_crop[0] : nb_row, ul_corner_crop[1] : nb_col
    ]
    assert np.allclose(
        sensor_pos_right[:, :, 0], ref_sensor_pos_right_x, equal_nan=True
    )
    assert np.allclose(
        sensor_pos_right[:, :, 1], ref_sensor_pos_right_y, equal_nan=True
    )


@pytest.mark.unit_tests
def test_matches_to_sensor_coords(
    epipolar_coords, ref_sensor_coords
):  # pylint: disable=redefined-outer-name
    """
    Test matching_data_to_sensor_coords with the cst.MATCHES_MODE
    """
    grid1 = absolute_data_path("input/abstract_geometry_input/grid.tif")
    grid2 = absolute_data_path("input/abstract_geometry_input/grid.tif")

    matches = np.hstack([epipolar_coords["left"], epipolar_coords["right"]])

    (
        sensor_pos_left,
        sensor_pos_right,
    ) = AbstractGeometry.matches_to_sensor_coords(
        grid1, grid2, matches, cst.MATCHES_MODE
    )

    assert np.allclose(sensor_pos_left, ref_sensor_coords["left"])
    assert np.allclose(sensor_pos_right, ref_sensor_coords["right"])