# ITk Quick Production Services (QPS)
Multi-functional CLI tool to optimise ATLAS ITk Pixel assemlby workflow. Includes automation of database queries and fast batch uploads of test runs (e.g. from .csv files). Redcues manual effort to retrieve(push) component(s) information from(to) the production database. 

## Details
![itkdb](https://img.shields.io/badge/itkdb-0.6.18-brightgreen)  

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license) 

## Installation
1. **Clone the repository**
```bash
   git clone https://github.com/4ndybuk/itk_qps.git
   cd itk_qps
```
2. **Install dependencies**
```bash
   pip install -r requirements.txt
```
4. **Run the application**
```bash
   python run_qps.py
```

## Usage
1. Use your ITk Prodcution Database login credentials to access the menu
2. Choose the service from the list of options (A -> G)
3. Retrieve(Push) information from(to) the database either by a single input or pre-filled .csv file

## License
1. This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
