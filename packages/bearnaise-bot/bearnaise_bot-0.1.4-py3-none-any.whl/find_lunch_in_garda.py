from requests_html import HTMLSession
from pprint import pprint
from fuzzywuzzy import fuzz
import click


@click.command()
@click.option('--menu_keyword', prompt='What do you want to eat?',
              help='Something you would like the meal to contain -like \"bearnise\n ')
def find_restaurants(menu_keyword: str):
    if menu_keyword.lower() == 'bearnaise':
        print('Mmmmmm bearnaise...\n\n')
    else:
        print('Good choice, but will you consider bearnaise for next time?\n\n')

    session = HTMLSession()
    r = session.get('http://www.kvartersmenyn.se/find/_/city/19/area/garda_161')
    restaurants = r.html.find('div.row.t_lunch')

    menus_with_keyword = []
    for r in restaurants:
        name = r.find('h5')[0].text
        menu = r.find('.rest-menu')[0].text
        # Fuzzywuzzy is commented out for now, as I haven't yet found an algoritm that works well here.
        #filtered_menu = list(filter(lambda word: len(word) > 1, menu.split()))

        #match_scores = map(lambda word: fuzz.partial_ratio(menu_keyword.lower(), word.lower()), filtered_menu)
        #if max(match_scores) > 87:
        if menu_keyword.lower() in menu.lower():
            menus_with_keyword.append(f'{name}: \n {menu}')

    if len(menus_with_keyword) < 1:
        print('Sorry, found no restaurants who serve that today :( ')
    else:
        for mwk in menus_with_keyword:
            print(mwk + '\n\n')


if __name__ == '__main__':
    find_restaurants()


