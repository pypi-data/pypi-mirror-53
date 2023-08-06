from pbiapi import PowerBIAPIClient

c = PowerBIAPIClient("tenant_id", "client_id", "client_secret")

print(c.bogus())
