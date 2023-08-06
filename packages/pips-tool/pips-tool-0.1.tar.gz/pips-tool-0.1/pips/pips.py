import argparse
import os
import sys
from unittest.mock import patch

import pipdeptree
from pip._internal import main as pipmain
from pip._internal.utils.misc import get_installed_distributions


class Pips:
    def __init__(self):
        parser = argparse.ArgumentParser(
            usage='''pips <command> [<args>]
        ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def install(self):
        parser = self.create_subparser()
        if sys.argv[2:]:

            args = parser.parse_args(sys.argv[2:])
            print('Running pips install, package=%s' % args.package)
            package = args.package
            pipmain(['install', package])
            self.add_requirements_to_req_txt_file(package)
            self.lock_dependencies()
        else:
            print('Running pips install')
            # install requirements from requirements.lock
            if os.path.isfile("requirements.lock"):
                pipmain(['install', '-r', 'requirements.lock'])
            elif os.path.isfile("requirements.txt"):
                pipmain(['install', '-r', 'requirements.txt'])
                self.lock_dependencies()
            else:
                print('No requirements files found')
                parser.print_help()
                exit(1)


    def create_subparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('package')
        return parser

    def lock_dependencies(self):
        with open("requirements.lock", "w") as f:
            for dist in get_installed_distributions():
                req = dist.as_requirement()
                f.write(str(req) + "\n")

    def add_requirements_to_req_txt_file(self, package):
        if not os.path.isfile("requirements.txt"):
            f = open("requirements.txt", "w+")
            f.close()
        with open("requirements.txt", "w") as f:
            f.writelines(package)


    def get_package_dependencies(self, package_name):
        test_args = ["pipdeptree", "--package", package_name]
        with patch.object(sys, 'argv', test_args):
            args = pipdeptree._get_args()
            pkgs = get_installed_distributions(local_only=args.local_only,
                                               user_only=args.user_only)

            dist_index = pipdeptree.build_dist_index(pkgs)
            tree = pipdeptree.construct_tree(dist_index)
            dep_names = []
            for entry in tree:
                if entry.key == package_name.lower():
                    dependencies = tree[entry]
                    for dep in dependencies:
                        dep_names.append(dep.key)
                    print(dep_names)
        return dep_names

    def uninstall(self):
        parser = self.create_subparser()
        if sys.argv[2:]:
            args = parser.parse_args(sys.argv[2:])
            package = args.package
            print('Running pips install, package=%s' % package)
            deps = self.get_package_dependencies(package)
            for dep in deps:
                pipmain(['uninstall', "--yes", dep])
            pipmain(['uninstall', "--yes", package])
            # remove_requirements_from_req_txt_file(package)


