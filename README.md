# Trost: Projekt - SoSe2024

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Installation

## Usage

- The server restart ist scheduled at 07:00 am ect.
- If you encounter performance issues you can check the server status by accessing the grafana dashboard.
- The DWH consists of two main components
    - A document oriented nosql db for mass storage of raw data (mongodb)
    - A sql db for more in depth analysis (mysql)


### Data Warehouse - SQL

1. Get a Compatible SQL Client<br>
You can download MySQL Workbench [here](https://dev.mysql.com/downloads/workbench/).

2. Setup the Connection to the DWH<br>
    You can use these credentials to connect to the DWH:
    - Connection Method: TCP/IP
    - Hostname (aka IP Address)
    - Port
    - Username
    - Password

3. Setup SSL to Encrypt Traffic Between You and the Database (Optional)<br>
    - Set "Use SSL" to "Require and Verify CA".
    - Save the ssl files and specify them as follows:
        - SSL Key: client-key.pem
        - SSL CERT: client-cert.pem
        - SSL CA: ca.pem
    
    **Note:** You may generate your own certificate if desired. If you wish to do so, please reach out to me to get it signed.

4. Test the Connection and Close the Window<br>


### Data Warehouse - MongoDB

1. Get a Compatible MongoDB Client<br>
You can download MongoDB Compass [here](https://www.mongodb.com/try/download/compass).

2. Setup the Connection to the DWH<br>
    You can use these credentials to connect to the MongoDB:
    - Connection Method: TCP/IP
    - Hostname (aka IP Address)
    - Port


### Data Warehouse - Power BI

1. Download and install Power BI Desktop (rip mac users)
    You can get Power BI Desktop [here](https://www.microsoft.com/en-us/download/details.aspx?id=58494).


### Data Warehouse - Notebook

1. Locate the Example<br>
    - Clone the repository
    - You can find a jupyter notebook example with preconfigured connection [here](/dwh/examples/dwh_example.ipynb).    

2. Configure the environment variables<br>
    - In order to use the notebook you need to setup the .env file.
    - Clone the repo
    - Open the [.env.example](.env.example) file
    - Fill in the your credentials
    - Remove .example to enable the file

3. Execute the first code cell and use the factions to get a connecter.


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
