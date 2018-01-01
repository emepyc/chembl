
# Installation and configuration

### Pre-requisites
Follow these steps to have all the software needed to proceed with the installation:

- Checkout the following repositories:
```
## The repository containing the Siren's ChEMBL demo
$ git clone https://github.com/sirensolutions/chembl

## The kibi-internal repository:
$ git clone https://github.com/sirensolutions/kibi-internal

## The kibi-enterprise repository:
$ git clone https://github.com/sirensolutions/kibi-enterprise
```


### Install the data into elasticsearch

Follow these steps to get a working copy of Siren's ChEMBL demo

- Download one of the working distributions of Siren's platform from https://artifactory.siren.io/. Take the latest distribution without preloaded data.
```
$ curl https://artifactory.siren.io/artifactory/webapp/#/artifacts/browse/tree/General/libs-snapshot-local/solutions/siren/siren-platform/10.0.0-SNAPSHOT/siren-platform-10.0.0-20171221.011202-10-darwin-x86_64.zip
$ unzip siren-platform-10.0.0-20171221.011202-10-darwin-x86_64.zip
$ cd siren-platform-10.0.0-20171221.011202-10-darwin-x86_64/
```

- Copy the `searchguard` certificates from the downloaded distribution to the `chembl` repository:
```
# You will not need all the certificates, but for simplicity 
$ cp -r kibi/pki/searchguard/ ../chembl/pki/
```

- Start elasticsearch. You can edit the configuration file `elasticsearch/config/elasticsearch.yml` if needed, for example, to change its `port` (`9220` by default)
```
$ ./elasticsearch/bin/elasticsearch
```

- Once you have elasticsearch up and running, open a new terminal window and `cd` into the ChEMBL repository
```
$ cd <path/to/your/chembl/repo>
```

- Install all needed software. Make sure you are using python3, for example by using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/):
```
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

- Run the `import.py` script:
```
$ python3 import.py -es "https://localhost:9221" -certs pki
```

   this will:
   * Download and extract the chembl dumps in SQLite format
   * Query the database and generate the input json file in the `import` directory
   * Load the json in elasticsearch with the proper mapping
   * Create the necessary index-pattern in kibi


### Test the elasticsearch imported data
```
$ curl --cacert ./pki/searchguard/ca.pem -ukibiadmin:password https://localhost:9221/_cat/indices
```

### Start the ChEMBL demo




### 
To connect via `curl` to your elasticsearch
```
curl --cacert ./pki/searchguard/ca.pem -ukibiadmin:password https://localhost:9221/_cat/health?v
```


The code in this repo can reproduce the second Kibi ChEMBL demo.
This are the steps to reproduce the demo.

1) Start up a kibi instance. E.g. using docker:
    ```docker run  -d -p 5606:5606 -p 9201:9220 --net=chembl --name chembl-kibi sirensolutions/kibi-community-standard:4.6.4```

2) ```pip install -r requirements.txt```

3) run ```python import.py -es http://localhost:9201``` using the port your elasticsearch instance is exposed to and wait for it to complete
   this will:
   * Download and extract the chembl dumps in SQLite format
   * Query the database and generate the input json file in the `import` directory
   * Load the json in elasticsearch with the proper mapping
   * Create the necessary index-pattern in kibi

4) explore the data at your kibi instance: http://localhost:5606

5) To persist the state of kibi you can run `dump_kibi.sh`. This requires [elasticdump](https://www.npmjs.com/package/elasticdump) to be installed.
   To save the data and the kibi configuartion in a compressed file you can run `dump_all.sh`.

