#!/bin/bash

curl -X POST \
  https://rss-updater-pkpovjepjq-wl.a.run.app/update/builds \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "New Build Example",
    "link": "http://example.com/build",
    "description": "This is a description of the build process.",
    "generator": "Build Generator 1.0",
    "language": "Python",
    "copyright": "2024 Example Corp",
    "lastBuildDate": "2024-07-11T16:26:32",
    "atom_link_href": "http://example.com/index.xml",
    "atom_link_rel": "self",
    "atom_link_type": "application/rss+xml"
}'
