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

AWS Web Service with DB Cluster

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster

# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import Route53

# Cluster puts a box around RDS nodes, and can connect outside ECS and Route53 to the primary RDS
with Diagram("AWS Web Service DB Cluster", show=bool(os.environ.get('CI', 0))):
    dns = Route53("Route53 DNS")
    web = ECS("ECS web service")

    with Cluster("RDS DB Cluster"):
        db_primary = RDS("primary")
        # pylint: disable=W0106
        db_primary - [RDS("replica2"),
                      RDS("replica1")]

    # pylint: disable=W0104
    dns >> web >> db_primary
