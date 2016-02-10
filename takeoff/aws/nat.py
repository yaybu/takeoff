from . import zone


class NatGateway(zone.Zone):

    resource_name = "nat_gateway"


class BuildWorkspace(zone.BuildWorkspace):

    resource = NatGateway
