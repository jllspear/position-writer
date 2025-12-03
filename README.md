# Position Writer

Writer MQTT vers PostgreSQL - Pont entre topics MQTT et tables de base de données.

## Customisation

### Créer un repo alembic

- `alembic.versions` - Migrations de base de données

### Modules a injecter dans la librairie
- `models` - Modèles SQLModel
- `parser` - Parsers et validateurs

### Exemple : Modèle + Parser

**Modèle de base de données** (`modules.database.custom_models`) :

```python
class DevicePosition(SQLModel, table=True):
    __tablename__ = "device_position"
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(default=None, max_length=50)
    base_station: str = Field(default=None, max_length=10)
    date: float = Field(default=None, sa_column=Column(Numeric()))
    coordinates: str = Field(default=None, sa_column=Column(Geometry("POINT", srid=4326)))
```

**Parser + Validateur** (`modules.mqtt.custom_parsers`) :

```python
class DevicePositionParser(MqttParser[DevicePosition]):
    def parse(self, payload: any) -> Optional[DevicePosition]:
        validated_data = DevicePositionValidator(**payload)
        coordinates_wkt = f"POINT({validated_data.lon} {validated_data.lat})"
        
        return DevicePosition(
            ip=validated_data.ip,
            base_station=validated_data.base_station,
            date=validated_data.date,
            coordinates=coordinates_wkt
        )

class DevicePositionValidator(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    ip: str = Field(..., max_length=50, pattern=r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^[a-zA-Z0-9\-\.]+$')
    base_station: str = Field(..., max_length=10)
    date: Optional[float] = Field(None, ge=0)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    
    @field_validator('date', mode='before')
    @classmethod
    def validate_date(cls, v):
        if v is None or isinstance(v, (int, float)):
            return float(v) if v is not None else v
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                raise ValueError('Date must be a numeric timestamp')
        return v
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