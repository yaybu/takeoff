from . import zone


class NatGateway(zone.Zone):

    resource_name = "nat_gateway"


class BuildWorkspace(zone.BuildWorkspace):

    resource = NatGateway

    def setup(self):
        super(BuildWorkspace, self).setup()

        workspace = self.runner.get_service(self.resource.environment.account.workspace, self.name)
        acc = self.runner.get_service(self.resource.environment.account, self.name)
        env = self.runner.get_service(self.resource.environment, self.name)

        self.nat_gateways = []
        for subnet in self.subnets:
            self.nat_gateways.append(subnet.add_nat_gateway(
                elastic_ip=acc.aws.add_elastic_ip(
                    name=subnet.name,
                    public_ip=workspace.project_config.add_string(
                        name="{}.{}.elastic_ip".format(env.vpc.name, subnet.name),
                    )
                )
            ))
