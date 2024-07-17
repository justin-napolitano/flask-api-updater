#!/bin/bash

# Define the API endpoint
API_URL="http://127.0.0.1:8080/update/toots"

# Define the sample toot data
TOOT_DATA=$(cat <<EOF
{
    "id": 112803351008011987,
    "created_at": "2024-07-17T18:55:38",
    "in_reply_to_id": null,
    "in_reply_to_account_id": null,
    "sensitive": false,
    "spoiler_text": "",
    "visibility": "public",
    "language": "en",
    "uri": "https://mastodon.social/users/jnapolitano/statuses/112803351008011987",
    "url": "https://mastodon.social/@jnapolitano/112803351008011987",
    "site_url": "https://mastodon.social/@jnapolitano",
    "replies_count": 0,
    "reblogs_count": 0,
    "favourites_count": 0,
    "favourited": false,
    "reblogged": false,
    "muted": false,
    "bookmarked": false,
    "pinned": false,
    "content": "<p>Tooting from Python using cobrabot !</p>",
    "filtered": [],
    "reblog": null,
    "application": {"name": "cobra-bot2", "website": "https://jnapolitano.com"},
    "account": {
        "id": 112594170137753100,
        "username": "jnapolitano",
        "acct": "jnapolitano",
        "display_name": "",
        "locked": false,
        "bot": false,
        "discoverable": null,
        "indexable": false,
        "group": false,
        "created_at": "2024-06-10T00:00:00",
        "note": "",
        "url": "https://mastodon.social/@jnapolitano",
        "uri": "https://mastodon.social/users/jnapolitano",
        "avatar": "https://mastodon.social/avatars/original/missing.png",
        "avatar_static": "https://mastodon.social/avatars/original/missing.png",
        "header": "https://mastodon.social/headers/original/missing.png",
        "header_static": "https://mastodon.social/headers/original/missing.png",
        "followers_count": 0,
        "following_count": 0,
        "statuses_count": 11,
        "last_status_at": "2024-07-17T00:00:00",
        "hide_collections": null,
        "noindex": false,
        "emojis": [],
        "roles": [],
        "fields": []
    },
    "media_attachments": [],
    "mentions": [],
    "tags": [],
    "emojis": [],
    "card": null,
    "poll": null
}
EOF
)

# Send the POST request to the API endpoint
response=$(curl -s -w "\nHTTP_STATUS_CODE:%{http_code}\n" -X POST "$API_URL" -H "Content-Type: application/json" -d "$TOOT_DATA")

# Extract the body and the HTTP status code from the response
body=$(echo "$response" | sed -e 's/HTTP_STATUS_CODE\:.*//g')
http_status=$(echo "$response" | grep -oP '(?<=HTTP_STATUS_CODE:)\d+')

# Print the response
echo "Response Body: $body"
echo "HTTP Status Code: $http_status"
