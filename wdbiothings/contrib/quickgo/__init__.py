"""
yeast:
ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/YEAST/goa_yeast.gaf.gz

all uniprot:
ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gaf.gz

The file on the ftp site doesn't include to the uniprot and interpro-derived annotations
only the SGD annotations. Can only see them in the API??


"""

from io import StringIO

import pandas as pd
import requests
from pymongo import MongoClient

# query to get the most used taxons
# http://tinyurl.com/zk65y54
# todo: automate
taxa = ['9606', '10090', '10116', '9545', '749927', '224911', '100226', '243090', '246196', '394', '266834', '366394',
        '559292', '272560', '160488', '1125630', '223283', '208964', '716541', '226900', '281309', '386585', '205918',
        '1133852', '1028307', '585056', '243160', '223926', '226186', '568707', '585057', '295405', '685038', '251221',
        '220341', '99287', '272943', '214092', '1208660', '190485', '224308', '211586', '380703', '511145', '36809',
        '198214', '393305', '83332', '233413', '324602', '269796', '312309', '272562', '272563', '189518', '190650',
        '300267', '871585', '882', '243231', '243277', '257313', '226185', '169963', '243230', '333849', '272624',
        '309807', '243275', '441771', '93061', '5833', '220668', '176299', '176280', '197221', '264732', '402612',
        '388919', '300852', '194439', '413999', '272623', '208435', '289376', '365659', '190304', '210007', '568814',
        '122586', '167539', '243274', '272621', '227377', '171101', '206672', '160490', '242231', '177416', '71421',
        '192222', '272631', '224324', '196627', '85962', '321967', '525284', '224326', '115713', '272632', '362948',
        '272561', '471472', '702459', '272947', '265311', '260799', '272634', '107806', '198094']

# yeast only
taxa = ['559292']


def get_go_taxon(taxon):
    data = {
        'tax': taxon,
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
    d = df.to_dict("records")
    return d


def main():
    coll = MongoClient().wikidata_src.quickgo

    for taxon in taxa:
        d = get_go_taxon(taxon)
        coll.insert_many(d)


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

# gb = df.iloc[:100].groupby(['ID','GO ID','Evidence','Source','DB'])['Reference'].apply(list)
# gb.ix['Q12272']
