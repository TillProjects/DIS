def execute_query(connection: object, query: object, params: object = (), fetch: object = False) -> object:
    cur = connection.cursor()
    print(cur, query, params)
    try:
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        else:
            connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Database error: {e}")
    finally:
        cur.close()

def prompt_with_default(prompt_text, default_value):
    user_input = input(f"{prompt_text} [{default_value}]: ")
    return user_input if user_input != "" else default_value

def menu(title, options):
    print(f"\n--- {title} ---")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt[0]}")
    choice = input("Choose an option: ")
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        options[int(choice) - 1][1]()
    else:
        print("Invalid choice.")
