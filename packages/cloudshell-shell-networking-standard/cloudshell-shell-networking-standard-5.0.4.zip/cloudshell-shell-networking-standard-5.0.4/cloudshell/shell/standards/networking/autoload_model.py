#!/usr/bin/python
# -*- coding: utf-8 -*-
import cloudshell.shell.standards.attribute_names as attribute_names
from cloudshell.shell.standards.autoload_generic_models import (
    GenericChassis,
    GenericModule,
    GenericPort,
    GenericPortChannel,
    GenericPowerPort,
    GenericResourceModel,
    GenericSubModule,
)
from cloudshell.shell.standards.core.autoload.resource_model import ResourceAttribute

__all__ = [
    "NetworkingResourceModel",
    "GenericResourceModel",
    "GenericChassis",
    "GenericModule",
    "GenericSubModule",
    "GenericPortChannel",
    "GenericPowerPort",
    "GenericPort",
]


class NetworkingResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ["CS_Switch", "CS_Router", "CS_WirelessController"]
    model_name = ResourceAttribute(
        attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME
    )

    @property
    def entities(self):
        class _NetworkingEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = GenericPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _NetworkingEntities
