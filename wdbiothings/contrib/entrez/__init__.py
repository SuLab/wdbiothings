"""

description of all reference genomes:
ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt

one gene -> 3 ensembl
http://mygene.info/v3/gene/854968

yeast: ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64

feature table:
ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_feature_table.txt.gz

# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=675
"""
import os
import subprocess
from pymongo import MongoClient
from tqdm import tqdm

os.environ['PATH'] += ':/home/gstupp/lib/edirect'
os.chdir("/home/gstupp/projects/wikidata-biothings/wdbiothings/data/entrez")


# For human, gets info from all annotations
taxid = 9606
subprocess.run(
    "esearch -db gene -query 'txid{}[Organism]' | esummary | ".format(taxid) +
    "xtract -pattern DocumentSummary -element Id -block LocationHistType -pfx ';' " +
    "-element AnnotationRelease,AssemblyAccVer,ChrAccVer,ChrStart,ChrStop > {}.genomic_pos".format(taxid),
    shell=True)

# for other. gets for only current annotation
taxid = 559292
subprocess.run(
    "esearch -db gene -query 'txid{}[Organism]' | esummary | ".format(taxid) +
    "xtract -pattern DocumentSummary -element Id -block GenomicInfoType " +
    "-element ChrLoc,ExonCount,ChrAccVer,ChrStart,ChrStop > {}".format(taxid),
    shell=True)



# how many species are in mygene?
# this takes 17 hours
coll = MongoClient("su05").genedoc_src.entrez_gene
all_mg_taxids = set([x['taxid'] for x in coll.find({}, {'taxid': True})])
print(len(all_mg_taxids))

# get from file:
# zcat gene_info.gz | tail -n +2 | cut -f1 | uniq | sort | uniq > all_tax

for taxid in all_mg_taxids:
    subprocess.run(
        "esearch -db gene -query 'txid{}[Organism]' | esummary | ".format(taxid) +
        "xtract -pattern DocumentSummary -element Id -block GenomicInfoType " +
        "-element ChrLoc,ExonCount,ChrAccVer,ChrStart,ChrStop > {}".format(taxid),
        shell=True)

" OR " .join(["txid{}[Organism]".format(x) for x in [1000373,1001263,1001283,1001530,1001533,1001585,1001592,1001595,100182,100190]])

#############
# check mygene
import requests
url = "https://mygene.info/v3/query?q=__all__&species=9606&size=10000&fields=all"
res = requests.get(url)
d = res.json()

for doc in d['hits']:
    if 'ensembl' not in doc:
        doc['ensembl'] = dict()

[x for x in d['hits'] if not isinstance(x['ensembl'], dict)]

