# PyAzDevOps

PyAzDevOps is a Python based library to access Azure DevOps API. It uses PAT as authentication token.

### Installation

`pip install pyazdevops`
PyAzDevOps is compatible with Python 2.7

```python
import azdevop

pat = 'xxxxxxxxxxxxxxx'
client = azdvop.AzDevOps(pat, 'myorganization')

# Get all organizations
organizations = client.get_organizations()

# Get organization by name
organization = client.get_organization('MyOrg')
print organization['subscription_details'] # Get subscription details linked to organization

# Get licenses for organization
licenses = client.get_licenses('MyOrg')
print licenses

# Get membership for organization
memberships = client.get_memberships('MyOrg')
print memberships

# Get membership with detailed entitlements
memberships = client.get_membership_details('MyOrg')
print memberships

john = next(member for member in memberships if member['user']['originId'] == '0f650ec3-2c58-1234-123-9b30ba3b8eec')

# Set user to stakeholder
client.set_stakeholder('MyOrg', john['id'])

# Set user to basic
client.set_basic('MyOrg', john['id'])

# Set user to test plan + basic
client.set_testplan('MyOrg', john['id'])

# Update user license
client.update_basic_license('MyOrg', 229) # Set Basic license to 229
client.update_testplan_license('MyOrg', 50) # Set Test Plan + Basic to 50
client.update_hosted_agent('MyOrg', 10) # Set microsoft hosted agent to 10
client.update_selfhosted_agent('MyOrg', 5) # Set self hosted agent to 5 
client.update_artifact_quota('MyOrg', 12) # Set artifacts quota to 12 GB

# Find users
results = client.find_users('MyOrg', 'john marston')
print results
```

License
----

MIT
