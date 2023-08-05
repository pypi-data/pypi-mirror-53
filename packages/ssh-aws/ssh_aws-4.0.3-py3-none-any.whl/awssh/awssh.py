#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import botocore.exceptions as exceptions
from os import path, system, getenv
import configparser
from pprint import pprint
import argparse
import itertools
from collections import deque
import time
import six

VERSION = "4.0.3"


def connect(instance, args):
    """

    :param instance:
    :param args:
    :return:
    """
    details = get_details(instance)
    print('\nConnecting to: {name}'.format(**details))
    if args.verbose:
        pprint(details)

    if args.console_output:
        print('\n================== console output start ==================')
        print(instance.console_output().get('Output', '').replace('\\n', '\n'))
        print('=================== console output end ===================\n')

    users = deque(args.users)
    # return code 65280 is 'Permission Denied'
    while _connect(users.popleft(), instance, args) == 65280 and len(users):
        pass


def _connect(user, instance, args):
    """

    :param user:
    :param instance:
    :param args:
    :return:
    """
    config = {
        'key_path': get_key_path(args, instance),
        'tunnel': get_tunnel(args),
        'host': "{}@{}".format(user, instance.public_ip_address),
        'timeout': args.timeout
    }
    command = 'ssh -i {key_path} {tunnel} {host} -o ConnectTimeout={timeout}'.format(**config)

    if args.command:
        # print('\nForce pseudo-terminal allocation.')
        command = "{} -t '{}'".format(command, args.command)

    print('\nTrying with user "{}".\nCommand: {}'.format(user, command))
    return system(command)


def jump_connect(ssh_instance, jump_server, args):
    """

    :param ssh_instance:
    :param jump_server:
    :param args:
    :return:
    """
    details_ssh_instance = get_details(ssh_instance)
    details_jump_server = get_details(jump_server)
    print('\nConnecting to {} via {}:'.format(details_ssh_instance.get('name'), details_jump_server.get('name')))
    if args.verbose:
        pprint(details_ssh_instance)

    if args.console_output:
        print('\n================== console output start ==================')
        print(ssh_instance.console_output().get('Output', '').replace('\\n', '\n'))
        print('=================== console output end ===================\n')

    users = deque(args.users)
    # return code 65280 is 'Permission Denied'
    while _jump_connect(users.popleft(), ssh_instance, jump_server, args) == 65280 and len(users):
        time.sleep(1)
    return True


def _jump_connect(user, ssh_instance, jump_server, args):
    """

    :param user:
    :param ssh_instance:
    :param jump_server:
    :param args:
    :return:
    """
    command_tuple = {
        'key_path': get_key_path(args, jump_server),
        'tunnel': get_tunnel(args),
        'jump_host': "{}@{}".format(user, jump_server.public_ip_address),
        'target_host': "{}@{}".format(user, ssh_instance.private_ip_address),
        'timeout': args.timeout
    }

    command = 'ssh-add {key_path}; ' \
              'ssh -A {tunnel} -o ConnectTimeout={timeout} ' \
              '-J {jump_host} {target_host}'.format(**command_tuple)

    if args.command:
        # print('\nForce pseudo-terminal allocation.')
        command = "{} -t '{}'".format(command, args.command)

    print('\nTrying with user "{}".\nCommand: {}'.format(user, command))
    return system(command)


def get_tunnel(args):
    """

    :param args:
    :return:
    """
    if not args.remote_host:
        return ''

    url = args.remote_host.split(':')
    if len(url) == 2:
        params = {'local_port': args.local_port or url[1], 'remote_host': url[0], 'remote_port': url[1]}
    elif len(url) == 3:
        params = {'local_port': url[0], 'remote_host': url[1], 'remote_port': url[2]}
    else:
        if not args.local_port:
            args.local_port = args.remote_port
        params = args.__dict__
    return "-L '{local_port}:{remote_host}:{remote_port}'".format(**params)


def get_details(instance):
    """

    :param instance:
    :return:
    """
    return {
        'id': instance.id,
        'name': get_name(instance),
        'type': instance.instance_type,
        'private_ip_address': str(instance.private_ip_address),
        'public_ip_address': str(instance.public_ip_address),
        'availability_zone': instance.placement.get('AvailabilityZone'),
        'security_groups': instance.security_groups,
        'state': instance.state.get('Name'),
        'launch time': instance.launch_time.isoformat(),
        'block devices': get_device_mappings(instance),
        'key_name': instance.key_name.replace(" ", "")
    }


def get_key_path(args, instance):
    """

    :param args:
    :param instance:
    :return:
    """
    if args.key_path:
        return args.key_path
    else:
        directory = path.expanduser(args.keys)
        return path.join(directory, instance.key_name.replace(" ", "") + '.pem')


def get_device_mappings(instance):
    return flatten([device.values() for device in instance.block_device_mappings])


def flatten(array):
    list(itertools.chain.from_iterable(array))


def get_name(instance):
    """

    :param instance:
    :return:
    """
    name = [tag for tag in instance.tags if tag['Key'] == 'Name']
    if not name or 'Value' not in name[0]:
        return 'not-named'
    return name[0].get('Value')


def get_instances(args):
    """

    :param args:
    :return:
    """
    # AWS_ACCESS_KEY_ID - Specifies an AWS access key associated with an IAM user or role.
    # AWS_SECRET_ACCESS_KEY - Specifies the secret key associated with the access key.
    #                         This is essentially the "password" for the access key.
    # AWS_SESSION_TOKEN – Specifies the session token value that is required if you are using temporary security
    #                     credentials. For more information, see the Output section of the assume-role command in
    #                     the AWS CLI Command Reference.
    # AWS_DEFAULT_REGION – Specifies the AWS Region to send the request to.
    # AWS_DEFAULT_OUTPUT – Specifies the output format to use.
    # AWS_DEFAULT_PROFILE – Specifies the name of the CLI profile with the credentials and options to use.
    #                       This can be the name of a profile stored in a credentials or config file, or the value
    #                       default to use the default profile. If you specify this environment variable,
    #                       it overrides the behavior of using the profile named [default] in the configuration file.
    # AWS_CA_BUNDLE – Specifies the path to a certificate bundle to use for HTTPS certificate validation.
    # AWS_SHARED_CREDENTIALS_FILE – Specifies the location of the file that the AWS CLI uses to store access keys
    #                               (the default is ~/.aws/credentials).
    # AWS_CONFIG_FILE - Specifies the location of the file that the AWS CLI uses to store configuration profiles
    #                   (the default is ~/.aws/config).
    #

    # The "env" values (e.g. `export AWS_DEFAULT_REGION='us-east-2'`) are read by boto3.resource('ec2')
    # except for AWS_DEFAULT_PROFILE, which needs to be read by the utility:
    aws_default_profile = getenv('AWS_DEFAULT_PROFILE')

    if args.profile:
        boto3.setup_default_session(profile_name=args.profile)
    elif aws_default_profile:
        boto3.setup_default_session(profile_name=aws_default_profile)

    # If user uses MFA:
    if args.token_code and args.serial_number:
        client = boto3.client('sts')
        sts_response = client.get_session_token(SerialNumber=args.serial_number, TokenCode=args.token_code)
        if args.verbose:
            print('\nMFA:')
            pprint(sts_response)
            print('\n')

        sts_access_key_id = sts_response['Credentials']['AccessKeyId']
        sts_secret_access_key = sts_response['Credentials']['SecretAccessKey']
        sts_session_token = sts_response['Credentials']['SessionToken']

        # The AWS shared credentials file has a default location of ~/.aws/credentials.
        # However, the user may have changed the location of the shared credentials file
        # by setting the AWS_SHARED_CREDENTIALS_FILE environment variable.
        aws_shared_credentials_file = getenv('AWS_SHARED_CREDENTIALS_FILE')

        config = configparser.ConfigParser()
        # MFA profile section
        config['mfa'] = {'aws_access_key_id': sts_access_key_id,
                         'aws_secret_access_key': sts_secret_access_key,
                         'aws_session_token': sts_session_token,
                         }

        # Save user MFA credentials under his profiles' file [mfa] section:
        if aws_shared_credentials_file:
            config.read(aws_shared_credentials_file)
        else:
            aws_shared_credentials_file = config.read(getenv('HOME') + '/.aws/credentials')[0]

        with open(aws_shared_credentials_file, 'w') as configfile:
            config.write(configfile)

        config.set('mfa', 'aws_access_key_id', sts_access_key_id)
        config.set('mfa', 'aws_secret_access_key', sts_secret_access_key)
        config.set('mfa', 'aws_session_token', sts_session_token)

        if args.region == 'default':  # default='default' was set by parser if none given
            ec2 = boto3.resource('ec2', aws_access_key_id=sts_access_key_id,
                                 aws_secret_access_key=sts_secret_access_key, aws_session_token=sts_session_token)
        else:
            ec2 = boto3.resource('ec2', region_name=args.region, aws_access_key_id=sts_access_key_id,
                                 aws_secret_access_key=sts_secret_access_key, aws_session_token=sts_session_token)
    else:

        if args.region == 'default':  # default='default' was set by parser if none given
            ec2 = boto3.resource('ec2')  # uses value found in AWS_DEFAULT_REGION or ~/.aws/config file
        else:
            ec2 = boto3.resource('ec2', region_name=args.region)

    filters = [
        {'Name': 'tag:Name', 'Values': ['*{filter}*'.format(**args.__dict__)]},
        {'Name': 'instance-state-name', 'Values': ['running']},

    ]
    # Filter out Windows and then remove these instances.
    filter_windows = [
        {'Name': 'tag:Name', 'Values': ['*{filter}*'.format(**args.__dict__)]},
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'platform', 'Values': ['windows']},
    ]

    all_platform_instances = list(ec2.instances.filter(Filters=filters))
    windows_platform_instances = list(ec2.instances.filter(Filters=filter_windows))

    for windows_instance in windows_platform_instances:
        all_platform_instances.remove(windows_instance)

    print('Querying AWS for EC2 instances in {region} region...\n'.format(**args.__dict__))

    # return sorted(ec2.instances.filter(Filters=filters), key=get_name)
    return sorted(all_platform_instances, key=get_name)


def main():
    """

    :return:
    """
    parser = create_parser()
    args = parser.parse_args()

    # MFA needs these two (mutually inclusive) arguments
    if args.serial_number or args.token_code:
        if not args.serial_number or not args.token_code:
            parser.error("MFA: --serial-number requires --token-code and vice versa.")

    if args.version:
        print(VERSION)
        exit(0)

    try:
        instances = get_instances(args)
    except(exceptions.EndpointConnectionError, ValueError):
        print('"{}" is an invalid Region.'.format(args.region))
        exit(0)
    except exceptions.ProfileNotFound:
        print('The config profile "{}" could not be found.\n'
              'To properly configure your AWS Profiles visit:\n'
              'https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html'.format(args.profile))
        exit(0)
    except exceptions.NoCredentialsError:
        print('Unable to locate your AWS credentials file.\n'
              'To properly configure your AWS Credentials, run `aws configure`:\n'
              'https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration')
        exit(0)
    except exceptions.ClientError:
        print('An error occurred (UnauthorizedOperation).\n'
              'You are not authorized to perform this operation.\n'
              'Contact your AWS Administrator or enable MFA in your account.')
        exit(0)

    except exceptions.ParamValidationError:
        print('Parameter validation failed: \n'
              'Invalid length for parameter TokenCode.')
        exit(0)

    display_instances(instances)

    if not instances:
        print('No running instances found.\n')
        exit(1)

    if len(instances) == 1:
        if instances[0].public_ip_address:
            print('Found one running instance and connecting to it...\n')
            connect(instances[0], args)
        else:
            print("The instance found has no public IP address.\n")
    else:
        select_instance(args, instances, parser)


def display_instances(instances):
    """

    :param instances:
    :return:
    """
    table_col_names = ['Name', 'Instance ID', 'Public IP',
                       'Private IP', 'Zone', 'Key Name']
    print("     {:<30}{:<21}{:<17}{:<17}{:<14}{}".format(*table_col_names))

    details_fmt = "{:2} - {name:<30}{id:<21}{public_ip_address:<17}" \
                  "{private_ip_address:<17}{availability_zone:<14}{key_name}"

    for i, instance in enumerate(instances, 1):
        print(details_fmt.format(i, **get_details(instance)))
    print('')


def select_instance(args, instances, parser):
    """

    :param args:
    :param instances:
    :param parser:
    :return:
    """

    connection = False
    try:
        server_selection = [int(x) for x in six.moves.input("Enter server number: ").split()]  # User selection

        if len(server_selection) == 1:
            server_selection[0] = server_selection[0] - 1  # server selection option starts with 1, not 0
            if instances[server_selection[0]].public_ip_address is None:
                for instance in instances:
                    if instance.key_name == instances[server_selection[0]].key_name:
                        if instance.public_ip_address is not None:
                            # ssh_instance, jump_server, args
                            if jump_connect(instances[server_selection[0]], instance, args):
                                connection = True
                                break

                if connection:
                    exit(0)
                else:
                    print("No jump servers with the same 'Key Name' were found.\n"
                          "You can input two instances to jump from <a> to <b>.\n"
                          "e.g.:\n"
                          "\tEnter server number: {} {}\n".format((server_selection[0] + 5),
                                                                  server_selection[0]))
            else:
                connect(instances[server_selection[0]], args)
        elif len(server_selection) == 2:
            # server_selection[0] -- jump server
            # server_selection[1] -- target server
            server_selection[0] = server_selection[0] - 1  # server selection options start with 1, not 0
            server_selection[1] = server_selection[1] - 1  # server selection options start with 1, not 0
            if instances[server_selection[0]].public_ip_address is None:
                print("The provided jump server has no public IP address.\n"
                      "You can input two instances to jump from a to b.\n"
                      "However, the jump server needs to be reachable.\n"
                      "e.g.:\n"
                      "\tEnter server number: {} {}\n".format((server_selection[0] + 5), server_selection[0]))
                exit(0)
            else:
                jump_connect(instances[server_selection[1]], instances[server_selection[0]], args)
        else:
            print('Invalid number of instances.\n')
            exit(0)

    except (ValueError, IndexError):
        print('Invalid instance.\n')

    except (EOFError, KeyboardInterrupt, SyntaxError):
        exit(0)


def create_parser():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description="""
    SSH into AWS instances. "awssh --profile prod-acc-2 --users fduran --region us-east-2 instance-name". The default 
    user list is centos, ubuntu, and ec2-user. "awssh --profile prod-acc-2" will attempt ssh with default users. Due to 
    the nature of nargs, "awssh --users user1 user2 instance-name" will not be parsed properly; instead try 
    "awssh instance-name --users user1 user2". If available, a "JumpHost" will be automatically chosen when the 
    instance selected has no external IP. You can also explicitly direct the JumpHost by providing two selections from 
    the list, i.e. Enter server number: <jump> <target>). MFA: when providing the --serial-number and --token-code
    options, awssh creates a profile [mfa] in your AWS credentials file (~/.aws/credentials or 
    AWS_SHARED_CREDENTIALS_FILE) with your MFA credentials. You can continue to call awssh --profile mfa for access 
    until your credentials expire.
    """)

    parser.add_argument('filter', nargs='?', default='*', help='Optional instance name or key word as a filter. '
                                                               'If only one instance is found, it will connect to it '
                                                               'directly.')
    parser.add_argument('--users', nargs='+', help='Users to try (centos, ubuntu, and ec2-user are defaults).',
                        default=['centos', 'ubuntu', 'ec2-user'])
    parser.add_argument('--profile', help='Use a specific profile from your credentials file.')
    parser.add_argument('--region', help='AWS region (User default if none is provided).', default='default')
    parser.add_argument('-i', '--key-path', help='Specific key path, overrides, --keys')
    parser.add_argument('-c', '--command', help='Translates to ssh -t <COMMAND>')
    parser.add_argument('-r', '--remote-host',
                        help='Open a tunnel. '
                             'Equivalent to ssh -L <local-port>:<remote-host>:<remote-port> '
                             '<selected-aws-host>')
    parser.add_argument('-p', '--remote-port', help='Port to use on the remote host (default is 5432).', default=5432)
    parser.add_argument('-l', '--local-port',
                        help='Port to use on the local host. Get overwritten by remote port if not defined.')
    parser.add_argument('--keys', help='Directory of the private keys (~/.ssh by default).', default='~/.ssh/')
    parser.add_argument('--timeout', help='SSH connection timeout.', default='5')
    parser.add_argument('--console-output', '-o', help='Display the instance console out before logging in.',
                        action='store_true')
    parser.add_argument('--version', '-v', help='Returns awssh\'s version.', action='store_true')
    parser.add_argument('--verbose', '-V', help='Verbose, prints instance details.', action='store_true')

    mfa_group = parser.add_argument_group(title='MFA', description='If MFA is required, provide both arguments:')
    mfa_group.add_argument('--serial-number', help='The identification number of the MFA device that is associated '
                                                   'with the IAM user. Specify this value if the IAM user has a policy '
                                                   'that requires MFA authentication. You can find the device for an '
                                                   'IAM user viewing the user\'s security credentials.')
    mfa_group.add_argument('--token-code', help='The value provided by the MFA device, if MFA is required. If any '
                                                'policy requires the IAM user to submit an MFA code, specify this '
                                                'value. If MFA authentication is required, the user must provide a '
                                                'code when requesting a set of temporary security credentials. A user '
                                                'who fails to provide the code receives an "access denied" response '
                                                'when requesting resources that require MFA authentication.')

    return parser


if __name__ == '__main__':
    main()
