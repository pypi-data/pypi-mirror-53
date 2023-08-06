#!/bin/bash
set -ex
DIR=$(dirname "$0")
if [-n $1]
    then
        echo "argument is not set"
    else
        DIR=$(dirname "$1")
fi
echo $DIR
aws s3 cp s3://healthchat-credentials/healthchat-credentials "${DIR}/config/credentials"
aws s3 cp s3://pharmacy-config/pioneer-listener-2.json "${DIR}/config/config.json"
aws s3 cp s3://pharmacy-config/pharmacy-automation-secrets.py "${DIR}/config/secrets.py"
aws s3 cp s3://pharmacy-config/pharmacy-automation-constants.py "${DIR}/config/constants.py"
aws s3 cp s3://falsepill-config/falsepill.json "${DIR}/py_common/config/database.json"