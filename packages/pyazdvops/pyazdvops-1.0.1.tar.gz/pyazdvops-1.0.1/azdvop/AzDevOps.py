import requests, logging, json
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

license_map = {
  'basic': 'ms.vss-vstsuser',
  'testplan': 'ms.vss-testmanager-web',
  'hostedagent': 'ms.build-release-hosted-pipelines',
  'selfhostedagent': 'ms.build-release-private-pipelines',
  'artifacts': 'ms.artifacts'
}

class AzDevOps:
  auth = None
  main_organization = ''
  error_codes = [203, 400, 401, 403, 404, 500]

  def __init__(self, pat, main_organization):
    omitted = pat[:5]
    for i in range(len(pat) - 5):
      omitted = omitted + '*'
    logger.debug('Initializing with pat {omitted}'.format(omitted = omitted))
    self.auth = HTTPBasicAuth('', pat)
    self.main_organization = main_organization

  def handle_response(self, response):
    if response.status_code in self.error_codes:
      try:
        logger.critical('Status code: {status_code}, Body: {body}'.format(
          status_code = str(response.status_code),
          body = response.text
        ))
      except UnicodeEncodeError:
        logger.critical(u'Status code: {status_code}, Body: {body}'.format(
          status_code = str(response.status_code),
          body = response.text
        ))
      raise Exception('Failed to perform request.')
    return response

  def get(self, url, headers = {}):
    logger.debug('GET ' + url + ', Headers: ' + json.dumps(headers))
    r = requests.get(url, auth = self.auth)
    return self.handle_response(r)

  def post(self, url, body, headers = {}):
    logger.debug('POST ' + url + ', Headers: ' + json.dumps(headers) + ', Body: ' + json.dumps(body))
    r = requests.post(url, auth = self.auth, headers=headers, data=json.dumps(body))
    return self.handle_response(r)
  
  def patch(self, url, body, headers = {}):
    logger.debug('PATCH {}, Headers: {}, Body: {}'.format(url, json.dumps(headers), json.dumps(body)))
    r = requests.patch(url, auth = self.auth, headers = headers, data = json.dumps(body))
    return self.handle_response(r)

  def query_organization(self, ids, organization = None):
    if organization == None:
      organization = self.main_organization
    r = self.post('https://dev.azure.com/{organization}/_apis/Contribution/HierarchyQuery'.format(organization = self.main_organization), {
      'contributionIds': ids }, {
      'Accept': 'application/json;api-version=5.0-preview.1;excludeUrls=true;enumsAsNumbers=true;msDateFormat=true;noArrayWrap=true',
      'Content-Type': 'application/json'
    })
    return json.loads(r.text)
  
  def get_organization(self, organization_name):
    r = self.query_organization(["ms.vss-admin-web.organization-admin-new-overview-component","ms.vss-admin-web.organization-admin-overview-data-provider"], organization_name)
    organization = r['dataProviders']['ms.vss-admin-web.organization-admin-overview-data-provider']

    r = self.get('https://commerceprodwus21.vscommerce.visualstudio.com/_apis/Subscription/Subscription?providerNamespaceId=0&accountId={account_id}'.format(account_id=organization['id']))
    subscription_details = json.loads(r.text)
    organization['subscription_details'] = subscription_details
    return organization
  
  def find_users(self, organization_name, query):
    r = self.post('https://dev.azure.com/{organization_name}/_apis/IdentityPicker/Identities'.format(organization_name = organization_name), {
        "query": query,
        "identityTypes":["user","group"],
        "operationScopes":["ims","source"],
        "properties":[
          "DisplayName",
          "IsMru",
          "ScopeName",
          "SamAccountName",
          "Active",
          "SubjectDescriptor",
          "Department",
          "JobTitle",
          "Mail",
          "MailNickname",
          "PhysicalDeliveryOfficeName",
          "SignInAddress",
          "Surname",
          "Guest",
          "TelephoneNumber",
          "Description"],
        "filterByAncestorEntityIds":[],
        "filterByEntityIds":[],
        "options":{
          "MinResults":40,
          "MaxResults":40
        }
      }, {
        'Accept': 'application/json;api-version=6.0-preview.1;excludeUrls=true',
        'Content-Type': 'application/json'
      })
    results = json.loads(r.text)
    if len(results['results']) > 0:
      return results['results'][0]['identities']
    else:
      return []

  def get_organizations(self):
    r = self.query_organization(['ms.vss-features.my-organizations-data-provider'])
    return r['dataProviders']['ms.vss-features.my-organizations-data-provider']['organizations']

  def get_licenses(self, organization):
    r = self.get('https://vsaex.dev.azure.com/{organization}/_apis/UserEntitlementSummary?select=accesslevels%2Clicenses'.format(organization=organization))
    return json.loads(r.text)['licenses']
  
  def get_memberships(self, organization):
    r = self.get('https://vsaex.dev.azure.com/{organization}/_apis/userentitlements?api-version=5.1-preview.2&top=1000&skip=0'.format(organization=organization))
    return json.loads(r.text)['members']
  
  def get_membership(self, organization, member_id):
    r = self.get('https://vsaex.dev.azure.com/{organization}/_apis/userentitlements/{member_id}?api-version=5.1-preview.2'.format(member_id=member_id, organization=organization))
    return json.loads(r.text)

  def get_membership_details(self, organization):
    members = self.get_memberships(organization)
    for member in members:
      member = self.get_membership(organization, member['id'])
    return members
  
  def set_stakeholder(self, organization, member_id):
    self.patch('https://vsaex.dev.azure.com/{organization}/_apis/UserEntitlements/{member_id}'.format(member_id = member_id, organization = organization), [{
      'from': '',
      'op': 2,
      'path': '/accessLevel',
      'value': {
        'accountLicenseType': 5,
        'licensingSource': 1
      }
    }], {
      'Accept': 'application/json;api-version=5.1-preview.2;excludeUrls=true',
      'Content-Type': 'application/json-patch+json'
    })

  def set_basic(self, organization, member_id):
    self.patch('https://vsaex.dev.azure.com/{organization}/_apis/UserEntitlements/{member_id}'.format(member_id = member_id, organization = organization), [{
      'from': '',
      'op': 2,
      'path': '/accessLevel',
      'value': {
        'accountLicenseType': 2,
        'licensingSource': 1
      }
    }], {
      'Accept': 'application/json;api-version=5.1-preview.2;excludeUrls=true',
      'Content-Type': 'application/json-patch+json'
    })

  def set_testplan(self, organization, member_id):
    self.patch('https://vsaex.dev.azure.com/{organization}/_apis/UserEntitlements/{member_id}'.format(member_id = member_id, organization = organization), [{
      'from': '',
      'op': 2,
      'path': '/accessLevel',
      'value': {
        'accountLicenseType': 4,
        'licensingSource': 1
      }
    }], {
      'Accept': 'application/json;api-version=5.1-preview.2;excludeUrls=true',
      'Content-Type': 'application/json-patch+json'
    })

  def update_license(self, organization, quantity, licence_type):
    if licence_type not in license_map:
      raise Exception('License type is invalid. Use following: {}'.format(license_map))
    organization = self.get_organization(organization)
    self.post('https://commerceprodwus21.vscommerce.visualstudio.com/_apis/OfferSubscription/OfferSubscription?billingTarget={organizationId}&skipSubscriptionValidation=true'.format(organizationId=organization['id']), {
      "azureSubscriptionId": organization['subscription_details']['subscriptionId'],
      "committedQuantity": str(quantity),
      "offerMeter": {
        "galleryId": license_map[licence_type]
      },
      "renewalGroup": 'null'
    }, {
      'Accept': 'application/json;api-version=5.1-preview.1;excludeUrls=true;enumsAsNumbers=true;msDateFormat=true;noArrayWrap=true',
      'Content-Type': 'application/json'
    })

  def update_basic_license(self, organization, quantity):
    self.update_license(organization, quantity, 'basic')
  
  def update_testplan_license(self, organization, quantity):
    self.update_license(organization, quantity, 'testplan')
  
  def update_hosted_agent(self, organization, hosted_agent_count):
    self.update_license(organization, hosted_agent_count, 'hostedagent')

  def update_selfhosted_agent(self, organization, selfhosted_agent_count):
    self.update_license(organization, selfhosted_agent_count, 'selfhostedagent')

  def update_artifact_quota(self, organization, quota):
    self.update_license(organization, quota, 'artifacts')
