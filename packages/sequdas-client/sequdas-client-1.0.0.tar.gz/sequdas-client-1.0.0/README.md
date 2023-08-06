# SeqUDAS: Sequence Upload and Data Archiving System

## Overview

Modern DNA sequencing machines generate several gigabytes (GB) of data per run. Organizing and archiving this data presents a challenge for small labs. We present a Sequence Upload and Data Archiving System (SeqUDAS) that aims to ease the task of maintaining a sequence data repository through process automation and an intuitive web interface.

## Features

- Automated upload and storage of sequence data to a central storage server.
- Data validation with MD5 checksums for data integrity assurance
- [Illumina modules](https://bitbucket.org/invitae/illuminate) are incorpated to parse metrics binaries and generate a report similar to Illumina SAV.
- FASTQC and MultiQC workflows are included to perform QC analysis automatically.
- A taxonomic report will be generated based on Kraken report 
- Archival information, QC results and taxonomic report can be viewed through a mobile-friendly web interface
- Pass sequence data along to another remote server via API (IRIDA) 

## Architecture

SeqUDAS consists of three components:

- Data manager: Installed on a PC directly attached to an illumina sequencing machine.
- Data analyzer: Installed on a server to run the data analysis jobs.
- Web Application: Installed on a web server to provide account management and report viewing.