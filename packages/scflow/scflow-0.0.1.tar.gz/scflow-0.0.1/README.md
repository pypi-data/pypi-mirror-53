# scflow

<p align="left">
	<a href='https://single-cell.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/single-cell/badge/?version=latest' alt='Documentation Status' /></a>
	<a href="https://travis-ci.com/Acribbs/single-cell.svg?branch=master", alt="Travis">
		<img src="https://travis-ci.com/Acribbs/single-cell.svg?branch=master" /></a>
	<a href="https://twitter.com/CribbsP?lang=en", alt="Twitter followers">
		<img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social&logo=twitter" /></a>
</p>


This repository contains a collection of pipelines that aid the analysis of single cell sequencing experiments. Currently there is one pipeline implimented that allows the analysis of drop-seq and 10X sequencing analysis. Current pipelines in development: 1) velocyto pipeline 2) smart-seq2 pipeline.

## Installation

### Conda installation

The preferred method for installation is through conda. Currently this installation is still in working progress. Preferably the 
installation should be in a seperate environment::

    conda create -n single-cell -c cgat single-cell
    conda activate single-cell
    single_cell --help
   
### Manual installation

The respository can also be installed manually, but dependancies will need to be installed seperately::

    python setup.py install
    single_cell --help
    
## Usage

Run the ``single_cell --help`` command view the help documentation for how to run the single-cell repository.

To run the main single_cell droplet based pipeline run first generate a configuration file::

    single_cell singlecell config

Then run the pipeline::

    single_cell singlecell make full -v5
    
Then to run the report::

    single_cell singlecell make build_report
    
## Documentation

Further help that introduces single-cell and provides a tutorial of how to run example
code can be found at [read the docs](http://single-cell.readthedocs.io/)
