# Notarius

Bitbucket Cloud/Github backup tool

## Installation

`pip install sourcerio`

## Usage

~~~
$ sourcerio -h
usage: sourcerio [-h] [--bitbucket-user USER] [--bitbucket-password PASSWORD]
                 -d DIRECTORY [--github-api-token API_KEY] -o ORGANIZATION -t
                 {bitbucket,github} [-v]

optional arguments:
  -h, --help            show this help message and exit
  --bitbucket-user USER
                        Bitbucket user
  --bitbucket-password PASSWORD
                        Bitbucket password
  -d DIRECTORY          Backup directory
  --github-api-token API_KEY
                        Github API key
  -o ORGANIZATION       Bitbucket/Github organization
  -t {bitbucket,github}
                        bitbucket/github
  -v                    verbose output
~~~
