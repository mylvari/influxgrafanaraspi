* putty
* web browser

# Initiating project
Login to server with ssh

Clone this repository to the server with command

    git clone https://github.com/mylvari/influxgrafana

Navigate into the project

    cd influxgrafana

Copy the supplied template file *.env.example* for environmental variables

    cp .env.example .env

Edit the environmental variable file

    nano .env

(You can save by pressing **ctrl+o and enter**, quit by **ctrl+x**)
You can use some random strings for the passwords. For alphavantage, you
can get apikey from [here](https://www.alphavantage.co/support/).

Take the edited environmental variables into use

    source .env

Verify that no Docker containers are currently running

    docker ps

Should only display

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

Start the project

    docker-compose up -d --build grafana

Verify it is running

    docker ps

Should now display something like

    CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                             NAMES
    980fd8fe1fc6        grafana/grafana:latest   "/run.sh"                5 seconds ago       Up 5 seconds        0.0.0.0:3000->3000/tcp                            influxgrafana_grafana_1
    bfd268efe09f        mailhog/mailhog          "MailHog"                6 seconds ago       Up 5 seconds        0.0.0.0:8025->8025/tcp, 0.0.0.0:32803->1025/tcp   influxgrafana_local-mailhog_1
    30f820947b59        influxdb:alpine          "/entrypoint.sh infl…"   6 seconds ago       Up 5 seconds        0.0.0.0:32802->8086/tcp                           influxgrafana_influxdb_1


Go with your browser to http://server-ip:3000 and login with user **admin** and password what you entered into GF_SECURITY_ADMIN_PASSWORD in .env

If everything went fine, you should be able to login.

## Setting data source
Click add datasource.

* Select type to be **influxdb**
* Type **http://influxdb:8086** as a URL
* Type **data** as database
* Press save&test and it should work

## Setting alert channel
Click bell on left of the screen --> Notification channels --> add channel

* Set type to be email
* Add **test@example.com** into email addressess
* Click send test
* Navigate with you browser to http://server-ip:8025 and verify that the test email is visible


# Using InfluxDb
Start a shell inside Influxdb container by

    docker-compose exec influxdb influx


Use commands from https://docs.influxdata.com/influxdb/v1.5/introduction/getting-started/
to 

1. Create a new database
2. Use that database
3. Write some data into the database
4. Read some data from database

After done, close the influxdb prompt by commanding ```exit```

Start our data loggers by

    docker-compose up -d --build stock-logger telegraf

Start the influx prompt again with

    docker-compose exec influxdb influx

You should be able to see some data being logged by commanding

    USE data
    SELECT * FROM stocks LIMIT 10