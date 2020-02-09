# This is a simple tool designed to sync files on a local computer with workbooks in a LabKey Server.  

On the LabKey Server, a folder can have a series of workbooks, which will be numered sequentially starting with 1.  Assuming
you computer has a folder with subfolders corresponding to workbooks, this tool can be used to sync files from these local folders 
to the server.  Please see the script, syncFolder.py, for a more extensive explanation of the sync process and running the script.

## Installation

The script has the following requirements:

- [Install Python](https://www.python.org/downloads/)
- [Download the WebDav-Sync JAR file](https://sourceforge.net/projects/webdav-sync/)
- Checkout or download the syncFolder.py file from this repository

## Usage

See the example scripts in /example_usage.  Execution is fairly simple:

<pre>
python syncFolder.py \
	--serverUrl="https://myServer.edu/" \
	--labkeyFolderPath="/Labs/" \
	--username="username" \
	--password="password" \
	--localFolder=/Expts \
	--lastExecutionFile=/Expts/.lastWorkbookSync.txt \
	--jarFile=webdav_sync1_1_8.jar 2>&1 > /Expts/sync-log.txt
</pre>

In the above example, the file .lastWorkbookSync.txt will store the time of the last sync operation.  The next sync will only attempt to sync directories with a file modified after this time.  This can greatly reduce the runtime if your source files do not change often.  Also, the above example saves the output of the last sync to sync-log.txt.

## Scheduling for Automatic Backup

To run your script script on a schedule, consider cron for [linux](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/) and [osx](https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx.html).  On windows, consider [Task Scheduler](https://www.digitalcitizen.life/how-create-task-basic-task-wizard).
