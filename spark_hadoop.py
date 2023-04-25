#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-20 14:48:53 +0100 (Thu, 20 Apr 2023)
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

Spark on Hadoop

"""

__author__ = 'Hari Sekhon'
__version__ = '0.2'

import os
from diagrams import Diagram, Cluster  # , Edge

# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Hadoop, Spark

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
    # "rotation": "90",
    "landscape": "false",
    # "center": "true",
    # "margin": "0",
    # "lheight": "200",
    # "lwidth": "5",
}

# pylint: disable=W0104,W0106
with Diagram('Spark on Hadoop',
             show=not bool(os.environ.get('CI', 0)),
             direction='TB',  # seems to set graphviz rankdir
             filename=os.path.join('images/spark_hadoop'),
             #outformat=['png', 'dot'],
             graph_attr=graph_attr,
             ):

    users = Users("Users - Quants, Devs, DevOps etc.")

    with Cluster("Hadoop cluster on-prem") as hadoop:
        spark = {}
        hdfs = {}
        node_range = range(1, 13, 1)
        for _ in reversed(node_range):
            with Cluster(f"Hadoop node {_}"):
                spark[_] = Spark("Spark")
                hdfs[_] = Hadoop("Hadoop HDFS")
                spark[_] >> hdfs[_]

    # doesn't materialize
    #users >> hadoop
