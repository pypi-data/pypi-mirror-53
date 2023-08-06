# Finance Scraper

## Table of contents
1. [Description](README.md#description)
2. [AWS infrastructure](README.md#aws-infrastructure)
3. [General prerequisites](README.md#general-prerequisites)
4. [Local installation](README.md#local-installation)
5. [Cloud installation](README.md#cloud-installation)

## Description
This repository contains a Extract-Transform-Load (ETL) pipeline which extracts security
data details from pages on morningstar.fr (see [an example here](http://tools.morningstar.fr/fr/stockreport/default.aspx?Site=fr&id=0P0001A178&LanguageId=fr-FR&SecurityToken=0P0001A178]3]0]E0WWE$$ALL,DREXG$XHEL,DREXG$XLON,DREXG$XNYS)). The steps of the pipeline are:
* extract: scrape web pages and save them raw on AWS S3.
* transform: parse raw web pages and store the results in a CSV file, then store in S3.
* load: copy the CSV file into a PostgresSQL database.

The pipeline can be run locally and load data in a database provided by the user, or in the Amazon Web Services cloud on an infrastructure built automatically by this software.

## AWS infrastructure
The AWS infrastructure provisioned here is free-tier, and should cost you a minimal amount of money once you finish your free-tier allowance.
The infrastructure is managed with Terraform and composed of the following elements (see picture below):
* an EC2 instance running Apache Airflow.
* an autoscaling group maintains a single running Airflow instance at all times.
* a security group for the Airflow instance allowing inbound SSH (admin tasks) and TCP traffic (Airflow webserver) only from your IP address.
* a data warehouse consisting of an RDS instance running the PostgresSQL engine, and hosted on a private subnet.
* a metadata database to store Airflow tasks status on a PostgresSQL RDS instance.
* a VPC with a public subnet to host the Airflow instance and a private subnet to host the data warehouse.
* an IAM role that allows the EC2 instance to communicate with S3 and RDS.
* 3 S3 buckets to store the Terraform state files, the scraped data, and the Airflow logs

<img src="docs/images/finance_scraper.png" width="800" alt="architecture" >

## General prerequisites
* this software is designed to work on a Linux distribution.
* Python 3.6 or a superior version is required.
* you need to provide a file containing a list of URLs to scrape (one URL per line, see an example URL in the description paragraph). Name this file `scraping_links.txt` and place it in folder `finance_scraping` (where the `main.py` module is located).

## Local installation
### Prerequisites
The following packages are required and will be installed along with `finance-scraping`:
* requests >= 2.22
* BeautifulSoup4 >= 4.7.1
* psycopg2 >= 2.8

You need to install PostgresSQL, and create a database to load data into. Take note of the user name and password with write privileges to this database, as you will need these during the configuration of `finance-scraping`.

### Installation and configuration
* Run `pip install finance-scraping`.
* Run `finance-scraper -c` to set the configuration of the scraper. You will be prompted to enter configuration values, which are saved in `~/.bashrc`.
* If you plan to run `finance-scraper` on an EC2 instance launched with an instance role, you can set the parameters `profile` as `None`.

### How to run
To run the entire ETL pipeline, run `finance-scraper -etl`. You can also run `finance-scraper` with any of the optional arguments `-e`, `-t` or `-l` to run an individual step. It is possible to specify the date parameter `-d` with `-t` and/or `-l` to process data scraped on a specific date. For more information run help with `finance-scraper -h`.

### Schedule runs with Apache Airflow
* Read the [Airflow documentation](https://airflow.apache.org/index.html) to install and configure Airflow for your system.
* Amend the file `finance_scraping_dag.py` from the `finance_scraping` folder with your scheduling preferences and copy it into the `dags` folder of your Airflow installation before starting the scheduler.

## Cloud installation
### Prerequisites
If you do not have an AWS account, create one [here](https://aws.amazon.com/console). Create a user with administrator permissions that Terraform will use to build the infrastructure by following these [instructions](https://docs.aws.amazon.com/mediapackage/latest/ug/setting-up-create-iam-user.html). Install the AWS command-line interface by running `pip install aws-cli` and configure it according to the [documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Install [Terraform 0.12](https://learn.hashicorp.com/terraform/getting-started/install.html).

### Installation and configuration
Run `pip install finance-scraping` to install the software. Run `finance-scraper --build` to start the configuration wizard and build the infrastructure in AWS. Parameters will be displayed one by one with the current value shown between brackets (empty brackets indicated the absence of value). It is required to provide a value for all parameters. The parameters are:
* aws_profile: the AWS user Terraform should assume to build the infrastructure.
* region: the AWS region where to build the infrastructure.
* user_agent: the User-Agent to use when scraping web pages. It is recommended to provide your email address so that the website administrator can contact you if there is a problem. If you want to include spaces, put the value to this parameter between quotes.
* max_retries: the maximum number of times the web scraper should retry a page when the request fails. 10 is an acceptable value.
* backoff_factor: factor to calculate delay times to apply when the request receives an error. 0.3 is an acceptable value. Learn more [here](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry).
* retry_on: comma-separated HTTP status codes that trigger a new request. An acceptable value is 500,502,503,504.
* timeout: timeout for the request in seconds. An acceptable value is 20.
* db_username: username to use when setting up the database.
* db_password: password to use when setting up the database.

Provisioning of the AWS infrastructure will start and takes between 10 and 15 minutes.

### Monitoring your infrastructure
When provisioning is done, you can take note of the public IP of the EC2 instance running Airflow on the AWS console and check the Airflow dashboard on port 8080. You can SSH into instance using the key `airflow-instance-ssh` located in your `~/.ssh` folder.

### Destroying the infrastructure
The whole infrastructure can be destroyed by running `finance-scraper --nuke`.

### Warning
Do not modify the configuration files manually (`.terraform` folders, `terraform.tfstate` files and `~/.bash_non_interactive` file). This will break your installation and require painful cleaning.

Be responsible when web scraping, and do not put a high burden on web servers by requesting a lot of pages in a short amount of time. It makes the job of maintaining webservers harder and you could be banned from accessing the website.
