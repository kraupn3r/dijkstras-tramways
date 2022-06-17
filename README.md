# Django public transport app based on Dijkstra's algorithm

This project uses Dijkstra's algorithm to create an optimal route between two points. Datasets are two weighted adjacency matrices created from set of nodes.
Demo database is provided with Warsaw tram network.
Currently the frontend is Vue.js as a single file, but backend is made with a frontend container in mind.


## Prerequisites
Docker & Docker Compose

## Setup Template

```
$ git clone https://github.com/iprogramstuff/docker-django-vue-postgres-template
$ cd dijkstras-tramways
```

Setup
```
$ docker-compose up --build
```

Served at 'localhost:8080'
