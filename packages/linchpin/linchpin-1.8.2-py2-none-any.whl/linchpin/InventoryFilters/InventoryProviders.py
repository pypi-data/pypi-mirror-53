"""
Inventory Providers List
"""
from __future__ import absolute_import
from linchpin.exceptions import LinchpinError

from .AWSInventory import AWSInventory
from .BeakerInventory import BeakerInventory
from .DuffyInventory import DuffyInventory
from .DummyInventory import DummyInventory
from .GCloudInventory import GCloudInventory
from .LibvirtInventory import LibvirtInventory
from .OpenstackInventory import OpenstackInventory
from .OvirtInventory import OvirtInventory
from .VMwareInventory import VMwareInventory
from .DockerInventory import DockerInventory
from .AzureInventory import AzureInventory
from .OpenshiftInventory import OpenshiftInventory

from .JSONInventoryFormatter import JSONInventoryFormatter
from .CFGInventoryFormatter import CFGInventoryFormatter

filter_classes = {
    "azure_vm": AzureInventory,
    "aws_ec2_res": AWSInventory,
    "beaker_res": BeakerInventory,
    "duffy_res": DuffyInventory,
    "dummy_res": DummyInventory,
    "nummy_res": DummyInventory,
    "gcloud_gce_res": GCloudInventory,
    "libvirt_res": LibvirtInventory,
    "os_server_res": OpenstackInventory,
    "ovirt_vms_res": OvirtInventory,
    "vmware_guest_res": VMwareInventory,
    "docker_container_res": DockerInventory,
    "docker_image_res": DockerInventory,
    "openshift_res": OpenshiftInventory
}

formatter_classes = {
    "cfg": CFGInventoryFormatter,
    "ini": CFGInventoryFormatter,
    "json": JSONInventoryFormatter
}


def get_driver(provider):

    if provider not in filter_classes:
        raise LinchpinError("Key {0} not found in"
                            " inventory provider dict".format(provider))

    return filter_classes[provider]


def get_all_drivers():
    return filter_classes


def get_inv_formatter(inv_type):
    if inv_type not in formatter_classes:
        raise LinchpinError("Key {0} not found in"
                            " formatters".format(inv_type))
    return formatter_classes[inv_type]


def get_all_inv_formatters():
    return formatter_classes
