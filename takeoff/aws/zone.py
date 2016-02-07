from touchdown.core import argument

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

    def setup(self):
        self.security_group = vpc.add_security_group(
            name=self.name,
        )

        subnet_ranges = self.cidr_block.subnet(self.cidr_block.prefixlen + 1)

        self.subnets = []
        for az, cidr_block in zip(self.availability_zones, subnet_ranges):
            name = "-".join(self.name, az)

            self.subnets.append(vpc.add_subnet(
                name=name,
                cidr_block=cidr_block,
                network_acl=self.setup_network_acls(name),
                route_table=self.setup_route_table(name),
            ))

        def setup_network_acls(self, name):
            return self.environment.vpc.add_network_acl(
                name=name,
            )

        def setup_route_table(self, name):
            routes = []

            if self.public:
                routes.append({
                    "cidr": "0.0.0.0/0",
                    "internet_gateway": self.environment.internet_gateway,
                })

            return self.environment.vpc.add_route_table(
                name=name,
                routes=routes,
            )
