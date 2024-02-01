var import_org_data_set = false;
var export_org_data_set = false;
var import_data_selected = false;
var export_data = {}
var import_settings = {}
var export_org_raw_data = {}

function arrayRemove(arr, value) {
		return arr.filter(function(ele){
				return ele != value;
		});
}

function get_export_settings() {
		import_settings["policy_name_prefix"] = document.getElementById("import_policy_name_prefix").value
}

async function save_import_orgs_settings() {
		var data = document.querySelectorAll(".newOrg");
		var new_orgs = {}
		data.forEach(org => {
				var org_key = document.getElementById("new_ImportOrgKey_" + org.id).value
				new_orgs[org_key] = {
					"URL": document.getElementById("new_ImportURL_" + org.id).value,
					"API_ID": document.getElementById("new_apiId_" + org.id).value,
					"API_SECRET": document.getElementById("new_apiSecretKey_" + org.id).value,
					"ORG_KEY": document.getElementById("new_ImportOrgKey_" + org.id).value,
					// "NOTES": document.getElementById("new_notes_" + org.id).value
				}
		});
		await eel.save_org_data(new_orgs, 'import_orgs')();
		await eel.read_config()();
		let new_data = await eel.refresh_org_data('import')();
		refresh_org_data(JSON.parse(new_data), 'import');
}

async function refresh_org_data(data, type) {
		if (type == 'export') {
				document.getElementById("export_meta_url").textContent = data.url;
				document.getElementById("export_meta_org_key").textContent = data.org_key;
				// document.getElementById("export_meta_data_source").textContent = data.data_source;
				document.getElementById("export_meta_timestamp").textContent = data.data_timestamp;
				document.getElementById("export_meta_rule_count_total").textContent = data.rule_count_total;
				document.getElementById("export_meta_policy_count_total").textContent = data.policy_count_total;
				document.getElementById("exportPolicyContainer").innerHTML = data.raw_html;
				document.getElementById("getPolicyInfoBtnSpinner").classList.add("d-none");
				if (data.org_key != "-"){
						document.getElementById("getAlertsBtn").disabled = false;
				}
		} else if (type == 'import') {
				let policyInfoBtnStat = false;
				let org_keys = "-";
				let orgs_count_total = "-";
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
				// document.getElementById("import_meta_org_keys").textContent = org_keys;
				// document.getElementById("import_meta_orgs_count_total").textContent = orgs_count_total;
				// document.getElementById("import_meta_timestamp").textContent = data.data_timestamp;
				// document.getElementById("import_meta_rule_count_total").textContent = data.rule_count_total;
				// document.getElementById("import_meta_policy_count_total").textContent = data.policy_count_total;
				document.getElementById("importPolicyContainer").innerHTML = raw_html;
				document.getElementById("getImportPolicyInfoBtn").disabled = policyInfoBtnStat;
				document.getElementById("getImportPolicyInfoBtnSpinner").classList.add("d-none");
		}
		// enable_import_export();
}

async function print_import_data() {
		let data = await eel.get_import_data_confirmation(export_data)();
		var parsed_data = JSON.parse(data);
		document.getElementById("importDataModalBody").innerHTML = parsed_data.raw_html;
}

async function import_data() {
		document.getElementById("importDataBtn").disabled = true;
		// document.getElementById("compareDataBtn").disabled = true;
		document.getElementById("importDataBtnSpinner").classList.remove("d-none");
		document.getElementById("importOrgsCard").classList.add("disableddiv");
		get_export_settings()
		let response = await eel.import_org_data(export_data, export_org_raw_data, import_settings)();
		get_import_orgs_info(response)
		document.getElementById("importDataBtn").disabled = false;
		// document.getElementById("compareDataBtn").disabled = false;
		document.getElementById("importDataBtnSpinner").classList.add("d-none");
		document.getElementById("importOrgsCard").classList.remove("disableddiv");
}


function select_policy(export_type, policy_id, rule_id) {
		if (rule_id) {
				rule_id = rule_id.toString();
		}
		policy_id = policy_id.toString();
		if (export_type == 'export_policy'){
				const checkbox = document.querySelectorAll(".export_rule_" + policy_id);
				const state = document.getElementById("export_policy_" + policy_id).checked;
				if (state == true) {
						import_data_selected = true;
						export_data[policy_id] = []
				} else {
						delete export_data[policy_id];
						if (Object.keys(export_data).length == 0) {
								import_data_selected = false;
						}
				}
				checkbox.forEach(check => {
				  	check.checked = state;
						if (state == true) {
								const words = check.id.split('_');
								export_data[policy_id].push(words[words.length - 1]);
						}
				});
		}
		else if (export_type == 'export_rule') {
				if (document.getElementById("export_rule_" + policy_id + '_' + rule_id).checked == true) {
						document.getElementById("export_policy_" + policy_id).checked = true;
						import_data_selected = true;
						if (policy_id in export_data) {
								export_data[policy_id].push(rule_id);
						} else {
								export_data[policy_id] = []
								export_data[policy_id].push(rule_id);
						}
				} else {
						export_data[policy_id] = arrayRemove(export_data[policy_id], rule_id);
				}
		}
		// enable_import_export();
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
		console.log(parsed_data)
		if (parsed_data) {
			export_org_data_set = true;
			// export_org_raw_data = parsed_data.raw_data;
			export_org_raw_data = parsed_data;
			document.getElementById("getAlertsBtn").disabled = false;
			document.getElementById("getAlertsBtnSpinner").classList.add("d-none");
			if (group == true) {
				document.getElementById("alertsHeader").innerText = "Grouped Alerts - Reason"
			} else {
				document.getElementById("alertsHeader").innerText = "All Alerts"
			}
			refresh_org_data(parsed_data, 'import');
			// enable_import_export();
		}
}

async function get_import_orgs_info(refresh_info) {
		document.getElementById("getImportPolicyInfoBtn").disabled = true;
		document.getElementById("getImportPolicyInfoBtnSpinner").classList.remove("d-none");
		let org_data = await eel.get_import_orgs_info(refresh_info)();
		var parsed_data = JSON.parse(org_data);
		import_org_data_set = false;
		if (parsed_data && refresh_info != true) {
				import_org_data_set = true;
				refresh_org_data(parsed_data, 'import');
		} else if (refresh_info == true){
				let new_data = await eel.refresh_org_data('import')();
				refresh_org_data(JSON.parse(new_data), 'import');
		}
		// enable_import_export();
}
