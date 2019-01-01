### Starting Production Environment
Make sure you have installed [docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/). To start DRS in production follow the steps below:
- Clone the repository
- Create a `drs` user with UID `9001` and change the ownership of the repo:
    ```bash
    sudo useradd -u 9001 -m -d /home/drs -s /bin/bash drs
    sudo chown -R 9001:9001 Device-Registration-Subsystem
    ```
- Produce distribution files using:
    ```bash
    make dist
    ```
- Change directory to `dist` and build the production containers:
    ```bash
    make -f docker/prd/Makefile
    ```
- After the build process is successful, launch the containers by changing directory to `dist/docker/prd`:
    ```bash
    docker-compose up -d
    ```
  This will launch production containers for `api` and `postgres`.
- Now open another terminal and login into the postgres shell:
    ```bash
    docker exec -it drs_db bash
    ```

- Checkout into the postgres shell:
    ```bash
    gosu postgres psql
    ```

- On the postgres shell, create a role `drs` with login:
    ```bash
    CREATE ROLE drs WITH login;
    ```

- On the postgres shell, create database named `drs`:
    ```bash
    CREATE database drs OWNER drs;
    ```

- Now switch to the server shell, and install database:
    ```bash
    make install-db
    ```

 After these steps are completed successfully, you can access api server.
