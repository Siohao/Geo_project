@echo off
SET CONTAINER_NAME=postgres-db
SET DB_NAME=geo_project_db
SET DB_USER=admin

docker cp schema.sql %CONTAINER_NAME%:/schema.sql
docker exec -i %CONTAINER_NAME% pslq -U %DB_USER% -d %DB_NAME% -f /schema.sql

echo Schema applied!
pause