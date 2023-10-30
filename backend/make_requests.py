import requests

# print(requests.get("http://127.0.0.1:8000/items/1").json())
# print(requests.get("http://127.0.0.1:8000/items/foobar").json())
# print(requests.get("http://127.0.0.1:8000/items?name=Nails").json())
print(requests.get("http://127.0.0.1:8000").json())

print("Add item")

print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={"name": "Screwdriver", "price": 3.99, "count": 3, "category": "tools", "id": 5},
    ).json()
)

print(requests.get("http://127.0.0.1:8000").json())

found = requests.get("http://127.0.0.1:8000/items?name=Screwdriver").json()
print(found)
id =  found['selection'][0]['id']

print("Update item")
update_result = requests.put(f"http://127.0.0.1:8000/update/{id}", json={"count": 4}).json()
print(update_result)

print("Update again")
update_result = requests.put(f"http://127.0.0.1:8000/update/{id}?count=5").json()
print(update_result)

print("Delete item")
print(requests.delete(f"http://127.0.0.1:8000/delete/{id}").json())




