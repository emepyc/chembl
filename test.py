from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['localhost'],
    http_auth=('kibiadmin', 'password'),
    port=9221,
    use_ssl=True,
    verify_certs=True,
    ca_certs='./pki/searchguard/ca.pem',
    # client_cert = './pki/searchguard/CN=sgadmin.crt.pem',
    # client_key = './pki/searchguard/CN=sgadmin.key.pem'
)

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.'
}
# es = Elasticsearch('https://localhost:9200')

es = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
## print(res['created'])

print (es)
