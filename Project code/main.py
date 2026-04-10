from persistence import load, save
from commands import (
    cmd_add_book, cmd_remove_book, cmd_search_book, cmd_list_books, cmd_check_availability,
    cmd_add_user, cmd_remove_user, cmd_list_users,
    cmd_loan_book, cmd_return_book, cmd_list_loans,
    cmd_help
)

COMMANDS = {
    "add_book"            : cmd_add_book,
    "remove_book"         : cmd_remove_book,
    "list_books"          : cmd_list_books,
    "search_book"         : cmd_search_book,
    "check_availability"  : cmd_check_availability,    
    "add_user"            : cmd_add_user,
    "remove_user"         : cmd_remove_user,
    "list_users"          : cmd_list_users,
    "loan_book"           : cmd_loan_book,
    "return_book"         : cmd_return_book,
    "list_loans"          : cmd_list_loans,
}

if __name__ == "__main__":
    print("   📚  Library Management System")

    library = load()
    print("\n  Welcome to '%s' — type 'help' for commands.\n" % library.name)

    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Saving and exiting...")
            save(library)
            break

        if cmd == "exit":
            print("  Saving and exiting...")
            save(library)
            break
        elif cmd == "help":
            cmd_help()
        elif cmd in COMMANDS:
            COMMANDS[cmd](library)
        elif cmd == "":
            continue
        else:
            print("  ❌ Unknown command '%s'. Type 'help' for the list of commands." % cmd)