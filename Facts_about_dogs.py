import requests
import json
import sqlite3

# This function returns facts about dogs (as many facts as the user wants and enters the number).
def get_random_dog_facts(num_facts):
    facts = []
    while len(facts) < num_facts:
        response = requests.get("https://dog-api.kinduff.com/api/facts")
        if response.status_code == 200:
            data = response.json()
            fact = data["facts"][0]
            facts.append(fact)
        else:
            print("Error: Unable to retrieve dog fact")
    return facts

num_facts = int(input("Enter the number of dog facts you want to know: "))
facts = get_random_dog_facts(num_facts)

for fact in facts:
    print(fact)

# Get the response headers
response = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dog-facts")
print(response.headers)


# Saves facts to a json file
with open('dog_facts.json', 'w') as f:
    json.dump(facts, f, indent=4)

# Stores dog fcts in a database
conn = sqlite3.connect('dog_facts.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS dog_facts (fact TEXT)''')
for fact in facts:
    c.execute("INSERT INTO dog_facts VALUES (?)", (fact,))
conn.commit()
conn.close()