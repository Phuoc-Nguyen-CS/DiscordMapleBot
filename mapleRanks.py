from bs4 import BeautifulSoup
import requests

session = requests.Session()
character_name = 'aurelionsøl'

def getInfo(character_name):
    # Opens Page
    url = f'https://www.mapleranks.com/u/{character_name}'
    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Finds current name
    name = soup.find('h3', class_='card-title text-nowrap')
    name = name.text.strip()
    print(name)

    # Finds current level and percent
    character_level = soup.find('h5', class_='card-text')
    character_level = character_level.text.strip()
    print(character_level)

    # Finds the exp
    exp_items = soup.find_all('div', class_='char-exp-cell')
    for v in range(6):
        label = exp_items[v].text.strip()
        print(f'{label}')
        
def main():
    session = requests.Session()
    # character_name = 'aurelionsøl'
    character_name = input('Name: ')
    getInfo(character_name)

if __name__ == "__main__":
    main()