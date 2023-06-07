import requests


relations = {
      'enabled_by': 'RO:0002333',
      'has_input':  'RO:0002233',
      'has_output': 'RO:0002234',
      'occurs_in':  'BFO:0000066',
      'part_of': 'BFO:0000050',
    }

relations_meta = {
  "enabled_by":{
    "id":"RO:0002333",
    "color":"green"
  },
  "has_input":{
    "id":"RO:0002233",
    "color":"lightblue"
  },
  "has_output":{
    "id":"RO:0002234",
    "color":"#FFC0CB"
  },
  "occurs_in":{
    "id":"BFO:0000066",
    "color":"blue"
  },
  "part_of":{
    "id":"BFO:0000050",
    "color":"brown"
  }
}

def find_relation_meta(search_id):
  for label, idx in relations.items():
    if idx==search_id:
      return relations_meta[label]


def gen_lookup_table(self, goids):
        goApi = 'http://api.geneontology.org/api/ontology/term/'
        table = dict()
        for v in goids:
            resp = requests.get(goApi+v)
            term = resp.json()
            table[v] = {
                'id': term['goid'],
                'label': term['label']
            }
        return table