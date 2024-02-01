import json


with open("111.json", "w", encoding="utf-8") as file:
    kleymos = [el["kleymo"] for el in json.load(open("test/test_data/_test_welders.json", "r", encoding="utf-8"))]
    print(kleymos)
    json.dump(kleymos, file, indent=4, ensure_ascii=False)