#!/bin/bash

# get configuration from user's input and save it as environment variables

ENV_FILE=~/.bashrc

declare -a PARAMS=(s3_bucket aws_profile urls_s3_key user_agent \
    max_retries backoff_factor retry_on timeout database table db_user \
    password host port)

echo "Please enter configuration values: "
echo

# loop through parameters
for ((i=0; i<${#PARAMS[@]}; i++)); do

    # show the existing value to the user
    VAR="FINANCE_SCRAPING_${PARAMS[i]^^}"
    EXISTING=`cat $ENV_FILE | grep $VAR | cut -d= -f2`
    echo "${PARAMS[i]}[$EXISTING]: "
    read VAL

    # keep waiting for user input if no value is set
    while [[ -z ${VAL} ]] && [[ -z $EXISTING ]]; do
	echo "${PARAMS[i]}[$EXISTING]: "
	read VAL
    done

    # user's input overwrites the existing variable
    if [[ ! -z ${VAL} ]]; then
	sed -i "/^export $VAR/d" $ENV_FILE
        echo "export $VAR=$VAL" >> $ENV_FILE
    fi
done

source $ENV_FILE

echo "Configuration is finished."

exec bash -l
