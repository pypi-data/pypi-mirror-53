# HY_sshapi  
A set of APIs used to contact with a remote (linux-like) server.  
# Usage 
```
from SSH_Operation.SSH_Operation import SSH_Operation
ssh = SSH_Operation({})
```
# Methods 
```

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   SSH_Operation
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 
#          2019/03/16
#                new upload function, to upload dir without compression.   
#          2019/03/09: 
#                1. rebuilt interface of InteractiveConnectionSSH
#                2. change filename to from RemoteContral1
#                3. make a package contains interface.py
#          2019/03/01
#          2018/06/01
#          2018/02/28
#          2017/09/04
#──────────────────────────
# discription:
#          operation between local PC with a remote server
#          remember to call connect or disconnect for some function.
#
#──────────────────────────
# Imported :
#     shutil , tempfile , stat
import paramiko
import shutil,os,tempfile,random
from .interactive import *  
# import SSH_Operation.interactive as interactive
#──────────────────────────
# Interface:
#
#        [ini] SSHDict   ( see details in paramiko )
#
#        [sub] connect()
#              connect to server.
# 
#        [sub] connectIfNotConnected()  
#
#        [sub] disconnect()
#              disconnect to server.
#
#        [fun] IsRemotePathExist(remotepah)
#              check if a remote path is existed or not.
#
#        [fun] IsRemoteDirExisted(remotepah):
#              for a given remote path, check if it is directory and existed.
#
#        [fun] RemoveRemoteDIr(remoeDir):
#              remove remote directory
#
#        [fun] send_commandlist(commandlist)
#              return error
#
#        [sub] upload_file(localfile,remotedestination)
#              if we call self.upload_file( "test.file"   ,   "/here"  )
#              then "test.file" will be renamed to "here" and be put at root ("/").
#              if there is file (the same name as localfile) existed at server, it will be coverd.
#
#        [sub] download_file(remotefile,localdestination)
#              the "remotefile" will be copied and be saved as "localdestination"
#              "remotefile" and "localdestination"  are all files exactly. The same as upload
#
#        [sub] CompressUploadDir(localdirectoy,remotedestination): !!!! linux dependent ("tar" is used)
#              The upload file can only be directory and compression will be used. Faster!
#              usage:
#                    localdirectoy     = "some/path/directory"
#                    remotedestination = "other/path"
#              the directory would be put at:    "other/path/directory"
#
#        [sub] upload_dir(localdirectoy,remotedestination)
#              the same as CompressUploadDir without compression
#
#        [sub] CompressDownloadDir(Remotedirectoy,localdestination): !!!! linux dependent ("zip/unzip" is also used)
#              The download file can only be directory and compression will be used. Faster!
#              usage:
#                    Remotedirectoy   = "some/path/directory"
#                    localdestination = "other/path"
#              the directory would be put at:    "other/path/directory"
#              This function is not well designed. Tempral file will be created in the folder.
#              But it looks working fine.
#
#-------------------------------------------------------------------------------------
#             ||     linux server actions    ||
#-------------------------------------------------------------------------------------
#        [fun] IsUserExist(username):
#              return True of False
#              check if username is exist in remote server.
#
#        [fun] CreatUser(username):
#              return possible errors.
#              1. Maybe only root user can use this command.
#              2. not forget to call IsUserExist to check if it is existed or not!
#
#        [fun] RemoveUser(username):
#              like "CreatUser".
#
#        [fun] GetHomePath():     (make connection before this sub)
#              get the home path of the remote
#
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

```
