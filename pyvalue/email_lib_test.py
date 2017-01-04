# The library for sending the notification email
# Author: Liang Tang
# License: BSD

import unittest

import email_lib


class EmailLibTest(unittest.TestCase):

    @staticmethod
    def test_send():
        email_lib.send("Test email from python", "Test email", "pyvalue", "tangl99@gmail.com")

if __name__ == '__main__':
    unittest.main()
