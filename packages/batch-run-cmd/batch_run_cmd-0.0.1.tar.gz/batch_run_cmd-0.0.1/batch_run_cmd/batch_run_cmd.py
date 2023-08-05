#!/usr/bin/env python3
import subprocess
import argparse
import sys
from string import Template

def get_para():
    desc = """
    To run commands line by line, and check each exit status.
    See https://github.com/linzhi2013/batch-run-cmd for more details.
    """

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f', dest='cmd_file', metavar='<file>',
        required=False,
        help="commands in a file.")

    parser.add_argument('-e', dest='continueOnReturnCode', nargs='+',
        metavar='<int>', type=int,
        default=[0], help="continueOnReturnCode [%(default)s]")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    return args


def batch_run_cmd(cmd_file=None, continueOnReturnCode=[0]):
    with open(cmd_file, 'r') as fh:
        for i in fh:
            i = i.strip()
            if not i:
                continue
            run_single_cmd(
                cmd=i,
                continueOnReturnCode=continueOnReturnCode
            )


def run_single_cmd(cmd=None, continueOnReturnCode=[0]):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, check=True, encoding='utf8')
    except subprocess.CalledProcessError as e:
        print('{0}\nGot returncode {1}'.format(cmd, e.returncode), file=sys.stderr)
        if e.returncode in continueOnReturnCode:
            pass
        else:
            raise e
    else:
        print(cmd, flush=True, file=sys.stdout)
        print(result.stdout, flush=True, file=sys.stdout)
        if result.returncode not in continueOnReturnCode:
            print('Got returncode {}'.format(result.returncode), file=sys.stderr)
            sys.exit(result.returncode)


def main():
    args = get_para()

    batch_run_cmd(
        cmd_file=args.cmd_file,
        continueOnReturnCode=args.continueOnReturnCode
    )


if __name__ == '__main__':
    main()
