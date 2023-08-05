# j2db

![CI Status](https://github.com/williamfzc/j2db/workflows/smoketest/badge.svg)  

standard and safe way to upload your json to db

## flow

![](./docs/pics/json2db.svg)

- request with json data
- check / convert
- upload to db

## why

Data uploader is a really important part in development workflow.

But many (so many) different db clients in different places or different languages ​​make me feel tired, and i have to implement them in different projects again and again ...

Why do not we use JSON directly? and actually, some (most of) projects should not operate database directly.

## how

- server for receiving http request, and get JSON
- check (support custom hook)
- convert JSON to model (ORM built with SQLAlchemy)
- upload to db

## usage

see [example](example/server.py)

## dependencies

- [fastapi](https://github.com/tiangolo/fastapi): as web server
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy): as db manager 

## bug report & suggestion

please let me know via issue

## license

[MIT](LICENSE)
