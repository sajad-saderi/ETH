# Installation

Have a Linux machine at your hands. There are four methods for installing
Cross-Secrecy's server. It is recommended to do the third one (pull a docker
image).


## Pure Python
Install the application directly on your system:

```bash
python3 setup.py install #--user
```

and run it via

```bash
cross-secrecy-servers --database=[DATABASE-PATH] --data=[PATH-TO-STATIC-AND-TEMPLATES]
# Example for this workdir:
cross-secrecy-servers --database=./database/database.sqlite3 --data=./data
```

## Docker Build

When building locally, rename `docker-compose.yml.local` to
`docker-compose.yml`.

Build a docker image:

```bash
docker build -t xss ./
```

And create a docker container with `docker-compose`

```bash
docker-compose up
```

## Pull the Docker Image

If necessary, login at GitLab:
```bash
docker login gitlab2.informatik.uni-wuerzburg.de:4567
```

And pull the image via docker-compose
```bash
docker-compose up
```

or manually:

```bash
docker pull gitlab2.informatik.uni-wuerzburg.de:4567/moritz.finke/attack-the-web-xss
```

## Vagrant

Head to [vagrant](../vagrant/) and run the Vagrantfile via

```bash
vagrant up
```

# Configuration
If you use a Docker container, then configure the application (ports, logging,
etc.) within the `docker-compose.yml` file. Else, use `cross-secrecy-servers
-h` to list available options.

# Database
If you use a Docker container, an SQLITE-database is automatically created in
this directory. Else, specify a database path with `cross-secrecy-servers
--database=`.