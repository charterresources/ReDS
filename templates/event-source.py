#!/usr/bin/env python

from troposphere import Template, Output, GetAtt, Parameter, Ref, events, awslambda

t = Template()

lambda_arn = t.add_parameter(Parameter(
    'LambdaArn',
    Type='String',
    Description='Lambda Arn'
))

rule = t.add_resource(
    events.Rule(
        "ReDSRule",
        Targets=[events.Target(
            Arn=Ref(lambda_arn),
            Id="ReDS"
        )],
        ScheduleExpression="rate(5 minutes)"
    )
    )

permission = t.add_resource(
    awslambda.Permission(
        "ReDSPerm",
        FunctionName=Ref(lambda_arn),
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        SourceArn=GetAtt(rule, "Arn")
    )
    )

t.add_output([
    Output(
        'EventRule',
        Description='ReDS Event Rule',
        Value=Ref(rule),
    ),
    Output(
        'EventPermission',
        Description='ReDS Lambda Permission',
        Value=Ref(permission),
    )
])

if __name__ == '__main__':
    print t.to_json()
