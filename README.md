![GitHub Logo](http://i.imgur.com/IAMScGQ.png)
# ReDS - ReActive Database System
RDS automatic resizing and scheduled scale up/down

###Save up to 50% on RDS costs and save yourself headache during traffic spikes

Features:
- Can be dropped into any project
- Handles low credit balance on T2 instances to upgrade to M/R instances automatically if they run out of credits
- Allows schedules to go up to bigger DB during weekdays and back down at nights and weekends (if enabled)
- Outputs logs to CloudWatch logs for review
- Automatically increases/decreases capacity if CPU is too high/low
- Creates multiple CloudFormation stacks to encapsulate the pieces
- Built to AWS best practices in terms of security and IAM roles etc.
- Uses CloudWatch alarms (that it creates) to determine when it needs to scale
- Configurable thresholds and cooldowns
- Virtually no cost to operate (maybe 10 cents/month?) but can provide big savings over nights and weekends (i.e. m4.large -> t2.small in off times)

Requirements:
- run **make prep** to install dependencies
- only works on multi-AZ RDS (Single AZ instances get taken offline during resize - not good!)
- Manually configure repeating source after install via Lambda console - there is no automated way to do this yet, unfortunately - but only one time (see below for instructions!)

Tests
- run **make test**
- Check ./htmlcov/index.html for coverage report

Instructions:
- Modify vars.yaml to meet your needs.
- set "rds_identifier" to the name of your RDS instance [Click to see picture of where to get it](http://i.imgur.com/G6gRawE.png)
- If you want to enable scheduled scaling:
  - set schedule_enabled: True
  - set "cron" vars in UTC time to represent default start/stop
  - default cron vars are 9a-5p M-F Pacific (or close to it)
  - set "scheduled_index" to be the index of instance size in "instance_sizes" (starting from 0) that you want to scale up to during those hours
- After loading a profile from AWS CLI that has admin access, run from root folder:
    **make prod** to install
- This will create all the stacks, buckets, lambda, cloudwatch, IAM roles, event sources etc needed for this project

This runs approxmiately 300,000 sec/month of lambda, well below the free tier for 128MB functions (3.2M) so it's free

Logs:
Sample log output:

```
START RequestId: 15e84aae-dc44-11e5-a5b6-b58f401b95b3 Version: $LATEST
INFO: Startup Time: 2016-02-26 04:51:01.301149
INFO: Configured instance sizes: ['db.t2.micro', 'db.t2.small', 'db.m3.medium', 'db.m4.large', 'db.m4.xlarge']
INFO: RDS rds-master size/status/MultiAZ: db.t2.small/available/True
INFO: DB pointer (0-4) is currently on 1
INFO: Scheduling not enabled
INFO: Checking alarm statuses
INFO: Low-CPU Alarm status is: ALARM
INFO: Attempting scale down one size!
INFO: Scaling to db.t2.micro
INFO: cooldown period (minutes) for scale_down is 60
INFO: Last finished modification 2016-02-26 04:20:07.665000+00:00 Diff: (Min, Sec): (30, 52)
INFO: Not enough time has passed since last modification (60)
NO_ACTION: scale_down Cooldown threshold not reached
END RequestId: 15e84aae-dc44-11e5-a5b6-b58f401b95b3
REPORT RequestId: 15e84aae-dc44-11e5-a5b6-b58f401b95b3  Duration: 1766.43 ms    Billed Duration: 1800 ms Memory Size: 128 MB    Max Memory Used: 29 MB
```
