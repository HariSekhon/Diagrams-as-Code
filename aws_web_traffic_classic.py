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
__version__ = '0.3'

import os
# from urllib.request import urlretrieve
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

from diagrams.custom import Custom

# pylint: disable=C0103
# aws_url =
aws_icon = 'aws.png'

image_dir = 'images'

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
}


# NOTE: filename=images/ parameter to Diagram() changes the $PWD so icon path must be local dir,
# but at this point we're still at top level dir so must join to prefix it with the image_dir
# nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
# urlretrieve(aws_url, os.path.join(image_dir, aws_icon))

# pylint: disable=W0104,W0106
with Diagram('AWS Web Traffic Classic',
             show=not bool(os.environ.get('CI', 0)),
             direction='LR',     # left-to-right, other options: TB, BT, LR, RL
             filename=os.path.join(image_dir, 'aws_web_traffic_classic'),
             graph_attr=graph_attr,
             ):

    users = Users("Users")

    with Cluster("AWS"):
        Custom('', aws_icon)
        cdn = CloudFront("CloudFront CDN")
        s3 = S3("S3 bucket (static assets)")
        users \
            >> Route53("Route53 DNS")
        users \
            >> cdn

        with Cluster("VPC"):
            # VPC("VPC")

            lb = ELB("ELB Load Balancer")
            cdn >> lb
            cdn >> s3

            with Cluster("AutoScaling Group"):
                lb >> EC2("Web Server 1")
                lb >> EC2("Web Server 2")
                lb >> EC2("Web Server 3")
                # ApplicationAutoScaling("AutoScaling Group")
