#!/usr/local/bin/python3
import json
import get_alerts as ga
import eel


@eel.expose
def get_alerts(group, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime, alert_id):
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

    get_similar = False
    if alert_id != "" and alert_id is not None:
        req_metadata["alert_id"] = alert_id
        get_similar = True
    alerts = ga.get_alerts(req_metadata)

    metadata = {
        "TOTAL_ALERTS": len(alerts),
        "CB_ANALYTICS": 0,
        "WATCHLIST": 0,
        "DEVICE_CONTROL": 0,
        "HOST_BASED_FIREWALL": 0,
        "INTRUSION_DETECTION_SYSTEM": 0,
        "CONTAINER_RUNTIME": 0,
    }

    html = ''
    for alert in alerts:
        if group is False:
            metadata[alerts[alert]['type']] += 1
        html += '<div class="card small mt-0 m-3 border">\n'
        html += '    <div class="card-body p-3 position-relative">\n'

        # "Match Similar" Button
        if get_similar is False:
            if group is True:
                first_id = next(iter(alerts[alert]['alerts']))
                alert_id = first_id
            else:
                alert_id = alert
            html += f'        <button type="button" onClick="get_alerts(\'{alert_id}\')" id="get_similar_{alert_id}" class="btn btn-sm btn-outline-primary position-absolute top-0 end-0 m-3">Match Similar</button>\n'

        # Alert Details
        html += '        <dl class="row lh-1 hr-margin-y">\n'

        # Rest of the card content
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

        # Modal Trigger for Details
        html += '        </dl>\n'
        if group is False and get_similar is False:
            html += f'       <a href="#" data-bs-toggle="modal" data-bs-target="#alert_{alert}_modal">Details</a>\n'
            html += f'        <div class="modal modal-xl fade" id="alert_{alert}_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\n'
            html += '          <div class="modal-dialog modal-dialog-scrollable">\n'
            html += '            <div class="modal-content">\n'
            html += '              <div class="modal-header">\n'
            html += '                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\n'
            html += '              </div>\n'
            html += '              <div class="modal-body">\n'
            html += f'                {alerts[alert]["raw"]}\n'
            html += '              </div>\n'
            html += '            </div>\n'
            html += '          </div>\n'
            html += '        </div>\n'

        html += '    </div>\n'
        html += '</div>\n'
    results = {"raw_html": json.dumps(html), "metadata": metadata}

    return results


if __name__ == "__main__":
    eel.init("web")
    eel.start("index.html")
