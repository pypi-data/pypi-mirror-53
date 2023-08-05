#!/usr/bin/env python3

"""
Summary:
    Script to copy tags on all EC2 instances in a region to their respective
    EBS Volumes while eliminating or retaining certain tags as specified

Args:
    profiles (list): awscli profile roles.  Denotes accounts in which to run
    regions (list): AWS region codes
    DEBUGMODE (bool): don't change tags, but print out tags to be copied
    SUMMARY_REPORT (bool): gen summary report only
    logger (logging object):  logger

Author:
    Blake Huber, copyright 2017

    (although it's hard to think someone would be desperate enough to rip
    off such hastily written crap code. At some pt I'll clean it up, meanwhile
    Use at your own risk)
"""

import sys
import argparse
import inspect
import datetime
from time import sleep
import boto3
from botocore.exceptions import ClientError
from libtools.io import export_json_object
from libtools import stdout_message
from pyaws import exit_codes, logger, local_config


DEBUGMODE = True           # will not retag any resources
SUMMARY_REPORT = True       # print summary report only
VALID_TYPES = ['instances', 'volumes', 'display']

regions = ['ap-southeast-1', 'eu-west-1', 'us-east-1']

profiles = [
    'gcreds-phht-gen-ra1-pr',
    'gcreds-phht-gen-ra2-pr',
    'gcreds-phht-gen-ra3-pr',
    'gcreds-phht-gen-ra4-pr',
    'gcreds-phht-gen-ra5-pr',
]

profiles = ['gcreds-phht-gen-ra3-pr']

# tags - to remove
TAGKEY_BACKUP = 'MPC-AWS-BACKUP'
TAGKEY_CPM = 'cpm backup'
TAGKEY_SNOW_CPM = 'MPC-SN-BACKUP'
NETWORKER = 'networker backup'
NAME = 'Name'

# tags we should not copy from the ec2 instance to the ebs volume
NO_COPY_LIST = [TAGKEY_BACKUP, TAGKEY_CPM, TAGKEY_SNOW_CPM, NETWORKER, NAME]

# tags on ebs volumes to preserve and ensure we do not overwrite or rm
PRESERVE_TAGS = ['Name']


# -- declarations -------------------------------------------------------------


def filter_tags(tag_list, *args):
    """
        - Filters a tag set by exclusion
        - variable tag keys given as parameters, tag keys corresponding to args
          are excluded

    RETURNS
        TYPE: list
    """
    clean = tag_list.copy()
    for tag in tag_list:
        for arg in args:
            if arg == tag['Key']:
                clean.remove(tag)
    return clean


def valid_tags(tag_list):
    """ checks tags for invalid chars """
    for tag in tag_list:
        if ':' in tag['Key']:
            return False
    return True


def pretty_print_tags(tag_list):
    """ prints json tags with syntax highlighting """
    export_json_object(tag_list)
    print('\n')
    return


def select_tags(tag_list, key_list):
    """
    Return selected tags from a list of many tags given a tag key
    """
    select_list = []
    # select tags by keys in key_list
    for tag in tag_list:
        for key in key_list:
            if key == tag['Key']:
                select_list.append(tag)
    # ensure only tag-appropriate k,v pairs in list
    return [{'Key': x['Key'], 'Value': x['Value']} for x in select_list]


def get_instances(profile, rgn):
    """ returns all EC2 instance Ids in a region """
    vm_ids = []
    session = boto3.Session(profile_name=profile, region_name=rgn)
    client = session.client('ec2')
    r = client.describe_instances()
    for detail in [x['Instances'] for x in r['Reservations']]:
        for instance in detail:
            vm_ids.append(instance['InstanceId'])
    return vm_ids


def get_volumes(profile, rgn):
    """
    returns all EC2 volume Ids in a region
    """
    session = boto3.Session(profile_name=profile, region_name=rgn)
    client = session.client('ec2')
    return [x['VolumeId'] for x in client.describe_volumes()['Volumes']]


def calc_runtime(start, end):
    """ Calculates job runtime given start, end datetime stamps
    Args:
        - start (datetime object): job start timestamp
        - end (datetime object): job end timestamp
    """
    duration = end - start
    if (duration.seconds / 60) < 1:
        return (duration.seconds), 'seconds'
    else:
        return (duration.seconds / 60), 'minutes'


def display_valid(print_object):
    """
    Help Function | Displays an attribute of this program
    """
    if print_object in ('list', 'print', 'display'):
        print('\n' + VALID_TYPES + '\n')
    return True


def options(parser):
    """
    Summary:
        parse cli parameter options
    Returns:
        TYPE: argparse object, parser argument set
    """
    parser.add_argument("-p", "--profile", nargs='?', default="default",
                              required=False, help="type (default: %(default)s)")
    parser.add_argument("-t", "--type", nargs='?', default='list', type=str,
                        choices=VALID_TYPES, required=False)
    parser.add_argument("-a", "--auto", dest='auto', action='store_true', required=False)
    parser.add_argument("-d", "--debug", dest='debug', action='store_true', required=False)
    parser.add_argument("-V", "--version", dest='version', action='store_true', required=False)
    return parser.parse_args()


# -- main ---------------------------------------------------------------------


def main():
    """ copies ec2 instance tags to attached resources """
    for profile in profiles:
        # derive account alias from profile
        account = '-'.join(profile.split('-')[1:])
        for region in regions:
            #instances = []
            session = boto3.Session(profile_name=profile, region_name=region)
            client = session.client('ec2')
            ec2 = session.resource('ec2')
            instances = get_instances(profile, region)
            volumes = get_volumes(profile, region)
            # print summary
            if SUMMARY_REPORT:
                print('\nFor AWS Account %s, region %s, Found %d Instances\n' % (account, region, len(instances)))
                continue
            # copy tags
            if instances:
                try:
                    base = ec2.instances.filter(InstanceIds=instances)
                    ct = 0
                    for instance in base:
                        ids, after_tags = [], []
                        ct += 1
                        if instance.tags:
                            # filter out tags to prohibited from copy
                            filtered_tags = filter_tags(instance.tags, *NO_COPY_LIST)
                        else:
                            # no tags on instance to copy
                            continue

                        if not valid_tags(filtered_tags):
                            print('\nWARNING:')
                            logger.warning('Skipping instance ID %s, Invalid Tags\n' % instance.id)
                            continue
                        # collect attached resource ids to be tagged
                        for vol in instance.volumes.all():
                            ids.append(vol.id)
                        for eni in instance.network_interfaces:
                            ids.append(eni.id)
                        logger.info('InstanceID %s, instance %d of %d:' % (instance.id, ct, len(instances)))
                        logger.info('Resource Ids to tag is:')
                        logger.info(str(ids) + '\n')
                        if DEBUGMODE:
                            # BEFORE tag copy
                            logger.info('BEFORE list of %d tags is:' % (len(instance.tags)))
                            pretty_print_tags(instance.tags)

                            # AFTER tag copy | put Name tag back into apply tags, ie, after_tags
                            retain_tags = select_tags(instance.tags, PRESERVE_TAGS)
                            for tag in (*retain_tags, *filtered_tags):
                                after_tags.append(tag)
                            logger.info('For InstanceID %s, the AFTER FILTERING list of %d tags is:' % (instance.id, len(after_tags)))
                            logger.info('Tags to apply are:')
                            pretty_print_tags(after_tags)
                        else:
                            logger.info('InstanceID %s, instance %d of %d:' % (instance.id, ct, len(instances)))
                            if filtered_tags:     # we must have something to apply
                                # apply tags
                                for resourceId in ids:
                                    # retain a copy of tags to preserve if is a volume
                                    if resourceId.startswith('vol-'):
                                        r = client.describe_tags(
                                            Filters=[{
                                                        'Name': 'resource-id',
                                                        'Values': [resourceId],
                                                    },
                                                ]
                                            )
                                        retain_tags = select_tags(r['Tags'], PRESERVE_TAGS)
                                        # add retained tags before appling to volume
                                        if retain_tags:
                                            for tag in retain_tags:
                                                filtered_tags.append(tag)
                                    # clear tags
                                    print('\n')
                                    logger.info('Clearing tags on resource: %s' % str(resourceId))
                                    client.delete_tags(Resources=[resourceId], Tags=[])

                                    # create new tags
                                    logger.info('Applying tags to resource %s\n' % resourceId)
                                    ec2.create_tags(Resources=[resourceId], Tags=filtered_tags)
                                    # delay to throttle API requests
                                    sleep(1)

                except ClientError as e:
                    logger.exception(
                        "%s: Problem (Code: %s Message: %s)" %
                        (inspect.stack()[0][3], e.response['Error']['Code'],
                            e.response['Error']['Message'])
                        )
                    raise


def init_cli():
    # parser = argparse.ArgumentParser(add_help=False, usage=help_menu())
    parser = argparse.ArgumentParser(add_help=False)

    try:
        args = options(parser)
    except Exception as e:
        help_menu()
        stdout_message(str(e), 'ERROR')
        sys.exit(exit_codes['EX_OK']['Code'])

    if len(sys.argv) == 1:
        help_menu()
        sys.exit(exit_codes['EX_OK']['Code'])

    elif args.help:
        help_menu()
        sys.exit(exit_codes['EX_OK']['Code'])

    elif args.version:
        package_version()

    elif args.configure:
        r = option_configure(args.debug, local_config['PROJECT']['CONFIG_PATH'])
        return r
    else:
        if precheck():              # if prereqs set, run
            if authenticated(profile=args.profile):
                # execute keyset operation
                success = main(
                            operation=args.operation,
                            profile=args.profile,
                            user_name=args.username,
                            auto=args.auto,
                            debug=args.debug
                            )
                if success:
                    logger.info('IAM access keyset operation complete')
                    sys.exit(exit_codes['EX_OK']['Code'])
            else:
                stdout_message(
                    'Authenication Failed to AWS Account for user %s' % args.profile,
                    prefix='AUTH',
                    severity='WARNING'
                    )
                sys.exit(exit_codes['E_AUTHFAIL']['Code'])

    failure = """ : Check of runtime parameters failed for unknown reason.
    Please ensure local awscli is configured. Then run keyconfig to
    configure keyup runtime parameters.   Exiting. Code: """
    logger.warning(failure + 'Exit. Code: %s' % sys.exit(exit_codes['E_MISC']['Code']))
    print(failure)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    duration, unit = calc_runtime(start_time, end_time)
    logger.info('Job Start: %s' % start_time.isoformat())
    logger.info('Job End: %s' % end_time.isoformat())
    logger.info('Job Completed. Duration: %d %s' % (duration, unit))
    sys.exit(0)
