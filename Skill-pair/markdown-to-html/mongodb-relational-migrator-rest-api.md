# MongoDB Relational Migrator REST API

## Description
This is version `1.15.3` of this API documentation. Last update on Feb 26, 2026.
OpenAPI specification for MongoDB Relational Migrator tool

## Servers
- http://127.0.0.1:8278/api/v1: http://127.0.0.1:8278/api/v1 ()




## Endpoints and operations

### [Analysis](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/group/endpoint-analysis.md)
- [Get pre-migration analysis task by `projectId`](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getanalysistask.md)
- [Create a task for pre-migration analysis](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-createanalysistask.md)
- [Cancel a running pre-migration analysis task](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-cancelanalysistask.md)
- [Get a pre-migration analysis report](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getreport.md)
### [Job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/group/endpoint-job.md)
- [Get all migration jobs](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getjobs.md)
- [Post a new migration job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-createjob.md)
- [Get the status of a migration job by ID](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getjob.md)
- [Pause a running migration job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-pausejob.md)
- [Resume a paused migration job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-resumejob.md)
- [Stop a running migration job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-stopjob.md)
- [Get the events of a migration job](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getjoblogs.md)
### [Project](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/group/endpoint-project.md)
- [Get all projects](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getprojects.md)
- [Imports a project from an export file](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-importproject.md)
- [Get all collections belonging to a project](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-getcollections.md)
- [Export an existing project](https://www.mongodb.com/docs/api/doc/mongodb-relational-migrator-rest-api/operation/operation-exportproject.md)



[Powered by Bump.sh](https://bump.sh)
