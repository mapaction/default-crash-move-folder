Default Crash Move Folder (CMF)
===============================
This repo contains the working copy of MapAction's default crash move folder.

**TL;DR** Selecting "Download.zip" from the Github website will **_always fail_** for this repo.

USING; If you need a fresh copy for a new deployment/response/project:
--------------
Do not use take a copy from this repo. Instead please take a fresh copy from the R:\ drive. See details here: https://wiki.mapaction.org/display/datacircle/Crash+Move+Folder


CONTRIBUTING; If you want to make and/or propose changes to the default/template crash move folder:
----------------
If you want to make and/or propose changes to the default/template crash move folder, then clone the Github repo and make a pull request https://wiki.mapaction.org/display/softwaredevcircle/default-crash-move-folder 

This repo uses [Git's Large Files Storage](https://git-lfs.github.com) (LFS). You must use a LFS enabled git client, such as Github for Desktop. If you are using a commandline git client you may need to explicitly do the extra step after you clone the repo:
```
git lfs pull
```

**Notes:**
* No harm can be done by making opening or updating a pull request, and only Matt Sims and Andy Smith have permissions to merge a PR on this repo. When we merge a pull request then the changes are automatically sync'd to the R: drive.
* Even without any changes you will see slightly different content between the two copies. This is because when the contents to copied from the Github repo to the R:\ drive, some of git's working files (eg the .git dir and .gitignore file etc) are removed as they are not relevant in an emergency.
