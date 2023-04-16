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

AWS Clustered Web Services

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
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, Route53

with Diagram("AWS Clustered Web Services", show=bool(os.environ.get('CI', 0))):
    dns = Route53("Route53")
    lb = ELB("ELB")

    with Cluster("Web Services"):
        svc_group = [ECS("web2"),  # middle
                     ECS("web3"),  # puts below
                     ECS("web1")]  # puts above
                     # this is why it's ordered weirdly here but comes out ordered in diagram

    with Cluster("RDS Cluster"):
        # pylint: disable=W0106
        db_primary = RDS("userdb")
        db_primary - [RDS("userdb ro")]

    memcached = ElastiCache("ElastiCache\nmemcached")

    # pylint: disable=W0104
    dns >> lb >> svc_group
    svc_group >> db_primary
    svc_group >> memcached
