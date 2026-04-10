# 📚 Library Management System

A command-line library management application written in Python. Built as an academic project, it handles books, users, and loans with persistent JSON storage and a clean modular architecture.

---

## Features

- Add, remove, search, and list books
- Add, remove, and list users
- Loan and return books
- Check book availability
- Persistent storage via JSON
- Input validation with cancellable prompts at every step

---

## Project Structure

```
├── main.py          — Entry point and command loop
├── commands.py      — User-facing command handlers (I/O layer)
├── biblio.py        — Core library logic split into manager classes
├── models.py        — Data models: livre, utilisateur
├── persistence.py   — JSON save/load
└── library_data.json
```

### Architecture

The `biblio` class acts as the single public interface. Internally it delegates to three manager classes, each responsible for one domain:

- `BookManager` — book operations
- `UserManager` — user operations
- `LoanManager` — loan operations

This separation keeps each class focused while `commands.py` only ever talks to `biblio`, unaware of the internal split.

---

## Getting Started

**Requirements:** Python 3.x — no external dependencies.

```bash
python main.py
```

On first launch you will be prompted to name your library. Data is automatically saved after every operation.

### Available Commands

```
── Books ────────────────────────────────────
  add_book               — Add a book (or copies of an existing one)
  remove_book            — Remove a book by title and author
  search_book            — Search for a book by title and author
  list_books             — List all books with their IDs
  check_availability     — Check if a book is available by title and author

── Users ────────────────────────────────────
  add_user               — Add a user (matricule, first/last name, specialty)
  remove_user            — Remove a user by matricule
  list_users             — List all users

── Loans ────────────────────────────────────
  loan_book              — Loan a book to a user
  return_book            — Return a book from a user
  list_loans             — List all active loans

── General ──────────────────────────────────
  help                   — Show this help message
  exit                   — Save and quit
  0                      — Cancel current operation (at any prompt)
```

---

## Design Decisions

### Book removal is a complete wipe from the library

When a book is removed, it is treated as physically gone from the library entirely not just marked inactive. This means:

- The book is deleted from the books catalogue
- All references to it are cleaned from the loan records

### Books currently on loan cannot be silently deleted

If a book is currently loaned out, a simple `remove_book` call will not go through. Instead, the system warns the librarian and lists every user who currently has a copy:

```
  ⚠️  'Python Programing'--'linus' is currently loaned by:
       - [1234567890] Younes Bouarroudj
       - [1234567894] Abdelrahmane Khelifi
  Force delete? (y/n) :
```

This is a **soft block, not a hard one**. The librarian is given the full picture and can decide. Confirming will remove the book from all loan lists and delete it.

### Users with active loans cannot be deleted

Unlike books, users cannot be force-deleted. A user with active loans represents a real person who physically holds library property. Deleting their record would mean losing accountability for those books entirely, with no way to recover who has them.

The correct flow is always: the user returns all books first, then they can be removed from the system.

### Input validation with graceful cancellation

Every prompt rejects empty input and asks again. At any prompt, entering `0` cancels the current operation and returns to the main menu — no partial data is ever saved.

### Copy tracking per book

Books are not stored as individual physical copies. Instead, each title/author pair has a copy count. Loaning decrements it, returning increments it. This keeps the data model simple while accurately reflecting availability.

A user cannot loan the same title twice simultaneously, but multiple different users can each hold a copy as long as copies are available.

---

## Data Format

Data is stored in `library_data.json` in the project directory. Example:

```json
{
  "name": "USTHB BIB",
  "next_book_id": 3,
  "books": [
    { "id": 2, "titre": "Python Programing", "auteur": "linus", "copies": 4 }
  ],
  "users": [
    { "matricule": "1919310442", "prenom": "Younes", "nom": "Bouarroudj", "specialty": "PhD2 RSSI" }
  ],
  "loans": [
    { "matricule": "1919310442", "books": [{ "id": 2, "titre": "Python Programing", "auteur": "linus" }] }
  ]
}
```
