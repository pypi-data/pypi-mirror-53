# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.api.distribution_trees_distribution_trees_api import DistributionTreesDistributionTreesApi  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException


class TestDistributionTreesDistributionTreesApi(unittest.TestCase):
    """DistributionTreesDistributionTreesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_rpm.api.distribution_trees_distribution_trees_api.DistributionTreesDistributionTreesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete(self):
        """Test case for delete

        Delete a distribution tree  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List distribution trees  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a distribution tree  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
