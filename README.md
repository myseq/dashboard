# Baseline Compliance Dashboard

This Streamlit application presents a **Baseline Dashboard** based on compliance scan results provided in CSV format.

## Features

 - Provides an overview of compliance data for quick analysis.
 - Displays compliance scan results in an interactive dashboard.
 - Calculate the compliance status automatic.
 - Filters results by **Operating System (OS)** and **Compliance Status**.
 - Display the details of those pass/fail controls.
 - Provide an overview compliance scan for host.

## Prerequisites

- Python installed on your system.
- CSV file containing compliance scan data with the following mandatory columns:
  - `Hostname`
  - `OS`
  - `Control`
  - `Result`

## Installation

1. Clone the repository:

```bash
$ git clone <repository_url>
$ cd <repository_directory>
```

2. Install required Python packages:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Usage

 1. Place your compliance scan CSV file in the project directory.
 1. Run the Streamlit app:

```console
(venv) $ streamlit run app.py
```

 1. Use the sidebar to filter data by:
   - **Operating System** (e.g., Windows, Linux).
   - **Compliance Status** (e.g., Compliant, Non-Compliant).

 1. Select any host in the interactive DataFrame with row selection via index.

## Sample CSV Format

Note that the CSV file may contain more columns.
And only the 4 column names are below are mantatory.

```csv
Hostname,OS,Control,Result
host_a,win11,c1,pass
host_a,win11,c2,pass
host_a,win11,c3,pass
host_b,rhel9,c1,pass
host_b,rhel9,c2,fail
host_b,rhel9,c3,fail
host_c,ws2022,c1,pass
host_c,ws2022,c2,pass
```

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy using the Baseline Compliance Dashboard!


