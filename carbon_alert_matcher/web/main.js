var import_org_data_set = false;
var export_org_data_set = false;
var import_data_selected = false;
var export_data = {}
var import_settings = {}
var export_org_raw_data = {}

async function refresh_org_data(data) {
	let policyInfoBtnStat = false;
	let raw_html = "";
	if (data.orgs_count_total == 0) {
		org_keys = "-"
		orgs_count_total = "-"
		policyInfoBtnStat = true;
		raw_html = "<div class='alert alert-warning m-3 text-center' role='alert'>Import Orgs not configured.</div>"
	} else {
		org_keys = 'asd';
		orgs_count_total = data.orgs_count_total;
		policyInfoBtnStat = false;
		raw_html = data;
	}
	document.getElementById("importPolicyContainer").innerHTML = raw_html;
	document.getElementById("getImportPolicyInfoBtn").disabled = policyInfoBtnStat;
	document.getElementById("getImportPolicyInfoBtnSpinner").classList.add("d-none");
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
	let org_data = await eel.get_alerts(group, cb_analytics, watchlists, usb_device_control, host_based_firewall, intrusion_detection_system, containers_runtime)();
	var parsed_data = JSON.parse(org_data);
	if (parsed_data) {
		export_org_data_set = true;
		export_org_raw_data = parsed_data;
		document.getElementById("getAlertsBtn").disabled = false;
		document.getElementById("getAlertsBtnSpinner").classList.add("d-none");
		if (group == true) {
			document.getElementById("alertsHeader").innerText = "Grouped Alerts - Reason"
		} else {
			document.getElementById("alertsHeader").innerText = "All Alerts"
		}
		refresh_org_data(parsed_data);
	}
}
