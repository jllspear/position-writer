# Geobin Writer

Writer MQTT vers PostgreSQL - Pont entre topics MQTT et tables de base de données.

## Build & Tag

```bash
docker buildx build --platform linux/amd64 -t registry.optimaize.fr/jllspear/geobin-writer:0.0.1 --load .
```

## Push to registry
```bash
docker buildx build --platform linux/amd64 -t registry.optimaize.fr/jllspear/geobin-writer:0.0.1 --push .
```

## Configuration

Associer topics MQTT et parsers via variable d'environnement :

```bash
BROKER__TOPICS={"device_log":"DeviceLogParser","device_position":"DevicePositionParser"}
```

## Tests MQTT

**Topic `device_position`** :
```json
{
  "ip": "123.321.111",
  "base_station": "CAP",
  "date": "123",
  "lat": "44.8488",
  "lon": "-0.67390"
}
```

**Topic `device_log`** :
```json
{
  "ip": "123.321.111",
  "log": "test_log"
}
```

## .env (local testing)
```markdown
# -------------------------
# Database Settings
# -------------------------
DATABASE__PROVIDER=postgresql
DATABASE__DIALECT=psycopg
DATABASE__HOST=localhost
DATABASE__PORT=5432
DATABASE__USER=rockwool
DATABASE__PASSWORD=
DATABASE__DATABASE=
DATABASE__CLIENT_NAME=rockwool-broker
DATABASE__ECHO=false

# -------------------------
# Broker Settings
# -------------------------
BROKER__URL=localhost
BROKER__PORT=1883
BROKER__USERNAME=geobin
BROKER__PASSWORD=

BROKER__TOPICS={"device_log":"DeviceLogParser","device_position":"DevicePositionParser"}

BROKER__FIRST_RECONNECT_DELAY=1
BROKER__RECONNECT_RATE=2
BROKER__MAX_RECONNECT_COUNT=8
BROKER__MAX_RECONNECT_DELAY=180
BROKER__RECHECK_EQUIPMENT_INTERVAL=180
BROKER__VERBOSE=true

```