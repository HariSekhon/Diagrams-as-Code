#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-17 03:04:55 +0100 (Mon, 17 Apr 2023)
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

AWS Web Traffic

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster

# ============================================================================ #
# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#

from diagrams.aws.compute import EC2  # , ApplicationAutoScaling
from diagrams.aws.network import ELB, Route53, CloudFront  # , VPC
from diagrams.aws.storage import S3
from diagrams.aws.general import Users

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
}

# pylint: disable=W0104,W0106
with Diagram('AWS Web Traffic',
             show=not bool(os.environ.get('CI', 0)),
             direction='LR',     # left-to-right, other options: TB, BT, LR, RL
             filename='images/aws_web_traffic',
             graph_attr=graph_attr,
             ):

    users = Users("Users")

    with Cluster("AWS"):
        cdn = CloudFront("CloudFront CDN")
        s3 = S3("S3 bucket (static assets)")
        users \
            >> Route53("Route53 DNS") \
            >> cdn

        with Cluster("VPC"):
            # VPC("VPC")

            lb = ELB("ELB Load Balancer")
            cdn >> lb
            cdn >> s3

            with Cluster("AutoScaling Group"):
                lb >> EC2("Server 1")
                lb >> EC2("Server 2")
                # ApplicationAutoScaling("AutoScaling Group")
