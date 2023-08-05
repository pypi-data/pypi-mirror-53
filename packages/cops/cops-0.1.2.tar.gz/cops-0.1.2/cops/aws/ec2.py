# -*- coding: utf-8 -*-
#
# @see: https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.run_instances
# @see: https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_volumes

import time, sys, os, unicodedata
#from datetime import datetime
import yaml, boto3
import copy


__CLIENT = boto3.client('ec2')

__DEBUG = False

FIRST_INSTANCE_IDX = 0



def struct_params(config):

    ec2_params = {}

    ## Basic information
    #ec2_params['DryRun'] = True
    ec2_params['ImageId'] = config['ami-id']

    ec2_params['MinCount'] = 1
    ec2_params['MaxCount'] = 1
    ec2_params['InstanceType'] = config['instance-type']

    # Storage
    ec2_params['BlockDeviceMappings'] = remove_ebs_tags_from_config(config['block-device-mappings'])
    ec2_params['InstanceInitiatedShutdownBehavior'] = config['shutdown-behavior']
    ec2_params['EbsOptimized'] = config['ebs-optimized']

    #ec2_params['KernelId'] = config['kernel-id']
    #ec2_params['RamdiskId'] = config['ramdisk-id']



    #ec2_params['DisableApiTermination'] = config['DisableApiTermination']
    ec2_params['InstanceInitiatedShutdownBehavior'] = config['shutdown-behavior']

    ## Network
    if 'network-interfaces' in config:
        ec2_params['NetworkInterfaces'] = create_enis_params(config['network-interfaces'], config['subnet-id'])
    else:
        #ec2_params['SecurityGroups'] = config['security-groups']
        ec2_params['SecurityGroupIds'] = config['security-group-ids']
        ec2_params['SubnetId'] = config['subnet-id']

    if 'placement-group' in config:
        ec2_params['Placement'] = config['placement-group']

    ## Security and Permission
    ec2_params['KeyName'] = config['key-pair']
    ec2_params['IamInstanceProfile'] = {
    #            'Arn': config['iam-role-arn'],
        'Name': config['iam-role-name']
    }

    ## Advanced
    ### detail-monitoring
    if 'detail-monitoring' in config:
        ec2_params['Monitoring'] = {
            'Enabled': config['detail-monitoring']
        }
    else:
        ec2_params['Monitoring'] = {
            'Enabled': False
        }

    if 'terminate-protection' in config:
        ec2_params['DisableApiTermination'] = config['terminate-protection']

    if 'userdata' in config:
        ec2_params['UserData'] = handle_userdata(config['userdata'])

    return ec2_params
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------

def handle_userdata(userdata):
    # inline
    if type(userdata) is str:
        return userdata
    # iterate
    elif type(userdata) is list:
        return handle_userdata_scripts(userdata)
    # exception
    else:
        print 'The userdata is invalid, it has to been string or list, please check.'
        sys.exit(1)

def handle_userdata_scripts(userdata):
    buf = []
    for script in userdata:
        f = open(script['path'], 'r').read()
        if 'parameters' in script:
            for key in script['parameters'].keys():
                value = script['parameters'][key]
                key = '{{ %s }}' % key
                f = f.replace(key, value)
        buf.append(f)

    return "\n".join(buf)



# -----------------------------------------------------------------------------
# Restructure the tags form config
# {
#     "ip_address": {
#         "ip_address": "10.50.x.y",
#         "tags": []
#     }
# }
# -----------------------------------------------------------------------------
def get_eni_tags_from_config(config):
    enis = {}
    if 'network-interfaces' in config:
        for eni in config['network-interfaces']:
            eni_obj = {}
            for ip_info in eni['private-ip-addresses']:
                if ip_info['Primary'] is True:
                    eni_obj['ip-address'] = ip_info['PrivateIpAddress']
                    eni_obj['tags'] = eni['tags']
                    break
            enis[eni_obj['ip-address']] = eni_obj
    #print 'enis: %s' % enis
    return enis


def update_tag_for_enis(config, response):
    #enis = {}
    enis_tags = get_eni_tags_from_config(config)
    try:
        for eni in response['Instances'][FIRST_INSTANCE_IDX]['NetworkInterfaces']:
            eni_id = eni['NetworkInterfaceId']
            private_addr = eni['PrivateIpAddress']
            if private_addr in enis_tags:
                #print "tags: %s" % enis_tags[private_addr]['tags']
                __CLIENT.create_tags(
                    Resources=[ eni_id ],
                    Tags=conv_tags_as_str(enis_tags[private_addr]['tags'])
                )
    except Exception as ex:
        print ex
    #return enis
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Restructure the tags form config for update_tag_for_ebs
# {
#     "device_name": tags,
# }
# -----------------------------------------------------------------------------
def get_ebs_tags_from_config(config):
    rs = {}
    if 'block-device-mappings' in config:
        for ebs in config['block-device-mappings']:
            if 'tags' in ebs:
                device_name = ebs['DeviceName']
                tags = ebs['tags']
                rs[device_name] = tags
    return rs


def update_tag_for_ebs(config, instance_id):

    volume_tags = get_ebs_tags_from_config(config)

    response = __CLIENT.describe_volumes(
        Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [ instance_id ]
            }
        ]
    )

    for volume in response['Volumes']:
        for attachment in volume['Attachments']:
            volume_id = attachment['VolumeId']
            device_name = attachment['Device']
            #print 'volume_id: %s, device_name: %s' % (volume_id, device_name)
            if device_name in volume_tags:
                tags = volume_tags[device_name]

                __CLIENT.create_tags(
                    Resources=[volume_id],
                    Tags=conv_tags_as_str(tags)
                )

    #return rs


def remove_ebs_tags_from_config(ebs_config):
    new_ebs_config = []
    for device in ebs_config:
        if 'tags' in device:
            del device['tags']
        new_ebs_config.append(device)
    return new_ebs_config


# -----------------------------------------------------------------------------

def create_enis_params(eni_list, subnet_id):
    rs = []
    device_index = 0

    # create ENIs
    for item in eni_list:
        _subnet_id = subnet_id
        _associate_public_ip_address = False

        if 'subnet-id' in item:
            _subnet_id = item['subnet-id']

        if 'associate-public-ip-address' in item:
            _associate_public_ip_address = item['associate-public-ip-address']

        params = {
            'DeviceIndex': device_index,
            'AssociatePublicIpAddress': _associate_public_ip_address,
            'SubnetId': _subnet_id,
            'Description': item['description'],
            'Groups': item['security-group-ids'],
            'DeleteOnTermination': item['delete-on-termination'],
            'PrivateIpAddresses': item['private-ip-addresses']
        }
        rs.append(params)
        device_index += 1
    # end of for

    #print rs
    return rs


# -----------------------------------------------------------------------------
# Convert the tags as:
#  - String
#  - Datetime
# -----------------------------------------------------------------------------
def conv_tags_as_str(tags):
    _tags = []
    for tag in tags:
        val = str(tag['Value'])
        val = val.replace('${cf:datetime}', time.strftime("%Y%m%d-%H%M"))

        _tags.append({
            'Key': tag['Key'],
            'Value': val
        })

    return _tags

# -----------------------------------------------------------------------------

def update_tag_for_instance(config, response):
    instance_id = response['Instances'][FIRST_INSTANCE_IDX]['InstanceId']
    __CLIENT.create_tags(
        Resources=[instance_id],
        Tags=conv_tags_as_str(config['tags'])
    )

# -----------------------------------------------------------------------------
# @return 0 normal
#         1 exceptions
def create(config):
    instance_id = None
    try:
        ec2_params = struct_params(copy.deepcopy(config))
        response = __CLIENT.run_instances(**ec2_params)

        instance_id = response['Instances'][FIRST_INSTANCE_IDX]['InstanceId']
        #print instance_id
        print "Your EC2 instance is on the way, InstanceId: [%s]." % instance_id
        print "Waiting for updating tags to resources."

        time.sleep(5)

        update_tag_for_instance(config, response)
        update_tag_for_enis(config, response)
        update_tag_for_ebs(config, instance_id)

        print "Done."

    except Exception as ex:
        print 'Fail to create ec2 instance, reason:'
        print ex
        return 1

    return 0
