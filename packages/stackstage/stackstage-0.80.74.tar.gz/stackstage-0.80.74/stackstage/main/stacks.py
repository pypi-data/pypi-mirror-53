
import sys
import re
import string
import json
import random

#from botocore.exceptions import ClientError
from botocore.exceptions import WaiterError

from .miscutils import serialize
from .miscutils import random_string
from .validators import verify_http

def random_string(size=12):
    """Return randomn string of length size"""
    return ''.join([random.choice(string.ascii_lowercase + string.digits)
                    for i in range(size)])


def configure_stackprotection(client, stackname, enable=True):
    response, status_code = verify_http(
        client.update_termination_protection(
            EnableTerminationProtection=enable,
            StackName=stackname))
    if status_code != 200:
        sys.stderr.write("ERROR - SETTING STACK PROTECTION:\n")
        sys.stderr.write(json.dumps(response, indent=4, default=str))
        return 1
    return 0


def statusfilter(exclude=['DELETE_COMPLETE']):
    """Return a list of stack status response strings
    by default remove deleted stacks"""
    if not isinstance(exclude, list):
        raise ValueError("exclude should be of format list")

    STACK_STATUSLIST = ['CREATE_IN_PROGRESS','CREATE_FAILED','CREATE_COMPLETE','ROLLBACK_IN_PROGRESS','ROLLBACK_FAILED','ROLLBACK_COMPLETE','DELETE_IN_PROGRESS','DELETE_FAILED','DELETE_COMPLETE','UPDATE_IN_PROGRESS','UPDATE_COMPLETE_CLEANUP_IN_PROGRESS','UPDATE_COMPLETE','UPDATE_ROLLBACK_IN_PROGRESS','UPDATE_ROLLBACK_FAILED','UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS','UPDATE_ROLLBACK_COMPLETE','REVIEW_IN_PROGRESS']

    return list([status for status in STACK_STATUSLIST if status not in exclude])


def retrieve_stacks(client, stackname):
    """List existing stacks with this name"""
    response = client.list_stacks(StackStatusFilter=statusfilter())

    stacks = response.get('StackSummaries')
    if not isinstance(stacks, list) or len(stacks) < 1:
        return []

    # create a list with (name, stack) tuples, to allow for easy grouping
    named_stacks = list([(stack['StackName'], stack) for stack in stacks
                         if isinstance(stack.get('StackName'), str)
                         #and stack.get('DeletionTime') is None
                         and re.match('^' + stackname + '$', stack.get('StackName')) 
                            is not None])

    # create dict for each unique stack name
    grouped_stacks = {name: [] for name in set(stack[0] for stack in named_stacks)}

    for stack in named_stacks:
        stack_name, stack_value = stack
        grouped_stacks[stack_name].append(stack_value)

    return grouped_stacks


def get_current_stacks(client, stackname):
    """Get a list of running stacks that match stackname"""
    stacks = retrieve_stacks(client, stackname)
    filterlist = statusfilter()
    if len(stacks) > 0 and stackname in stacks.keys():
        return list([stack for stack in stacks[stackname]
                     if stack.get('DeletionTime') is None
                     or (isinstance(stack.get('StackStatus'), str)
                     and stack['StackStatus'] in filterlist)])
                     #and re.search('_IN_PROGRESS$', stack['StackStatus']))])
    return []


def get_stackstatus(stack):
    """Get status of a stack, return status Complete and Inprogress"""
    if not isinstance(stack, dict):
        raise ValueError("Stack format invalid")

    stackstatus = stack.get('StackStatus')

    if not isinstance(stackstatus, str):
        raise ValueError("Cant get StackStatus from currrent stack")

    if re.search('_IN_PROGRESS$', stackstatus):
        return None, stackstatus, None
    if re.match('^CREATE_COMPLETE$|^UPDATE_COMPLETE$|^UPDATE_ROLLBACK_COMPLETE$',
                stackstatus):
        return stackstatus, None, None

    return None, None, stackstatus


def stackdeploy(client,
                stackname,
                stackurl=None,
                templatebody=None,
                rolearn=None,
                tags_in={},
                parameters_in={},
                protected=False):
    """Create or update a cloudformation stack"""

    # rewrite tags_in and parameters_in to list of dictionaries
    tags = [{'Key': key, 'Value': value}
            for key, value in  tags_in.items()]
    parameters = [{'ParameterKey': key, 'ParameterValue': value}
                  for key, value in parameters_in.items()]
    current_stacks = get_current_stacks(client, stackname)

    if len(current_stacks) < 1:
        # assume to create a new stack
        changeset_type = 'CREATE'
    else:
        # update an existing stack. Extract information from first item in list.
        complete, inprogress, unknown = get_stackstatus(current_stacks[0])
        if complete is None:
            if isinstance(inprogress, str):
                sys.stdout.write(json.dumps(current_stacks[0], indent=4, default=str))
                return 0
            sys.stderr.write("ERROR - STACKSTATUS:\n")
            sys.stderr.write(json.dumps(current_stacks[0], indent=4, default=str))
            return 1

        changeset_type = 'UPDATE'

    # name must start with a char within a-z
    changeset_name = random.choice(string.ascii_lowercase) + random_string(size=15)

    if stackurl:
        # deploy stack by url

        # validate template
        response, status_code = verify_http(
            client.validate_template(TemplateURL=stackurl))
        if status_code != 200:
            sys.stderr.write("ERROR - VALIDATING TEMPLATE:\n")
            sys.stderr.write(json.dumps(response, indent=4, default=str))
            return 1

        # deploy stack
        response, status_code = verify_http(client.create_change_set(StackName=stackname,
                                            TemplateURL=stackurl,
                                            RoleARN=rolearn,
                                            Capabilities=['CAPABILITY_IAM'],
                                            ChangeSetName=changeset_name,
                                            ChangeSetType=changeset_type,
                                            Tags=tags,
                                            Description="abc",
                                            Parameters=parameters))
        if status_code != 200:
            sys.stderr.write("ERROR - DEPLOYING CHANGESET:\n")
            sys.stderr.write(json.dumps(response, indent=4, default=str))
            return 1

    else:
        # deploy stack by template file

        # validate
        response, status_code = verify_http(
            client.validate_template(TemplateBody=templatebody))
        if status_code != 200:
            sys.stderr.write("ERROR - VALIDATING TEMPLATE:\n")
            sys.stderr.write(json.dumps(response, indent=4, default=str))
            return 1

        response, status_code = verify_http(client.create_change_set(StackName=stackname,
                                            TemplateBody=templatebody,
                                            Capabilities=['CAPABILITY_IAM'],
                                            ChangeSetName=changeset_name,
                                            ChangeSetType=changeset_type,
                                            Tags=tags,
                                            Description="abc",
                                            Parameters=parameters))
        if status_code != 200:
            sys.stderr.write("ERROR - DEPLOYING CHANGESET:\n")
            sys.stderr.write(json.dumps(response, indent=4, default=str))
            return 1


    # insert a waiter -- changeset takes a couple of seconds to be ready
    try:
        changeset_id = response['Id']
        waiter = client.get_waiter('change_set_create_complete')
        waiter.wait(ChangeSetName=changeset_id,
                    WaiterConfig={'Delay': 3, 'MaxAttempts': 100})
    except WaiterError as error:
        # retrieve error
        response = client.describe_change_set(ChangeSetName=changeset_id)
        if isinstance(response.get('Status'), str) and response['Status'] == 'FAILED':
            if isinstance(response.get('StatusReason'), str):
                if re.search("submitted information didn't contain changes",
                             response.get('StatusReason')):
                    sys.stdout.write(response.get('StatusReason') + "\n")
                    return 0
                sys.stderr.write("ERROR - CHANGESET FAILURE, REASON:\n"\
                                 + response.get('StatusReason') + "\n")
                return 1

        # unknown error 
        sys.stderr.write("ERROR - CHANGESET FAILURE, UNKNOWN ERROR:\n"\
                         + str(error) + "\n")
        return 1

    # finally -- deploy the stack
    response, status_code = verify_http(
        client.execute_change_set(ChangeSetName=changeset_name, StackName=stackname))
    if status_code != 200:
        sys.stderr.write("ERROR - DEPLOYING STACK:\n")
        sys.stderr.write(json.dumps(response, indent=4, default=str))
        return 1

    sys.stdout.write("DEPLOYMENT INITIATED: " + stackname)
    sys.stdout.write(json.dumps(response, indent=4, default=str))

    if protected is True:
        # projected stack -- immediately toggle protection flag
        return configure_stackprotection(client, stackname, enable=True)

    return 0


def stackdelete(client, stackname, rolearn=None):
    current_stacks = get_current_stacks(client, stackname)
    if len(current_stacks) < 1:
        sys.stdout.write("No running stack with name: " + stackname + "\n")
        return 0

    complete, inprogress, unknown = get_stackstatus(current_stacks[0])
    if isinstance(inprogress, str) and re.match('^DELETE_IN_PROGRESS$', inprogress):
        # delete already in progress
        sys.stdout.write(json.dumps(current_stacks[0], indent=4, default=str))
        return 0
    elif isinstance(unknown, str) and re.match('^.*_FAILED$', unknown):
        # delete not possible due to a stackfailure 
        # don't return, keep retrying
        sys.stderr.write("WARNING - DELETE FAILURE, ERROR:\n")
        sys.stderr.write(json.dumps(current_stacks[0], indent=4, default=str) + "\n")

    # fire up a delete request
    if isinstance(rolearn, str):
        response = client.delete_stack(StackName=stackname, RoleARN=rolearn)
    else:
        response = client.delete_stack(StackName=stackname)
    sys.stdout.write("DELETE (RE-)INITIATED:")
    sys.stdout.write(json.dumps(response, indent=4, default=str))

    return 0
