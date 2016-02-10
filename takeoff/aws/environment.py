from touchdown.core.resource import Resource
from touchdown.core import argument

from .account import Account


class Environment(Resource):

    resource_name = "environment"

    name = argument.String()
    cidr_block = argument.IPNetwork()
    account = argument.Resource(Account)

    def setup(self):
       self.keypair = aws.add_keypair(
           name=self.name,
       )

       self.vpc = aws.add_vpc(
            name=self.name,
            cidr_block=self.cidr_block,
       )
