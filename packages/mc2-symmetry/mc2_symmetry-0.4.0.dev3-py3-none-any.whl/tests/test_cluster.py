import os
import unittest

from symmetry.api import NodeInfo
from symmetry.clusterd import RedisClusterInfo
from symmetry.common.cluster import ConfigNodeLister, RedisNodeManager
from tests.testutils import RedisResource


class TestCluster(unittest.TestCase):
    redis_resource = RedisResource()

    def setUp(self) -> None:
        self.redis_resource.setUp()

    def tearDown(self) -> None:
        self.redis_resource.tearDown()

    def test_config_node_lister(self):
        ini = os.path.join(os.path.dirname(__file__), 'test_nodes.ini')

        manager = ConfigNodeLister(ini)

        node1 = manager.nodes[0]
        node2 = manager.nodes[1]

        self.assertEqual('node1', node1.node_id)
        self.assertEqual('192.168.0.1', node1.host)
        self.assertEqual('01:02:03:04:05:01', node1.mac)
        self.assertEqual('node1user', node1.user)
        self.assertEqual(22, node1.ssh_port)

        self.assertEqual('node2', node2.node_id)
        self.assertEqual('192.168.0.2', node2.host)
        self.assertEqual('node2user', node2.user)
        self.assertEqual(22, node2.ssh_port)

    def test_redis_node_manager(self):
        manager = RedisNodeManager(self.redis_resource.rds)

        node1 = NodeInfo('node1', 'localhost', ssh_port=22001, user='root')
        node2 = NodeInfo('node2', 'localhost', ssh_port=22002, user='root')
        node3 = NodeInfo('node3', 'localhost', ssh_port=22003, user='root')

        manager.save_node(node1)
        manager.save_node(node2)
        manager.save_node(node3)

        manager.set_node_state('node1', 'unknown')
        manager.set_node_state('node2', 'unknown')
        manager.set_node_state('node3', 'unknown')

        nodes = list(manager.get_nodes())

        nodes.sort(key=lambda item: item.node_id)

        self.assertEqual(3, len(nodes))

        self.assertEqual('node1', nodes[0].node_id)
        self.assertEqual('node2', nodes[1].node_id)
        self.assertEqual('node3', nodes[2].node_id)

    def test_redis_node_manager_get_node(self):
        manager = RedisNodeManager(self.redis_resource.rds)
        node1 = NodeInfo('node1', 'localhost', ssh_port=22001, user='root')
        manager.save_node(node1)

        self.assertEqual(node1, manager.get_node('node1'))

    def test_redis_node_manager_get_node_on_non_existing_node(self):
        manager = RedisNodeManager(self.redis_resource.rds)

        self.assertIsNone(manager.get_node('NOTEXISTS'))

    def test_redis_cluster_info(self):
        manager = RedisNodeManager(self.redis_resource.rds)

        node1 = NodeInfo('node1', 'localhost', ssh_port=22001, user='root')
        node2 = NodeInfo('node2', 'localhost', ssh_port=22002, user='root')

        manager.save_node(node1)
        manager.save_node(node2)

        cluster = RedisClusterInfo(self.redis_resource.rds)
        self.assertIn('node1', cluster.nodes)
        self.assertIn('node2', cluster.nodes)
        self.assertEqual(2, len(cluster.nodes))

        self.assertEqual([], cluster.active_nodes)

        self.assertEqual(node1, cluster.node_info('node1'))
        self.assertEqual(node2, cluster.node_info('node2'))


if __name__ == '__main__':
    unittest.main()
