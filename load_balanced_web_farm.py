#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-14 13:54:52 +0100 (Fri, 14 Apr 2023)
#
#  https://github.com/HariSekhon/Diagrams-as-Code
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn
#  and optionally send me feedback to help steer this or other code I publish
#
#  https://www.linkedin.com/in/HariSekhon
#

"""

Load Balanced Web Farm

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

from diagrams import Diagram

# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Load Balanced Web Farm", show=True, direction="TB"):
    # can use variables to connect nodes to the same items
    # lb = ELB("lb")
    # db = RDS("events")
    # lb >> EC2("worker1") >> db
    # lb >> EC2("worker2") >> db
    # lb >> EC2("worker3") >> db
    # lb >> EC2("worker4") >> db
    # lb >> EC2("worker5") >> db

    # but less redundant code than the above can be achieved by grouping the workers into a list[]
    # pylint: disable=W0106
    ELB("ELB") >> [EC2("web1"),
                  EC2("web2"),
                  EC2("web3"),
                  EC2("web4"),
                  EC2("web5")] >> RDS("RDS DB")
