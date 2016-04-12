import unittest
import ipaddress


class TestIpAllocator(unittest.TestCase):

    def setUp(self):
        self.ipa = IpAllocator(ipaddress.ip_network(u'10.30.0.0/20'))

    def test_too_big(self):
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet1', 0)
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet1', 19)

    def test_allocate_everything_once(self):
        assert self.ipa.allocate('subnet1', 20).with_prefixlen == '10.30.0.0/20'
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet2', 20)

    def test_allocate_2_21(self):
        assert self.ipa.allocate('subnet1', 21).with_prefixlen == '10.30.0.0/21'
        assert self.ipa.allocate('subnet2', 21).with_prefixlen == '10.30.8.0/21'
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet3', 21)

    def test_allocate_1_21_2_22(self):
        assert self.ipa.allocate('subnet1', 21).with_prefixlen == '10.30.0.0/21'
        assert self.ipa.allocate('subnet2', 22).with_prefixlen == '10.30.8.0/22'
        assert self.ipa.allocate('subnet3', 22).with_prefixlen == '10.30.12.0/22'
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet4', 19)

    def test_allocate_2_22_1_21(self):
        assert self.ipa.allocate('subnet1', 22).with_prefixlen == '10.30.0.0/22'
        assert self.ipa.allocate('subnet2', 22).with_prefixlen == '10.30.4.0/22'
        assert self.ipa.allocate('subnet3', 21).with_prefixlen == '10.30.8.0/21'
        self.assertRaises(ValueError, self.ipa.allocate, 'subnet4', 19)
