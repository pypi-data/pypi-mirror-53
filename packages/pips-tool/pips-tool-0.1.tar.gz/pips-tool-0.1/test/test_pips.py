import subprocess
import sys
import os
import unittest
from pips.pips import Pips
from unittest.mock import patch


class PipsTest(unittest.TestCase):
    def setUp(self) -> None:
        #self.path_to_site_packages = "../venv36/Lib/site-packages/"
        # on MacOS
        self.path_to_site_packages = "../venv36/lib/python3.6/site-packages/"
        self.package = "Jinja2"
        self.sub_dependency = "MarkupSafe"
        self.requirements_file = "requirements.txt"

    def test_install(self):
        """Tests if all packages from the requirements.txt are installed"""
        print(os.getcwd())
        if not os.path.isfile(self.requirements_file):
            f = open(self.requirements_file, "w+")
            f.close()
        with open(self.requirements_file, "w") as f:
            f.writelines(self.package)
        test_args = ["pips", "install"]

        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertTrue(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertTrue(os.path.exists(self.requirements_file))
        self.assertTrue(os.path.exists("requirements.lock"))

    def test_install_package(self):
        """Tests if a single package can be installed and locked"""

        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertTrue(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertTrue(os.path.exists(self.requirements_file))
        self.assertTrue(os.path.exists("requirements.lock"))

        with open("requirements.txt", "r") as f:
            lines = f.readlines()
            package_found = False
            for line in lines:
                if self.package in line:
                    package_found = True
            self.assertTrue(package_found)

        with open("requirements.lock", "r") as f:
            lines = f.readlines()
            package_found = False
            sub_dep_found = False
            for line in lines:
                if self.package in line:
                    package_found = True
                if self.sub_dependency in line:
                    sub_dep_found = True
            self.assertTrue(package_found)
            self.assertTrue(sub_dep_found)

    def test_uninstall_package(self):
        """Tests if a single package can be uninstalled"""

        test_args = ["pips", "install", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        test_args = ["pips", "uninstall", self.package]
        with patch.object(sys, 'argv', test_args):
            Pips()

        self.assertFalse(os.path.exists(self.path_to_site_packages + self.package.lower()))
        self.assertFalse(os.path.exists(self.path_to_site_packages + self.sub_dependency.lower()))

    def tearDown(self) -> None:
        print("teardown")
        process = subprocess.Popen("pip uninstall --yes" + self.package, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        print(out)
        if os.path.exists(self.requirements_file):
            os.remove(self.requirements_file)
        if os.path.exists("requirements.lock"):
            os.remove("requirements.lock")


if __name__ == '__main__':
    unittest.main()
