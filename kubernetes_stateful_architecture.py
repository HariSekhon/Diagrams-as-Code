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

Kubernetes Stateful Architecture

"""

__author__ = 'Hari Sekhon'
__version__ = '0.1'

import os
from diagrams import Diagram, Cluster

# K8s resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#
from diagrams.k8s.compute import Pod, StatefulSet
# from diagrams.k8s.network import Service
from diagrams.k8s.storage import PV, PVC, StorageClass

with Diagram("Kubernetes Stateful Architecture", show=not bool(os.environ.get('CI', 0))):
    with Cluster("App"):
        # Service clutters this diagram
        # svc = Service("Service)")
        sts = StatefulSet("StatefulSet")

        apps = []
        # pylint: disable=W0104
        # count from 3 to 1 to get the apps to come out in the right order top to bottom
        for _ in range(3, 0, -1):
            pod = Pod(f"Pod {_}")
            pvc = PVC(f"Persistent\nVolume Claim {_}")
            pv = PV(f"Persistent Volume {_}")
            #pod - sts - pvc
            #apps.append(svc >> pod >> pvc >> pv)
            apps.append(sts >> pod >> pvc >> pv)

        # pylint: disable=W0106
        apps << StorageClass("Storage Class")
