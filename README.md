# Holdings UI

Holdings UI is a lightweight Python application for geospatial database querying and automated report generation.  
It provides a simple user interface to extract, visualize, and export geographic region data from a PostgreSQL/PostGIS database into professional PowerPoint presentations.

---

## Features
- **Secure Database Integration**: Connects to a PostgreSQL/PostGIS database with credentials managed via a configuration file.
- **Dynamic Region Selection**: Lists and allows selection of available regions from the database.
- **Geospatial Data Retrieval**: Fetches geospatial datasets for selected regions or region groups using optimized SQL queries.
- **Automated Presentation Generation**: Exports selected geographic data into structured PowerPoint reports.
- **Minimal User Interface**: Enables users to interact with the system without requiring knowledge of SQL.

---

## Technologies Used
- Python
- GeoPandas
- SQLAlchemy
- psycopg2-binary
- Matplotlib (optional, for map generation)
- Pandas
- ConfigParser

---

## Project Structure

| File | Description |
|:-----|:------------|
| `db_handler.py` | Manages database connections and spatial queries |
| `ui.py` | Provides a graphical interface for region selection and report generation |
| `image_generator.py` | (Optional) Generates map images for use in reports |
| `ppt_generator.py` | Creates PowerPoint files populated with selected region data |
| `config.ini` | Configuration file for secure database credential management |
| `how to add readonly user to db.txt` | Instructions for setting up a readonly database user |
