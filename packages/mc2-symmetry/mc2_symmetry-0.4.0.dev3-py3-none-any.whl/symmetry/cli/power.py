import argparse
import logging
import os
import signal

from symmetry.common import config
from symmetry.telemetry.power import PowerMonitor

logger = logging.getLogger(__name__)


def main():
    log_level = os.getenv('symmetry_logging_level')
    if log_level:
        logging.basicConfig(level=logging._nameToLevel[log_level])

    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', help='sampling interval', type=float,
                        default=os.getenv('symmetry_power_sampling'))

    args = parser.parse_args()
    rds = config.get_redis()
    powmon = PowerMonitor(rds, interval=args.interval)

    def terminate(signum, frame):
        logger.info('signal received %s', signum)
        powmon.cancel()
        raise NotImplementedError

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)

    try:
        logging.info('starting power monitor')
        powmon.run()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('stopping power monitor...')
        powmon.cancel()


if __name__ == '__main__':
    main()
