#!/bin/bash

if [ -f '../users.db' ]
then
    rm ../users.db
fi

echo "Databases removed."