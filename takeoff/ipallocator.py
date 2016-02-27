import ipaddress


class IpAllocator(object):

    def __init__(self, network):
        """
        Given an ipaddress.ip_network, manage allocating it into smaller pieces
        """
        self.network = network
        self.allocations = {}
        self.free = {int(network.prefixlen): [self.network]}

    def allocate(self, name, prefixlen):
        print(name, prefixlen)
        if prefixlen < int(self.network.prefixlen):
            raise ValueError("Cannot fit /{} inside /{}".format(prefixlen, self.network.prefixlen))

        for i in range(prefixlen, int(self.network.prefixlen)-1, -1):
            print i
            if self.free.get(i, None):
                selected = self.free[i].pop()
                break
        else:
            raise ValueError("There is not enough space left to allocate a /{}".format(prefixlen))

        while int(selected.prefixlen) < prefixlen:
            selected, leftover = selected.subnets()
            self.free[int(leftover.prefixlen)] = [leftover]

        self.allocations[name] = selected

        return selected
