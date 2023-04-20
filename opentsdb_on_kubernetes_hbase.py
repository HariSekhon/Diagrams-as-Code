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

OpenTSDB on Kubernetes with HBase

"""

__author__ = 'Hari Sekhon'
__version__ = '0.2'

import os
from urllib.request import urlretrieve
from diagrams import Diagram, Cluster  # , Edge

# ============================================================================ #
# Kubernetes resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#

# from diagrams.k8s.compute import StatefulSet
from diagrams.k8s.network import Service

# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Hadoop
# from diagrams.onprem.compute import Server
from diagrams.onprem.database import HBase
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Apache, Nginx

# ============================================================================ #
#
# Custom - for creating a custom object using a downloaded image
#
#   https://diagrams.mingrammer.com/docs/nodes/custom
#

from diagrams.custom import Custom

# pylint: disable=C0103
opentsdb_url = "https://avatars.githubusercontent.com/u/2086220?s=200&v=4"
opentsdb_icon = "opentsdb.png"

image_dir = 'images'

# NOTE: filename=images/ parameter to Diagram() changes the $PWD so icon path must be local dir,
# but at this point we're still at top level dir so must join to prefix it with the image_dir
urlretrieve(opentsdb_url, os.path.join(image_dir, opentsdb_icon))

# ============================================================================ #

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
    # "rotation": "90",
    "landscape": "false",
}

# pylint: disable=W0104,W0106
with Diagram('OpenTSDB on Kubernetes and HBase',
             show=not bool(os.environ.get('CI', 0)),
             direction='TB',  # seems to set graphviz rankdir
             filename=os.path.join(image_dir, 'opentsdb_kubernetes_hbase'),
             graph_attr=graph_attr,
             ):

    users = Users("Users - Quants, Devs, DevOps etc.")
    tcollectors = Custom("TCollector agents metrics", opentsdb_icon)

    with Cluster("Kubernetes on-prem") as k8s:

        grafana_ingress = Nginx("Nginx Ingress Grafana")

        opentsdb_ingress = Nginx("Nginx Ingress OpenTSDB")
        opentsdb_service = Service("OpenTSDB service")

        tcollectors \
            >> opentsdb_ingress \
            >> opentsdb_service

        # with Cluster("Grafana"):
        grafana_service = Service("Grafana service")
        grafana = {}
        httpd = {}
        for _ in range(1, 3, 1):
            with Cluster(f"Grafana pod {_}"):
                httpd[_] = Apache("Apache httpd\nkerberos proxy")
                grafana[_] = Grafana("Grafana")
                grafana_service \
                    >> httpd[_] \
                    >> grafana[_] \
                    >> opentsdb_service

        users \
            >> grafana_ingress \
            >> grafana_service

        opentsdb = {}
        opentsdb_range = range(1, 16, 1)
        # crude instead of algo positioning but quick
        ordering = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1 , 2]
        ordered_opentsdb_range = [opentsdb_range[ordering.index(i)] for i in opentsdb_range]
        for _ in ordered_opentsdb_range:
            opentsdb[_] = Custom(f"OpenTSDB pod {_}", opentsdb_icon)
            opentsdb_service >> opentsdb[_]

    with Cluster("Hadoop cluster on-prem") as hadoop:
        hbase = {}
        hdfs = {}
        node_range = range(1, 13, 1)
        # crude instead of algo positioning but quick
        ordering = [6, 9, 3, 12, 2, 10, 5, 7, 8, 4, 11, 1]
        ordered_node_range = [node_range[ordering.index(i)] for i in node_range]
        for _ in ordered_node_range:
            with Cluster(f"Hadoop node {_}"):
                    hbase[_] = HBase("HBase")
                    hdfs[_] = Hadoop("Hadoop HDFS")
                    hbase[_] >> hdfs[_]
                    for i in opentsdb_range:
                        hbase[_] << opentsdb[i]
    print(dir(hadoop))
