from bs4 import BeautifulSoup
import requests

session = requests.Session()
# character_name = 'aurelionsøl'

def get_info(character_name):
    """
    Retrieves information related to character exp based on the ingame name.

    Args:
        character_name (str): The name of the character to look up.
    
    Returns:
        dict: A dictionary containing details related to character.
    """
    # Opens Page
    url = f'https://www.mapleranks.com/u/{character_name}'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Empty dictionary for information
    character_info = {}

    # Get picture
    url = soup.img['src']
    character_info['url'] = url

    # Get name
    name = soup.find('h3', class_='card-title text-nowrap')
    character_info['name'] = name.text.strip()
    
    # Get Class and World
    class_world = soup.find('p', class_='card-text mb-0')
    character_info['class_world'] = (class_world.text.strip())


    # Get level
    character_level = soup.find('h5', class_='card-text')
    character_info['level'] = character_level.text.strip()

    # Get average exp
    exp_items = soup.find_all('div', class_='char-exp-cell')
    # character_info.update({f'exp_{v+1}': item.text.strip() for v, item in enumerate(exp_items)})
    first_exp_value = exp_items[0].text.strip()
    words = first_exp_value.split()
    character_info['exp_1'] = words[-1]

    return character_info
        
def main():
    session = requests.Session()
    # character_name = 'aurelionsøl'
    character_name = input('Name: ')
    info = get_info(character_name)
    print(info)

if __name__ == "__main__":
    main()