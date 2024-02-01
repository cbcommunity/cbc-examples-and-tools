#!/usr/local/bin/python3
import datetime
import json
import get_alerts as ga
import eel


@eel.expose
def get_alerts(group, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime):
    "text"
    req_metadata = {
        "group": group,
        "cb_analytics": cb_analytics,
        "watchlists": watchlists,
        "usb_device_control": usb_device_control,
        "host_based_firewall": host_based_firewall,
        "intrusion_detection_system": intrusion_detection_system,
        "containers_runtime": containers_runtime,
        "severity": []
    }
    alerts = ga.get_alerts(req_metadata)

    html = ''
    for alert in alerts:
        html += '<div class="card small mt-0 m-3 border">\n'
        html += '    <div class="card-body p-3 position-relative">\n'
        html += '        <button type="button" class="btn btn-sm btn-outline-primary position-absolute top-0 end-0 m-3" data-bs-toggle="modal" data-bs-target="#matchSimilarModal">Match Similar</button>\n'
        html += '        <dl class="row lh-1 hr-margin-y">\n'
        html += '        <div class="modal fade" id="matchSimilarModal" tabindex="-1" aria-labelledby="matchSimilarModalLabel" aria-hidden="true">'
        html += '          <div class="modal-dialog">'
        html += '            <div class="modal-content">'
        html += '              <div class="modal-header">'
        html += '                <h6 class="modal-title" id="matchSimilarModalLabel">Match Similar Alerts</h6>'
        html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
        html += '              </div>'
        html += '              <div class="modal-body">'
        html += '                <form>'
        html += '                  <div class="mb-3">'
        html += '                    <label for="startDate" class="form-label">Start Date</label>'
        html += '                    <input type="datetime-local" class="form-control" id="startDate" required>'
        html += '                  </div>'
        html += '                  <div class="mb-3">'
        html += '                    <label for="endDate" class="form-label">End Date</label>'
        html += '                    <input type="datetime-local" class="form-control" id="endDate" required>'
        html += '                  </div>'
        html += '                  <button type="submit" class="btn btn-primary">Submit</button>'
        html += '                </form>'
        html += '              </div>'
        html += '            </div>'
        html += '          </div>'
        html += '        </div>'
        if group is False:
            html += '            <dt class="col-sm-3">Alert ID</dt>\n'
            html += f'            <dd class="col-sm-7">{alert}</dd>\n'
        else:
            html += '            <dt class="col-sm-3">Alert IDs</dt>\n'
            html += f'            <dd class="col-sm-7">\n'
            for alert_id in alerts[alert]["alerts"]:
                html += f'<div>{alert_id}</div>\n'
            html += '</dd>\n'
        for item in alerts[alert]:
            try:
                if item in ['raw', 'alerts']:
                    continue
            except KeyError:
                continue
            html += f'<dt class="col-sm-3">{item.capitalize()}</dt>\n'
            html += f'<dd class="col-sm-7">{alerts[alert][item]}</dd>\n'
        html += '        </dl>\n'
        if group is False:
            html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#alert_{alert}_modal">Details</a>'
            html += f'        <div class="modal modal-xl fade" id="alert_{alert}_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">'
            html += '          <div class="modal-dialog modal-dialog-scrollable">'
            html += '            <div class="modal-content">'
            html += '              <div class="modal-header">'
            html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
            html += '              </div>'
            html += '              <div class="modal-body">'
            html += f'                {alerts[alert]["raw"]}'
            html += '              </div>'
            html += '            </div>'
            html += '          </div>'
            html += '        </div>'
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
