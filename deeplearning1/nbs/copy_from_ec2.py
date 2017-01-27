#!/usr/bin/env python
"""
Short description - This module ...

func1: Function to
func2: Function to

:copyright: 2016 DataHoliks
:author: Rajendra Koppula <rkoppula@dataholiks.com>
"""
import argparse
import os
# import subprocess
PEM_KEY = '~/AWS/dh-aws-key.pem'
EC2_USERNAME = 'ubuntu'
EC2_T2_PUBLIC_DNS = 'ec2-35-161-1-194.us-west-2.compute.amazonaws.com'
EC2_P2_PUBLIC_DNS = 'ec2-35-165-195-150.us-west-2.compute.amazonaws.com'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('instance', type=str, help='Specify whether dataholiks t2 or p2 instance')
    parser.add_argument('source', type=str, help='Specify source file on your instance')
    parser.add_argument('destination', type=str, help='Specify destination file on your local computer')

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()  # parse command's arguments

    if args.instance == 't2':
        ec2_public_dns = EC2_T2_PUBLIC_DNS
    elif args.instance == 'p2':
        ec2_public_dns = EC2_P2_PUBLIC_DNS
    else:
        raise('Unknown instance')

    full_source = EC2_USERNAME + '@' + ec2_public_dns + ':' + args.source
    exec_string = 'scp -r -i ' + PEM_KEY + ' ' + full_source + ' ' + args.destination

    # RK: TODO
    # Subprocess is preferred over os.system. But the command failes with file not found error. Likely due to
    # environment variables/aws config in the spawned subprocess. os.sys runs in the parent shell?
    # subprocess.call(exec_string)

    # Execute the command
    os.system(exec_string)


if __name__ == '__main__':
    main()

