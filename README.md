
Table of Contents
=================

*   Project Overview
*   Installation Guide
    *   Environment Requirements
    *   Dependencies
    *   Distribution Files
    *   Installation Instructions
    *   Test Cases
*   User Guide

Project Overview
================

**Project Name:** Property Graph Model (PGM) C++ under the Task Analytical Performance Modeling (APM)
**Contact:** Arun Sathanur and/or Sutanay Choudhury. Email (for either) first_name.last_name@pnnl.gov


PGM-C++ is a C++/OpenMP software tool to generate statisitically equivalent property graphs from a given source property graph. The tool is currently capable of generating target datasets of similar or expanded sizes when compared to the source dataset. Property graphs can be used to represent heterogeneous networks with labeled (attributed) vertices and edges.Given a property graph, simulating another graph with same or greater size with the same statistical properties with respect to the labels and connectivity is critical for privacy preservation and benchmarking purposes. In this work we tackle the problem of capturing the statistical dependence of the edge connectivity on the vertex labels and using the same distribution to regenerate property graphs of the same or expanded size in a scalable manner. However, accurate simulation becomes a challenge when the attributes do not completely explain the network structure.  Our Property Graph Model (PGM) approach uses a label augmentation strategy to mitigate this problem and preserve the vertex label and the edge connectivity distributions as well as their correlation, while also replicating the degree distribution. We refer the reader to our CIKM 2017 paper for further details on the methods.

Citation: Sathanur, Arun V., Sutanay Choudhury, Cliff Joslyn, and Sumit Purohit. "When Labels Fall Short: Property Graph Simulation via Blending of Network Structure and Vertex Attributes." In Proceedings of the 2017 ACM on Conference on Information and Knowledge Management, pp. 2287-2290. ACM, 2017.

ACM link to the paper: https://dl.acm.org/citation.cfm?id=3133065

arXiv link to the paper: https://arxiv.org/abs/1709.02339 


Installation Guide for PGM-C++
==================

The following sections detail the compilation, packaging, and installation of the software. Also included are test data and scripts to verify the installation was successful.

Environment Requirements
------------------------

**Programming Language:** C++ and Python (Optional) to compare source and target dataset properties

**Operating System & Version:** RedHat Enterprise Linux or CentOS

**Required Disk Space:** 2 MB for source and executable files, 6 MB for examples, Output sizes can run into several GB depending on the size of the target requested

**Required Memory:** Depends on the target graph size generated. Upto 25 GB for billion edge graphs

**Nodes / Cores Used:** Tested upto Single Node / 20 cores

Dependencies
------------

The C++ portion of the software requires g++ compiler/linker with OpenMP support. Version 7.1 or later is recommended. This is part of the gcc 7.1 or latrer installlation

The python script that is optional and that is used to compare the properties of the source and target degree distributions, requires Python 2.7, and the Networkx, Numpy and Matplotlib (for plotting) modules.

Distribution Files
------------------

The software is packaged into three directories. The directories and their contents are described below

*  src : This contains all the source C++ files and the header files necessary. "pgm.cpp" provides the entry point to the program. "options.cpp" takes care of all the program options, "graph.cpp" is where all the work such as reading/writing files, building models, label augmentation gets done. "distributions.cpp" handles all the random distributions related functions. Finally "utils.cpp" provides some helper functions.
* scripts: This directory contains the Python script that can be used to compare the basic network properties of the source and the target datasets. The usage of this script is completely optional. If utilized, this script has some dependencies that are outlined previously.
* data: This directory holds three test cases and the options file needed to run each of them. Detailed description is provided in the Test Cases section


Installation Instructions
-------------------------
The installation is a very simple two step process.

1. Unzip the source files into the directory of choice
2. After ensuring that gcc/7.1+ is available on the system, from the "src" directory, run "make". After a few seconds the "pgm" executable will be generated.

Test Cases
----------

The "data" sub-directory contains three test cases as sub directories and three options files needed to run the three test cases. The three test cases are "role", "pa" and "netflow".

The corresponding options files are "options-role.txt", "options-pa.txt" and "options-netflow.txt" respectively. The three sub-directories corresponding to the test cases contain the source dataset edgelist for the source graph and the source node attribute values. File formats are described in detail in the user guide. Also included are reference outputs (with suffix op-ref) that were obtained by running the included options files with the included, corresponding source dataset files. Note that the "role" and "pa" examples are the primary testcases with smooth degree distributions whereas the real-world example "netflow" is more challenging and involves very skewed degree distributions.

For example ``./pgm ../data/options-role.txt``

User Guide
==========

A separate file "pgm-cpp-user_guide.pdf" is provided with the distribution which details the commands for running the program and the explanation of all the options.
