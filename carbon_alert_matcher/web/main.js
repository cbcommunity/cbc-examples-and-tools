async function clear_page() {
	document.getElementById("importPolicyContainer").classList.add("logo");
	document.getElementById("importPolicyContainer").innerHTML = "<div style=\'width: 90%; text-align: center; padding: 10px; color: #F8F8F8; font-size: 170px;'>Carbon Black.</div>";
	document.getElementById("TOTAL_ALERTS").innerText = "-"
	document.getElementById("WATCHLIST").innerText = "-"
	document.getElementById("CB_ANALYTICS").innerText = "-" 
	document.getElementById("DEVICE_CONTROL").innerText = "-" 
	document.getElementById("HOST_BASED_FIREWALL").innerText = "-" 
	document.getElementById("INTRUSION_DETECTION_SYSTEM").innerText = "-" 
	document.getElementById("CONTAINER_RUNTIME").innerText = "-" 
}
async function refresh_page(data, group, metadata, alert_id) {
	document.getElementById("importPolicyContainer").classList.remove("logo");
	document.getElementById("importPolicyContainer").innerHTML = data;
	document.getElementById("getAlertsBtn").disabled = false;
	document.getElementById("getAlertsBtnSpinner").classList.add("d-none");
	document.getElementById("TOTAL_ALERTS").innerText = metadata.TOTAL_ALERTS
	document.getElementById("WATCHLIST").innerText = metadata.WATCHLIST
	document.getElementById("CB_ANALYTICS").innerText = metadata.CB_ANALYTICS
	document.getElementById("DEVICE_CONTROL").innerText = metadata.DEVICE_CONTROL
	document.getElementById("HOST_BASED_FIREWALL").innerText = metadata.HOST_BASED_FIREWALL
	document.getElementById("INTRUSION_DETECTION_SYSTEM").innerText = metadata.INTRUSION_DETECTION_SYSTEM
	document.getElementById("CONTAINER_RUNTIME").innerText = metadata.CONTAINER_RUNTIME
	if (group == true) {
		document.getElementById("alertsHeader").innerText = "Grouped Alerts - Reason";
		document.getElementById("TOTAL_ALERTS_TEXT").innerText = "Total Alert Groups";
		document.getElementsByClassName("alert_metadata")[0].style.visibility = "hidden";

	} else {
		document.getElementById("alertsHeader").innerText = "All Alerts"
		document.getElementById("TOTAL_ALERTS_TEXT").innerText = "Total Alerts"
		document.getElementsByClassName("alert_metadata")[0].style.visibility = "visible";
	}
	if (alert_id) {
		document.getElementById("alertsHeader").innerText = "Similar Alerts"
	}
}

async function get_alerts(alert_id) {
	clear_page();
	document.getElementById("getAlertsBtn").disabled = true;
	document.getElementById("getAlertsBtnSpinner").classList.remove("d-none");
	var group = document.getElementById("group").checked;
	var cb_analytics = document.getElementById("cbAnalitycs").checked;
	var watchlists = document.getElementById("watchlists").checked;
	var usb_device_control = document.getElementById("usbDeviceControl").checked;
	var host_based_firewall = document.getElementById("hostBasedFirewall").checked;
	var intrusion_detection_system = document.getElementById("intrusionDetectionSystem").checked;
	var containers_runtime = document.getElementById("containersRuntime").checked;
	let results = await eel.get_alerts(group, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime, alert_id)();
	var parsed_data = JSON.parse(results.raw_html);
	if (parsed_data) {
		refresh_page(parsed_data, group, results.metadata, alert_id);
	}
}
