import json
from dotenv import load_dotenv
import os
import os.path
import requests

load_dotenv()
token = os.getenv('READWISE_TOKEN')


def fetch_from_export_api(updated_after=None):
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {token}"}, verify=False
        )
        full_data.extend(response.json()['results'])
        next_page_cursor = response.json().get('nextPageCursor')
        if not next_page_cursor:
            break
    return full_data


# Get all of a user's books/highlights from all time
all_data = fetch_from_export_api()


for book in all_data:
    for highlights in book['highlights']:
        path = os.path.join('./src/content/notes/',
                            book['title'] + '/' + str(highlights['id']) + '.json')
        tags = []
        if highlights['tags']:
            for tag in highlights['tags']:
                tags.append(tag['name'])
        json_data = {
            'id': highlights['id'],
            'source_title': book['title'],
            'pubDate': highlights['created_at'],
            'author': book['author'],
            'text': highlights['text'],
            'note': highlights['note'],
            'tags': tags,
            'url': book['source_url'],
            'is_discard': highlights['is_discard']
        }
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as f:
            json.dump(json_data, f, indent=4)

# with open('./src/content/notes/note_data.json', 'w') as f:
#     json.dump(filtered_data, f, indent=4)
