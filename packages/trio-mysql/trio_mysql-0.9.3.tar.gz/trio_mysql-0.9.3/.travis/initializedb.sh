#!/bin/bash

#debug
set -x
#verbose
set -v

if [ ! -z "${DB}" ]; then
    # disable existing database server in case of accidential connection
    sudo service mysql stop

    docker pull ${DB}
    docker run -it --name=mysqld -d -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -p 3306:3306 ${DB}
    sleep 10

    mysql() {
        docker exec mysqld mysql "${@}"
    }
    while :
    do
        sleep 5
        mysql -e 'select version()'
        if [ $? = 0 ]; then
            break
        fi
        echo "server logs"
        docker logs --tail 5 mysqld
    done

    echo -e "[client]\nhost = 127.0.0.1\nprotocol = TCP\n" > "${HOME}"/.my.cnf

    mysql -e 'select VERSION()'

    if [ $DB == 'mysql:8.0' ]; then
        WITH_PLUGIN='with mysql_native_password'
        mysql -e 'SET GLOBAL local_infile=on'
        docker cp mysqld:/var/lib/mysql/public_key.pem "${HOME}"
        docker cp mysqld:/var/lib/mysql/ca.pem "${HOME}"
        docker cp mysqld:/var/lib/mysql/server-cert.pem "${HOME}"
        docker cp mysqld:/var/lib/mysql/client-key.pem "${HOME}"
        docker cp mysqld:/var/lib/mysql/client-cert.pem "${HOME}"

        # Test user for auth test
        mysql -e '
            CREATE USER
                user_sha256   IDENTIFIED WITH "sha256_password" BY "pass_sha256",
                nopass_sha256 IDENTIFIED WITH "sha256_password",
                user_caching_sha2   IDENTIFIED WITH "caching_sha2_password" BY "pass_caching_sha2",
                nopass_caching_sha2 IDENTIFIED WITH "caching_sha2_password"
                PASSWORD EXPIRE NEVER;'
        mysql -e 'GRANT RELOAD ON *.* TO user_caching_sha2;'
    else
        WITH_PLUGIN=''
    fi
    mysql -u root -e "create user travis@localhost; create user travis@'%'; grant all on *.* to  travis@localhost WITH GRANT OPTION;grant all on *.* to  travis@'%' WITH GRANT OPTION;"

    cp .travis/docker.json tests/databases.json
else
    cat ~/.my.cnf

    mysql -e 'select VERSION()'
    mysql -e 'create database test_trio_mysql DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;'
    mysql -e 'create database test_trio_mysql2 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;'

    mysql -u root -e "create user test2           identified by 'some password'; grant all on test_trio_mysql2.* to test2;"
    mysql -u root -e "create user test2@localhost identified by 'some password'; grant all on test_trio_mysql2.* to test2@localhost;"

    cp .travis/database.json tests/databases.json
fi
