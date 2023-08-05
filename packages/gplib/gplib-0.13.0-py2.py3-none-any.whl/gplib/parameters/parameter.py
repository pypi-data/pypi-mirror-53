# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from .parametrizable import Parametrizable


class Parameter(Parametrizable):
    """

    """
    def __init__(self, name, optimizable, transformation,
                 default_value, bounds=None, grid=None):
        """

        :param name:
        :type name:
        :param optimizable:
        :type optimizable:
        :param transformation:
        :type transformation:
        :param default_value:
        :type default_value:
        :param bounds:
        :type bounds:
        :param grid:
        :type grid:
        """

        self.optimizable = optimizable
        self.name = name
        self.transformation = transformation
        self.default_value = default_value
        self.array = hasattr(self.default_value, "__len__")
        self.current_value = self.default_value
        self.bounds = bounds
        if self.bounds is None:
            self.bounds = (np.exp(-10), np.exp(10))
        self.grid = grid
        if self.grid is None:
            self.grid = [np.nan]

        self.dims = 1
        if self.array:
            self.dims = len(self.default_value)

    def is_array(self):
        """

        :return:
        :rtype:
        """
        return self.array

    def set_param_values(self, params, optimizable_only=False, trans=False):
        """

        :param params:
        :type params:
        :param optimizable_only:
        :type optimizable_only:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return

        assert len(params) == self.dims, \
            "length of {} is not correct".format(self.name)

        if trans:
            if self.array:
                params = self.transformation.inv_trans(params).tolist()
            else:
                params = self.transformation.inv_trans(params)

        if self.array is False:
            self.current_value = params[0]
        else:
            self.current_value = params

    def set_params_to_default(self, optimizable_only=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return

        self.current_value = self.default_value

    def get_param_values(self, optimizable_only=False, trans=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return []

        assert self.current_value is not None, \
            "{} has not been initialized".format(self.name)

        current_value = self.current_value
        if trans:
            current_value = self.transformation.trans(current_value)
            if self.array:
                current_value = current_value.tolist()

        if self.array:
            return current_value
        return [current_value]

    def get_param_bounds(self, optimizable_only=False, trans=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return []

        current_bounds = self.bounds
        if trans:
            current_bounds = tuple(
                self.transformation.trans(bound)
                for bound in current_bounds
            )

        return [current_bounds] * self.dims

    def get_param_grid(self, optimizable_only=False, trans=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return [[]]

        current_elements = self.grid
        if trans:
            current_elements = [
                self.transformation.trans(element)
                for element in current_elements
            ]

        current_elements = [current_elements] * self.dims

        current_grid = np.array(np.meshgrid(*current_elements))
        current_grid = current_grid.T.reshape(-1, len(current_elements))

        return current_grid.tolist()

    def get_param_keys(self, recursive=True, optimizable_only=False):
        """

        :param recursive:
        :type recursive:
        :param optimizable_only:
        :type optimizable_only:
        :return:
        :rtype:
        """

        if optimizable_only and not self.optimizable:
            return []

        if not recursive:
            return self.name

        if self.dims == 1:
            return [self.name]

        return [
            "{}_d{}".format(self.name, dim) for dim in range(self.dims)
        ]

    def get_param_n(self, optimizable_only=False):
        """

        :param optimizable_only:
        :type optimizable_only:
        :return:
        :rtype:
        """
        if optimizable_only and not self.optimizable:
            return 0

        return self.dims

    def grad_trans(self, df):
        """

        :param df:
        :type df:
        :return:
        :rtype:
        """

        return self.transformation.grad_trans(self.current_value, df)
