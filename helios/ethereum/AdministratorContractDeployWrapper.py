from django.conf import settings
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from helios.ethereum.interface import ContractInterface

class AdministratorContractDeployWrapper:

    __instance = None

    w3 = Web3(HTTPProvider(settings.HTTP_PROVIDER_WEB3))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    contractInterface = ContractInterface(w3, 'HeliosAdministrator', settings.CONTRACTS_DIR)
    contractInstance = None

    @staticmethod
    def getInstance():
        if AdministratorContractDeployWrapper.__instance is None:
            AdministratorContractDeployWrapper()
        return AdministratorContractDeployWrapper.__instance

    def  __init__(self):
        if AdministratorContractDeployWrapper.__instance is None:
            AdministratorContractDeployWrapper.__instance = self
            self.contractInterface.compile_source_files()

    def set_deployed_contract_from_address(self, contract_address):
        if (self.contractInstance is None):
            self.contractInterface.set_deployed_contract(contract_address)
            self.contractInstance = self.contractInterface.get_instance()
            return self.contractInstance

    def register_new_election_contract(self, contract_address, short_name):
        if (self.contractInstance is not None):
            self.contractInterface.send('createElection', [contract_address, short_name])