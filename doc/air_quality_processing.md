Certainly! Here's an extensive documentation for the provided code:

---

# Air Quality Data Processing

The "Air Quality Data Processing" project focuses on collecting, processing, and analyzing air quality data. This script interacts with air quality sensors, gathers data related to temperature, humidity, and particle size, and provides users with valuable insights into the air quality trends.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Running the Script](#running-the-script)
  - [Auto Data Loading](#auto-data-loading)
- [Functions](#functions)
  - [create_connection(db_file)](#create_connectiondb_file)
  - [get_temperature(date)](#get_temperaturedate)
  - [get_humidity(date)](#get_humiditydate)
  - [get_particle1(date)](#get_particle1date)
  - [get_particle2(date)](#get_particle2date)
  - [import_data(date, connection)](#import_datadate-connection)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.x
- Required Python packages: `sqlite3`, `pandas`
- Internet connectivity to fetch data from the Sensor.Community archive

## Usage

### Running the Script

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/MobDevOne/AirQuality.git
   ```

2. Navigate to the project directory:
   ```bash
   cd air-quality-data-processing
   ```

3. Install the required Python packages:
   ```bash
   pip install pandas
   ```

4. Run the main script:
   ```bash
   python3 air_quality_processing.py
   ```

5. Follow the on-screen instructions to retrieve air quality data for a specific date.

### Auto Data Loading

The script supports an automated data loading process that retrieves and processes data for the past days. This feature ensures that the database is up to date with the latest air quality information.

## Functions

### create_connection(db_file)

This function creates a connection to the SQLite database file specified by `db_file`.

### get_temperature(date)

Fetches temperature statistics for the specified `date` from the `dht_sensor` table in the database.

### get_humidity(date)

Fetches humidity statistics for the specified `date` from the `dht_sensor` table in the database.

### get_particle1(date)

Fetches particle size statistics (P1) for the specified `date` from the `sds_sensor` table in the database.

### get_particle2(date)

Fetches particle size statistics (P2) for the specified `date` from the `sds_sensor` table in the database.

### import_data(date, connection)

Imports air quality data for the specified `date` and inserts it into the database. Data is fetched from URLs provided by the Sensor.Community archive.

## Configuration

The script uses a configuration file named `config.json` to track the latest data updates and failed attempts. The configuration file structure includes fields like `latest` (latest data date) and `not_found` (dates with failed data fetch attempts).

## Contributing

Contributions to this project are welcome. If you'd like to contribute, follow the guidelines mentioned in the [Contributing](#contributing) section of this README.

## License

This project is licensed under the [MIT License](LICENSE).

---

Thank you for exploring the "Air Quality Data Processing" project. For any questions or suggestions, feel free to contact us!
