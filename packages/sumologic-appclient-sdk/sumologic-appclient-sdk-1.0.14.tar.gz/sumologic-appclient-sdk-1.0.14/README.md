# sumologic-appclient-sdk
SDK with utility libraries for App team's collection clients

## omnistorage
Omnistorage is a persistent key value store library which provides a unified and easy to use API and can be used with both oncloud and onprem applications.
It hides the differences between datastores from major cloud providers like aws, gcp, azure and prevent data lock-in on a single vendor. 

## common
Contains common utilities for config management, log management etc.

## sumoclient
Sumo Logic Client supporting multiple output handlers like http, file, s3 etc.


## pkggenerator
This module is responsible for building and deploying packages for both oncloud(aws, gcp and azure) and onprem enviroments(in pypi repo).

