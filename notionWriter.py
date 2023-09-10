import config
import requests

NOTION_URL = 'https://api.notion.com/'
NOTION_PAGES_URL = 'v1/pages/'
NOTION_BLOCKS_URL = 'v1/blocks/'
NOTION_AUTH_HEADER = f'Authorization: Bearer {config.NOTION_PAGE_ID}'

def main():
  notionReq = requests.get(NOTION_URL + NOTION_BLOCKS_URL + config.NOTION_PAGE_ID2 + '/children?page_size=100', headers = { 'Authorization': f'Bearer {config.NOTION_API_KEY}', 'Notion-Version': '2022-06-28' })

  print(notionReq.json())

if __name__ == '__main__':
  main()