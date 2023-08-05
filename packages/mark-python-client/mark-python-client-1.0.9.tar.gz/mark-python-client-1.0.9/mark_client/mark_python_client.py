"""
the mark_python_client script can be used to instantiate a MarkClient object that can be used to communicate with
the MARK server and deal with the MongoDB to add or fetch data
"""
import requests
import json
from argparse import ArgumentParser
from operator import itemgetter


class MarkClient:

  def __init__(self):
    self.server_url = None
    self.verbose = False
    self.proxy = None

  def get_server_status(self):
    print "- Get the status of the server"
    parameters = {'method': 'status', 'id': 123}
    response = requests.post(self.server_url, data=json.dumps(parameters), proxies=self.proxy)
    if self.verbose:
      print "-- Status of the get_server_status request:"
      print "-- " + str(response.json())
    response_data = response.json()["result"]
    print "-- Current Active Jobs: " + str(response_data["executor.job.running"])
    return response_data

  def add_evidence(self, evidence_data):
    print "- Adding Evidence Data to the server"
    post_data = {'method': 'addEvidence', 'params': [evidence_data], 'id': 123}
    response = requests.post(self.server_url, json=post_data, proxies=self.proxy)
    if self.verbose:
      print "-- Status of the add_evidence request:"
      print "-- " + str(response.json())

  def find_evidence(self, label, subject):
    print "- Fetching Evidences from to the server"
    parameters = {'method': 'findEvidence', 'params': json.dumps([label, subject]), 'id': 123}
    response = requests.get(self.server_url, params=parameters, proxies=self.proxy)
    if self.verbose:
      print "-- Status of the find_evidence request:"
      print "-- " + str(response.json())
    result_data = response.json()["result"]
    return result_data

  def get_ranked_list(self, label):
    print"- Fetching Evidence Ranked List from the server"
    result_data = []
    parameters = {'method': 'findEvidence', 'id': 123, 'params': json.dumps([label])}
    response = requests.get(self.server_url, params=parameters, proxies=self.proxy)
    if self.verbose:
      print "-- Status of the get_ranked_list request:"
      print "-- " + str(response.json())
    result_data = result_data + response.json()["result"]
    # sort the fetched data in descending order (highest score at the top)
    sorted_result_data = sorted(result_data, key=itemgetter('score'), reverse=True)
    return sorted_result_data

  def get_unique_subject_count(self, subject):
    print "- Fetching count of unique subjects in Evidences"
    parameters = {'method': 'findUniqueSubjects',
                  'params': json.dumps([subject]),
                  'id': 123}
    response = requests.get(self.server_url, params=parameters, proxies=self.proxy)
    if self.verbose:
      print "-- Status of the get_unique_subject_count request:"
      print "-- " + str(response.json())
    result_data = response.json()["result"]
    return result_data

  def set_server_url(self, url):
    self.server_url = url

  def get_server_url(self):
    return self.server_url

  def set_verbose(self, boolean):
    self.verbose = boolean

  def get_verbose(self):
    return self.verbose

  def set_proxy(self, proxy):
    self.proxy = proxy

  def get_proxy(self):
    return self.proxy
