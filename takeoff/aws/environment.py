from touchdown.core.resource import Resource
from touchdown.core import argument, plan

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
        parent = self.runner.get_service(self.resource.parent, self.name)
        self.keypair = parent.aws.add_keypair(
            name=self.resource.name,
        )

        self.vpc = parent.aws.add_vpc(
            name=self.resource.name,
            cidr_block=str(self.resource.cidr_block),
        )
