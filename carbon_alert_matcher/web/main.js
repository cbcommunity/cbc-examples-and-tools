async function refresh_page(data, group) {
	document.getElementById("importPolicyContainer").innerHTML = data;
	document.getElementById("getAlertsBtn").disabled = false;
	document.getElementById("getAlertsBtnSpinner").classList.add("d-none");
	if (group == true) {
		document.getElementById("alertsHeader").innerText = "Grouped Alerts - Reason"
	} else {
		document.getElementById("alertsHeader").innerText = "All Alerts"
	}
}

async function get_alerts() {
	document.getElementById("getAlertsBtn").disabled = true;
	document.getElementById("getAlertsBtnSpinner").classList.remove("d-none");
	var group = document.getElementById("group").checked;
	var cb_analytics = document.getElementById("cbAnalitycs").checked;
	var watchlists = document.getElementById("watchlists").checked;
	var usb_device_control = document.getElementById("usbDeviceControl").checked;
	var host_based_firewall = document.getElementById("hostBasedFirewall").checked;
	var intrusion_detection_system = document.getElementById("intrusionDetectionSystem").checked;
	var containers_runtime = document.getElementById("containersRuntime").checked;
	let alerts = await eel.get_alerts(group, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime)();
	var parsed_data = JSON.parse(alerts);
	if (parsed_data) {
		refresh_page(parsed_data, group);
	}
}
