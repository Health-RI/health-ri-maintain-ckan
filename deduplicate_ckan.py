from ckanapi import RemoteCKAN
from collections import defaultdict
from dateutil.parser import parse as parse_date

ckan = RemoteCKAN('https://ckan.healthdata.nl', apikey='your-api-key')

# 1. Fetch all active packages
start = 0
rows = 1000
packages = []

while True:
    result = ckan.action.package_search(q='state:active', start=start, rows=rows)
    packages.extend(result['results'])
    if start + rows >= result['count']:
        break
    start += rows

print(f"Total active packages fetched: {len(packages)}")

# 2. Extract URI (from top-level or extras)
def extract_uri(pkg):
    if pkg.get('uri'):
        return pkg['uri']
    for extra in pkg.get('extras', []):
        if extra['key'] == 'uri' and extra['value']:
            return extra['value']
    return None

# 3. Group packages by URI
uri_to_packages = defaultdict(list)

for pkg in packages:
    uri = extract_uri(pkg)
    if uri:
        uri_to_packages[uri].append(pkg)

# 4. Filter for duplicated URIs
duplicates = {uri: pkgs for uri, pkgs in uri_to_packages.items() if len(pkgs) > 1}

# 5. Keep the most recently modified one per duplicated URI
for uri, pkg_group in duplicates.items():
    pkg_group.sort(key=lambda x: parse_date(x['metadata_modified']), reverse=True)
    to_keep = pkg_group[0]
    to_delete = pkg_group[1:]

    print(f"\n✅ Keeping: {to_keep['name']} for URI: {uri}")
    for pkg in to_delete:
        print(f" → Marking as deleted: {pkg['name']} (modified: {pkg['metadata_modified']})")
        ckan.action.package_patch(id=pkg['id'], state='deleted')


