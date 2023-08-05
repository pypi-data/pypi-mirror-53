
import sys
from .miscutils import readyaml

CONFIGURATION_DEFAULT = "etc/configuration.yaml"


def validate_namespace_str(namespace):
    """Validate if namespace is a string, and within length boundaries."""
    if not isinstance(namespace, str) \
        or len(namespace) < 3 \
        or len(namespace) > 32:
            return False
    return True


def namespace_name(namespace):
    """Retrieve or validate namespace name"""
    if validate_namespace_str(namespace) is not True:
        try:
            configuration = readyaml(CONFIGURATION_DEFAULT)
            namespace = configuration["namespace"]["default"]
            if validate_namespace_str(namespace) is not True:
                raise ValueError
        except (ValueError, KeyError, FileNotFoundError):
            sys.stderr.write("Cant retrieve default namespace. Verify configuration.yaml\n")
            sys.exit(1)
    return namespace


def namespace_configuration_template(namespace):
    """Retrieve namespace templatebody"""
    namespace = namespace_name(namespace)

    template_file = "cloudformation/namespace-" + namespace + "/main.yaml"
    try:
        with open(template_file, "r") as opened:
            templatebody = opened.read().strip()
        if not isinstance(templatebody, str):
            raise ValueError
    except (ValueError, FileNotFoundError):
        sys.stderr.write("Cant read template: " + template_file + "\n")
        sys.exit(1)
    return namespace, templatebody
