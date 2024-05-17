# Trost: Projekt - SoSe2024

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Installation

## Usage

### References

- [API](https://docs.google.com/spreadsheets/d/1itYdtVbfjQgLpScrXZugvm9qUZenOuqP/edit?usp=sharing&ouid=112245649497495850593&rtpof=true&sd=true)
- [Frontend](https://knaeckebrothero.github.io/University-Projekt-SoSe24/)
- [Server](109.91.181.97)

### Data warehouse

#### Get a Compatible SQL Client
You can download MySQL Workbench here:<br>
[https://dev.mysql.com/downloads/workbench/](https://dev.mysql.com/downloads/workbench/)

#### Setup the Connection to the DWH
You can use the following credentials to connect to the DWH:
- Connection Method: TCP/IP
- Hostname: [IP](109.91.181.97)
- Port: 31749
- Username: root
- Password: [Password](4fAXg!jq@2&8B986hAU@J#T)

#### Setup SSL to Encrypt Traffic Between You and the Database
1. Set "Use SSL" to "Require and Verify CA".
2. Save the files from the repository deployment/encryption/ssl/ and specify them as follows:
    - SSL Key: client-key.pem
    - SSL CERT: client-cert.pem
    - SSL CA: ca.pem

#### Test the Connection and Close the Window
**Note:** You may generate your own certificate if desired. If you wish to do so, please reach out to me to get it signed.

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
