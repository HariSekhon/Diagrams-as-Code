#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-21 00:32:11 +0100 (Fri, 21 Apr 2023)
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

Classic Web Architecture

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from urllib.request import urlretrieve
from diagrams import Diagram, Cluster  # , Edge

# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#

from diagrams.onprem.client import Users
# from diagrams.onprem.compute import Server
from diagrams.onprem.database import Cassandra
from diagrams.onprem.inmemory import Memcached  # , Redis
from diagrams.onprem.network import Apache, Glassfish

# ============================================================================ #
# Generic - Datacentre, Operating Systems, Virtualization, Mobile Devices:
#
#   https://diagrams.mingrammer.com/docs/nodes/generic
#

from diagrams.generic.place import Datacenter
# from diagrams.generic.os import LinuxGeneral

# ============================================================================ #
#
# Programming - flowcharts, programming languages and frameworks
#
#   https://diagrams.mingrammer.com/docs/nodes/programming
#

from diagrams.programming.language import Java

# ============================================================================ #
#
# Custom - for creating a custom object using a downloaded image
#
#   https://diagrams.mingrammer.com/docs/nodes/custom
#

from diagrams.custom import Custom

# ============================================================================ #
# ============================================================================ #

# pylint: disable=C0103

dns_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsXGy2J1B7jR56GNfbAhNXC0Nw9bokO9gHqw&usqp=CAU"
dns_icon = "dns.png"

f5_url = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/F5_Networks_logo.svg/800px-F5_Networks_logo.svg.png"
f5_icon = "f5.png"

image_dir = 'images'

# NOTE: filename=images/ parameter to Diagram() changes the $PWD so icon path must be local dir,
# but at this point we're still at top level dir so must join to prefix it with the image_dir
urlretrieve(f5_url, os.path.join(image_dir, f5_icon))
urlretrieve(dns_url, os.path.join(image_dir, dns_icon))

graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
}

# pylint: disable=W0104,W0106
with Diagram('Classic Web Architecture',
             show=not bool(os.environ.get('CI', 0)),
             direction='LR',
             filename='images/classic_web_architecture',  # override the default filename, without the extension
             graph_attr=graph_attr,
             ):

    gslb = Custom("DNS GSLB\nGlobal Server Load Balancing\nHealth Check Datacenters", dns_icon)

    for n in range(1, 3, 1):
        with Cluster(f"Datacenter {n}") as dc:
            Datacenter(f"DC{n}")
            lb = Custom("F5 Big-IP 8900\nLoad Balancer", f5_icon)
            with Cluster("Cassandra") as cassandra:
                cassandra_cluster = []
                for i in range(2):
                    cassandra_cluster.append(Cassandra("Cassandra node"))
                for i, node in enumerate(cassandra_cluster):
                    j = i + 1
                    if j >= len(cassandra_cluster):
                        j = 0
                    cassandra_cluster[i] >> cassandra_cluster[j]

            for _ in range(2):
                with Cluster(f"Server {_}"):
                    # Server("Server")
                    # LinuxGeneral("Linux")
                    httpd = Apache("Apache httpd")
                    glassfish = Glassfish("Glassfish")
                    java = Java("Java")
                    # redis = Redis("Redis")
                    memcached = Memcached("Memcached")
                    lb >> httpd >> glassfish
                    glassfish - java
                    java >> memcached
                    java >> cassandra_cluster
        gslb >> lb

    Users("Internet Users") \
        >> gslb
