transientNamer
==============

*A python package and command-line tools for working with and interacting with the Transient Naming Server*.

Here’s a summary of what’s included in the python package:

Command-Line Usage
==================

``` sourceCode
Documentation for transientNamer can be found here: http://transientNamer.readthedocs.org/en/stable

Usage:
    transientNamer [-c] search <ra> <dec> <arcsecRadius> [<render> | mysql <tableNamePrefix>] [-o directory]
    transientNamer [-c] search <name> [<render> | mysql <tableNamePrefix>] [-o directory]
    transientNamer [-c] new <discInLastDays> [<render> | mysql <tableNamePrefix>] [-o directory]

Commands:
    search                search the TNS and return the results
    new                   list newly discovered TNS objects

Arguments:
    ra
    dec
    arcsecRadius
    name                  the name of the object the search for (TNS or survey name)
    render                output format for results. Options include json, csv, table, markdown, yaml
    tableNamePrefix       the prefix for the tables to write the mysql insert statements for
    dirPath               path to the directory to save the output to

Options:
    -h, --help                           show this help message
    -v, --version                        show version
    -s, --settings                       the settings file
    -c, --withComments                   return TNS comments in result sets
    -o directory --output=directory      output to files in the directory path
```

Installation
============

The easiest way to install transientNamer us to use `pip`:

``` sourceCode
pip install transientNamer
```

Or you can clone the [github repo](https://github.com/thespacedoctor/transientNamer) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/transientNamer.git
cd transientNamer
python setup.py install
```

To upgrade to the latest version of transientNamer use the command:

``` sourceCode
pip install transientNamer --upgrade
```

Documentation
=============

Documentation for transientNamer is hosted by [Read the Docs](http://transientNamer.readthedocs.org/en/stable/) (last [stable version](http://transientNamer.readthedocs.org/en/stable/) and [latest version](http://transientNamer.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

This is a tutorial on how to use the command-line tools for transientNamer, to use transientNamer within your own python scripts please refer to the package’s documentation.

Search Types
------------

The are three kinds of search you can perform on the TNS with transientNamer; a *name* search, a *conesearch* or a search for *recent discoveries*.

### Name Search

To perform a name-search for the transient *Gaia16bbi*, run the command:

``` sourceCode
transientNamer search Gaia16bbi
```

The results are printed to stdout:

``` sourceCode
1 transients found

# Matched Transients
+---------------+------------+-------------+--------------+-----------------------------------------------+-----------+----------------+----------+----------------+-----------+----------+---------------+-----------+----------------------+----------+----------------+
| decSex        | TNSName    | discSurvey  | raSex        | objectUrl                                     | hostName  | transRedshift  | decDeg   | discoveryName  | raDeg     | TNSId    | hostRedshift  | specType  | discDate             | discMag  | discMagFilter  |
+---------------+------------+-------------+--------------+-----------------------------------------------+-----------+----------------+----------+----------------+-----------+----------+---------------+-----------+----------------------+----------+----------------+
| +22:03:00.70  | SN2016fbz  | GaiaAlerts  | 23:59:16.00  | http://wis-tns.weizmann.ac.il/object/2016fbz  |           | 0.045          | 22.0502  | Gaia16bbi      | 359.8167  | 2016fbz  |               | SN Ia     | 2016-08-16 19:59:31  | 17.4     | G-Gaia         |
+---------------+------------+-------------+--------------+-----------------------------------------------+-----------+----------------+----------+----------------+-----------+----------+---------------+-----------+----------------------+----------+----------------+

# Transient Photometry
+----------+--------------+----------------------+---------+--------------+----------+---------+----------+----------------+------------------------+----------+----------------------+-------------+
| TNSId    | survey       | obsdate              | filter  | limitingMag  | mag      | magErr  | magUnit  | suggestedType  | telescope              | exptime  | reportAddedDate      | objectName  |
+----------+--------------+----------------------+---------+--------------+----------+---------+----------+----------------+------------------------+----------+----------------------+-------------+
| 2016fbz  | Pan-STARRS1  | 2016-08-30 13:19:12  | w-PS1   | 0            | 17.8     | 0.02    | ABMag    | PSN            | PS1_GPC1               | 45       | 2016-09-02 15:54:03  | PS16ebg     |
| 2016fbz  | iPTF         | 2016-08-25 12:00:00  | g-PTF   | 0            | 17.2823  |         | ABMag    | PSN            | P48_CFH12k             | 60       | 2016-08-25 12:34:00  | iPTF16fbz   |
| 2016fbz  | iPTF         | 2009-01-01 00:00:00  | R-PTF   | 1            | 21.5     |         | ABMag    | PSN            | P48_CFH12k             | 60       | 2016-08-25 12:34:00  | iPTF16fbz   |
| 2016fbz  | GaiaAlerts   | 2016-08-16 19:59:31  | G-Gaia  | 0            | 17.4     | 0.2     | ABMag    | PSN            | Gaia_Gaia-photometric  | 60       | 2016-08-19 09:13:29  | Gaia16bbi   |
| 2016fbz  | GaiaAlerts   | 2016-07-05 02:38:24  | G-Gaia  | 1            | 21.5     |         | ABMag    | PSN            | Gaia_Gaia-photometric  |          | 2016-08-19 09:13:29  | Gaia16bbi   |
+----------+--------------+----------------------+---------+--------------+----------+---------+----------+----------------+------------------------+----------+----------------------+-------------+

# Transient Spectra
+----------+---------+----------------------+-----------+----------------+----------------------+----------+----------------------+----------+
| TNSId    | survey  | obsdate              | specType  | transRedshift  | telescope            | exptime  | reportAddedDate      | TNSuser  |
+----------+---------+----------------------+-----------+----------------+----------------------+----------+----------------------+----------+
| 2016fbz  | iPTF    | 2016-08-26 08:56:52  | SN Ia     | 0.045          | P60_SED-Machine      |          | 2016-09-02 08:06:07  | rferr    |
| 2016fbz  |         | 2016-08-27 14:24:00  | SN Ia     | 0.045          | BAO-2.16m_Phot-spec  | 3000     | 2016-09-02 08:06:07  | rferr    |
+----------+---------+----------------------+-----------+----------------+----------------------+----------+----------------------+----------+

# Transient Supplementary Files
+----------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+----------------------+-------------+
| TNSid    | filename                                                    | url                                                                                                                   | dateObs              | spec1phot2  |
+----------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+----------------------+-------------+
| 2016fbz  | tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii  | https://wis-tns.weizmann.ac.il/system/files/uploaded/iPTF/tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii  | 2016-08-26 08:56:52  | 1           |
| 2016fbz  | tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt           | https://wis-tns.weizmann.ac.il/system/files/uploaded/general/tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt        | 2016-08-27 14:24:00  | 1           |
+----------+-------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------+----------------------+-------------+

# Original TNS Search URL
https://wis-tns.weizmann.ac.il/search?decl=&date_end%5Bdate%5D=&num_page=1000&display%5Bsources%5D=1&name=&display%5Bdiscmagfilter%5D=1&display%5Bspectra_count%5D=1&display%5Bdiscoverymag%5D=1&display%5Bdiscoverydate%5D=1&display%5Bhost_redshift%5D=1&date_start%5Bdate%5D=&radius=&ra=&internal_name=iPTF16fbz&display%5Bsource_group_name%5D=1&display%5Bbibcode%5D=1&display%5Bredshift%5D=1&display%5Binternal_name%5D=1&page=0&display%5Bhostname%5D=1&display%5Bdiscoverer%5D=1
```

Run the same command now with the -c flag to also return the comments and remarks about the data found in the TNS. Note the comments tend to clutter up the output and make it less readable:

``` sourceCode
transientNamer -c search Gaia16bbi
```

You can use any name the transient is known as to search the TNS

``` sourceCode
transientNamer search SN2016fbz
transientNamer search 2016fbz
transientNamer search PS16ebg
transientNamer search iPTF16fbz
```

### Conesearch

To perform a conesearch on the TNS use a command with the syntax:

``` sourceCode
transientNamer [-c] cone <ra> <dec> <arcsecRadius>
```

So to return the same result as the name search above run the following:

> transientNamer cone 23:59:16.00 +22:03:00.70 5

or

> transientNamer cone 359.8167 22.0502 5

### Recent Discoveries

If you want to return a list of transients that have been recently discovered, use the command syntax:

``` sourceCode
transientNamer [-c] new <discInLastDays>
```

So to return transients discovered in the past 3 weeks:

``` sourceCode
transientNamer new 21
```

The recent discovery search will often return many transients, but data for individual transients are always reported with the transient’s unique TNSId.

Results
-------

### Four Categories of Results

Each search will always return four types of data

1.  **Source Data** - top-level discovery and classification data
2.  **Photometry Data** - time series photometry
3.  **Spectral Data** - any classification and spectral coverage information
4.  **Related Files** - any related image stamps, finder charts, spectral FITS or ascii files etc.

The URL built to generate the search of the TNS is also returned if you want to view the results via the TNS webpages.

### Rendering Results

By default the results are rendered as easily readable ascii tables. But by passing a few extra arguments to the command-line it’s possible to render the results in a variety of different formats; *csv*, *json*, *yaml*, *table* or *markdown*:

``` sourceCode
transientNamer search PS16ebg csv
transientNamer search PS16ebg json
transientNamer search PS16ebg yaml
transientNamer search PS16ebg table
transientNamer search PS16ebg markdown
```

It is also possible to render the results as mysql insert statements to add the results to a set of mysql database tables. The rendering requires an extra tableNamePrefix argument, that acts as the prefix to the table names use in mysql insert statements.

``` sourceCode
transientNamer search PS16ebg mysql tns
```

``` sourceCode
1 transient found

# Matched Transients
INSERT INTO `tns_transients` (TNSId,TNSName,dateCreated,decDeg,decSex,discDate,discMag,discMagFilter,discSurvey,discoveryName,hostName,hostRedshift,objectUrl,raDeg,raSex,specType,transRedshift) VALUES ("2016fbz" ,"SN2016fbz" ,"2016-09-20T15:23:05" ,"22.05019" ,"+22:03:00.70" ,"2016-08-16 19:59:31" ,"17.4" ,"G-Gaia" ,"GaiaAlerts" ,"Gaia16bbi" ,null ,null ,"http://wis-tns.weizmann.ac.il/object/2016fbz" ,"359.816667" ,"23:59:16.00" ,"SN Ia" ,"0.045")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", TNSName="SN2016fbz", dateCreated="2016-09-20T15:23:05", decDeg="22.05019", decSex="+22:03:00.70", discDate="2016-08-16 19:59:31", discMag="17.4", discMagFilter="G-Gaia", discSurvey="GaiaAlerts", discoveryName="Gaia16bbi", hostName=null, hostRedshift=null, objectUrl="http://wis-tns.weizmann.ac.il/object/2016fbz", raDeg="359.816667", raSex="23:59:16.00", specType="SN Ia", transRedshift="0.045", updated=1, dateLastModified=NOW() ;


# Transient Photometry
INSERT INTO `tns_photometry` (TNSId,dateCreated,exptime,filter,limitingMag,mag,magErr,magUnit,objectName,obsdate,reportAddedDate,suggestedType,survey,telescope) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"45" ,"w-PS1" ,"0" ,"17.8" ,"0.02" ,"ABMag" ,"PS16ebg" ,"2016-08-30 13:19:12" ,"2016-09-02 15:54:03" ,"PSN" ,"Pan-STARRS1" ,"PS1_GPC1")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", dateCreated="2016-09-20T15:23:05", exptime="45", filter="w-PS1", limitingMag="0", mag="17.8", magErr="0.02", magUnit="ABMag", objectName="PS16ebg", obsdate="2016-08-30 13:19:12", reportAddedDate="2016-09-02 15:54:03", suggestedType="PSN", survey="Pan-STARRS1", telescope="PS1_GPC1", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_photometry` (TNSId,dateCreated,exptime,filter,limitingMag,mag,magErr,magUnit,objectName,obsdate,reportAddedDate,suggestedType,survey,telescope) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"60" ,"g-PTF" ,"0" ,"17.2823" ,"" ,"ABMag" ,"iPTF16fbz" ,"2016-08-25 12:00:00" ,"2016-08-25 12:34:00" ,"PSN" ,"iPTF" ,"P48_CFH12k")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", dateCreated="2016-09-20T15:23:05", exptime="60", filter="g-PTF", limitingMag="0", mag="17.2823", magErr="", magUnit="ABMag", objectName="iPTF16fbz", obsdate="2016-08-25 12:00:00", reportAddedDate="2016-08-25 12:34:00", suggestedType="PSN", survey="iPTF", telescope="P48_CFH12k", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_photometry` (TNSId,dateCreated,exptime,filter,limitingMag,mag,magErr,magUnit,objectName,obsdate,reportAddedDate,suggestedType,survey,telescope) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"60" ,"R-PTF" ,"1" ,"21.5" ,"" ,"ABMag" ,"iPTF16fbz" ,"2009-01-01 00:00:00" ,"2016-08-25 12:34:00" ,"PSN" ,"iPTF" ,"P48_CFH12k")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", dateCreated="2016-09-20T15:23:05", exptime="60", filter="R-PTF", limitingMag="1", mag="21.5", magErr="", magUnit="ABMag", objectName="iPTF16fbz", obsdate="2009-01-01 00:00:00", reportAddedDate="2016-08-25 12:34:00", suggestedType="PSN", survey="iPTF", telescope="P48_CFH12k", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_photometry` (TNSId,dateCreated,exptime,filter,limitingMag,mag,magErr,magUnit,objectName,obsdate,reportAddedDate,suggestedType,survey,telescope) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"60" ,"G-Gaia" ,"0" ,"17.4" ,"0.2" ,"ABMag" ,"Gaia16bbi" ,"2016-08-16 19:59:31" ,"2016-08-19 09:13:29" ,"PSN" ,"GaiaAlerts" ,"Gaia_Gaia-photometric")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", dateCreated="2016-09-20T15:23:05", exptime="60", filter="G-Gaia", limitingMag="0", mag="17.4", magErr="0.2", magUnit="ABMag", objectName="Gaia16bbi", obsdate="2016-08-16 19:59:31", reportAddedDate="2016-08-19 09:13:29", suggestedType="PSN", survey="GaiaAlerts", telescope="Gaia_Gaia-photometric", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_photometry` (TNSId,dateCreated,exptime,filter,limitingMag,mag,magErr,magUnit,objectName,obsdate,reportAddedDate,suggestedType,survey,telescope) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"" ,"G-Gaia" ,"1" ,"21.5" ,"" ,"ABMag" ,"Gaia16bbi" ,"2016-07-05 02:38:24" ,"2016-08-19 09:13:29" ,"PSN" ,"GaiaAlerts" ,"Gaia_Gaia-photometric")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", dateCreated="2016-09-20T15:23:05", exptime="", filter="G-Gaia", limitingMag="1", mag="21.5", magErr="", magUnit="ABMag", objectName="Gaia16bbi", obsdate="2016-07-05 02:38:24", reportAddedDate="2016-08-19 09:13:29", suggestedType="PSN", survey="GaiaAlerts", telescope="Gaia_Gaia-photometric", updated=1, dateLastModified=NOW() ;


# Transient Spectra
INSERT INTO `tns_spectra` (TNSId,TNSuser,dateCreated,exptime,obsdate,reportAddedDate,specType,survey,telescope,transRedshift) VALUES ("2016fbz" ,"rferr" ,"2016-09-20T15:23:05" ,"" ,"2016-08-26 08:56:52" ,"2016-09-02 08:06:07" ,"SN Ia" ,"iPTF" ,"P60_SED-Machine" ,"0.045")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", TNSuser="rferr", dateCreated="2016-09-20T15:23:05", exptime="", obsdate="2016-08-26 08:56:52", reportAddedDate="2016-09-02 08:06:07", specType="SN Ia", survey="iPTF", telescope="P60_SED-Machine", transRedshift="0.045", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_spectra` (TNSId,TNSuser,dateCreated,exptime,obsdate,reportAddedDate,specType,survey,telescope,transRedshift) VALUES ("2016fbz" ,"rferr" ,"2016-09-20T15:23:05" ,"3000" ,"2016-08-27 14:24:00" ,"2016-09-02 08:06:07" ,"SN Ia" ,"" ,"BAO-2.16m_Phot-spec" ,"0.045")  ON DUPLICATE KEY UPDATE  TNSId="2016fbz", TNSuser="rferr", dateCreated="2016-09-20T15:23:05", exptime="3000", obsdate="2016-08-27 14:24:00", reportAddedDate="2016-09-02 08:06:07", specType="SN Ia", survey="", telescope="BAO-2.16m_Phot-spec", transRedshift="0.045", updated=1, dateLastModified=NOW() ;


# Transient Supplementary Files
INSERT INTO `tns_files` (TNSid,dateCreated,dateObs,filename,spec1phot2,url) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"2016-08-26 08:56:52" ,"tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii" ,"1" ,"https://wis-tns.weizmann.ac.il/system/files/uploaded/iPTF/tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii")  ON DUPLICATE KEY UPDATE  TNSid="2016fbz", dateCreated="2016-09-20T15:23:05", dateObs="2016-08-26 08:56:52", filename="tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii", spec1phot2="1", url="https://wis-tns.weizmann.ac.il/system/files/uploaded/iPTF/tns_2016fbz_2016-08-26_08-56-52_P60_SED-Machine_iPTF.ascii", updated=1, dateLastModified=NOW() ;
INSERT INTO `tns_files` (TNSid,dateCreated,dateObs,filename,spec1phot2,url) VALUES ("2016fbz" ,"2016-09-20T15:23:05" ,"2016-08-27 14:24:00" ,"tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt" ,"1" ,"https://wis-tns.weizmann.ac.il/system/files/uploaded/general/tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt")  ON DUPLICATE KEY UPDATE  TNSid="2016fbz", dateCreated="2016-09-20T15:23:05", dateObs="2016-08-27 14:24:00", filename="tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt", spec1phot2="1", url="https://wis-tns.weizmann.ac.il/system/files/uploaded/general/tns_2016fbz_2016-08-27.60_BAO-2.16m_Phot-spec.txt", updated=1, dateLastModified=NOW() ;


# Original TNS Search URL
https://wis-tns.weizmann.ac.il/search?decl=&date_end%5Bdate%5D=&num_page=1000&display%5Bsources%5D=1&name=&display%5Bdiscmagfilter%5D=1&display%5Bspectra_count%5D=1&display%5Bdiscoverymag%5D=1&display%5Bdiscoverydate%5D=1&display%5Bhost_redshift%5D=1&date_start%5Bdate%5D=&radius=&ra=&internal_name=PS16ebg&display%5Bsource_group_name%5D=1&display%5Bbibcode%5D=1&display%5Bredshift%5D=1&display%5Binternal_name%5D=1&page=0&display%5Bhostname%5D=1&display%5Bdiscoverer%5D=1 
```

### Saving to File

To save the results to file instead of outputting to stdout, pass in the path to the directory you want to save the results to. The four categories of results are save to four separate file.

For ascii tables run either of the 2 commands:

``` sourceCode
transientNamer search PS16ebg -o /path/to/tns-data
transientNamer search PS16ebg tables -o /path/to/tns-data
```

<img src="https://i.imgur.com/m09M0ho.png" alt="ascii files" width="800" />

For csv:

``` sourceCode
transientNamer search PS16ebg csv -o /path/to/tns-data
```

<img src="https://i.imgur.com/BwwqMBg.png" alt="csv output" width="800" />

For yaml:

``` sourceCode
transientNamer search PS16ebg yaml -o /path/to/tns-data
```

<img src="https://i.imgur.com/ZpJIC6p.png" alt="yaml output" width="800" />

For json:

``` sourceCode
transientNamer search PS16ebg json -o /path/to/tns-data
```

<img src="https://i.imgur.com/wAHqARI.png" alt="json output" width="800" />

For markdown tables:

``` sourceCode
transientNamer search PS16ebg markdown -o /path/to/tns-data
```

<img src="https://i.imgur.com/AYLBQoJ.png" alt="markdown output" width="800" />

For mysql inserts:

``` sourceCode
transientNamer search PS16ebg mysql tns -o /path/to/tns-data
```

<img src="https://i.imgur.com/CozySPW.png" alt="mysql output" width="800" />

When exporting to file, the mysql insert statements also come with table create statements so that if the table doesn’t yet exist in the database you are importing into it will be created for you will all of the correct field types and unique index constraints applied.
