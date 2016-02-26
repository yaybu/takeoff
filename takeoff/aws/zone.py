from touchdown.core.resource import Resource
from touchdown.core import argument, plan

from .environment import Environment


class Zone(Resource):

    name = argument.String()

    cidr_block = argument.IPNetwork()

    """ Is this zone on the public internet? """
    public = argument.Boolean(default=False)

    """ The availability zones to create this zone in """
    availability_zones = argument.List(
        argument.String(min=1, max=1),
        min=2,
        max=2,
        default=["a", "b"],
    )

    environment = argument.Resource(Environment)


class BuildWorkspace(plan.Plan):

    name = "takeoff::build-workspace"

    def setup(self):
        parent = self.runner.get_service(self.resource.parent, self.name)

        self.security_group = parent.vpc.add_security_group(
            name=self.resource.name,
        )

        subnet_ranges = self.resource.cidr_block.subnet(self.resource.cidr_block.prefixlen + 1)

        self.subnets = []
        for az, cidr_block in zip(self.resource.availability_zones, subnet_ranges):
            name = "-".join((self.resource.name, az))

            self.subnets.append(parent.vpc.add_subnet(
                name=name,
                cidr_block=str(cidr_block),
                network_acl=self.setup_network_acls(parent.vpc, name),
                route_table=self.setup_route_table(parent.vpc, name),
            ))

    def setup_network_acls(self, vpc, name):
        return vpc.add_network_acl(
            name=name,
        )

    def setup_route_table(self, vpc, name):
        routes = []

        #if self.public:
        #    routes.append({
        #        "cidr": "0.0.0.0/0",
        #        "internet_gateway": self.environment.internet_gateway,
        #    })

        return vpc.add_route_table(
            name=name,
            routes=routes,
        )
