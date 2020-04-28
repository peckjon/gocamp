[![Total alerts](https://img.shields.io/lgtm/alerts/g/peckjon/gocamp.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/peckjon/gocamp/alerts/)  [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/peckjon/gocamp.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/peckjon/gocamp/context:python)

# GoCamp

Unofficial Python wrapper for the web API at https://washington.goingtocamp.com

## Structure

**models.py**: core datastructures

**app.py**: routines for listing camps and finding site availability

**console.py**: barebones command-line example (runnable)

**setup.py**: added to allow for
[installation via pip](https://www.fir3net.com/Miscellaneous/Programming/how-to-install-a-git-repo-directly-via-pip.html)

## Purpose

The web interface at washington.goingtocamp.com has several bugs and
search limitations, very high latency, and no programmatic access.

Developers wishing to create searches for more complex queries (e.g.
"all weekends in June at these specific campgrounds"), build
higher-level tools/scripts, or simply search without interacting with a
website are encouraged to make use of and contribute to this library. 

## Limitations

Reservations cannot be created using this tool. Instead, a convenience
method is provided to link directly to the reservations website, with
the search results prefilled.

## Contributing

This library is in its infancy, and as it uses an unofficial API, is
expected to be brittle. PRs to keep up with additions and changes to the
API, and to extend the functionality with improved and higher-level
searches, are enthusiastically welcomed.
