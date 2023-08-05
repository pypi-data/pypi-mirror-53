"""
Tests for rebalancing of channels.
"""
import time
from unittest import TestCase

from lnregtest.lib.network import RegtestNetwork

from lndmanage import settings
from lndmanage.lib.node import LndNode
from lndmanage.lib.listchannels import ListChannels
from lndmanage.lib.rebalance import Rebalancer
from lndmanage.lib.ln_utilities import channel_unbalancedness_and_commit_fee

from test.testing_common import (
    bin_dir,
    test_data_dir,
    lndmanage_home,
    test_graphs_paths,
    SLEEP_SEC_AFTER_REBALANCING)

import logging.config
settings.set_lndmanage_home_dir(lndmanage_home)
logging.config.dictConfig(settings.logger_config)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers[0].setLevel(logging.DEBUG)


class TestRebalance(TestCase):
    def setUp(self):
        self.testnet = RegtestNetwork(
            binary_folder=bin_dir,
            network_definition_location=test_graphs_paths['small_star_ring'],
            nodedata_folder=test_data_dir,
            node_limit='H',
            from_scratch=True
        )
        self.testnet.run_nocleanup()
        # to run the lightning network in the background and do some testing
        # here, run:
        # $ lnregtest --nodedata_folder /path/to/lndmanage/test/test_data/
        # self.testnet.run_from_background()

        # logger.info("Generated network information:")
        # logger.info(format_dict(self.testnet.node_mapping))
        # logger.info(format_dict(self.testnet.channel_mapping))
        # logger.info(format_dict(self.testnet.assemble_graph()))

        master_node_data_dir = self.testnet.master_node.lnd_data_dir
        master_node_port = self.testnet.master_node.grpc_port
        master_node_networkinfo = self.testnet.master_node.getnetworkinfo()

        self.assertEqual(4, master_node_networkinfo['num_nodes'])
        self.assertEqual(6, master_node_networkinfo['num_channels'])

        self.lndnode = LndNode(
            lnd_home=master_node_data_dir,
            lnd_host='localhost:' + str(master_node_port),
            regtest=True
        )

        # self.lndnode.print_status()
        logger.info('Initializing done.')

        # channels:
        # A -> B (channel #1)
        # A -> C (channel #2)
        # A -> D (channel #6)
        # B -> C (channel #3)
        # B -> D (channel #4)
        # C -> D (channel #5)

    def tearDown(self):
        self.testnet.cleanup()

    def rebalance_and_check(self, test_channel_number, target,
                            allow_unbalancing, places=5, should_fail=False):
        """
        Test function for rebalancing to a specific target and assert after-
        wards that is was reached.

        :param test_channel_number: int
        :param target: float:
            unbalancedness target
        :param allow_unbalancing: bool:
            unbalancing should be allowed
        :param places: int
            number of digits the result should match to the requested
        :param should_fail: bool:
            indicates whether the rebalancing should fail as requested due to
            maybe unbalancing of other channels
        """
        rebalancer = Rebalancer(
            self.lndnode,
            max_effective_fee_rate=50,
            budget_sat=20
        )

        channel_id = self.testnet.channel_mapping[
            test_channel_number]['channel_id']
        rebalancer.rebalance(
            channel_id,
            dry=False,
            chunksize=1.0,
            target=target,
            allow_unbalancing=allow_unbalancing
        )
        time.sleep(SLEEP_SEC_AFTER_REBALANCING)
        graph = self.testnet.assemble_graph()
        channel_data = graph['A'][test_channel_number]
        listchannels = ListChannels(self.lndnode)
        listchannels.print_all_channels('rev_alias')

        channel_unbalancedness, _ = channel_unbalancedness_and_commit_fee(
            channel_data['local_balance'],
            channel_data['capacity'],
            channel_data['commit_fee'],
            channel_data['initiator']
        )

        if not should_fail:
            self.assertAlmostEqual(target, channel_unbalancedness,
                                   places=places)
        else:
            self.assertNotAlmostEqual(target, channel_unbalancedness,
                                      places=places)

    def test_rebalance_channel_6(self):
        test_channel_number = 6
        self.rebalance_and_check(test_channel_number, 0.0, False)

    def test_small_positive_target_channel_6(self):
        test_channel_number = 6
        self.rebalance_and_check(test_channel_number, 0.2, False)

    def test_large_positive_channel_6(self):
        test_channel_number = 6
        self.rebalance_and_check(test_channel_number, 0.8, False)

    def test_small_negative_target_channel_6_fail(self):
        # this test should fail when unbalancing is not allowed, as it would
        # unbalance another channel if the full target would be accounted for
        test_channel_number = 6
        self.rebalance_and_check(test_channel_number, -0.2, False,
                                 should_fail=True)

    def test_small_negative_target_channel_6_succeed(self):
        # this test should fail when unbalancing is not allowed, as it would
        # unbalance another channel if the full target would be accounted for
        test_channel_number = 6
        self.rebalance_and_check(test_channel_number, -0.2, True)

    def test_rebalance_channel_1(self):
        test_channel_number = 1
        self.rebalance_and_check(test_channel_number, 0.0, False)

    def test_rebalance_channel_2(self):
        test_channel_number = 2
        self.rebalance_and_check(test_channel_number, 0.0, False, places=1)

    def test_shuffle_arround(self):
        """
        Shuffles sat around in channel 6.
        """
        first_target_amount = -0.1
        second_target_amount = 0.1
        test_channel_number = 6

        self.rebalance_and_check(
            test_channel_number, first_target_amount, True)
        self.rebalance_and_check(
            test_channel_number, second_target_amount, True)
