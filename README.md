<p align="center">
  <a href="https://mapaction.org/">
      <img alt="MapAction" src="https://qb19onvfjt-flywheel.netdna-ssl.com/wp-content/themes/mapaction/images/logo.svg" width="210" />
  </a>
</p>
<h1 align="center">
Default Crash Move Folder <br /> (CMF)
</h1>

# Summary

This repo contains the working copy of MapAction's default crash move folder.

> ⚠️ Selecting "Download.zip" from the Github website will **_always fail_** for this repo

# Deployments

If you need a fresh copy for a new deployment/response/project please take a fresh copy from the **`R:\`** drive.

See the [Crash Move Folder](https://wiki.mapaction.org/display/datacircle/Crash+Move+Folder) wiki article for more details.

# Contributing

Anyone with a MapAction Github account can create a pull request with proposed changes to this repo.

Please see [Default Crash Move folder](https://wiki.mapaction.org/display/softwaredevcircle/default-crash-move-folder) wiki page for more details on contributing & automated checks.

## Large File Storage

This repo uses [Git's Large Files Storage](https://git-lfs.github.com) (LFS) therefore you'll need to use a LFS enabled git client, such as Github for Desktop. If you are using a commandline git client you may need to explicitly do the extra step after you clone the repo:

```bash
git lfs pull
```

**Notes:**

- No harm can be done by making opening or updating a pull request, and only Matt Sims and Andy Smith have permissions to merge a PR on this repo. When we merge a pull request then the changes are automatically sync'd to the R: drive.
- Even without any changes you will see slightly different content between the two copies. This is because when the contents to copied from the Github repo to the R:\ drive, some of git's working files (eg the .git dir and .gitignore file etc) are removed as they are not relevant in an emergency.
