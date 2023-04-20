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

Kubernetes Deployment with HPA & Ingress

"""

# based on https://diagrams.mingrammer.com/docs/getting-started/examples

__author__ = 'Hari Sekhon'
__version__ = '0.2'

import os
from diagrams import Diagram

# ============================================================================ #
# Kubernetes resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

graph_attr = {
    "splines": "spline",
}

with Diagram("Kubernetes Deployment HPA Ingress",
             show=not bool(os.environ.get('CI', 0)),
             filename='images/kubernetes_deployment_hpa_ingress',
             #graph_attr=graph_attr,
             ):
    net = Ingress("Ingress\nwww.domain.com") >> Service("Service")
    # pylint: disable=W0106
    net >> [Pod("web1"),
            Pod("web2"),
            Pod("web3")] << ReplicaSet("ReplicaSet") << Deployment("Deployment") << HPA("Horizontal Pod Autoscaler")
