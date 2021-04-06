# TEST2.md
## Given: please follow
### URL
https://mock.com/
### VERB
GET
### Request headers
{'User-Agent': 'python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
### Response status code
200
### Response headers
{'Content-Type': 'application/json'}
###  Response content

~~~json
{
  "one": "one",
  "two": [
    "one",
    "two"
  ]
}
~~~

## When: last
### URL
https://mock.com/
### VERB
GET
### Request headers
{'User-Agent': 'python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
### Response status code
200
### Response headers
{'Content-Type': 'application/json'}
###  Response content

~~~xml
<?xml version="1.0" ?>
<xml>
   <one>one</one>
   <two>
      <item>one</item>
      <item>two</item>
   </two>
</xml>

~~~

