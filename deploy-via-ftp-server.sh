#!/bin/sh

# echo $GO_SCM_DEFAULT_CMF_PR_BRANCH
if [ -n $GO_SCM_DEFAULT_CMF_PR_BRANCH] && [ "mapaction:master" = $GO_SCM_DEFAULT_CMF_PR_BRANCH ]
then
  echo deploy from master
  lftp -f default-cmf/deploy-via-ftp-server.lftp.txt
else
  echo not deploying from non-master branch
fi
