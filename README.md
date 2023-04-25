# suitetalk_auth
Authenticating(OAuth 1.0) into NetSuite using python


if faced with the need of accessing data from Netsuite using their suitetalk API, here is a user friendle script that allows for authenticating
into your netsuite account using TBA method. You then need to use python requests library to get responses from NetSuite. 

you can either use SuiteQL approach to send SQL like queries to Netsute using POST Http method or their records rest api to get responses from interested tables.


## still a work in progress.. cuurently testing the parsing of parameters to my base url such as limit and offset parameters. 
this is to help get past the 1000 records limit per request that Netsuite uses to paginate its responses. 