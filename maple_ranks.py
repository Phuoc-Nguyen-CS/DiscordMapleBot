from bs4 import BeautifulSoup
import requests
import time

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

    # Get url
    character_info['url'] = url

    # Get picture
    img = soup.img['src']
    character_info['img'] = img

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

def get_xp(name):
    # Opens Page
    url = f'https://www.mapleranks.com/u/{name}'
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            exp_items = soup.find_all('div', class_='char-exp-cell')
            first_exp_value = exp_items[0].text.strip()
            words = first_exp_value.split()
            val = words[-1]
            return val
        except Exception as e:
            print(f"An error occurred: {e}")
            retries += 1
            print(f"Retry {retries} of {max_retries}")
            time.sleep(5)  # Wait for 5 seconds before retrying

    print("Failed to load the page after maximum retries")
    return None