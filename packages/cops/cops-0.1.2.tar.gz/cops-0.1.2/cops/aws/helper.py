import yaml, json, boto3





def desc_subnets(client, filter):
    print "Subnets:"
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets
    response = client.describe_subnets( Filters=filter )
    for item in response['Subnets']:
        print '  - SubnetId: [%s], IPv4 CIDR: [%s], AZ: [%s]' % (item['SubnetId'], item['CidrBlock'], item['AvailabilityZone'])

def desc_security_groups(client, filter):
    rs = []
    print "Security Groups:"
    response = client.describe_security_groups( Filters=filter )
    for item in response['SecurityGroups']:
        print '  - GroupName: [%s], GroupId: [%s]' % (item['GroupName'], item['GroupId'])
        rs.append({'GroupName': item['GroupName'], 'GroupId': item['GroupId']})
    return rs

def desc_key_pairs(client, filter):
    rs = []
    print "KeyPairs:"
    response = client.describe_key_pairs()
    for item in response['KeyPairs']:
        print '  - KeyName: [%s], KeyFingerprint: [%s]' % (item['KeyName'], item['KeyFingerprint'])
        rs.append({'KeyName': item['KeyName']})

    return rs

