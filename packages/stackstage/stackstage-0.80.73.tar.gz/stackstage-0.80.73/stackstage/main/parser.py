
import os
import sys
import re
import json

from .cloudformation import CloudFormationStack
from .cloudformation import namespace_configuration

from .s3utils import s3sync
from .s3utils import s3empty


def main(lambda_args={}):
    """This function is called when run as python3 -m ${MODULE}
    Parse any additional arguments and call required module functions."""

    if lambda_args:
        # invoked from lambda
        print("Lambda invokation not yet supported")
        return 1
    else:
        # invoked from current host
        import argparse

        module_name = '.'.join(__loader__.name.split('.')[0:-1])
        argument_parser = argparse.ArgumentParser(
            prog=module_name,
            description='Create a remotestate backend to hold infra state configration'
        )

        exclusive_action = argument_parser.add_mutually_exclusive_group()
        exclusive_action.add_argument('--init', action='store_true', required=False,
                                      help="Initialise new or update existing account")
        exclusive_action.add_argument('--upload', action='store', required=False,\
                                      help="Upload a cloudformation stack")
        exclusive_action.add_argument('--apply', action='store', required=False,\
                                      help="Apply CloudFormation \"infra-as-code\"")
        exclusive_action.add_argument('--list', action='store_true', required=False,\
                                      help="List running CloudFormation stacks\n")
        exclusive_action.add_argument('--delete', action='store', required=False,\
                                      help="Delete a running CloudFormation Stack")

        argument_parser.add_argument('--namespace', action='store', nargs=1,\
                                     required=False, help="Set namespace")
        argument_parser.add_argument('--emptybucket', action='store_true', required=False,\
                                     help="Empty s3 (configuration) bucket")
        

        args = argument_parser.parse_args(sys.argv[1:])

        if isinstance(args.namespace, list) and len(args.namespace) == 1:
            namespace = args.namespace[0]
        else:
            namespace = None

        if args.init:
            namespace, _, templatebody = namespace_configuration(namespace=namespace,
                                                                 init=True)

            stackobject = CloudFormationStack(stackname="namespace--" + namespace,
                                              namespace=namespace)
            stackobject.deploy(templatebody=templatebody)
        elif args.upload:
            if not os.path.isdir(args.upload):
                raise ValueError("--upload should be given a directory")
            directory = args.upload
            _, namespace_outputs, _ = namespace_configuration(namespace=namespace)

            prefix = os.path.join("cloudformation", os.path.basename(directory))
            s3sync(directory,
                   namespace_outputs['S3BucketName'],
                   prefix=prefix,
                   update_only=True)
        elif args.apply:
            # strip off accidental $namespace-- and directory path input
            stackname = re.sub('^.*?--', '', os.path.basename(args.apply))

            namespace, namespace_outputs, _ = namespace_configuration(namespace=namespace)

            appstack = CloudFormationStack(stackname=namespace + "--" + stackname,
                                           namespace=namespace,
                                           rolearn=namespace_outputs['IAMServiceRole'])
            url = namespace_outputs['S3BucketSecureURL'] \
                  + '/cloudformation/' + stackname + '/main.yaml'
            appstack.deploy(stackurl=url)
        elif args.list:
            namespace, namespace_outputs, _ = namespace_configuration(namespace=namespace)
            stack = CloudFormationStack(stackname="namespace--" + namespace)
            siblings = stack.search_stacks(namespace=namespace)
            if len(siblings) > 0:
                sys.stdout.write(json.dumps(siblings, indent=4, default=str) + "\n")

        elif args.delete:
            # strip off accidental $namespace-- and directory path input
            stackname = re.sub('^.*?--', '', os.path.basename(args.delete))
            namespace, namespace_outputs, _ = namespace_configuration(namespace=namespace)

            if stackname == namespace:
                # namespace stack:
                stack = CloudFormationStack(stackname="namespace--" + namespace)

                # verify there are no stack dependencies (siblings)
                siblings = stack.search_stacks(namespace=namespace)
                if len(siblings) > 0:
                    sys.stderr.write("ERROR - CANT DELETE NAMESPACE, SIBLINGS FOUND:\n")
                    sys.stderr.write(json.dumps(siblings, indent=4, default=str) + "\n")
                    return 1

                # remove protection
                stack.protect(enable=False)

                # remove all s3 objects
                bucketname = namespace_outputs['S3BucketName']
                if args.emptybucket is True:
                    sys.stdout.write("CLEANING UP CONFIGURATION BUCKET: " + bucketname + "\n")
                    s3empty(bucketname, delete_versions=True)
                else:
                    sys.stderr.write("CAN ONLY CONTINUE WITH --emptybucket SET\n")
                    sys.exit(1)

            else:
                # regular stack
                stack = CloudFormationStack(stackname=namespace + "--" + stackname,
                                            namespace=namespace,
                                            rolearn=namespace_outputs['IAMServiceRole'])

            stack.delete()
 
        else:
            sys.exit(1)
    return 0

