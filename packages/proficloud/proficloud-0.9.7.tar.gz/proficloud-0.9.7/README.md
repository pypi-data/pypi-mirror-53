# PROFICLOUD Python package
Alexander von Birgelen, avonbirgelen@phoenixcontact.com

This is the Git-repository of the PROFICLOUD Python package.
This is a development version.
Testing is done with Python3.6 and newer.

## The idea

PROFICLOUD already has several running solutions where time series data (TSD) is stored. The solutions for TSD and EWIMA use a Kairosdb in the backend which can be accessed through RESTful web services.
Accessing the data to have it available for machine learning is key. Also, the data has to be available in the state-of-the-art data science tools and libraries. 

The solution for this is a library, written in Python 3, which is outlined in this section.

At this point in time, the typical PROFICLOUD user is probably no data scientist or not even a programmer, which is why in the beginning most of the development for customers has to be done by the PROFICLOUD-team. The programming efforts have to be simplified or hidden completely. Since data success is key, a library is required that the PROFICLOUD-team can use. The library can also be made available to experienced or advanced customers who want to develop their own solution. For this, good documentation and many examples are required.

The library development should follow the minimum-viable-product concept: starting with basic features and implement more functionality over time.
First, access to the different time series data solutions (TSD, EWIMA) is needed. This can be used to develop first solutions and test application of machine learning to different use cases at Phoenix Contact, for example the ballpen-maker, the trabtech smartspd and the smart safety relays. From the solutions it should be possible to derive building block and functions for the library or integrate functionality into the library directly. 
A future feature could be the access to the PLCnext GDS for deployment purposes.

The development of the Proficloud Python package (libraries are called packages in Python while the functionalities within the packages are called modules) has already started to show the possibilities, develop the concepts, and develop first solutions. It is also possible to nest packages. 
The package can be extended in several ways as demand for specific functionality arises. Currently, interaction with TSD is in focus as it is te base for other technologies such as the machine learning part. Different solutions dealing with time series data exist in PROFICLOUD: TSD and Ewima. Both TSD services are backed by a Kairosdb running on top of a Cassandra database. The Kairosdb offers a convenient REST-interface to query data. Repeating functionality should always be bundled in separate classes of functions for easy re-use. Since authentication is a little different for TSD and Ewima, a KairosdbConnector class was created and sub-classes for TSD and Ewima (which set the appropriate authentication header and uri) can be created. A first implementation for the Kairosdb connector and TSD is already available.

Current and future sub-packages and modules for the PROFICLOUD package are listed below. The mentioned functionalities go in line with the concepts presented in this document.


## The structure

* proficloud
  *	proficloud.timeseries
    * proficloud.kairos
      Base interface for querying Kairos
    * proficloud.tsd
      TSD connector (sub-class of Kairos-connector)
    * proficloud.ewima
      Not done yet
    * proficloud.stream
      Streaming functionality using the KairosConnector (currently using “streamz”, Spark streaming implementation planned when needed)
    * proficloud.proficloudutil
      Utility functions used my multiple other classes and modules in timeseries (currently time and pandas handling functions)
  * proficloud.api
    Planned package: integration with the other REST APIs available via Connector4C SDK.
  * proficloud.machinelearning
    Planned package: pre-defined machine learning and preprocessing modules for CM/PM, and more. Also provides interface to SageMaker hosted algorithms
  * proficloud.plcnext
    Planned package: access to PLCnext GDS
  * …?

## Installation

After cloning, you can cd into the target folder and install this via a symlink with:
```
pip3 install -e . --user
```

## Documentation

The source code should be documented using docstrings and Sphinx is used to generate HTML documentation in docs/html.
Just call the makeDoc.sh shell script to automatically generate the documentation.

```
pip3 install sphinx_rtd_theme --user
pip3 install sphinxcontrib-confluencebuilder --user
pip3 install twine --user

./makeDoc.sh
./publish_pypi.sh
```

## Development

* The master branch always contains the currently working production version.
* Versions are marked with tags.
* The develop branch is the main development branch.
* Feature branches are created for new features and merged back into develop when the feature is implemented.
* Release branches are used to transfer new current state of the develop branch to the production master branch.
* Hotfix branches can be used to fix bugs found in the master branch without interfering with current planned development.

![Branching](./branching.PNG)

The idea originates from the following video: https://www.youtube.com/watch?v=aJnFGMclhU8

## Committing IPython notebooks

Currently, no nice way of checking in notebooks is available. There is the nbdime package, but this seems not to be working at this point in time.
The solution will be added to this readme once available.