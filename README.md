# RPI Weather #



### Pré-requis ###

* Python v3.5.2
* Docker

### Script Pyhton ###





### InfluxDB ###

Commande docker pour lancement de la bdd : 
```
#!shell

docker run -p 8083:8083 -p 8086:8086 \
      -v influxdb:/var/lib/influxdb \
      influxdb

```

**Création de l'utilisateur**

```
#!shell

CREATE USER "influx" WITH PASSWORD 'influx'
```

**Création de la base de données**

```
#!shell

CREATE DATABASE "weather"
```


### Grafana ###

Commande docker pour lancement du dashboard : 
```
#!shell

docker run -i -p 3000:3000 grafana/grafana

```

**Requête de génération du graphique**


```
#!SQL

SELECT "value" FROM "temperature.readings" WHERE $timeFilter
```