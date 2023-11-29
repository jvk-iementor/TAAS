from tetpyclient import RestClient
import json
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
# Get Varables from the environment
VRF_NAME = os.getenv('vrf_name')
UI_VIP = os.getenv('ui_vip')
OUTPUT_FOLDER = os.getenv('output_folder')
API_ENDPOINT = f'https://{UI_VIP}'
CREDS = './credentials.json'

restclient = RestClient(API_ENDPOINT,
credentials_file=CREDS,
verify=True)

appIDList = []
baseDataCollection = [
    (f'{OUTPUT_FOLDER}/flowSearchMetrics.json', '/flowsearch/metrics'),
    (f'{OUTPUT_FOLDER}/searchDim.json',  '/flowsearch/metrics'),
    (f'{OUTPUT_FOLDER}/flowSearchDim.json',  '/inventory/search/dimensions'),
    (f'{OUTPUT_FOLDER}/inventorySearchDim.json',  '/inventory/search/dimensions'),
    (f'{OUTPUT_FOLDER}/inventoryList.json',  '/filters/inventories'),
    (f'{OUTPUT_FOLDER}/userList.json',  '/users'),
    (f'{OUTPUT_FOLDER}/applications.json',  '/applications'),
    (f'{OUTPUT_FOLDER}/appScopes.json',  '/app_scopes'),
    (f'{OUTPUT_FOLDER}/workloads.json',  '/sensors'),
    (f'{OUTPUT_FOLDER}/inventoryConfigProfiles.json',  '/inventory_config/profiles'),
    (f'{OUTPUT_FOLDER}/forensicProfiles.json',  '/inventory_config/forensic_profiles'),
    (f'{OUTPUT_FOLDER}/softWareInstallID.json',  '/sw_assets/installation_id'),
    (f'{OUTPUT_FOLDER}/softWarePlatforms.json',  '/sw_assets/platforms'),
    (f'{OUTPUT_FOLDER}/forensicRules.json',  '/inventory_config/forensic_rules'),
    (f'{OUTPUT_FOLDER}/forensicIntents.json',  '/inventory_config/forensic_intents')]
machineTypes = [
    "VM1","VM3","NTP","LOG","LDAP","NETFLOW","IPFIX","NETSCALER","F5",
    "AWS","ENDPOINT","SLACK_NOTIFIER","GCP_CONNECTOR","PAGERDUTY_NOTIFIER",
    "SYSLOG_NOTIFIER","KINESIS_NOTIFIER","EMAIL_NOTIFIER","ISE","MERAKI",
    "SLACK_NOTIFIER_OVERRIDE","PAGERDUTY_NOTIFIER_OVERRIDE",
    "AZURE_CONNECTOR","EMAIL_NOTIFIER_OVERRIDE","SYSLOG_SEVERITY_MAPPING",
    "SERVICENOW","SYNC_INTERVAL","ALERT","VM3_ERSPAN","AWS_CONNECTOR","VM0"]
def getHostData(hostDataCollection)-> None:
    for host in hostDataCollection:
        file_name = host[0]
        endpoint = host[1]
        _outputs = []
        for machine in machineTypes:
            print(f'Processing {machine}')
            _output = getDataByEndpoint(endpoint)
            _outputs.append(_output)
        print(f'Saving to: {file_name}')
        saveAsJsonFile(_outputs, file_name)

def getData(endpoint_in) -> None:
    output = restclient.get(endpoint_in)
    return output.json()

def getDataByEndpoint(endpoint)-> None:
    output = restclient.get(endpoint)
    return output.json()

def saveAsJsonFile(inputFile, outputFile) -> None:
    with open (outputFile, 'w') as jsonFile:
        json.dump(inputFile, jsonFile, indent=4)

def downloadData(outputFilePath, endpoint_in) -> None:
    outputSession = restclient.download(outputFilePath,endpoint_in)

def getAppList() -> None:
    application_list = getData(f'/applications')
    _applications = []
    for application in application_list:
        appIDList.append(application)
        _applications.append(application)
    return _applications

def getBaseData(baseDataCollection)-> None:
    for command in baseDataCollection:
        file_name, endpoint = command
        print(f'Processing {command}')
        _output = getDataByEndpoint(endpoint)
        print(f'Saving to: {file_name}')
        saveAsJsonFile(_output, file_name)

def getHostData(hostDataCollection)-> None:
    for command in baseDataCollection:
        file_name, endpoint = command
        print(f'Processing {command}')
        _output = getDataByEndpoint(endpoint)
        print(f'Saving to: {file_name}')
        saveAsJsonFile(_output, file_name)

def getDefaultPoliciesByAppID(app_id) -> None:
    _defaultPolicyList = []
    _defaultPolicyListbyApp = getData(f'/applications/{app_id}/default_policies')
    print(f'Collection default policy list from {app_id}')
    for _policy in _defaultPolicyListbyApp:
        _defaultPolicyList.append(_policy)
    _app_policy = {'app_id': app_id, 'default_policies' : _defaultPolicyList}

    return app_id, _defaultPolicyList

def getCatchAllPoliciesByAppID(app_id) -> None:
    _catchAllPolicybyApp = getData(f'/applications/{app_id}/catch_all')
    print(f'Collection default policy list from {app_id}')
    _app_policy = {'app_id': app_id, 'catch_all' : _catchAllPolicybyApp}

    return app_id, _catchAllPolicybyApp

def getAllPoliciesByAppID(app_id) -> None:
    _policyList = []
    _policyListbyApp = getData(f'/applications/{app_id}/policies')
    print(f'Collection full policy list from {app_id}')
    for _policy in _policyListbyApp:
        _policyList.append(_policy)
    _app_policy = {'app_id': app_id, 'default_policies' : _policyList}

    return app_id, _policyList

def getAllCatchAllPolicies() -> None:
    _catchAllPolicyList = []
    for id in appIDList:
        app_id = id['id']
        _catchAllPolicies = getCatchAllPoliciesByAppID(app_id)
        _app_policy = {'app_id': app_id, 'catch_all' : _catchAllPolicies}
        _catchAllPolicyList.append(_app_policy)
    return _catchAllPolicyList

def getAllDefaultPolicies() -> None:
    _defaultAppPolicies = []
    for id in appIDList:
        app_id = id['id']
        _defaultPolicies = getDefaultPoliciesByAppID(app_id)
        _app_policy = {'app_id': app_id, 'default_policies' : _defaultPolicies}
        _defaultAppPolicies.append(_app_policy)
    return _defaultAppPolicies
    
def getAllPolicies() -> None:
    _allPolcies = []
    for id in appIDList:
        app_id = id['id']
        _policies = getAllPoliciesByAppID(app_id)
        _policy = {'app_id': app_id, 'policies' : _allPolcies}
        _allPolcies.append(_policies)
    return _allPolcies
