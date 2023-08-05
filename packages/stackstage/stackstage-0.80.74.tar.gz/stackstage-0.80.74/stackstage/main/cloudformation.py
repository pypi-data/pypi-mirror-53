
import os
import sys
import re
import boto3

from .stacks import stackdeploy
from .stacks import stackdelete
from .stacks import statusfilter
from .stacks import retrieve_stacks
from .stacks import configure_stackprotection

from .namespace import namespace_configuration_template
from .namespace import namespace_name
from .validators import validate_url

from .validators import verify_http


class CloudFormationStack():
    """CloudFormation Stack Object"""
    def __init__(self,
                 stackname=None,
                 tags={},
                 parameters={},
                 rolearn=None,
                 namespace=None):
        if not isinstance(stackname, str):
            raise TypeError("Stackname is mandatory")
        if len(stackname) < 3 or len(stackname) > 63:
            raise ValueError('stackname not within expected length')

        self.client = boto3.client('cloudformation')

        self.stackname = stackname
        self.is_namespace = False
        self.rolearn = rolearn
        self.tags = tags
        self.parameters = parameters

        # assume stack does not (yet) exist
        self.is_active = False

        # if namespace not set, stack belongs to itself
        if isinstance(namespace, str):
            self.namespace = namespace
            if re.match('^namespace--', stackname):
                self.is_namespace = True
        else:
            self.namespace = None

    def check_active(self):
        """Verify if stackname exists and update status"""
        if len(retrieve_stacks(self.client, self.stackname)) < 1:
            self.is_active = False
        else:
            self.is_active = True
        return self.is_active

    def retrieve_configuration(self, parameters=[]):
        """Retrieve stack and return configuration based on a list of requested parameters,
        if this list is empty return the full configuration,
        always return a dict -- may be empty if nothing is matched"""
        if not isinstance(parameters, list):
            raise TypeError("parameters should be of format list")

        # verify if stack exist -- required because else describe_stacks will fail
        if self.is_active is False and self.check_active() is False:
            return {}

        # retrieve and verify response
        response, statuscode = verify_http(
            self.client.describe_stacks(StackName=self.stackname))
        if statuscode != 200:
            sys.stderr.write("ERROR - DESCRIBE STACKS:\n")
            sys.stderr.write(json.dumps(response, indent=4, default=str))
            return {}

        if not isinstance(response.get('Stacks'), list) \
            or len(response['Stacks']) < 1 \
            or not isinstance(response['Stacks'][0], dict):
                return {}

        # validate stack integrity, than return required parameters
        stack = response['Stacks'][0]
        if not isinstance(stack, dict):
            return {}
        #if stack.get('DeletionTime') is None \
        #    and (isinstance(stack.get('StackStatus'), str) \
        #    and re.match('^CREATE_COMPLETE$|^UPDATE_COMPLETE$|^UPDATE_ROLLBACK_COMPLETE$',
        #                 stack['StackStatus'])):
        #        if len(parameters) < 1:
        #            return stack
        return {param: stack.get(param) for param in parameters}

    def search_stacks(self, namespace=None):
        """Find a list of stacks within namespace"""
        response = self.client.list_stacks(StackStatusFilter=statusfilter())
        stacks = response.get('StackSummaries')
        if not isinstance(stacks, list) or len(stacks) < 1:
            return []

        if not isinstance(namespace, str):
            # return all stacks if no specific namespace is given
            return stacks

        return  [stack for stack in stacks
                 if isinstance(stack.get('StackName'), str)
                 and re.match("^" + namespace + "--", stack.get('StackName'))]

    def retrieve_outputs(self, parameters=[]):
        """Retrieve outputvalues from stack and filter on parameters,
        if not parameters are given than return all values,
        always return a dict -- may be empty if nothing is matched"""
        if not isinstance(parameters, list):
            raise TypeError("parameters should be of format list")
        try:
            outputs = self.retrieve_configuration(parameters=['Outputs'])['Outputs']
            if not isinstance(outputs, list):
                raise ValueError
            outputs = {pair['OutputKey']: pair['OutputValue'] for pair in outputs}
        except (KeyError, IndexError, ValueError):
            return {}

        if len(parameters) < 1:
            return outputs

        return {param: outputs[param] for param in outputs.keys() if param in parameters}

    def protect(self, enable=True):
        """Set stack protection"""
        return configure_stackprotection(self.client, self.stackname, enable=enable)

    def deploy(self,
               stackurl=None,
               templatebody=None,
               templatefile=None):
        """Deploy a new CloudFormation stack"""
        # either templatebody, templatefile or stackurl must be provided
        if isinstance(templatefile, str):
            if not os.path.isfile(templatefile):
                raise ValueError("Cant find file: " + templatefile)
        elif isinstance(templatebody, str):
            pass
        elif not isinstance(stackurl, str):
            raise TypeError("Either stackurl or templatefile is mandatory")

        if templatebody:
            # check templatebody first
            pass
        elif templatefile:
            # check templatefile second
            with open(template, 'r') as templatefile:
                templatebody = templatefile.read().strip()
        elif stackurl:
            stackurl_root = '/'.join(stackurl.split('/')[0:-1])
            self.parameters['S3BucketSecureURL'] = stackurl_root
            self.parameters['LastChange'] = '20190912'

            # check stackurl last
            (is_valid, error_message) = validate_url(stackurl)
            if is_valid is False:
                raise ValueError(error_message)

        if isinstance(self.namespace, str):
            self.tags['__namespace__'] = self.namespace

        if self.is_namespace is True:
            # project namespace stacks
            protected = True
        else:
            protected = False

        return_code = stackdeploy(self.client,
                                  self.stackname,
                                  stackurl=stackurl,
                                  templatebody=templatebody,
                                  rolearn=self.rolearn,
                                  parameters_in=self.parameters,
                                  tags_in=self.tags,
                                  protected=protected)

    def delete(self):
        """Delete the CloudFormation stack"""
        return stackdelete(self.client, self.stackname, self.rolearn)


def namespace_configuration(namespace=None, init=False):
    """Retrieve namespace configuration: validated name, outouts or template"""
    if init is True:
        # initialisation request --- only return validated name and template body
        namespace, templatebody = namespace_configuration_template(namespace)
        return namespace, None, templatebody
    # non-initialisation --- assume namestack is deployed, return name and outputs
    namespace = namespace_name(namespace)

    stack = CloudFormationStack(stackname="namespace--" + namespace)
    # verify if namespace exist
    if stack.check_active() is False:
        sys.stderr.write("No namespace configured or active -- initialize first\n")
        sys.exit(1)
    outputs = stack.retrieve_outputs(parameters=['S3BucketName',
                                                           'S3BucketSecureURL',
                                                           'IAMServiceRole'])
    return namespace, outputs, None
