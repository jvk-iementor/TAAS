from tetpyclient import RestClient
from TAAS_Support import *

def main() -> None:
    print('Collecting Application Data')
    getAppList()
    print('Collecting Base Data')
    getBaseData(baseDataCollection)
    defaultPolicies = getAllDefaultPolicies()
    saveAsJsonFile(defaultPolicies,f'{OUTPUT_FOLDER}/policies.json')
    catchAllPolies = getAllCatchAllPolicies()
    saveAsJsonFile(catchAllPolies, f'{OUTPUT_FOLDER}/catchAll.json')

if __name__ == "__main__":
    main()