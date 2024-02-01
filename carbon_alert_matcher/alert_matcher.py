#!/usr/local/bin/python3
import datetime
import json
import get_alerts as ga
import eel


@eel.expose
def get_alerts():
    "text"
    alerts = ga.get_alerts()

    # clean, alerts_info = dict()
    print('clean', alerts, '\n')
    html = ''
    # for alert in alerts:
    #     html += '<div class="card small mt-0 m-3 border">\n'
    #     html += '    <div class="card-header bg-light">\n'
    #     html += '        <dl class="row lh-1 hr-margin-y">\n'
    #     html += '            <dt class="col-sm-4">URL</dt>\n'
    #     html += f'            <dd class="col-sm-8">{alerts[import_org]["URL"]}</dd>\n'
    #     html += '            <dt class="col-sm-4">Org Key</dt>\n'
    #     html += f'            <dd class="col-sm-8">{alerts[import_org]["ORG_KEY"]}</dd>\n'
    #     html += '            <dt class="col-sm-4">Policy id</dt>\n'
    #     html += f'            <dd class="col-sm-8">{policy.id}</dd>\n'
    #     html += '            <dt class="col-sm-4">Policy Name</dt>\n'
    #     html += f'            <dd class="col-sm-8">{policy.name}</dd>\n'
    #     html += '            <dt class="col-sm-4">Priority Level</dt>\n'
    #     html += f'            <dd class="col-sm-8">{policy.priority_level}</dd>\n'
    #     html += '            <dt class="col-sm-4">Is System</dt>\n'
    #     html += f'            <dd class="col-sm-8">{policy.is_system}</dd>\n'
    #     html += '            <dt class="col-sm-4">Total Rules</dt>\n'
    #     html += f'            <dd class="col-sm-8">{len(policy.rules)}</dd>\n'
    #     html += '            <dt class="col-sm-4">Description</dt>\n'
    #     html += f'            <dd class="col-sm-8">{policy.description}</dd>\n'
    #     html += '        </dl>\n'
    #     html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#import_policy_{policy.id}_{policy.org_key}_modal">View Policy Details</a>'
    #     html += f'        <div class="modal modal-xl fade" id="import_policy_{policy.id}_{policy.org_key}_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'
    #     html += '          <div class="modal-dialog modal-dialog-scrollable">'
    #     html += '            <div class="modal-content">'
    #     html += '              <div class="modal-header">'
    #     html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
    #     html += '              </div>'
    #     html += '              <div class="modal-body">'
    #     html += f'                {generate_policy_html_table(policy._info)}'
    #     html += '              </div>'
    #     html += '            </div>'
    #     html += '          </div>'
    #     html += '        </div>'
    #     html += '    </div>\n'
    #     html += '    <div class="card-body p-0">\n'
    #     html += '<div class="accordion accordion-flush" id="import_rules_accordion">'
    #     html += '  <div class="accordion-item">'
    #     html += '    <h2 class="accordion-header">'
    #     html += f'      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#rules_{policy.id}_{policy.org_key}" aria-expanded="false" aria-controls="flush-collapseOne">'
    #     html += '        Rules'
    #     html += '      </button>'
    #     html += '    </h2>'
    #     html += f'    <div id="rules_{policy.id}_{policy.org_key}" class="accordion-collapse collapse">'
    #     html += '      <div class="accordion-body">'
    #     for rule in policy.rules:
    #         html += '        <div class="row mx-3 align-items-center py-2 position-relative border-bottom border-200">\n'
    #         html += '            <div class="col-1">\n'
    #         html += '            </div>\n'
    #         html += '            <div class="col py-1 position-static">\n'
    #         html += '                <div class="d-flex align-items-center">\n'
    #         html += '                    <dl class="row pt-3 lh-1 hr-margin-y">\n'
    #         html += '                        <dt class="col-sm-4">Rule id</dt>\n'
    #         html += f'                        <dd class="col-sm-8">{rule["id"]}</dd>\n'
    #         html += '                        <dt class="col-sm-4">Required</dt>\n'
    #         html += f'                        <dd class="col-sm-8">{rule["required"]}</dd>\n'
    #         html += '                        <dt class="col-sm-4">Action</dt>\n'
    #         html += f'                        <dd class="col-sm-8">{rule["action"]}</dd>\n'
    #         html += '                        <dt class="col-sm-4">Operation</dt>\n'
    #         html += f'                        <dd class="col-sm-8">{rule["operation"]}</dd>\n'
    #         html += '                        <dt class="col-sm-4">Application</dt>\n'
    #         html += '                        <dd class="col-sm-8">\n'
    #         html += '                            <dl class="row">\n'
    #         html += '                                <dt class="col-sm-6">type</dt>\n'
    #         html += f'                                <dd class="col-sm-6">{rule["application"]["type"]}</dd>\n'
    #         html += '                                <dt class="col-sm-6">value</dt>\n'
    #         html += f'                                <dd class="col-sm-6">{rule["application"]["value"]}</dd>\n'
    #         html += '                            </dl>\n'
    #         html += '                        </dd>\n'
    #         html += '                    </dl>\n'
    #         html += '                </div>\n'
    #         html += '            </div>\n'
    #         html += '        </div>\n'
    #     html += '            </div>'
    #     html += '        </div>'
    #     html += '    </div>'
    #     html += '</div>'
    #     html += '    </div>\n'
    #     html += '</div>\n'
    #     org_info["raw_html"] = html

    # org_info["raw_html"] = html
    # org_info["data_timestamp"] = str(datetime.datetime.now())
    # org_info["org_keys"] = ', '.join(alerts.keys())
    # org_info["orgs_count_total"] = len(alerts.keys())

    # return json.dumps(org_info)


if __name__ == "__main__":
    eel.init("web")
    eel.start("index.html")
