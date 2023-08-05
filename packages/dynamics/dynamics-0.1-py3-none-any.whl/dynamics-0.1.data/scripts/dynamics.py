import adal
import pandas
import requests


class Entity:

    def __init__(self, connection, name):
        self.endpoint = f'{connection.resource}/api/data/v9.1/'
        self.name = name
        
        context = adal.AuthenticationContext("https://login.microsoftonline.com/common/")
        
        result = context.acquire_token_with_username_password(
            connection.resource,
            connection.login,
            connection.password,
            '2ad88395-b77d-4561-9441-d0e40824f9bc')
                
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': 'Bearer ' + result['accessToken'],
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
        }
        
        result = self.session.get(f"{self.endpoint}EntityDefinitions(LogicalName='{self.name}')?$select=LogicalCollectionName")
        result = result.json()
        
        self.base = f"{self.endpoint}{result['LogicalCollectionName']}"

    def read(self) -> pandas.DataFrame:
        result = self.session.get(f'{self.base}')
        result = result.json()
        result = result['value']
        return pandas.DataFrame(result)

    def write(self, data: pandas.DataFrame):
        pass


class Connection:

    def __init__(self, resource, login, password):
        self.resource = resource
        self.login = login
        self.password = password

    def entity(self, name) -> Entity:
        pass
