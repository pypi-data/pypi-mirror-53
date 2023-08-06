#!/bin/bash

ES_MAJOR_VERSION=${ES_MAJOR_VERSION:-2}

source ~/elasticsearch${ES_MAJOR_VERSION}/bin/activate

bin/start.sh $@