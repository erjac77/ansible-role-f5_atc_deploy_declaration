#!/usr/bin/python
import json
from ansible.module_utils.basic import AnsibleModule


def process_json(data, ansible_version):
    try:
        assert data["class"]
        assert data["class"].lower() == "as3"
        assert data["declaration"]
        assert data["declaration"]["class"].lower() == "adc"
        if "controls" in data["declaration"]:
            assert not data["declaration"]["controls"]["userAgent"]
    except AssertionError:
        return (False, data)

    as3_declaration = data["declaration"]

    if "controls" not in as3_declaration:
        adc_controls = {
            "class": "Controls",
            "userAgent": "ansible/{ansible_version}".format(
                ansible_version=ansible_version)
        }
        data["declaration"]["controls"] = adc_controls
    else:
        data["declaration"]["controls"]["userAgent"] = \
            "ansible/{ansible_version}".format(
                ansible_version=ansible_version)
    return (True, data)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            atc_json_data=dict(type='json', required=True)
        ),
        supports_check_mode=True,
    )

    atc_json_data = module.params['atc_json_data']

    atc_json_data = json.loads(atc_json_data)

    (isChanged, result) = process_json(atc_json_data, module.ansible_version)

    results = dict(
        changed=isChanged,
        result=result
    )

    module.exit_json(**results)


if __name__ == '__main__':
    main()
