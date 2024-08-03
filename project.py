import os
import sys
import requests
import json
import random
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from recipes.spiders.lidl_spider import LidlSpider
# from recipes.spiders.ah_spider import AhSpider

recipider = {
    'state': 'running',
}
# ewww!
t = 0

def main():
    global recipider
    # all available recipes on the scraped sites
    items = get_recipes()

    clear_terminal()
    print("Thank you for using Recipider.\nyour personal kooking idea buddy.\nhaving trouble finding something to cook, or you just want to try something new?\nrecpider will provide you with a small list of recipes from popular grosserybrands for you to try.\nincluding nutritional information and the ability to 're-roll' the result if the provided recipes are not to your liking.\nsimply select a recipe by typing either 1, 2 or 3 to select the corosponding recipe and 0 to re-roll.")
    
    # the 3 randomly picked recipes from the above
    recipe_names = Roll(items)
    
    # display the options in the terminal
    recipider['state'] = " > displaying picked recipes"
    display(recipe_names)
    
    # get the input from the user through the comand line
    recipe_name = get_user_input(recipe_names)
    
    # complete recipe data for the picked recipe
    recipider['state'] = " > displaying full recipe"
    complete_recipe = get(recipe_name)
    display(complete_recipe)
    input("press Enter to kill recipider.\n\nenjoy the food.\nuntill next time.")

def get_recipes():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    got_recipes = os.path.join(base_path, "recipes.json")
    if not got_recipes:
        print(" > get no recipes")
        process = CrawlerProcess(settings={
            'FEEDS': {'recipes.json': {'format':'json'}},
            "SELENIUM_DRIVER_NAME": 'edge',
            "SELENIUM_DRIVER_ARGUMENTS": ['--headless'],
            "DOWNLOADER_MIDDLEWARES": {'scrapy_selenium.SeleniumMiddleware': 800}
            })
        process.crawl(LidlSpider)
        print(" > lidl crawling")
        # process.crawl(AhSpider)
        # print(" > ah crawling")
        process.start()
        # print(" > save scraped data to file: recipes.json")
    with open(got_recipes, 'r') as file:
        recipes = json.load(file)
    return recipes

def Roll(items):
    recipider['state'] = " > picking recipes"
    recipes = []
    picked = set()
    while len(recipes) < 3:
        i = random.randrange(len(items))
        if i not in picked:
            recipes.append(items[i])
            picked.add(i)
    recipider['state'] = " > recipes picked"
    return recipes

def display(items):
    global recipider
    global t
    
    match recipider['state']:
        case " > displaying picked recipes":
            print("\n0: Re-Roll\n")
            i = 0
            for recipe in items:
                i += 1
                print(f"Recipe {i}: {recipe['name']}\n")
            recipider['state'] = " > picked recipes displayed"

        case " > displaying full recipe":
            try:
                if t <= 0:
                    print("ingredients: \n")
                    t += 1 
                for ingredient in items['ingredients']:
                    print(f"{ingredient}")
                print("\n\ninstructions: ")
                for step in items['instructions']:
                    print(f"{step}\n")
            except TypeError:
                pass
            ...

def get_user_input(recipes):
    a = input("pick a recipe by typing either 1, 2, 3 or 0 to re-roll\n")
    match a:
        case "1" | "2" | "3" | "0":
            if a == "0":
                print("You chose to re-roll")
                main()
                sys.exit()

            i = int(a) - 1
            if 0 <= i < len(recipes):
                print(f"You picked recipe {int(a)}: {recipes[i]['name']}\n")
                return recipes[i]
            
        case _:
            print("Invalid input, please try again.")
            return get_user_input(recipes)
            
def get(recipe):
    try:
        match recipe['site']:
            case "lidl":
                Full_Recipe = scrape_lidl(recipe)
            # case "ah":
            #     Full_Recipe = scrape_ah(recipe)
        return Full_Recipe
    except TypeError:
        pass

def scrape_lidl(recipe):
    response = requests.get(recipe["url"])
    soup = BeautifulSoup(response.content, features="lxml")
    ingredients = get_ingredients(soup)
    instructions = get_instructions(soup)
    Full_Recipe = {
        #'name' : recipe['name'],
        #'Nutrition' : values,
        'ingredients' : ingredients,
        'instructions' : instructions
    }
    return Full_Recipe

def get_ingredients(soup):
    ingredients = []
    ingredient_section = soup.find('div',{'class': 'bg-white relative shadow-md p-4'})
    for ingredient in ingredient_section.find_all('span', attrs={'data-rid': 'ingredient'}):
        ingredients.append(ingredient.get_text(strip = True))
    #print(f" > ingerdients: ", ingredients)
    return ingredients

def get_instructions(soup):
    instructions = []
    instruction_section = soup.find('ol', attrs={'data-rid': 'cooking-step'})
    for p in instruction_section.find_all('p'):
        instructions.append(p.get_text(strip=True))
    #print(f" > instructions: ", instructions)
    return instructions

'''
def scrape_ah(recipe):
    token = get_token()
    if token:
        headers = {
            'User-Agent': 'Appie/8.66',
            'Authorization': f'Bearer {token}',
                }
        response = requests.get(recipe["url"], headers = headers)
        soup = BeautifulSoup(response.content, features="lxml")
        # find recipe data on page an return it
        name = soup.find('h2').text
        ingredients = soup.find('ul', class_='ingredients').text
        values = soup.find('div', class_='values').text
        instructions = soup.find('div', class_='instructions').text
        Full_Recipe = {
            'name' : name,
            'ingredients' : ingredients,
            'instructions' : instructions,
            'Nutrition' : values
        }
    return Full_Recipe

def get_token():
    url = "https://api.ah.nl/mobile-auth/v1/auth/token/anonymous"
    headers = {
    'User-Agent': 'Appie/8.66',
    'Content-Type': 'application/json',
    }
    data = {
    "clientId": "appie",
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        if token:
            return token
        else:
            print("no token in response, teminating ah scrape")
'''

def clear_terminal():
    if os.name == 'nt':
        print(" > windows")
        os.system('cls')
    else:
        os.system('clear')
    #print(" > cleared")

if __name__ == "__main__":
    main()
