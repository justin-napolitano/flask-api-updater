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
import json

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

    stmt_select = sqlalchemy.text(
        "SELECT lastBuildDate FROM builds WHERE link = :link"
    )
    stmt_insert = sqlalchemy.text(
        "INSERT INTO builds (title, link, description, generator, language, copyright, lastBuildDate, atom_link_href, atom_link_rel, atom_link_type) "
        "VALUES (:title, :link, :description, :generator, :language, :copyright, :lastBuildDate, :atom_link_href, :atom_link_rel, :atom_link_type)"
    )
    stmt_update = sqlalchemy.text(
        "UPDATE builds SET title = :title, description = :description, generator = :generator, language = :language, "
        "copyright = :copyright, lastBuildDate = :lastBuildDate, atom_link_href = :atom_link_href, "
        "atom_link_rel = :atom_link_rel, atom_link_type = :atom_link_type WHERE link = :link"
    )

    try:
        with db.connect() as conn:
            result = conn.execute(stmt_select, {"link": link}).fetchone()
            if result:
                existing_last_build_date = result[0]
                if existing_last_build_date != last_build_date:
                    conn.execute(stmt_update, {
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
                    return jsonify({'message': 'Build record updated successfully'}), 200
                else:
                    return jsonify({'message': 'No update needed for the build record'}), 200
            else:
                conn.execute(stmt_insert, {
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
                return jsonify({'message': 'Build record added successfully'}), 201
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating builds table'}), 500


@app.route('/update/feed', methods=['POST'])
def update_feed():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    pubDate = data.get('pubDate')
    guid = data.get('guid')
    description = data.get('description')

    stmt_select = sqlalchemy.text(
        "SELECT pubDate FROM feed WHERE guid = :guid"
    )
    stmt_insert = sqlalchemy.text(
        "INSERT INTO feed (title, link, pubDate, guid, description) VALUES (:title, :link, :pubDate, :guid, :description)"
    )
    stmt_update = sqlalchemy.text(
        "UPDATE feed SET title = :title, link = :link, pubDate = :pubDate, description = :description WHERE guid = :guid"
    )

    try:
        with db.connect() as conn:
            result = conn.execute(stmt_select, {"guid": guid}).fetchone()
            if result:
                existing_pubDate = result[0]
                if existing_pubDate != pubDate:
                    conn.execute(stmt_update, {
                        "title": title,
                        "link": link,
                        "pubDate": pubDate,
                        "guid": guid,
                        "description": description
                    })
                    conn.commit()
                    return jsonify({'message': 'Feed record updated successfully'}), 200
                else:
                    return jsonify({'message': 'No update needed for the feed record'}), 200
            else:
                conn.execute(stmt_insert, {
                    "title": title,
                    "link": link,
                    "pubDate": pubDate,
                    "guid": guid,
                    "description": description
                })
                conn.commit()
                return jsonify({'message': 'Feed record added successfully'}), 201
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating feed table'}), 500
    
# New endpoint to get a post from feed table that does not exist in the specified table
# New endpoint to get a post from feed table that does not exist in the specified table
@app.route('/get/post', methods=['GET'])
def get_post():
    table_name = request.args.get('table')
    if not table_name:
        return jsonify({'message': 'Missing table parameter'}), 400

    stmt = sqlalchemy.text(
        f"SELECT * FROM feed WHERE guid NOT IN (SELECT site_url FROM {table_name}) LIMIT 1"
    )

    try:
        with db.connect() as conn:
            result = conn.execute(stmt)
            if result:
                # print(cursor)
                # row = dict(zip(conn.column_names, conn.fetchone()))
                result_mapping = result.mappings().fetchone()
                post = {key: result_mapping[key] for key in result_mapping.keys()}
                return jsonify(post), 200
            else:
                return jsonify({'message': 'No new posts available'}), 404
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error fetching post'}), 500
    

@app.route('/update/toots', methods=['POST'])
def update_toots():
    data = request.json
    
    toot_id = data.get('id')
    created_at = data.get('created_at')
    in_reply_to_id = data.get('in_reply_to_id')
    in_reply_to_account_id = data.get('in_reply_to_account_id')
    sensitive = data.get('sensitive')
    spoiler_text = data.get('spoiler_text')
    visibility = data.get('visibility')
    language = data.get('language')
    uri = data.get('uri')
    url = data.get('url')
    site_url = data.get('site_url')
    replies_count = data.get('replies_count')
    reblogs_count = data.get('reblogs_count')
    favourites_count = data.get('favourites_count')
    favourited = data.get('favourited')
    reblogged = data.get('reblogged')
    muted = data.get('muted')
    bookmarked = data.get('bookmarked')
    pinned = data.get('pinned')
    content = data.get('content')
    filtered = json.dumps(data.get('filtered', []))
    reblog = json.dumps(data.get('reblog'))
    application = json.dumps(data.get('application'))
    account = json.dumps(data.get('account'))
    media_attachments = json.dumps(data.get('media_attachments', []))
    mentions = json.dumps(data.get('mentions', []))
    tags = json.dumps(data.get('tags', []))
    emojis = json.dumps(data.get('emojis', []))
    card = json.dumps(data.get('card'))
    poll = json.dumps(data.get('poll'))

    stmt = sqlalchemy.text("""
    INSERT INTO toots (
        id, created_at, in_reply_to_id, in_reply_to_account_id, `sensitive`, spoiler_text, visibility, language,
        uri, url, site_url, replies_count, reblogs_count, favourites_count, favourited, reblogged, muted, bookmarked,
        pinned, content, filtered, reblog, application, account, media_attachments, mentions, tags, emojis, card, poll
    ) VALUES (
        :id, :created_at, :in_reply_to_id, :in_reply_to_account_id, :sensitive, :spoiler_text, :visibility, :language,
        :uri, :url, :site_url, :replies_count, :reblogs_count, :favourites_count, :favourited, :reblogged, :muted, :bookmarked,
        :pinned, :content, :filtered, :reblog, :application, :account, :media_attachments, :mentions, :tags, :emojis, :card, :poll
    )
    ON DUPLICATE KEY UPDATE
        created_at=VALUES(created_at),
        in_reply_to_id=VALUES(in_reply_to_id),
        in_reply_to_account_id=VALUES(in_reply_to_account_id),
        `sensitive`=VALUES(`sensitive`),
        spoiler_text=VALUES(spoiler_text),
        visibility=VALUES(visibility),
        language=VALUES(language),
        uri=VALUES(uri),
        url=VALUES(url),
        site_url=VALUES(site_url),
        replies_count=VALUES(replies_count),
        reblogs_count=VALUES(reblogs_count),
        favourites_count=VALUES(favourites_count),
        favourited=VALUES(favourited),
        reblogged=VALUES(reblogged),
        muted=VALUES(muted),
        bookmarked=VALUES(bookmarked),
        pinned=VALUES(pinned),
        content=VALUES(content),
        filtered=VALUES(filtered),
        reblog=VALUES(reblog),
        application=VALUES(application),
        account=VALUES(account),
        media_attachments=VALUES(media_attachments),
        mentions=VALUES(mentions),
        tags=VALUES(tags),
        emojis=VALUES(emojis),
        card=VALUES(card),
        poll=VALUES(poll);
    """)
    
    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters={
                "id": toot_id,
                "created_at": created_at,
                "in_reply_to_id": in_reply_to_id,
                "in_reply_to_account_id": in_reply_to_account_id,
                "sensitive": sensitive,
                "spoiler_text": spoiler_text,
                "visibility": visibility,
                "language": language,
                "uri": uri,
                "url": url,
                "site_url": site_url,
                "replies_count": replies_count,
                "reblogs_count": reblogs_count,
                "favourites_count": favourites_count,
                "favourited": favourited,
                "reblogged": reblogged,
                "muted": muted,
                "bookmarked": bookmarked,
                "pinned": pinned,
                "content": content,
                "filtered": filtered,
                "reblog": reblog,
                "application": application,
                "account": account,
                "media_attachments": media_attachments,
                "mentions": mentions,
                "tags": tags,
                "emojis": emojis,
                "card": card,
                "poll": poll
            })
            conn.commit()
    except Exception as e:
        app.logger.exception(e)
        return jsonify({'message': 'Error updating toot table'}), 500

    return jsonify({'message': 'Toot record added/updated successfully'}), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
