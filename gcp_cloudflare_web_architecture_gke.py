#!/usr/bin/env python3
#  coding=utf-8
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2023-04-17 06:28:23 +0100 (Mon, 17 Apr 2023)
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

GCP Cloudflare Web Architecture GKE

"""

__author__ = 'Hari Sekhon'
__version__ = '0.4'

import os
from diagrams import Diagram, Cluster, Edge

# ============================================================================ #
# GCP resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/gcp
#

from diagrams.gcp.compute import GKE
from diagrams.gcp.network import FirewallRules, LoadBalancing
from diagrams.gcp.storage import GCS

# ============================================================================ #
# Kubernetes resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#

from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service

# ============================================================================ #
# On-premise / Open Source resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/onprem
#

# from diagrams.onprem.certificates import CertManager, LetsEncrypt
# from diagrams.onprem.ci import Jenkins
# from diagrams.onprem.gitops import ArgoCD
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
# from diagrams.onprem.vcs import Github


# ============================================================================ #
# SaaS:
#
#   https://diagrams.mingrammer.com/docs/nodes/saas
#

from diagrams.saas.cdn import Cloudflare
# from diagrams.saas.chat import Slack

# ============================================================================ #

# https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "splines": "spline",  # rounded arrows, much nicer
}

# pylint: disable=W0104,W0106
with Diagram('GCP Cloudflare Web Architecture GKE',
             show=not bool(os.environ.get('CI', 0)),
             direction='TB',
             filename='images/gcp_cloudflare_web_architecture_gke',
             graph_attr=graph_attr,
             ):

    # letsencrypt = LetsEncrypt("LetsEncrypt Certificate Authority")
    users = Users("Internet Users")
    # github = Github("GitHub")

    with Cluster("Cloudflare"):
        dns = Cloudflare("Cloudflare\nDNS")
        cdn = Cloudflare("Cloudflare\nCDN / WAF")
        users >> Edge(label="DNS queries") >> dns
        users >> Edge(label="HTTPS traffic") >> cdn

    with Cluster("Google Cloud"):
        firewall = FirewallRules("Firewall")
        load_balancer = LoadBalancing("Cloud Load Balancer")
        gcs = GCS("GCS bucket\n(static assets)")
        cdn \
            >> Edge(label="Proxied HTTPS Traffic") \
            >> firewall \
            >> load_balancer
        cdn >> gcs
        # load_balancer - dns

        with Cluster("Kubernetes Cluster"):
            eks = GKE("GKE")

            # with Cluster("ArgoCD"):
            #     argocd = ArgoCD("ArgoCD")

            with Cluster("Ingress"):
                nginx = Nginx("Nginx\nIngress Controller")
                #ingress = Ingress("Kubernetes Ingress")

            with Cluster("WebApp 1"):
                service = Service("WebApp 1 Service")
                nginx >> service
                pods = []
                for _ in range(1, 4, 1):
                    pods.append(service >> Pod(f"Web {_}"))
                #     argocd >> service
                # argocd >> pods

            with Cluster("WebApp 2"):
                service = Service("WebApp 2 Service")
                nginx >> service
                pods = []
                for _ in range(1, 4, 1):
                    pods.append(service >> Pod(f"Web {_}"))
                #     argocd >> service
                # argocd >> pods

            # with Cluster("Cert Manager"):
            #     certmanager = CertManager("Cert Manager")
            #
            # letsencrypt \
            #     >> Edge(label="ACME protocol\ngenerated certificate", style="dashed") \
            #     >> certmanager \
            #     >> Edge(label="SSL cert", style="dashed") \
            #     >> nginx

            # ( load_balancer >> ingress ) - nginx
            load_balancer >> nginx

            # github >> \
            #     Edge(label="GitOps trigger", style="dashed") \
            #     >> argocd \
            #     >> Edge(label="updates", style="dashed") \
            #     >> nginx
