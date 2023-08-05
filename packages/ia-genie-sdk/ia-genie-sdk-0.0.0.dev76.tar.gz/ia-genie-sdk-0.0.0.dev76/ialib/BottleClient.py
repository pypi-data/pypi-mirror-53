import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ialib.GenomeInfo import Genome
from ialib.GenieMetalanguage import *

class BottleClient:
    def __init__(self, bottle_info, genome=None, ingress_nodes=[], query_nodes=[]):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

        """
        self.genome = genome
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = ingress_nodes
        self.query_nodes = query_nodes
        self.failures = []
        self.system_failures = []
        self._connected = False
        self.headers = {'content-type': 'application/json'}
        if self.genome == None:
            self.genie = None
        else:
            self.genie = self.genome.agent
        if 'secure' not in self.bottle_info or self.bottle_info['secure'] == True:
            self.secure = True
            self.url = 'https://{name}.{domain}/api'.format(**self.bottle_info)
        else:
            self.secure = False
            self.url = 'http://{name}.{domain}/api'.format(**self.bottle_info)
        return
    
    def __repr__(self):
        return '<{name}.{domain}| secure: %r, connected: %s, genie: %s, ingress_nodes: %i, query_nodes: %i, failures: %i>'.format(**self.bottle_info) %(self.secure, self._connected, self.genie, len(self.ingress_nodes), len(self.query_nodes), len(self.failures))

    def connect(self):
        "Grabs the bottle's genie's genome for node definitions."
        r = requests.post(self.url, data=json.dumps({"method": "connect", "params": {"api_key": self.api_key}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']

        self.genome = Genome(r['genome'])
        self.genie = r['genome']['agent']
        if r['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False
        return {'connection': r['connection'], 'genie': r['genie']}

    def setIngressNodes(self, nodes=[]):
        "Use list of primitive names to define where data will be sent."
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return
    
    def setQueryNodes(self, nodes=[]):
        "Use list of primitive names to define which nodes should return answers."
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return
    
    def _query(self, query, data=None):
        x = []
        for node in self.query_nodes:
            try:
                if data:
                    r = requests.post(self.url, data=json.dumps({"method": query, "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': data}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                else:
                    r = requests.post(self.url, data=json.dumps({"method": query, "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x
    
    def observe(self, data=None):
        "Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."
        x = []
        for node in self.ingress_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "observe", "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': data}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x

    def observeClassification(self, data=None):
        """
        Best practice is to send a classification to all ingress and query nodes as a singular symbol in the last event.
        This function does that for us.
        """
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "observe", "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': data}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Observe Failure:", {node['name']: e})
        return x
    
    def showStatus(self):
        x = []
        for node in set(self.ingress_nodes + self.query_nodes):
            try:
                r = requests.post(self.url, data=json.dumps({"method": "showStatus", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x
    
    def learn(self):
        x = []
        for node in self.ingress_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "observe", "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': LEARN}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x
     
     def getWM(self):
        x = []
        for node in set(self.ingress_nodes + self.query_nodes):
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getWM", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

     def getPredictions(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getPredictions", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def clearWM(self):
        x = []
        for node in self.ingress_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "observe", "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': CLEAR_WM}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def clearAllMemory(self):
        x = []
        for node in self.ingress_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "observe", "params": {"api_key": self.api_key, "primitive_id": node['id'], 'data': CLEAR_ALL_MEMORY}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x
    
    def getPerceptData(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getPerceptData", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def getCognitionData(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getCognitionData", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def getCogitated(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getCogitated", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def getDecisionTable(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getDecisionTable", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def getActionData(self):
        x = []
        for node in self.query_nodes:
            try:
                r = requests.post(self.url, data=json.dumps({"method": "getActionData", "params": {"api_key": self.api_key, "primitive_id": node['id']}, "jsonrpc": "2.0", "id": 1}), headers=self.headers).json()['response']
                x.append({node['name']: r['message']})
            except Exception as e:
                self.failures.append({node['name']: e})
                raise Exception("Query Failure:", {node['name']: e})
        return x

    def changeGenes(self, gene_data):
        """
        Use primitive names.
        This will do live updates to an existing agent, rather than stopping an agent and starting a new one as per 'injectGenome'.
        gene_data of form: 
        
            {node-name: {gene: value}}
        
        where node-id is the ID of a primitive or manipulative.

        Only works on primitive nodes at this time.
        """
        self.genome.changeGenes(gene_data)
        x = []
        for node, updates in gene_data.keys(): ## only primitive nodes at this time.
            for gene, value in updates.items():
                r = requests.post(self.url %(self.genome.primitive_map[node]), json={'api_key': self.api_key, 'query': 'updateGene', 'data': {gene: value}}).json()
                if 'error' in r or r['message'] != 'updated-genes':
                    self.system_failures.append({node: r})
                    print("System Failure:", {node: r})
                x.append({node: r['message']})
        return x