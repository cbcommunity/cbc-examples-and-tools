#!/usr/local/bin/python3.9
import datetime
import os
import subprocess
import time
import json
import requests
import eel
from cbc_sdk import CBCloudAPI
from cbc_sdk.platform import Policy

__title__ = 'Policy Copier App'
__version__ = 'v1.0.0'


def get_cbc(profile):
    "text"
    return CBCloudAPI(profile=profile, integration_name=(__title__ + __version__))


def credentials_handler():
    "text"
    path = os.path.expanduser( '~' )
    credentials = path + "/.carbonblack/credentials.cbc"
    contents = ''
    try:
        with open(credentials) as credentials_f:
            contents = credentials_f.readlines()
    except FileNotFoundError:
        with open(credentials, "w") as credentials_f:
            credentials_f.write('')
        subprocess.call(['chmod', '600', credentials])
    return contents, credentials


@eel.expose
def delete_org(org_type, org_key):
    "text"
    contents, credentials_file = credentials_handler()
    if org_type == 'export_org':
        for num, line in enumerate(contents):
            if line.startswith(f"[PolicyApp_ExportProfile_{org_key}_"):
                contents[num] = line.replace('[', '[DELETED_')
            else:
                continue
    elif org_type == 'import_org'.strip():
        for num, line in enumerate(contents):
            if line == f"[PolicyApp_ImportProfile_{org_key.upper()}]\n":
                contents[num] = line.replace('[', '[DELETED_')
            else:
                continue
    with open(credentials_file, "w") as updated_credentials:
        updated_credentials.writelines(contents)


@eel.expose
def read_config():
    "text"
    contents, credentials_file = credentials_handler()

    global IMPORT_ORG_PROFILES
    IMPORT_ORG_PROFILES = {'export': {}, 'import': {}}
    for line in contents:
        if line.startswith("[PolicyApp_ImportProfile_"):
            profile_name = line[1:-2]
            cbc = get_cbc(profile_name)
            IMPORT_ORG_PROFILES['import'][cbc.credentials.org_key] = {
                "URL": cbc.credentials.url,
                "TOKEN": cbc.credentials.token,
                "ORG_KEY": cbc.credentials.org_key,
                "PROFILE": profile_name
            }
        elif line.startswith("[PolicyApp_ExportProfile_"):
            profile_name = line[1:-2]
            cbc = get_cbc(profile_name)
            IMPORT_ORG_PROFILES['export'] = {
                "URL": cbc.credentials.url,
                "TOKEN": cbc.credentials.token,
                "ORG_KEY": cbc.credentials.org_key,
                "PROFILE": profile_name
            }


@eel.expose
def add_new_org():
    "text"

    org_id = time.monotonic_ns()
    html = '<div class="card m-3 mb-4 border">\n'
    html += f'    <form class="p-3 was-validated newOrg" id="{org_id}">\n'
    html += '        <div class="mb-3">\n'
    html += f'            <label for="new_ImportOrgKey_{org_id}" class="form-label mb-0"><h6>Org Key</h6></label>\n'
    html += f'            <input value="" required class="form-control form-control-sm text-muted is-invalid" id="new_ImportOrgKey_{org_id}">\n'
    html += '        </div>\n'
    html += '        <div class="mb-3">\n'
    html += f'            <label for="new_ImportURL_{org_id}" class="form-label mb-0"><h6>URL</h6></label>\n'
    html += f'            <input value="" required class="form-control form-control-sm text-muted is-invalid" id="new_ImportURL_{org_id}">\n'
    html += '        </div>\n'
    html += '        <div class="mb-3">\n'
    html += f'            <label for="new_apiId_{org_id}" class="form-label mb-0"><h6>API ID</h6></label>\n'
    html += f'            <input value="" required class="form-control form-control-sm text-muted is-invalid" id="new_apiId_{org_id}">\n'
    html += '        </div>\n'
    html += '        <div class="mb-3">\n'
    html += f'            <label for="new_apiSecretKey_{org_id}" class="form-label mb-0"><h6>API Secret Key</h6></label>\n'
    html += f'            <input value="" required class="form-control form-control-sm text-muted is-invalid" id="new_apiSecretKey_{org_id}">\n'
    html += '        </div>\n'
    # html += '        <div class="mb-3">\n'
    # html += f'            <label for="new_notes_{id}" class="form-label mb-0"><h6>Notes</h6></label>\n'
    # html += f'            <input value="" class="form-control form-control-sm text-muted" id="new_notes_{id}">\n'
    # html += '        </div>\n'
    html += '    </form>\n'
    html += '</div>\n'

    return html


@eel.expose
def save_org_data(orgs, org_type):
    "text"
    lines = ''
    for org in orgs:
        data = orgs[org]
        profile_name = 'PolicyApp_ImportProfile'
        if org_type == 'export_org':
            profile_name = 'PolicyApp_ExportProfile'
        if data['URL'] == '' or data['ORG_KEY'] == '' or data['API_ID'] == '' or data['API_SECRET'] == '':
            continue
        lines += f'\n[{profile_name}_{data["ORG_KEY"]}_{data["API_ID"]}]\n'
        if data["URL"][-1] != '/':
            data["URL"] += '/'
        lines += f'url={data["URL"]}\n'
        lines += f'token={data["API_SECRET"]}/{data["API_ID"]}\n'
        # if data["NOTES"]:
        #     lines += f'notes={data["NOTES"]}\n'
        lines += f'org_key={data["ORG_KEY"]}\n'

    if lines != '':
        with open("/Users/hkaragitliev/.carbonblack/credentials.cbc", "a") as updated_credentials:
            updated_credentials.write(lines)
        read_config()


@eel.expose
def import_orgs_settings():
    "text"
    read_config()
    org_profiles = IMPORT_ORG_PROFILES['import']
    html = ''
    for org in org_profiles:
        url = org_profiles[org]['URL']
        api_secret, api_id = org_profiles[org]['TOKEN'].split('/')
        # notes = ''
        html += '<div class="card m-3 mb-4 border">\n'
        html += f'    <button type="button" onClick="delete_org(\'import_org\', \'{org}_{api_id}\')" data-bs-dismiss="modal" class="btn btn-outline-danger btn-sm position-absolute m-3 end-0 btn-sm">\n'
        html += '      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">\n'
        html += '        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>\n'
        html += '        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>\n'
        html += '      </svg>\n'
        html += '    </button>\n'
        html += '    <fieldset disabled>\n'
        html += '        <form class="p-3 mt-3">\n'
        html += '            <div class="mb-3">\n'
        html += f'                <label for="ImportOrgKey_{org}_{api_id}" class="form-label mb-0"><h6>Org Key</h6></label>\n'
        html += f'                <input value="{org}" class="form-control form-control-sm text-muted" id="ImportOrgKey_{org}_{api_id}">\n'
        html += '            </div>\n'
        html += '            <div class="mb-3">\n'
        html += f'                <label for="ImportURL_{org}_{api_id}" class="form-label mb-0"><h6>URL</h6></label>\n'
        html += f'                <input value="{url}" class="form-control form-control-sm text-muted" id="ImportURL_{org}_{api_id}">\n'
        html += '            </div>\n'
        html += '            <div class="mb-3">\n'
        html += f'                <label for="apiId_{org}_{api_id}" class="form-label mb-0"><h6>API ID</h6></label>\n'
        html += f'                <input value="{api_id}" class="form-control form-control-sm text-muted" id="apiId_{org}_{api_id}">\n'
        html += '            </div>\n'
        html += '            <div class="mb-3">\n'
        html += f'                <label for="apiSecretKey_{org}_{api_id}" class="form-label mb-0"><h6>API Secret Key</h6></label>\n'
        html += f'                <input type="password" value="{api_secret}" class="form-control form-control-sm text-muted" id="apiSecretKey_{org}_{api_id}">\n'
        html += '            </div>\n'
        # html += '            <div class="mb-3">\n'
        # html += f'                <label for="notes_{org}" class="form-label mb-0"><h6>Notes</h6></label>\n'
        # html += f'                <input value="{notes}" class="form-control form-control-sm text-muted" id="notes_{org}">\n'
        # html += '            </div>\n'
        html += '        </form>\n'
        html += '    </fieldset>\n'
        html += '</div>\n'

    return html


@eel.expose
def export_org_settings():
    "text"
    data = {"org_key": "",
            "url": "",
            "api_id": "",
            "api_secret_key": ""}
    read_config()
    org_profile = IMPORT_ORG_PROFILES['export']
    if 'ORG_KEY' not in org_profile:
        return json.dumps(data)
    api_secret_key, api_id = org_profile['TOKEN'].split('/')

    return json.dumps(
        {"org_key": org_profile['ORG_KEY'],
         "url": org_profile['URL'],
         "api_id": api_id,
         "api_secret_key": api_secret_key})


def generate_policy_html_table(data):
    "text"
    html = ' <dl class="row lh-1 hr-margin-y">\n'
    # FIXME this needs to handle nested structures
    for line in data:
        if isinstance(data[line], (str, int, bool)):
            html += f'     <dt class="col-sm-6">{line}</dt>\n'
            if data[line] == '':
                data[line] = 'null'
            html += f'     <dd class="col-sm-6">{data[line]}</dd>\n'
        elif isinstance(data[line], dict):
            html += f'     <dt class="col-sm-6">{line}</dt>\n'
            html += f'     <dd class="col-sm-6">{data[line]}</dd>\n'
        elif isinstance(data[line], list):
            html += f'     <dt class="col-sm-6">{line}</dt>\n'
            html += f'     <dd class="col-sm-6">{data[line]}</dd>\n'
    html += ' </dl>\n'

    return html


@eel.expose
def get_import_data_confirmation(data):
    "text"
    org_info = {"raw_html": ""}
    html = ''
    html += '<ul class="list-group mt-3 mb-3">'
    for policy in data:
        html += '  <li class="list-group-item d-flex justify-content-between align-items-start">'
        html += '    <div class="ms-2 me-auto mt-1">'
        html += f'      <div><span class="fw-bold">Policy</span> {policy}</div>'
        if data[policy]:
            html += f'      <span class="fw-bold">Rules</span> {", ".join(map(str, data[policy]))}'
        else:
            html += '      <span class="fw-bold">Rules</span> None'
        html += '    </div>'
        html += '  </li>'
    html += '</ul>'

    org_info["raw_html"] = html

    return json.dumps(org_info)


@eel.expose
def get_import_orgs_info():
    "text"
    org_profiles = IMPORT_ORG_PROFILES['import']

    org_info = {"org_keys": "",
                "data_timestamp": str(datetime.datetime.now()),
                "orgs_count_total": 0,
                "rule_count_total": 0,
                "policy_count_total": 0,
                "raw_html": "",
                "orgs_metainfo_html": ""}

    html = ''
    for import_org in org_profiles:
        cbc = get_cbc(org_profiles[import_org]['PROFILE'])
        policy_info = cbc.select(Policy)
        org_info["policy_count_total"] += len(policy_info)
        for policy in policy_info:
            org_info["rule_count_total"] += len(policy.rules)
            html += '<div class="card small mt-0 m-3 border">\n'
            html += '    <div class="card-header bg-light">\n'
            html += '        <dl class="row lh-1 hr-margin-y">\n'
            html += '            <dt class="col-sm-4">URL</dt>\n'
            html += f'            <dd class="col-sm-8">{org_profiles[import_org]["URL"]}</dd>\n'
            html += '            <dt class="col-sm-4">Org Key</dt>\n'
            html += f'            <dd class="col-sm-8">{org_profiles[import_org]["ORG_KEY"]}</dd>\n'
            html += '            <dt class="col-sm-4">Policy id</dt>\n'
            html += f'            <dd class="col-sm-8">{policy.id}</dd>\n'
            html += '            <dt class="col-sm-4">Policy Name</dt>\n'
            html += f'            <dd class="col-sm-8">{policy.name}</dd>\n'
            html += '            <dt class="col-sm-4">Priority Level</dt>\n'
            html += f'            <dd class="col-sm-8">{policy.priority_level}</dd>\n'
            html += '            <dt class="col-sm-4">Is System</dt>\n'
            html += f'            <dd class="col-sm-8">{policy.is_system}</dd>\n'
            html += '            <dt class="col-sm-4">Total Rules</dt>\n'
            html += f'            <dd class="col-sm-8">{len(policy.rules)}</dd>\n'
            html += '            <dt class="col-sm-4">Description</dt>\n'
            html += f'            <dd class="col-sm-8">{policy.description}</dd>\n'
            html += '        </dl>\n'
            html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#import_policy_{policy.id}_{policy.org_key}_modal">View Policy Details</a>'
            html += f'        <div class="modal modal-xl fade" id="import_policy_{policy.id}_{policy.org_key}_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'
            html += '          <div class="modal-dialog modal-dialog-scrollable">'
            html += '            <div class="modal-content">'
            html += '              <div class="modal-header">'
            html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
            html += '              </div>'
            html += '              <div class="modal-body">'
            html += f'                {generate_policy_html_table(policy._info)}'
            html += '              </div>'
            html += '            </div>'
            html += '          </div>'
            html += '        </div>'
            html += '    </div>\n'
            html += '    <div class="card-body p-0">\n'
            for rule in policy.rules:
                html += '        <div class="row mx-3 align-items-center py-2 position-relative border-bottom border-200">\n'
                html += '            <div class="col-1">\n'
                html += '            </div>\n'
                html += '            <div class="col py-1 position-static">\n'
                html += '                <div class="d-flex align-items-center">\n'
                html += '                    <dl class="row pt-3 lh-1 hr-margin-y">\n'
                html += '                        <dt class="col-sm-4">Rule id</dt>\n'
                html += f'                        <dd class="col-sm-8">{rule["id"]}</dd>\n'
                html += '                        <dt class="col-sm-4">Required</dt>\n'
                html += f'                        <dd class="col-sm-8">{rule["required"]}</dd>\n'
                html += '                        <dt class="col-sm-4">Action</dt>\n'
                html += f'                        <dd class="col-sm-8">{rule["action"]}</dd>\n'
                html += '                        <dt class="col-sm-4">Operation</dt>\n'
                html += f'                        <dd class="col-sm-8">{rule["operation"]}</dd>\n'
                html += '                        <dt class="col-sm-4">Application</dt>\n'
                html += '                        <dd class="col-sm-8">\n'
                html += '                            <dl class="row">\n'
                html += '                                <dt class="col-sm-6">type</dt>\n'
                html += f'                                <dd class="col-sm-6">{rule["application"]["type"]}</dd>\n'
                html += '                                <dt class="col-sm-6">value</dt>\n'
                html += f'                                <dd class="col-sm-6">{rule["application"]["value"]}</dd>\n'
                html += '                            </dl>\n'
                html += '                        </dd>\n'
                html += '                    </dl>\n'
                html += '                </div>\n'
                html += '            </div>\n'
                html += '        </div>\n'
            html += '    </div>\n'
            html += '</div>\n'
        org_info["raw_html"] = html

    org_info["raw_html"] = html
    org_info["org_keys"] = ', '.join(org_profiles.keys())
    org_info["orgs_count_total"] = len(org_profiles.keys())

    return json.dumps(org_info)


@eel.expose
def get_export_org_info():
    "text"
    read_config()
    profile = IMPORT_ORG_PROFILES['export']
    cbc = get_cbc(profile['PROFILE'])
    policy_info = cbc.select(Policy)

    org_info = {"org_key": profile['ORG_KEY'],
                "url": profile['URL'],
                "data_source": "HTTP Request",
                "data_timestamp": str(datetime.datetime.now()),
                "policy_count_total": len(policy_info),
                "rule_count_total": 0,
                "raw_html": "",
                "raw_data": {}}

    html = ''
    for policy in policy_info:
        policy.refresh()
        raw_data = policy._info.copy()
        del raw_data['id']
        del raw_data['update_time']
        del raw_data['rule_configs']
        del raw_data['sensor_configs']
        policy_id = str(policy.id)
        org_info['raw_data'][policy_id] = raw_data
        org_info["rule_count_total"] += len(policy.rules)
        html += '<div class="card small mt-0 m-3 border">\n'
        html += '    <div class="card-header bg-light">\n'
        html += '        <div class="form-check mb-3">\n'
        html += f'            <input class="form-check-input" type="checkbox" value="" onClick="select_policy(\'export_policy\', {policy_id}, {""})" id="export_policy_{policy_id}">\n'
        html += '        </div>\n'
        html += '        <dl class="row lh-1 hr-margin-y">\n'
        html += '            <dt class="col-sm-4">Policy id</dt>\n'
        html += f'            <dd class="col-sm-8">{policy_id}</dd>\n'
        html += '            <dt class="col-sm-4">Policy Name</dt>\n'
        html += f'            <dd class="col-sm-8">{policy.name}</dd>\n'
        html += '            <dt class="col-sm-4">Priority Level</dt>\n'
        html += f'            <dd class="col-sm-8">{policy.priority_level}</dd>\n'
        html += '            <dt class="col-sm-4">Is System</dt>\n'
        html += f'            <dd class="col-sm-8">{policy.is_system}</dd>\n'
        html += '            <dt class="col-sm-4">Total Rules</dt>\n'
        html += f'            <dd class="col-sm-8">{len(policy.rules)}</dd>\n'
        html += '            <dt class="col-sm-4">Description</dt>\n'
        html += f'            <dd class="col-sm-8">{policy.description}</dd>\n'
        html += '        </dl>\n'
        html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#export_policy_{policy_id}_modal">View Policy Details</a>'
        html += f'        <div class="modal modal-xl fade" id="export_policy_{policy_id}_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        html += '          <div class="modal-dialog modal-dialog-scrollable">'
        html += '            <div class="modal-content">'
        html += '              <div class="modal-header">'
        html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
        html += '              </div>'
        html += '              <div class="modal-body">'
        html += f'                {generate_policy_html_table(policy._info)}'
        html += '              </div>'
        html += '            </div>'
        html += '          </div>'
        html += '        </div>'
        html += '    </div>\n'
        html += '    <div class="card-body p-0">\n'
        for rule in policy.rules:
            rule_id = str(rule["id"])
            rule_identifier = str(policy.id) + '_' + str(rule_id)
            html += '        <div class="row mx-3 align-items-center py-2 position-relative border-bottom border-200">\n'
            html += '            <div class="col-1">\n'
            html += '                <div class="form-check">\n'
            html += f'                    <input class="form-check-input export_rule_{policy_id}" type="checkbox" rule="{rule_id}" onClick="select_policy(\'export_rule\', {policy_id}, {rule_id})" id="export_rule_{rule_identifier}">\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '            <div class="col py-1 position-static">\n'
            html += '                <div class="d-flex align-items-center">\n'
            html += '                    <dl class="row pt-3 lh-1 hr-margin-y">\n'
            html += '                        <dt class="col-sm-4">Rule id</dt>\n'
            html += f'                        <dd class="col-sm-8">{rule_id}</dd>\n'
            html += '                        <dt class="col-sm-4">Required</dt>\n'
            html += f'                        <dd class="col-sm-8">{rule["required"]}</dd>\n'
            html += '                        <dt class="col-sm-4">Action</dt>\n'
            html += f'                        <dd class="col-sm-8">{rule["action"]}</dd>\n'
            html += '                        <dt class="col-sm-4">Operation</dt>\n'
            html += f'                        <dd class="col-sm-8">{rule["operation"]}</dd>\n'
            html += '                        <dt class="col-sm-4">Application</dt>\n'
            html += '                        <dd class="col-sm-8">\n'
            html += '                            <dl class="row">\n'
            html += '                                <dt class="col-sm-6">type</dt>\n'
            html += f'                                <dd class="col-sm-6">{rule["application"]["type"]}</dd>\n'
            html += '                                <dt class="col-sm-6">value</dt>\n'
            html += f'                                <dd class="col-sm-6">{rule["application"]["value"]}</dd>\n'
            html += '                            </dl>\n'
            html += '                        </dd>\n'
            html += '                    </dl>\n'
            html += '                </div>\n'
            html += '            </div>\n'
            html += '        </div>\n'
        html += '    </div>\n'
        html += '</div>\n'
    org_info["raw_html"] = html

    return json.dumps(org_info)


def sanitise_strings(data):
    "text"
    for item in data:
        data[item] = data[item].replace(" ", "_")
    if data['policy_name_prefix']:
        data['policy_name_prefix'] += '_'

    return data


def create_policy(data, raw_data, settings):
    "text"
    import_orgs = IMPORT_ORG_PROFILES['import']
    settings = sanitise_strings(settings)
    for org in import_orgs:
        for policy in data:
            req_body = raw_data[policy].copy()
            req_body['rules'] = []
            req_body['org_key'] = import_orgs[org]['ORG_KEY']
            req_body['name'] = settings['policy_name_prefix'] + \
                req_body['name']
            for raw_rule in raw_data[policy]['rules']:
                if str(raw_rule['id']) in data[policy]:
                    req_body['rules'].append(raw_rule)

            req_body_json = json.dumps(req_body)
            req_url = f'{import_orgs[org]["URL"]}policyservice/v1/orgs/{import_orgs[org]["ORG_KEY"]}/policies'
            req_headers = {'Content-Type': 'application/json',
                           'integration_name': f'{__title__} {__version__}',
                           'X-AUTH-TOKEN': import_orgs[org]["TOKEN"]}

            requests.post(url=req_url, data=req_body_json, headers=req_headers)


@eel.expose
def import_org_data(selected_policies, raw_data, import_settings):
    "text"
    create_policy(selected_policies, raw_data, import_settings)


if __name__ == "__main__":
    eel.init("web")
    read_config()
    eel.start("index.html")
