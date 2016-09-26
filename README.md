# This is a simple tool designed to sync files on a local computer with workbooks in a LabKey Server.  
On the LabKey Server, a folder can have a series of workbooks, which will be numered sequentially starting with 1.  Assuming
you computer has a folder with subfolders corresponding to workbooks, this tool can be used to sync files from these local folders 
to the server.  Please see the script, syncFolder.py, for a more extensive explanation of the sync process and running the script.

#Installation
The script has the following requirements:

- [Install Python](https://www.python.org/downloads/)
- [Download the WebDav-Sync JAR file](https://sourceforge.net/projects/webdav-sync/)
- Checkout or download the syncFolder.py file from this repository
