# `launchec2`

Simple boto script to:
- Utilize the AWS API
- Accept the arguments: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `INSTANCE_TYPE`
- Wait for an instance to come online, and then return the instance launch time to STDOUT
- add a handy Makefile for a tester to plug their AWS creds into, run the util with all 4 stated inputs on the command line
