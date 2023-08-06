from ansible.module_utils.basic import AnsibleModule
import os
import glob
import re

try:
    import hcl
except ImportError:
    hc = None


VARIABLE_DECL = r'^variable\s+\"([\w_]+)\"\s+{'


def get_variables_in_file(path: str) -> list:
    with open(path, 'r') as stream:
        data = stream.readlines()
    data = [line.strip() for line in data if line.strip()]
    defined_variables = []
    for line in data:
        if re.match(VARIABLE_DECL, line):
            match = re.match(VARIABLE_DECL, line)
            defined_variables.append(match.group(1))
    return defined_variables


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(required=True),
            destination_key=dict(required=False, default='terraformVariables')
        ),
        supports_check_mode=True,
    )

    path = module.params['path']
    destination_key = module.params['destination_key']

    if not os.path.isdir(path):
        module.fail_json(msg="{} is not a directory".format(path))
    if hcl is None:
        module.fail_json(msg="hcl module is not available run this command to make it available pip install pyhcl ")

    files = [f for f in glob.glob(path + "**/*.tf", recursive=False)]

    variables = []
    for file in files:
        variables.extend(get_variables_in_file(file))

    module.exit_json(**{"changed": False, destination_key: variables})

