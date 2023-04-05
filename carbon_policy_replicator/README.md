# Carbon Policy Replicator
Replicate policies and their rules to an unlimited number organizations across different Environments.

The `Carbon Policy Replicator` is a user-friendly Python-based GUI tool that easily transfers policies and rules from one organization to
numerous others. This tool can replicate one or more policies with just a few clicks or save your data so that you can return to it later.

Under the hood, this tool uses the `Carbon Black Cloud Python SDK` for things like Authentication and Credentials Handling, Retrieving Data from Carbon Black Cloud and Handling Errors and Exceptions. This is one example of how the SDK can be used to build powerful tools and integrations to streamline your workflows.

**Latest Version:** 1.0.0

**Release Date:** January 17, 2023

**Supported OS:** MacOS

## App Features

* Replicate policies and rules from one organization to any number of other organizations across multiple environments
* View multi-org policy and rule information from a single source

Have an idea of a functionality that you want in the tool? Make a suggestion as a [GitHub issue](https://github.com/cbcommunity/cbc-examples-and-tools/issues).

## Future Extensions
* Compare Policy information between organizations (coming in next release)
* Save and Load Policy information (coming in next release)
* Copy Core Prevention and Host Based Firewall rules

<img width="900" alt="Screenshot 2023-03-16 at 12 33 28" src="https://user-images.githubusercontent.com/74309356/225590737-e36fac22-6dbf-4a29-9713-77d6e450632a.png">

## Getting Started

1. Download, or clone the tool.
  * To download, navigate to the repository base, and click `Code` > `Download ZIP`
  * To clone it, navigate to the repository base, click `Code` and go trough the `Clone` sequence
    ```shell
    git clone git@github.com:cbcommunity/cbc-examples-and-tools.git
    ```
2. Navigate to the directory where you downloaded/cloned the tool and install the dependencies by running the following command in your console.
```shell
cd cbc-examples-and-tools/carbon_policy_replicator
pip install -r requirements.txt
```
3. Run the tool
Run the following command in your console
```shell
python main.py
```

## Terms
**Export Org** - describes the organization that you want to replicate policies and rules from. This is always a single org.

**Import Orgs** - describes multiple organizations that you want to replicate policies and rules to. These can be any number of orgs located trough different CBC environments.

## Setting up the Tool
To start using the app, fill in your credentials into the tools' Settings. **Export Org** and **Import Orgs** have separate settings menus.
* Add the **Export Org** credentials
  * Click the Settings icon in the top-right corner of the **Export Org** window, and insert your data, and hit Save. `Org Key`, `URL`, `API ID` and `API Secret Key` are required.
  * To check your configuration, click **Get Policy Info** button. The policy and rule configuration for the organization should load.
* Add the **Import Orgs** credentials
  * Click the Settings icon in the top-right corner of the **Import Orgs** window. Click `Add Org` and insert the required `Org Key`, `URL`, `API ID` and `API Secret Key`. Repeat this step for as many organizations as you need, and click `Save`.
  * To check your configuration, click **Get Policy Info** button in the **Import Orgs** window. The policy and rule configuration for the organizations that you set up should load.

## Using the Tool
After you are done [Setting up the Tool](#setting-up-the-tool), you can move to reviewing or replication policy information.
* To view the current policy setup, click the `Get Policy Info` button in either **Export Org** or **Import Orgs** window.
* To replicate a policy, you need to select atleast one policy from the **Export Org**, then click the `Import Data` button. After you confirm your input in the pop-up prompt, the policy and its selected rules(selected rules) will be replicated in all the **Import Orgs** that you setup.

## Resources:
Carbon Black Cloud Python SDK
* [PyPi](https://pypi.org/project/carbon-black-cloud-sdk/)
* [Github](https://github.com/carbonblack/carbon-black-cloud-sdk-python/tree/master)
* [Read the Docs](https://carbon-black-cloud-python-sdk.readthedocs.io/)

Developer Network - Carbon Black API Documentation
* [Developer Network](https://developer.carbonblack.com)
* [Policy Service API](https://developer.carbonblack.com/reference/carbon-black-cloud/platform/latest/policy-service/)

Postman
* [CBC Postman Collection](https://documenter.getpostman.com/view/19038029/2s8YK4to5o#intro)

## Have questions or feedback?
* Open an issue in the [GitHub Repository](https://github.com/cbcommunity/cbc-examples-and-tools/issues)
* Other ways to [contact us](https://developer.carbonblack.com/contact)
