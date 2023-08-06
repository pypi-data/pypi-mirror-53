## Amazon Relational Database Service Construct Library
<!--BEGIN STABILITY BANNER-->

---

![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a _developer preview_ (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

### Starting a Clustered Database

To set up a clustered database (like Aurora), define a `DatabaseCluster`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```ts
const cluster = new DatabaseCluster(this, 'Database', {
    engine: DatabaseClusterEngine.AURORA,
    masterUser: {
        username: 'admin'
    },
    instanceProps: {
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        vpcSubnets: {
            subnetType: ec2.SubnetType.PUBLIC,
        },
        vpc
    }
});
```
By default, the master password will be generated and stored in AWS Secrets Manager.

Your cluster will be empty by default. To add a default database upon construction, specify the
`defaultDatabaseName` attribute.

### Starting an Instance Database
To set up a instance database, define a `DatabaseInstance`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```ts
const instance = new DatabaseInstance(stack, 'Instance', {
    engine: rds.DatabaseInstanceEngine.ORACLE_SE1,
    instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
    masterUsername: 'syscdk',
    vpc
});
```
By default, the master password will be generated and stored in AWS Secrets Manager.

Use `DatabaseInstanceFromSnapshot` and `DatabaseInstanceReadReplica` to create an instance from snapshot or
a source database respectively:

```ts
new DatabaseInstanceFromSnapshot(stack, 'Instance', {
    snapshotIdentifier: 'my-snapshot',
    engine: rds.DatabaseInstanceEngine.POSTGRES,
    instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
    vpc
});

new DatabaseInstanceReadReplica(stack, 'ReadReplica', {
    sourceDatabaseInstance: sourceInstance,
    engine: rds.DatabaseInstanceEngine.POSTGRES,
    instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
    vpc
});
```
Creating a "production" Oracle database instance with option and parameter groups:

```ts
    // Set open cursors with parameter group
    const parameterGroup = new rds.ParameterGroup(this, 'ParameterGroup', {
      family: 'oracle-se1-11.2',
      parameters: {
        open_cursors: '2500'
      }
    });

```
Add XMLDB and OEM with option group
```ts
    const optionGroup = new rds.OptionGroup(this, 'OptionGroup', {
      engine: rds.DatabaseInstanceEngine.ORACLE_SE1,
      majorEngineVersion: '11.2',
      configurations: [
        {
          name: 'XMLDB'
        },
        {
          name: 'OEM',
          port: 1158,
          vpc
        }
      ]
    });

    // Allow connections to OEM
    optionGroup.optionConnections.OEM.connections.allowDefaultPortFromAnyIpv4();

    // Database instance with production values
    const instance = new rds.DatabaseInstance(this, 'Instance', {
      engine: rds.DatabaseInstanceEngine.ORACLE_SE1,
      licenseModel: rds.LicenseModel.BRING_YOUR_OWN_LICENSE,
      instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MEDIUM),
      multiAz: true,
      storageType: rds.StorageType.IO1,
      masterUsername: 'syscdk',
      vpc,
      databaseName: 'ORCL',
      storageEncrypted: true,
      backupRetention: cdk.Duration.days(7),
      monitoringInterval: cdk.Duration.seconds(60),
      enablePerformanceInsights: true,
      cloudwatchLogsExports: [
        'trace',
        'audit',
        'alert',
        'listener'
      ],
      cloudwatchLogsRetention: logs.RetentionDays.ONE_MONTH,
      autoMinorVersionUpgrade: false,
      optionGroup,
      parameterGroup
    });

    // Allow connections on default port from any IPV4
    instance.connections.allowDefaultPortFromAnyIpv4();

    // Rotate the master user password every 30 days
    instance.addRotationSingleUser('Rotation');

    // Add alarm for high CPU
    new cloudwatch.Alarm(this, 'HighCPU', {
      metric: instance.metricCPUUtilization(),
      threshold: 90,
      evaluationPeriods: 1
    });

    // Trigger Lambda function on instance availability events
    const fn = new lambda.Function(this, 'Function', {
      code: lambda.Code.fromInline('exports.handler = (event) => console.log(event);'),
      handler: 'index.handler',
      runtime: lambda.Runtime.NODEJS_8_10
    });

    const availabilityRule = instance.onEvent('Availability', { target: new targets.LambdaFunction(fn) });
    availabilityRule.addEventPattern({
      detail: {
        EventCategories: [
          'availability'
        ]
      }
    });
```


### Instance events
To define Amazon CloudWatch event rules for database instances, use the `onEvent`
method:

```ts
const rule = instance.onEvent('InstanceEvent', { target: new targets.LambdaFunction(fn) });
```

### Connecting

To control who can access the cluster or instance, use the `.connections` attribute. RDS databases have
a default port, so you don't need to specify the port:

```ts
cluster.connections.allowFromAnyIpv4('Open to the world');
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.readerEndpoint`
attributes:

```ts
const writeAddress = cluster.clusterEndpoint.socketAddress;   // "HOSTNAME:PORT"
```

For an instance database:
```ts
const address = instance.instanceEndpoint.socketAddress;   // "HOSTNAME:PORT"
```

### Rotating master password
When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```ts
const cluster = new rds.DatabaseCluster(stack, 'Database', {
  engine: rds.DatabaseClusterEngine.AURORA,
  masterUser: {
    username: 'admin'
  },
  instanceProps: {
    instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
    vpc
  }
});

cluster.addRotationSingleUser('Rotation');
```

Rotation of the master password is also supported for an existing cluster:
```ts
new SecretRotation(stack, 'Rotation', {
    secret: importedSecret,
    application: SecretRotationApplication.ORACLE_ROTATION_SINGLE_USER
    target: importedCluster, // or importedInstance
    vpc: importedVpc,
})
```

The `importedSecret` must be a JSON string with the following format:
```json
{
  "engine": "<required: database engine>",
  "host": "<required: instance host name>",
  "username": "<required: username>",
  "password": "<required: password>",
  "dbname": "<optional: database name>",
  "port": "<optional: if not specified, default port will be used>"
}
```

### Metrics
Database instances expose metrics (`cloudwatch.Metric`):
```ts
// The number of database connections in use (average over 5 minutes)
const dbConnections = instance.metricDatabaseConnections();

// The average amount of time taken per disk I/O operation (average over 1 minute)
const readLatency = instance.metric('ReadLatency', { statistic: 'Average', periodSec: 60 });
```

