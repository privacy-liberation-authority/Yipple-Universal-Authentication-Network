#!/bin/bash
# Students: Please do not take away from the defaults.
# You are however welcome to add new parameters to the database
if [ -f ../users.db ]
then
    rm ../users.db
    echo "Cleared users database."
fi

if [ -f ../creds.db ]
then
    rm ../creds.db
    echo "Cleared creds database"
fi

cat userSchema.sql | sqlite3 ../users.db && echo "Created ../users.db"
cat credSchema.sql | sqlite3 ../creds.db && echo "Created ../creds.db"
