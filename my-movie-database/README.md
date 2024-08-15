docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=mysecretpassword -e MYSQL_DATABASE=movies_db -p 3306:3306 -d mysql:latest

docker run --name mysql-db \
    -e MYSQL_ROOT_PASSWORD=mysecretpassword \
    -e MYSQL_DATABASE=movies_db \
    -v mysql_data:/var/lib/mysql \
    -p 3306:3306 \
    -d mysql:latest