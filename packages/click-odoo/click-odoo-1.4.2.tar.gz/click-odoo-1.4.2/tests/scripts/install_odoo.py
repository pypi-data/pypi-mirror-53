#!/usr/bin/env python
import os
import subprocess
import sys

odoo_branch = sys.argv[1]
odoo_dir = sys.argv[2]


def odoo_installed():
    try:
        import odoo  # noqa

        return True
    except ImportError:
        # odoo < 10
        try:
            import openerp  # noqa

            return True
        except ImportError:
            # odoo not installed
            return False


def odoo_cloned():
    return os.path.isdir(os.path.join(odoo_dir, ".git"))


def clone_odoo():
    subprocess.check_call(
        [
            "git",
            "clone",
            "--depth=1",
            "-b",
            odoo_branch,
            "https://github.com/odoo/odoo",
            odoo_dir,
        ]
    )


def install_odoo():
    # Odoo not compatible with recent pyyaml due to load() now being safe by default
    # XXX an alternative is to pip install -r requirements.txt with
    # XXX the correct one for each Odoo version but this is slower as
    # XXX many wheels more need to be built because Odoo's requirements.txt
    # XXX pin old library versions.
    subprocess.check_call(["pip", "install", "pyyaml<4"])
    subprocess.check_call(["pip", "install", "-e", odoo_dir])


def main():
    if not odoo_installed():
        if not odoo_cloned():
            clone_odoo()
        install_odoo()


if __name__ == "__main__":
    main()
