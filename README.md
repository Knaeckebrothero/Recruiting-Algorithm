# Trost: Projekt - SoSe2024

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Installation

## Usage

### Data Warehouse - SQL

#### Get a Compatible SQL Client
You can download MySQL Workbench [here](https://dev.mysql.com/downloads/workbench/).

#### Setup the Connection to the DWH
You can use these credentials to connect to the DWH:
- Connection Method: TCP/IP
- Hostname (IP Address)
- Port
- Username
- Password

#### Setup SSL to Encrypt Traffic Between You and the Database
1. Set "Use SSL" to "Require and Verify CA".
2. Save the ssl files and specify them as follows:
    - SSL Key: client-key.pem
    - SSL CERT: client-cert.pem
    - SSL CA: ca.pem

#### Test the Connection and Close the Window
**Note:** You may generate your own certificate if desired. If you wish to do so, please reach out to me to get it signed.

### Data Warehouse - Power BI

#### Download and install MS Power BI (rip mac users)
You can get Power BI Desktop [here](https://www.microsoft.com/en-us/download/details.aspx?id=58494).

### Data Warehouse - Notebook

#### Locate the Example
You can find a jupyter notebook example with preconfigured connection [here](/dwh/examples/dwh_example.ipynb)

#### Configure the environment variables
In order to use the notebook you need to setup the .env file.

1. Clone the repo
2. Open the [.env.example](.env.example) file
3. Fill in the your credentials
3. Remove .example to enable the file

#### Execute the first code cell to enable the functions and use them to get the connection

### Backend (development)
1. Clone repo
2. Install docker
3. Start docker
4. Run backend
5. Spring autocreates dbcontainers and connects them to the backend for testing

## License

This project is licensed under the terms of the Creative Commons Attribution 4.0 International License (CC BY 4.0) and the All Rights Reserved License. See the [LICENSE](LICENSE.txt) file for details.

## Contact
[Github](https://github.com/Knaeckebrothero) <br>
[Mail](mailto:OverlyGenericAddress@pm.me) <br>
