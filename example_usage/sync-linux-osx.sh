#/bin/bash

python syncFolder.py \
	--serverUrl="https://myServer.edu/" \
	--labkeyFolderPath="/Labs/" \
	--username="username" \
	--password="password" \
	--localFolder=/Expts \
	--lastExecutionFile=/Expts/.lastWorkbookSync.txt \
	--jarFile=webdav_sync1_1_8.jar 2>&1 > sync-log.txt

echo 'Sync Done' >> log.txt
