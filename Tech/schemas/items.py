def ListEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "lt": item["lt"],
        "answer": item["answer"]
    }

def ListsEntity(entity) -> list:
    return[ListEntity(item) for item in entity]