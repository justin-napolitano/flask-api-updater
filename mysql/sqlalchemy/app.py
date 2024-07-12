from __future__ import annotations

import logging
import os
import datetime
from flask import Flask, request, jsonify
import sqlalchemy

from connect_connector import connect_with_connector
from connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from connect_tcp import connect_tcp_socket
from connect_unix import connect_unix_socket

app = Flask(__name__)

logger = logging.getLogger()

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""
    if os.environ.get("INSTANCE_HOST"):
        return connect_tcp_socket()
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        return (
            connect_with_connector_auto_iam_authn()
            if os.environ.get("DB_IAM_USER")
            else connect_with_connector()
        )
    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

# This global variable is declared with a value of `None`, instead of calling
# `init_db()` immediately, to simplify testing.
db = None

@app.before_request
def init_db() -> sqlalchemy.engine.base.Engine:
    """Initiates connection to database and its' structure."""
    global db
    if db is None:
        db = init_connection_pool()

@app.route('/update/builds', methods=['POST'])
def update_builds():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    description = data.get('description')
    generator = data.get('generator')
    language = data.get('language')
    copyright = data.get('copyright')
    last_build_date = data.get('lastBuildDate')
    atom_link_href = data.get('atom_link_href')
    atom_link_rel = data.get('atom_link_rel')
    atom_link_type = data.get('atom_link_type')

    stmt = sqlalchemy.text(
        "INSERT INTO builds (title, link, description, generator, language, copyright, lastBuildDate, atom_link_href, atom_link_rel, atom_link_type) "
        "VALUES (:title, :link, :description, :generator, :language, :copyright, :lastBuildDate, :atom_link_href, :atom_link_rel, :atom_link_type)"
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters={
                "title": title,
                "link": link,
                "description": description,
                "generator": generator,
                "language": language,
                "copyright": copyright,
                "lastBuildDate": last_build_date,
                "atom_link_href": atom_link_href,
                "atom_link_rel": atom_link_rel,
                "atom_link_type": atom_link_type
            })
            conn.commit()
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating builds table'}), 500

    return jsonify({'message': 'Build record added successfully'}), 201



@app.route('/update/feed', methods=['POST'])
def update_feed():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    pubDate = data.get('pubDate')
    guid = data.get('guid')
    description = data.get('description')

    stmt = sqlalchemy.text(
        "INSERT INTO feed (title, link, pubDate, guid, description) VALUES (:title, :link, :pubDate, :guid, :description)"
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters={
                "title": title,
                "link": link,
                "pubDate": pubDate,
                "guid": guid,
                "description": description
            })
            conn.commit()
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating feed table'}), 500

    return jsonify({'message': 'Feed record added successfully'}), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
