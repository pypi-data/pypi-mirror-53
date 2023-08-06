# SAFER-STORAGE System Backend REST API Server

This backend is implemented using [FastAPI](https://github.com/tiangolo/fastapi)

## Quick start

Install the module on your system sing PyPI:
```
pip install sysapi
```

Then start the service using default settings (test on localhost:8000), run the following command:
```
uvicorn sysapi.main:app --reload
```

## File system organization

![File system organization](schema_fs.svg) (download [PDF](schema_fs.pdf))

## REST Routes


## GET routes

### Version prefix
All routes start with a `/{version}/` prefix, which is currently set to `v1`

### Meta data 
These routes are used to retrieve data about users and snapshots
* `/v1/users` : list user accounts
* `/v1/user/{user}` : get `user`'s meta-data
* `/v1/snapshots` : list of all available snapshots
* `/v1/snapshots?user={user}` : list of available snapshots for `user`
* `/v1/snapshot/{@snapshot}` : get `@snapshot` meta-data

NB: 
* `users`, `snapshots`, and `root` are reserved user names to avoid conflicts.
* snapshots are always identified using an `@`-prefixed name, eg. `@initial`, which also solved ambiguity between snapshot and user routes.

### Filesystem navigation in time and space

The general form is as follows:
* `/v1/{user}/{time-location}/{space-location}`

With the following constructs:
* `{time-location}` is one of:
   * `fat/{@sanpshot}` : the state of a single file as captured in snapshot named `{snapid}` 
   * `dat/{@sanpshot}` : the state of a directory as captured in snapshot named `{snapid}` 
   * `fbefore/{@snapshot}` : the state of a file as captured in snapshot immediately preceding the snapshot named `{@snapshot}` (if any)
   *  `dbefore/{@snapshot}` : the state of a directory as captured in snapshot immediately preceding the snapshot named `{@snapshot}` (if any)
   * `past/{@snapshot}` : merged view of a directory composed of all snapshot(s) preceding, and including, the snapshot named `{@snapshot}`. 
   * `historic/{username}/{path}` : list of snapshots that contain the given file for the given user
   * The special name `@current` is reserved and used to designate the current state of the filesystem. It is actually a real snapshot, that is created each time an API call requests this time-point.
* `{space-location}` is of the form:
   * `` (empty): `user`'s homedir content
   * `{path}/` : content of the directory designated by the URL-encoded `path` starting from the `user`'s homedir
   * `{path}/file` : file located in directory designated by `path`

NB: the `root` virtual user is only available to the admin user and his/her home directpry is at the root of the filesystem

Examples:
* `/v1/joe/at/@current/` : `joe`'s current homedir
* `/v1/joe/at/@snap-2019-09-18-2230/Photos/Kickoff/people.jpg` : `joe`'s file named `people.jpg` in sub-directory `Photos/Kickoff` as it was captured by snapshot named `@snap-2019-09-18-2230`
* `/v1/root/before/@snap-2019-09-18-2230/users/joe/Photos/` : content of directory `users/joe/Photos/` for admin user as it was captured by snapshot immediately preceding the snapshot named `@snap-2019-09-18-2230`
* 

## POST routes

* `/v1/users/new`
  
   Creates a user with following elements:
   * login
   * password
   * email

* `/v1/copyto/{space-location}`
  
   Copies the list of files designated in the body to the space-location designated by the URL:
   In the body, each file is designated by a triplet:
   - `"path"="path/to/file"`
   - `"snapshot"="@snapshot"` from which the file is copied
   - `"destructive"=boolean` 
   Returns: The updated content of target directory (`space-location`)




