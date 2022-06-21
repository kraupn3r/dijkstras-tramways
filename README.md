# Django public transport app based on Dijkstra's algorithm

This project uses Dijkstra's algorithm to create an optimal route between two points. Datasets are two weighted adjacency matrices created from set of nodes.
Demo database is provided with Warsaw tram network.
Currently the frontend is Vue.js as a single file, but backend is made with a frontend container in mind.


## Preview
See it hosted at:
https://dijkstras-tramways.herokuapp.com

## Prerequisites
Docker & Docker Compose

## Setup

```
$ git clone https://github.com/iprogramstuff/docker-django-vue-postgres-template
$ cd dijkstras-tramways
$ docker-compose up --build
```
Please note that matrices building can take up to several minutes.



Served at 'localhost:8080'
