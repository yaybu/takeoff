from touchdown.core.resource import Resource
from touchdown.core import argument, plan
from touchdown.config import expressions

from .account import Account


class Environment(Resource):

    resource_name = "environment"

    name = argument.String()
    cidr_block = argument.IPNetwork()
    account = argument.Resource(Account)


class BuildWorkspace(plan.Plan):

    name = "takeoff::build-workspace"
    resource = Environment

    def setup(self):
        workspace = self.runner.get_service(
            self.resource.account.workspace,
            self.name
        )
        parent = self.runner.get_service(self.resource.parent, self.name)

        self.keypair = parent.aws.add_keypair(
            name=self.resource.name,
            private_key=workspace.project_config.add_string(
                name="secrets.keypair",
                default=expressions.rsa_private_key(),
                retain_default=True,
            )
        )

        self.vpc = parent.aws.add_vpc(
            name=self.resource.name,
            cidr_block=str(self.resource.cidr_block),
        )

        self.allocations = workspace.project_config.add_ip_allocations(
            name=self.resource.name + ".subnets",
            network=str(self.resource.cidr_block),
        )
