# Copyright 2017 - 2019 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Multiple progress bars example
"""

import logging
import platform
import random
import time

import enlighten


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('enlighten')

DATACENTERS = 5
SYSTEMS = (10, 20)  # Range
FILES = (100, 1000)  # Range


def process_files(manager):
    """
    Process a random number of files on a random number of systems across multiple data centers
    """

    # Get a top level progress bar
    enterprise = manager.counter(total=DATACENTERS, desc='Processing:', unit='datacenters')

    # Iterate through data centers
    for dnum in range(1, DATACENTERS + 1):
        systems = random.randint(*SYSTEMS)  # Random number of systems
        # Get a child progress bar. leave is False so it can be replaced
        currCenter = manager.counter(total=systems, desc='  Datacenter %d:' % dnum,
                                     unit='systems', leave=False)

        # Iterate through systems
        for snum in range(1, systems + 1):

            # Has no total, so will act as counter. Leave is False
            system = manager.counter(desc='    System %d:' % snum, unit='files', leave=False)
            files = random.randint(*FILES)  # Random file count

            # Iterate through files
            for fnum in range(files):  # pylint: disable=unused-variable
                system.update()  # Update count
                time.sleep(random.uniform(0.0001, 0.0005))  # Random processing time

            system.close()  # Close counter so it gets removed
            # Log status
            LOGGER.info('Updated %d files on System %d in Datacenter %d', files, snum, dnum)
            currCenter.update()  # Update count

        currCenter.close()  # Close counter so it gets removed

        enterprise.update()  # Update count

    enterprise.close()  # Close counter, won't be removed but does a refresh


def main():
    """
    Main function
    """

    manager = enlighten.get_manager()
    process_files(manager)
    manager.stop()  # Clears all temporary counters and progress bars


if __name__ == '__main__':

    # https://docs.microsoft.com/en-us/windows/desktop/api/timeapi/nf-timeapi-timebeginperiod
    if platform.system() == 'Windows':
        from ctypes import windll
        windll.winmm.timeBeginPeriod(1)
        main()
        windll.winmm.timeEndPeriod(1)
    else:
        main()
