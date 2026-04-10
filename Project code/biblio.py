from models import livre, utilisateur


class biblio:
    def __init__(self, name, next_book_id=1):
        self.name = name
        self.next_book_id = next_book_id
        self.books = {}
        self.users = []
        self.loans = {}

        self.book_manager = BookManager(self)
        self.user_manager = UserManager(self)
        self.loan_manager = LoanManager(self)

    def add_book(self, titre, auteur, copies=1):
        return self.book_manager.add_book(titre, auteur, copies)

    def remove_book(self, titre, auteur):
        return self.book_manager.remove_book(titre, auteur)

    def force_remove_book(self, titre, auteur):
        return self.book_manager.force_remove_book(titre, auteur)

    def get_book_borrowers(self, titre, auteur):
        return self.book_manager.get_book_borrowers(titre, auteur)

    def _find_book(self, titre, auteur):
        return self.book_manager._find_book(titre, auteur)

    def search_book(self, titre, auteur):
        return self.book_manager.search_book(titre, auteur)

    def check_availability(self, titre, auteur):
        return self.book_manager.check_availability(titre, auteur)

    def get_books(self):
        return self.book_manager.get_books()

    def add_user(self, matricule, prenom, nom, specialty):
        return self.user_manager.add_user(matricule, prenom, nom, specialty)

    def remove_user(self, matricule):
        return self.user_manager.remove_user(matricule)

    def _find_user(self, matricule):
        return self.user_manager._find_user(matricule)

    def get_users(self):
        return self.user_manager.get_users()

    def loan_book(self, matricule, titre, auteur):
        return self.loan_manager.loan_book(matricule, titre, auteur)

    def return_book(self, matricule, titre, auteur):
        return self.loan_manager.return_book(matricule, titre, auteur)

    def get_loans(self):
        return self.loan_manager.get_loans()



class BookManager:

    def __init__(self, library):
        self.library = library


    def add_book(self, titre, auteur, copies=1):
        book = livre(self.library.next_book_id, titre, auteur)
        self.library.books[book] = copies
        self.library.next_book_id += 1
        print("  ✅ [ID:%d] '%s'--'%s' added (%d copy(ies))." % (book.id, titre, auteur, copies))


    def remove_book(self, titre, auteur):
        book = self._find_book(titre, auteur)
        if not book:
            return "  ❌ '%s'--'%s' not found." % (titre, auteur)
        if any(book in books for books in self.library.loans.values()):
            return None  # signals that a conflict exists
        del self.library.books[book]
        return "  ✅ [ID:%d] '%s'--'%s' removed." % (book.id, titre, auteur)


    def force_remove_book(self, titre, auteur):
        book = self._find_book(titre, auteur)
        # remove the book from every user's loan list
        for user in list(self.library.loans):
            if book in self.library.loans[user]:
                self.library.loans[user].remove(book)
                if not self.library.loans[user]:
                    del self.library.loans[user]
        del self.library.books[book]
        return "  ✅ [ID:%d] '%s'--'%s' force-removed." % (book.id, titre, auteur)


    def get_book_borrowers(self, titre, auteur):
        book = self._find_book(titre, auteur)
        return [user for user, books in self.library.loans.items() if book in books]


    def get_books(self):
        if not self.library.books:
            return "  The library is empty."
        output = "\n  %-6s | %-30s | %-20s | %s\n" % ("ID", "Title", "Author", "Copies")
        output += "  " + "-" * 65 + "\n"
        for book, copies in self.library.books.items():
            output += "  %-6d | %-30s | %-20s | %d\n" % (book.id, book.titre, book.auteur, copies)
        return output


    def search_book(self, titre, auteur):
        book = self._find_book(titre, auteur)
        if not book:
            return "  ❌ '%s'--'%s' not found." % (titre, auteur)
        return "  ✅ [ID:%d] '%s' by '%s' — %d copy(ies) available." % (
            book.id, book.titre, book.auteur, self.library.books[book])


    def check_availability(self, titre, auteur):
        book = self._find_book(titre, auteur)
        if not book:
            return "  ❌ '%s'--'%s' not found." % (titre, auteur)
        available = self.library.books[book] > 0
        if available:
            return "  ✅ [ID:%d] '%s'--'%s' is available — %d copy(ies)." % (book.id, titre, auteur, self.library.books[book])
        else:
            return "  ❌ [ID:%d] '%s'--'%s' is currently unavailable." % (book.id, titre, auteur)


    def _find_book(self, titre, auteur):
        return next((b for b in self.library.books
                     if b.titre.lower() == titre.lower()
                     and b.auteur.lower() == auteur.lower()), None)





class UserManager:

    def __init__(self, library):
        self.library = library


    def add_user(self, matricule, prenom, nom, specialty):
        user = utilisateur(matricule, prenom, nom, specialty)
        self.library.users.append(user)
        print("  ✅ [%s] '%s %s' added." % (matricule, prenom, nom))


    def remove_user(self, matricule):
        user = self._find_user(matricule)
        if not user:
            return "  ❌ Matricule '%s' not found." % matricule
        if user in self.library.loans:
            return "  ❌ [%s] '%s %s' has active loans, return them first." % (
                user.matricule, user.prenom, user.nom)
        self.library.users.remove(user)
        return "  ✅ [%s] '%s %s' removed." % (user.matricule, user.prenom, user.nom)


    def get_users(self):
        if not self.library.users:
            return "  No users yet added to the library."
        output = "\n  %-12s | %-20s | %s\n" % ("Matricule", "Full Name", "Specialty")
        output += "  " + "-" * 55 + "\n"
        for user in self.library.users:
            output += "  %-12s | %-20s | %s\n" % (
                user.matricule, user.prenom + " " + user.nom, user.specialty)
        return output


    def _find_user(self, matricule):
        return next((u for u in self.library.users
                     if u.matricule.lower() == matricule.lower()), None)





class LoanManager:

    def __init__(self, library):
        self.library = library


    def loan_book(self, matricule, titre, auteur):
        user = self.library.user_manager._find_user(matricule)
        if not user:
            return "  ❌ Matricule '%s' not found." % matricule

        book = self.library.book_manager._find_book(titre, auteur)
        if not book:
            return "  ❌ '%s'--'%s' not found." % (titre, auteur)

        if self.library.books[book] < 1:
            return "  ❌ No copies of '%s'--'%s' currently available." % (titre, auteur)

        if user in self.library.loans and any(b.id == book.id for b in self.library.loans[user]):
            return "  ❌ [%s] '%s %s' already has a copy of '%s'--'%s'." % (
                matricule, user.prenom, user.nom, titre, auteur)

        self.library.books[book] -= 1
        if user not in self.library.loans:
            self.library.loans[user] = []
        self.library.loans[user].append(book)

        return "  ✅ [ID:%d] '%s'--'%s' loaned to '%s %s' — %d copy(ies) left." % (
            book.id, titre, auteur, user.prenom, user.nom, self.library.books[book])


    def return_book(self, matricule, titre, auteur):
        user = self.library.user_manager._find_user(matricule)
        if not user:
            return "  ❌ Matricule '%s' not found." % matricule

        if user not in self.library.loans:
            return "  ❌ [%s] '%s %s' has no active loans." % (matricule, user.prenom, user.nom)

        book = next((b for b in self.library.loans[user]
                     if b.titre.lower() == titre.lower()
                     and b.auteur.lower() == auteur.lower()), None)
        if not book:
            return "  ❌ [%s] '%s %s' didn't loan '%s'--'%s'." % (matricule, user.prenom, user.nom, titre, auteur)

        self.library.loans[user].remove(book)
        if not self.library.loans[user]:
            del self.library.loans[user]

        self.library.books[book] += 1
        return "  ✅ [ID:%d] '%s'--'%s' returned by '%s %s' — %d copy(ies) now available." % (
            book.id, titre, auteur, user.prenom, user.nom, self.library.books[book])


    def get_loans(self):
        if not self.library.loans:
            return "  No active loans."
        output = "\n  %-12s | %-20s | %s\n" % ("Matricule", "Full Name", "Loaned Books")
        output += "  " + "-" * 70 + "\n"
        for user, books in self.library.loans.items():
            titles = ", ".join("[ID:%d] '%s'--'%s'" % (b.id, b.titre, b.auteur) for b in books)
            output += "  %-12s | %-20s | %s\n" % (user.matricule, user.prenom + " " + user.nom, titles)
        return output