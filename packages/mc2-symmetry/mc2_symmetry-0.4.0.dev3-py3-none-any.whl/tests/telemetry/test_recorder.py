import unittest
from queue import Queue

from symmetry.telemetry.recorder import TelemetryRecorder
from tests.testutils import RedisResource


class TelemetryRecorderTest(unittest.TestCase):
    redis = RedisResource()

    def setUp(self) -> None:
        self.redis.setUp()

    def tearDown(self) -> None:
        self.redis.tearDown()

    def test_recorder(self):
        queue = Queue()

        class TestTelemetryRecorder(TelemetryRecorder):
            def _record(self, timestamp, metric, node, value):
                queue.put((timestamp, metric, node, value))

        recorder = TestTelemetryRecorder(self.redis.rds)
        recorder.start()

        self.redis.rds.publish('telemetry:cpu:unittest', '1001 41')
        self.redis.rds.publish('telemetry:cpu:unittest', '1002 42')

        ts, m, n, v = queue.get(timeout=2)
        self.assertEqual('1001', ts)
        self.assertEqual('cpu', m)
        self.assertEqual('unittest', n)
        self.assertEqual('41', v)

        ts, m, n, v = queue.get(timeout=2)
        self.assertEqual('1002', ts)
        self.assertEqual('cpu', m)
        self.assertEqual('unittest', n)
        self.assertEqual('42', v)

        recorder.stop()
        recorder.join(timeout=2)
