GOOGLE_URL = 'https://www.google.com/search?tbm=isch&q={}'

def google_images_url(query, obj=None):
    '''
    Generates a google images url.

    Args:
        :query (str): string to search
        :obj (str): string representing the name of the common name
            of the searched object
    
    #EXAMPLE
    google_images_url(query='ford fiesta', obj='car')
    '''
    query = query.replace(' ', '+')
    if obj and type(obj) == str:
        query = query + '+{}'.format(obj)
    return GOOGLE_URL.format(query)

def download_file(path, url):
    '''
    Helper function for downloading files.
    
    Args:
        :path (str): path where to store the file
        :url (str): url of the file to download
    '''
    import requests
    r = requests.get(url, stream=True) 
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        raise ValueError('Impossible to get the link {}'.format(url))

NOT_ALLOWED_CHARS = r' *></\|&%$:?".'

def get_win_name(name):
    '''
    Given a string it returns a string cleaned from the chars not admissible
    for a windows file name.

    Args:
        :name (str): string
    '''
    for char in NOT_ALLOWED_CHARS:
        name = name.replace(char, '')
    return name

def download_object(name, model=None, n=5, path='.'):
    '''
    This function download images from google map.

    Args:
        :name (str): name of the object to search
        :model (list): list of strings classyfing different types of the same object
        :n (int): number of picture to download
        :path (str): existing path

    # EXAMPLE
    download_object('ford fiesta', model=['2008', '2013', '2019'], n=3, path='fiesta')

    This statement will download 3 pictures for each model of ford fiesta
    into the folder fiesta.
    '''
    import os
    import requests
    import bs4
    if not type(name) == str:
        raise ValueError('Error: name argument must be a string!')
    if model:
        if not type(model) == list:
            if all([type(_) == str for _ in model]):
                raise ValueError('Error: model argument must be a list of string!')
    if not type(n) == int:
        raise ValueError('Error: n argument must be a integer!')
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            raise ValueError('Error: path argument must be a valid path name!')
    m = len(model) if model else 1
    for i in range(m):
        if model:
            name_with_model = name + ' {}'.format(model[i])
        else:
            name_with_model = name
        url = google_images_url(name_with_model)
        r = requests.get(url)
        if not r.status_code == 200:
            raise ValueError('Impossible to get the link {}'.format(url))
        soup = bs4.BeautifulSoup(r.text, features="html.parser")
        imgs = soup.find_all('img')
        if not imgs:
            raise ValueError('Impossible to find images in the page requested!')
        urls = [imgs[i]['src'] for i in range(n)]
        for i, url in enumerate(urls):
            img_name = '{name}_{n}.jpg'.format(
                name=get_win_name(name_with_model),
                n=str(i).zfill(3)
            )
            try:
                download_file(os.path.join(path, img_name), url)
            except:
                raise ValueError('Impossible to get the link {}'.format(url))