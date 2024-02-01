#!/usr/local/bin/python3
import datetime
import json
import get_alerts as ga
import eel


@eel.expose
def get_alerts(match_similar, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime):
    "text"
    req_metadata = {
        "match_similar": match_similar,
        "cb_analytics": cb_analytics,
        "watchlists": watchlists,
        "usb_device_control": usb_device_control,
        "host_based_firewall": host_based_firewall,
        "intrusion_detection_system": intrusion_detection_system,
        "containers_runtime": containers_runtime
    }
    alerts = ga.get_alerts(req_metadata)

    html = ''
    for alert in alerts:
        html += '<div class="card small mt-0 m-3 border">\n'
        # html += '    <div class="card-header bg-light">\n'
        # html += f'        <div class="modal modal-xl fade" id="import_policy_asf" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'
        # html += '          <div class="modal-dialog modal-dialog-scrollable">'
        # # html += '            <div class="modal-content">'
        # # html += '              <div class="modal-header">'
        # # html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
        # # html += '              </div>'
        # # html += '              <div class="modal-body">'
        # # html += '                  <dl class="row lh-1 hr-margin-y">\n'
        # # html += f'                     <dt class="col-sm-6">{alerts[alert]["type"]}</dt>\n'
        # # html += f'                     <dd class="col-sm-6">asdasd</dd>\n'
        # # html += '                  </dl>\n'
        # # html += '              </div>'
        # # html += '            </div>'
        # html += '          </div>'
        # html += '        </div>'
        # html += '    </div>\n'
        html += '    <div class="card-body p-3">\n'
        html += '        <dl class="row lh-1 hr-margin-y">\n'
        html += '            <dt class="col-sm-3">Alert ID</dt>\n'
        html += f'            <dd class="col-sm-7">{alert}</dd>\n'
        for item in alerts[alert]:
            html += f'<dt class="col-sm-3">{item.capitalize()}</dt>\n'
            html += f'<dd class="col-sm-7">{alerts[alert][item]}</dd>\n'
        html += '        </dl>\n'
        html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#import_policyasfasfsaf_modal">Details</a>'
        html += '    </div>\n'
        html += '</div>\n'
        # org_info["raw_html"] = html

    # org_info["raw_html"] = html
    # org_info["data_timestamp"] = str(datetime.datetime.now())
    # org_info["org_keys"] = ', '.join(alerts.keys())
    # org_info["orgs_count_total"] = len(alerts.keys())

    return json.dumps(html)


if __name__ == "__main__":
    eel.init("web")
    eel.start("index.html")
