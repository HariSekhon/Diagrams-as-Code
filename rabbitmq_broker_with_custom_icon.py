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

RabbitMQ Broker with custom icon

"""

# based on https://diagrams.mingrammer.com/docs/getting-started/examples

__author__ = 'Hari Sekhon'
__version__ = '0.2'

import os
from urllib.request import urlretrieve

from diagrams import Diagram, Cluster

# ============================================================================ #
# AWS resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/aws
#

from diagrams.aws.database import Aurora

# ============================================================================ #
# Kubernetes resources:
#
#   https://diagrams.mingrammer.com/docs/nodes/k8s
#

from diagrams.k8s.compute import Pod

# ============================================================================ #
#
# Custom - for creating a custom object using a downloaded image
#
#   https://diagrams.mingrammer.com/docs/nodes/custom
#

from diagrams.custom import Custom

# ============================================================================ #

# pylint: disable=C0103
rabbitmq_url = "https://jpadilla.github.io/rabbitmqapp/assets/img/icon.png"
rabbitmq_icon = "rabbitmq.png"

image_dir = 'images'

# NOTE: filename=images/ parameter to Diagram() changes the $PWD so icon path must be local dir,
# but at this point we're still at top level dir so must join to prefix it with the image_dir
# nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
urlretrieve(rabbitmq_url, os.path.join(image_dir, rabbitmq_icon))

# pylint: disable=W0106
with Diagram("RabbitMQ Broker with custom icon",
             show=not bool(os.environ.get('CI', 0)),
             filename=os.path.join(image_dir, 'rabbitmq_broker_with_custom_icon'),
             ):
    with Cluster("Consumers"):
        consumers = [
            Pod("worker"),
            Pod("worker"),
            Pod("worker")]

    rabbitmq = Custom("RabbitMQ", rabbitmq_icon)

    rabbitmq >> consumers >> Aurora("Database")

#os.remove(rabbitmq_icon)
