import requests
from bs4 import BeautifulSoup


def is_valid_instagram(username):
    """
    Checks if an Instagram account exists.
    """
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('meta', property='og:description'):
            return True
    return False


def get_instagram_account_data(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            content = meta_tag.get('content')
            profile_image_url = extract_profile_image_url(soup)
            full_name = extract_full_name(soup)
            followers_count = extract_followers_count(soup)
            data = {
                'content': content,
                'full_name': full_name,
                'followers_count': followers_count,
                'profile_image_url': profile_image_url
            }
            return data
        else:
            return None
    else:
        return None


def extract_profile_image_url(soup):
    profile_image_tag = soup.find('meta', property='og:image')
    if profile_image_tag:
        return profile_image_tag['content']
    else:
        return None


def extract_full_name(soup):
    full_name_tag = soup.find('h1', class_='rhpdm')
    if full_name_tag:
        return full_name_tag.text.strip()
    else:
        return None


def extract_followers_count(soup):
    followers_count_tag = soup.find('span', class_='g47SY')
    if followers_count_tag:
        return followers_count_tag['title']
    else:
        return None
