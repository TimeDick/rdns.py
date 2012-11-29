import os, sys
import unittest

sys.path.insert(0, sys.path[0] + "/..")
import rdns

class TestRDNS(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_webhostinginfo(self):
        ip, count, hosts = rdns.wwhi_rip("67.15.149.209")()
        self.assertEqual("67.15.149.209", ip, "IP Not equal") #current webhosting.info ip address
        self.assertEqual(True, hosts.has_key("WEBHOSTING.INFO"), "hosts key not exists")
        self.assertEqual(True, hosts["WEBHOSTING.INFO"] == "67.15.149.209", "Ip not equal")

    def test_localhost(self):
        ip, count, hosts = rdns.wwhi_rip("127.0.0.1")()
        self.assertEqual("127.0.0.1", ip, "IP Not equal")
        self.assertEqual(0, len(hosts), "hosts not empty")
