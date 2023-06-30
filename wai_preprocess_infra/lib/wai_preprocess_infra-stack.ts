import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class WaiPreprocessInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

      const layer = new lambda.LayerVersion(this, "Baselayer", {
        code: lambda.Code.fromAsset("lambda_base_layer/layer.zip"),
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],  
      });

      const apiLambda = new lambda.Function(this, 'apiFunction',{
        runtime: lambda.Runtime.PYTHON_3_9,
        code: lambda.Code.fromAsset('../app/'),
        handler: 'wai_preprocess_api.handler',
        layers: [layer],
      });
  }
}
