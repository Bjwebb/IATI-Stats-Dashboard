#!/bin/bash
mkdir -p data/downloads/
wget "https://gist.github.com/Bjwebb/6726204/raw/errors" -O data/downloads/errors

wget "http://data.tickets.iatistandard.org/query?status=accepted&status=assigned&status=new&status=reopened&format=csv&col=id&col=summary&col=status&col=owner&col=component&col=element&col=data_provider_regisrty_id&order=priority" -O data/issues.csv
wget "http://iatiregistry.org/api/3/action/organization_list?all_fields=true" -O data/ckan_publishers.json

wget "http://dev.iatistandard.org/ssot/commit/IATI-Codelists/5d15ad6ea028e1dc75bb4337059839f685ddeb06/en/_static/codelists/mapping.json" -O data/mapping.json

rm -r data/github/
python fetch_data.py

cd data/downloads
if [ ! -d ./6726204 ]; then
    git clone https://gist.github.com/6726204.git
fi
cd ./6726204
git checkout master > /dev/null
git pull > /dev/null
for commit in `git log --format=format:%H`; do
    git checkout $commit
    date=`git log -1 --format="%ai"`
    count=`cat errors | grep -v '^\.$' | wc -l`
    echo $date,$count
done > ../history.csv

