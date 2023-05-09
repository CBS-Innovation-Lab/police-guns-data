# police guns data mining

This repo contains the data and code used to search various sources of firearm recovery data against serial numbers of firearms known to have been sold by police departments back to the public.

## Data sources

Any data files used in this project (aside from the sale data, which is stored in airtable) are in [raw](raw/).

### Data gathered from local police departments

We're using data files gathered through records requests to a number of police departments in the US. Relevant data is extracted from them in [task #1](tasks/1-extract-serials).

### Missing pieces data

I am also using a large amount of firearm recovery data contributed by The Trace during their ["Missing Pieces"](https://www.thetrace.org/missing-pieces-data/) project.

### Federal court filings

We are also using data scraped from alerts for federal court filings scraped by The Trace. That data is stored in json files in [raw/gun_cases](raw/gun_cases/) and is cleaned in [task #3](tasks/3-merge-gun-cases).

## Workflow

This pipeline is split up into tasks in the [tasks](tasks/) folder. Each task folder contains an input folder, which contains symlinks to output files from previous tasks (or the raw data). Each task folder also contains a Makefile which runs the task, and, optionally, a src directory containing task-specific scripts. 

Any scripts used by two or more tasks are stored in the [src](src/) directory in the project root. 

## How to run

### System requirements

This pipeline is intended to be run on a machine running ubuntu, with at least 4gb ram.

### Set up airtable

You need to have access to our police guns airtable, which is where the sale serials are stored. You also need to have your airtable API key saved to the AIRTABLE_API_KEY environment variable, or have that saved in a .env file in the project root.

### Set up environment

Upon cloning this repo, run the `make setup` command, which will create a python virtual environment, install any necessary packages, and initialize Git LFS and pull any files that aren't stored on github directly. 

### Run the pipeline

In the root of the project, run `make` to run the entire pipeline. Each task will run sequentially.
