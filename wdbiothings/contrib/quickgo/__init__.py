"""
yeast:
ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/YEAST/goa_yeast.gaf.gz

all uniprot:
ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz

The file on the ftp site doesn't include to the uniprot and interpro-derived annotations
only the SGD annotations. Can only see them in the API??


"""
from collections import defaultdict

import pandas as pd
import requests
from io import StringIO

from tqdm import tqdm

data = {
  'tax': '559292',
  'termUse': 'ancestor',
  'relType': 'IPO=',
  'customRelType': 'IPOR+-?=',
  'col': 'proteinDB,proteinID,proteinSymbol,qualifier,goID,goName,aspect,evidence,ref,with,proteinTaxon,date,from,splice',
  'select': 'normal',
  'start': '0',
  'count': '25',
  'format': 'tsv',
  'gz': 'false',
  'limit': '100000000'
}

response = requests.post('https://www.ebi.ac.uk/QuickGO/GAnnotation', data=data)
df = pd.read_csv(StringIO(response.text), sep='\t')
df = df.query("Evidence != 'ND'")
del df['With']
df.to_dict("records")

"""

def group_ref(thisdf):
    row = thisdf.iloc[0]
    row['Reference'] = list(thisdf['Reference'])
    row['DB'] = list(thisdf['DB'])
    row['Source'] = list(thisdf['Source'])
    return row

d = defaultdict(lambda : defaultdict(dict))
for key, this_df in tqdm(df.groupby(['ID','GO ID','Evidence'])):
    d[key[0]][key[1]][key[2]] = group_ref(this_df).to_dict()

for k,v in d.items():
    d[k] = dict(v)
d = dict(d)
"""

#gb = df.iloc[:100].groupby(['ID','GO ID','Evidence','Source','DB'])['Reference'].apply(list)
#gb.ix['Q12272']
