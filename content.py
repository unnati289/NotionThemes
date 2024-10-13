import wikipediaapi
from notion_client import Client
import os
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()
TOKEN_ID=os.getenv('INTEGRATION_TOKEN')
#to decide what I do want, i need to see what .page returns?
"""take a term, load its related wikipage, a list of its sections, summary of each subsection, and link to each section"""
wiki_wiki=wikipediaapi.Wikipedia('content (unnatisaraswat007@gmail.com)','en')
#first thing is there is a list of items in the notion page

def extract_text(block):
    if 'paragraph' in block and 'rich_text' in block['paragraph']:
        return ''.join([text['plain_text'] for text in block['paragraph']['rich_text']])
    return None

def get_list(page_id):
    notion = Client(auth=TOKEN_ID)
    response = notion.blocks.children.list(block_id=page_id)
    #print("Response from Notion API:", response)
    terms = [extract_text(block) for block in response['results'] if extract_text(block)]
    terms = [term for term in terms if term.strip()]
    print(terms)
    return terms
def generate_title(term):
    model=pipeline("text2text-generation",model="facebook/bart-large-cnn")
    prompt = f"Generate a concise title for a Wikipedia page based on the following text: {term}"
    
    # Generate the title
    title = model(prompt, max_length=10, num_return_sequences=1)[0]['generated_text']
    return title.strip()

#now I have a list of topics, I need a list of page for each topic


#like for each term, create a new page, add summary and its url to the topic.
#input: the present page_id, and the list of terms, 
#output : for each term, create a page, get summary and url and put it into that page
def create_notion_page(term, summary, url,parent_page_id):
    # Create a new page under the specified parent page
    notion = Client(auth=TOKEN_ID)
    if not summary or not url:
        print(f"Skipping creation for '{term}' due to missing summary or URL.")
        return

    notion.pages.create(
        parent={"page_id": parent_page_id},  # Use the parent page ID
        properties={
            "title": {
                "title": [
                    {
                        "text": {
                            "content": term
                        }
                    }
                ]
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": summary[:2000]  # Notion has a character limit per block
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"URL: {url}",
                                "link": {
                                    "url": url
                                }
                            }
                        }
                    ]
                }
            }
        ]
    )
    print(f"Page for '{term}' created successfully.")
def get_summary(term):
    page=wiki_wiki.page(term)
    if page.exists():
        return page.summary, page.fullurl
    """title=generate_title(term)
    print("generated title "+title)
    page=wiki_wiki.page(title)
    if page.exists():
        return page.summary, page.fullurl"""
    return None, None
def populate_contentpage(page_id,l):
    
    for i in l:
        summary,fullurl=get_summary(i)
        create_notion_page(i,summary,fullurl,page_id)


if __name__ == "__main__":
    
    page_id=input("enter input id")
    l=get_list(page_id)
    populate_contentpage(page_id,l)

