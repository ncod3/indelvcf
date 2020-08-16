# Indelvcf
indelvcf

## Features

## Contents

## Requirement

~~~
python 3.7

bcftools
sbava
~~~

## Installation

~~~
You can use vprimer enviromment on conda.
If you have not yet made vprimer environment on conda, you can make it.
$ conda create -n run_vprimer python=3.7
$ source activate run_vprimer
$ pip install git+https://github.com/ncod3/indelvcf

If you want to uninstall indelvcf, 
$ pip uninstall indelvcf




if you have not yet made vprimer environment on conda, you can make it.

$ conda create -n run_vprimer python=3.7
$ source activate run_vprimer
$ (run_vprimer) pip install git+https://github.com/ncod3/indelvcf

We recommend that you start by uninstalling vprimer as it will be updated frequently.

$ (run_vprimer) pip uninstall indelvcf

Even if vprimer is not installed, the following message will be output.
WARNING: Skipping vprimer as it is not installed.

$ (run_vprimer) conda install -c bioconda bcftools
$ (run_vprimer) conda install -c bioconda tabix
$ (run_vprimer) conda install -c bioconda svaba

~~~

## Getting Started

~~~
Get the sample data.

$ cd (your working directory)
$ git clone https://github.com/ncod3/data_vprimer
$ mv data_vprimer/ini* .

$ indelvcf -c ini_indelvcf_yam_small5.ini -t 10
~~~

## Usage

## Note

## Authors
- Satoshi Natsume

See also the list of contributors who participated in this project.

## Licence
This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgements

