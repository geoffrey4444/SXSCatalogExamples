import sxs
from sxs import zenodo as zen
import json
import argparse

p = argparse.ArgumentParser(description = "Get SXS Zenodo metadata")
p.add_argument("--output_json", help = "Name of output metadata JSON file", \
                                required = True)
p.add_argument("--output_res", help = "Name of output resolutiosn JSON file", \
                               required = True)
args = p.parse_args()

md = zen.api.Records.search(q='communities:sxs AND access_right:open')

catalog_json = {}
for simulation in md:
    sxs_id = simulation['title'].split(' ')[-1]
    if (len(sxs_id.split(':')) == 3):
        if (sxs_id.split(':')[-2] == 'BBH'):
            catalog_json[sxs_id] = simulation

with open(args.output_json, 'w') as file:
    file.write(json.dumps(catalog_json))

print("There are " + str(len(catalog_json.keys())) \
                   + " BBH simulations in the catalog.")

def resolutions_for_simulation(sxs_id):
    resolutions = []
    files = catalog_json[sxs_id]['files']
    for file in files:
        split_filename = file['filename'].split('/')
        if (str(split_filename[-1]) == "Horizons.h5"):
            resolutions.append(int(split_filename[-2].split('Lev')[-1]))
    return sorted(resolutions)

resolutions_available = {}
for simulation in catalog_json:
    resolutions_available[simulation] = resolutions_for_simulation(simulation)
    
with open(args.output_res, 'w') as file:
    file.write(json.dumps(resolutions_available))
