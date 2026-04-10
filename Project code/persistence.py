import json
import os

from models import livre, utilisateur
from biblio import biblio

DATA_FILE = "library_data.json"


def save(library):
    data = {
        "name"         : library.name,
        "next_book_id" : library.next_book_id,
        "books"        : [
            {"id": b.id, "titre": b.titre, "auteur": b.auteur, "copies": c}
            for b, c in library.books.items()
        ],
        "users"        : [
            {"matricule": u.matricule, "prenom": u.prenom, "nom": u.nom, "specialty": u.specialty}
            for u in library.users
        ],
        "loans"        : [
            {
                "matricule" : user.matricule,
                "books"     : [{"id": b.id, "titre": b.titre, "auteur": b.auteur} for b in books]
            }
            for user, books in library.loans.items()
        ]
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load():
    if not os.path.exists(DATA_FILE):
        name = input("  Enter a name for your library: ").strip() or "My Library"
        return biblio(name)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    lib = biblio(data["name"], next_book_id=data.get("next_book_id", 1))

    for entry in data["books"]:
        book = livre(entry["id"], entry["titre"], entry["auteur"])
        lib.books[book] = entry["copies"]

    for entry in data["users"]:
        user = utilisateur(entry["matricule"], entry["prenom"], entry["nom"], entry["specialty"])
        lib.users.append(user)

    for entry in data.get("loans", []):
        user = next((u for u in lib.users if u.matricule == entry["matricule"]), None)
        if not user:
            continue
        loaned_books = []
        for item in entry["books"]:
            book = next((b for b in lib.books if b.id == item["id"]), None)
            if book:
                loaned_books.append(book)
        if loaned_books:
            lib.loans[user] = loaned_books

    print("  ✅ Library '%s' loaded — %d title(s), %d user(s), %d active loan(s)." % (
        lib.name, len(lib.books), len(lib.users), len(lib.loans)))
    return lib