from persistence import save


def input_check(msg):
    while True:
        A = input(msg).strip()
        if A == "0":
            return None
        if len(A) != 0:
            return A
        print('  ⚠️  Please enter something. (or "0" to cancel)')


def cmd_add_book(library):
    titre  = input_check("  Book title  : ")
    if titre  is None: return
    auteur = input_check("  Author name : ")
    if auteur is None: return
    while True:
        try:
            copies = int(input("  Copies      : ").strip() or "1")
            if copies < 1:
                raise ValueError
            break
        except ValueError:
            print("  Please enter a valid number of copies.")
    book = library._find_book(titre, auteur)
    if book:
        library.books[book] += copies
        print("  ✅ [ID:%d] %d copy(ies) added to existing '%s'--'%s'." % (book.id, copies, titre, auteur))
        save(library)
        return
    library.add_book(titre, auteur, copies)
    save(library)


def cmd_remove_book(library):
    titre  = input_check("  Book title  : ")
    if titre  is None: return
    auteur = input_check("  Author name : ")
    if auteur is None: return

    result = library.remove_book(titre, auteur)

    # None signals a loan conflict time to enter the force-delete flow
    if result is None:
        borrowers = library.get_book_borrowers(titre, auteur)
        print("  ⚠️  '%s'--'%s' is currently loaned by:" % (titre, auteur))
        for user in borrowers:
            print("       - [%s] %s %s" % (user.matricule, user.prenom, user.nom))
        confirm = input("  Force delete? (y = yes, any other key = no) : ").strip().lower()
        if confirm == "y":
            print(library.force_remove_book(titre, auteur))
            save(library)
            return
        else:
            print("  ↩️  Deletion cancelled.")
            return
        
    print(result)
    save(library)


def cmd_search_book(library):
    titre  = input_check("  Book title  : ")
    if titre  is None: return
    auteur = input_check("  Author name : ")
    if auteur is None: return
    print(library.search_book(titre, auteur))


def cmd_list_books(library):
    print(library.get_books())


def cmd_check_availability(library):
    titre  = input_check("  Book title  : ")
    if titre  is None: return
    auteur = input_check("  Author name : ")
    if auteur is None: return
    print(library.check_availability(titre, auteur))


def cmd_add_user(library):
    matricule = input_check("  Matricule  : ")
    if matricule is None: return
    if library._find_user(matricule):
        print("  ❌ Matricule '%s' already exists." % matricule)
        return
    prenom    = input_check("  First name : ")
    if prenom    is None: return
    nom       = input_check("  Last name  : ")
    if nom       is None: return
    specialty = input_check("  Specialty  : ")
    if specialty is None: return
    library.add_user(matricule, prenom, nom, specialty)
    save(library)


def cmd_remove_user(library):
    matricule = input_check("  Matricule : ")
    if matricule is None: return
    print(library.remove_user(matricule))
    save(library)


def cmd_list_users(library):
    print(library.get_users())


def cmd_loan_book(library):
    matricule = input_check("  Matricule   : ")
    if matricule is None: return
    titre     = input_check("  Book title  : ")
    if titre     is None: return
    auteur    = input_check("  Author name : ")
    if auteur    is None: return
    print(library.loan_book(matricule, titre, auteur))
    save(library)


def cmd_return_book(library):
    matricule = input_check("  Matricule   : ")
    if matricule is None: return
    titre     = input_check("  Book title  : ")
    if titre     is None: return
    auteur    = input_check("  Author name : ")
    if auteur    is None: return
    print(library.return_book(matricule, titre, auteur))
    save(library)


def cmd_list_loans(library):
    print(library.get_loans())


def cmd_help():
    print("""
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
""")