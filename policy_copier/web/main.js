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

async function delete_org(org_type, org_id) {
		if (org_type == "export_org") {
				var org_key = document.getElementById("ExportOrgKey").value;
				document.getElementById("ExportURL").value = "";
				document.getElementById("ExportApiId").value = "";
				document.getElementById("ExportOrgKey").value = "";
				document.getElementById("ExportApiSecretKey").value = "";
				if (org_key != "") {
						await eel.delete_org(org_type, org_key)();
				}
		} else if (org_type == "import_org") {
				// var org_key = document.getElementById("ExportOrgKey").value;
				document.getElementById("ImportURL_"  + org_id).value = "";
				document.getElementById("apiId_" + org_id).value = "";
				document.getElementById("ImportOrgKey_" + org_id).value = "";
				document.getElementById("apiSecretKey_" + org_id).value = "";
				if (org_id != "") {
						await eel.delete_org(org_type, org_id)();
				}
		}
		await eel.read_config()();
}

async function add_new_org() {
		let data = await eel.add_new_org()();
		var new_html = data + document.getElementById("importOrgsSettingsModalPlaceholder").innerHTML;
		document.getElementById("importOrgsSettingsModalPlaceholder").innerHTML = new_html;
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
}

async function save_export_org_settings() {
		var new_org = {}
		var org_key = document.getElementById("ExportOrgKey").value
		new_org[org_key] = {
			"URL": document.getElementById("ExportURL").value,
			"API_ID": document.getElementById("ExportApiId").value,
			"API_SECRET": document.getElementById("ExportApiSecretKey").value,
			"ORG_KEY": document.getElementById("ExportOrgKey").value,
			// "NOTES": document.getElementById("new_notes_" + org.id).value
		}
		await eel.save_org_data(new_org, 'export_org')();
		await eel.read_config()();
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
		get_import_orgs_info()
		document.getElementById("importDataBtn").disabled = false;
		// document.getElementById("compareDataBtn").disabled = false;
		document.getElementById("importDataBtnSpinner").classList.add("d-none");
		document.getElementById("importOrgsCard").classList.remove("disableddiv");
}

function enable_import_export() {
		if (export_org_data_set == true && Object.keys(export_data).length > 0 && import_org_data_set == true) {
				document.getElementById("importDataBtn").disabled = false;
				// document.getElementById("compareDataBtn").disabled = false;
		} else {
				document.getElementById("importDataBtn").disabled = true;
				// document.getElementById("compareDataBtn").disabled = true;
		}
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
		enable_import_export();
}

async function get_export_org_settings() {
		let data = await eel.export_org_settings()();
		var credentials = JSON.parse(data);
		document.getElementById("ExportURL").value = credentials.url;
		document.getElementById("ExportApiId").value = credentials.api_id;
		document.getElementById("ExportApiSecretKey").value = credentials.api_secret_key;
		document.getElementById("ExportOrgKey").value = credentials.org_key;
		if (credentials.org_key != "") {
				document.getElementById("ExportOrgDeleteOrgBtn").classList.remove("d-none");
				document.getElementById("ImportOrgSettingsForm").disabled = true;
				document.getElementById("ImportOrgSettingsSaveBtn").classList.add("d-none");
		} else {
				document.getElementById("ExportOrgDeleteOrgBtn").classList.add("d-none");
				document.getElementById("ImportOrgSettingsForm").disabled = false;
				document.getElementById("ImportOrgSettingsSaveBtn").classList.remove("d-none");
		}
}

async function get_import_orgs_settings() {
		let data = await eel.import_orgs_settings()();
		document.getElementById("importOrgsSettingsModalPlaceholder").innerHTML = data;
}

async function get_export_org_info() {
		document.getElementById("getPolicyInfoBtn").disabled = true;
		document.getElementById("getPolicyInfoBtnSpinner").classList.remove("d-none");
		let org_data = await eel.get_export_org_info()();
		var parsed_data = JSON.parse(org_data);
		if (parsed_data) {
				export_org_data_set = true;
				export_org_raw_data = parsed_data.raw_data;
				enable_import_export();
		}
		document.getElementById("export_meta_url").textContent = parsed_data.url;
		document.getElementById("export_meta_org_key").textContent = parsed_data.org_key;
		document.getElementById("export_meta_data_source").textContent = parsed_data.data_source;
		document.getElementById("export_meta_timestamp").textContent = parsed_data.data_timestamp;
		document.getElementById("export_meta_rule_count_total").textContent = parsed_data.rule_count_total;
		document.getElementById("export_meta_policy_count_total").textContent = parsed_data.policy_count_total;
		document.getElementById("exportPolicyContainer").innerHTML = parsed_data.raw_html;
		// document.getElementById("savePolicyInfoBtn").classList.remove("d-none");
		document.getElementById("getPolicyInfoBtn").disabled = false;
		document.getElementById("getPolicyInfoBtnSpinner").classList.add("d-none");
}

async function get_import_orgs_info() {
		document.getElementById("getImportPolicyInfoBtn").disabled = true;
		document.getElementById("getImportPolicyInfoBtnSpinner").classList.remove("d-none");
		let org_data = await eel.get_import_orgs_info()();
		var parsed_data = JSON.parse(org_data);
		if (parsed_data) {
				import_org_data_set = true;
				enable_import_export();
		}
		document.getElementById("import_meta_org_keys").textContent = parsed_data.org_keys;
		document.getElementById("import_meta_orgs_count_total").textContent = parsed_data.orgs_count_total;
		document.getElementById("import_meta_timestamp").textContent = parsed_data.data_timestamp;
		document.getElementById("import_meta_rule_count_total").textContent = parsed_data.rule_count_total;
		document.getElementById("import_meta_policy_count_total").textContent = parsed_data.policy_count_total;
		document.getElementById("importPolicyContainer").innerHTML = parsed_data.raw_html;
		document.getElementById("getImportPolicyInfoBtn").disabled = false;
		document.getElementById("getImportPolicyInfoBtnSpinner").classList.add("d-none");
}
