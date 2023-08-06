import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, knora, BulkImport
import requests


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="http://0.0.0.0:3333", help="URL of the Knora server")
parser.add_argument("-u", "--user", default="root@example.com", help="Username for Knora")
parser.add_argument("-p", "--password", default="test", help="The password for login")
parser.add_argument("-P", "--projectcode", default="0826", help="Project short code")
parser.add_argument("-O", "--ontoname", default="teimww", help="Shortname of ontology")

args = parser.parse_args()


con = knora(args.server, args.user, args.password)
schema = con.create_schema(args.projectcode, args.ontoname)

# ----------------------------------------------------------------
# Buch erstellen
res_info1 = con.create_resource(schema, "book", "test-book", {
   "title": "Romeo und Julia"
})

pprint(res_info1)

# ----------------------------------------------------------------
# IRI zu property isAuthorOf muss ersetzt werden
res_info2 = con.create_resource(schema, "person", "test-person", {
    "firstName": "William",
    "lastName": "Shakespeare",
    "isAuthorOf": res_info1['iri']
})

pprint(res_info2)
