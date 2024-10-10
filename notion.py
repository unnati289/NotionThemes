import os
import requests
from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')

def create_notion_page(title, parent_id):
    url = 'https://api.notion.com/v1/pages'

    headers = {
        'Authorization': f'Bearer {NOTION_TOKEN}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-08-16'
    }

    
    data = {
        'parent': {'page_id': parent_id},
        'properties': {
            'title': {
                'title': [
                    {
                        'text': {
                            'content': title
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        page_id = response.json()['id']
        print(f"Page '{title}' created successfully with ID: {page_id}")
        return page_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def create_nested_pages(current_page_id, main_title):
    
    main_page_id = create_notion_page(main_title, current_page_id)

    if main_page_id:
        
        nested_titles = ["Main Ideas", "Patterns and Commonalities", "Content"]
        
        
        for title in nested_titles:
            create_notion_page(title, main_page_id)

if __name__ == "__main__":
    
    current_page_id = PAGE_ID  
    
    main_title = input("Enter the main title for the page: ")
    create_nested_pages(current_page_id, main_title)