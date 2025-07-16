import mysql.connector as sql

def connect_db():
    return sql.connect(host="localhost", user="root", passwd="12345", database="food")

def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS myc (
        cust_name VARCHAR(100),
        account_no INT PRIMARY KEY
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        account_no INT,
        food_name VARCHAR(100),
        price DECIMAL(10,2),
        address VARCHAR(255),
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_no) REFERENCES myc(account_no)
    )
    """)

def create_account(cursor, conn):
    print("\n" + "=" * 40)
    print("         CREATE YOUR ACCOUNT")
    print("=" * 40)

    while True:
        name = input("Enter your full name: ").strip()
        if name and len(name) >= 2:
            break
        print("Name must be at least 2 characters!")

    while True:
        try:
            acc = int(input("Enter your account number (4-6 digits): "))
            if 1000 <= acc <= 999999:
                break
            else:
                print("Account number must be between 1000 and 999999.")
        except ValueError:
            print("Enter a valid number!")

    cursor.execute("SELECT * FROM myc WHERE account_no = %s", (acc,))
    if cursor.fetchone():
        print("❌ Account number already exists!")
        return

    cursor.execute("INSERT INTO myc (cust_name, account_no) VALUES (%s, %s)", (name, acc))
    conn.commit()
    print("✅ Account created successfully!")

    while True:
        print("\n1. Login")
        print("2. Exit")
        next_choice = input("Enter your choice: ")
        if next_choice == "1":
            login(cursor, conn)
            break
        elif next_choice == "2":
            print("Exiting. Thank you!")
            exit()
        else:
            print("Invalid choice.")

def login(cursor, conn):
    print("\n" + "=" * 40)
    print("              LOGIN")
    print("=" * 40)

    try:
        acc_no = int(input("Enter your account number: "))
    except ValueError:
        print("Invalid input.")
        return

    cursor.execute("SELECT cust_name FROM myc WHERE account_no = %s", (acc_no,))
    result = cursor.fetchone()

    if not result:
        print("❌ No account found with that number.")
        return

    name = result[0]
    print(f"\n✅ Welcome, {name}!")

    while True:
        print("\n1. Order Food")
        print("2. See Ordered Food")
        print("3. Update Order Address")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            food_name = input("Enter food name: ")
            try:
                price = float(input("Enter price: "))
            except ValueError:
                print("Invalid price!")
                continue
            address = input("Enter delivery address: ")

            cursor.execute("INSERT INTO sales (account_no, food_name, price, address) VALUES (%s, %s, %s, %s)",
                           (acc_no, food_name, price, address))
            conn.commit()
            print("✅ Order placed successfully!")

        elif choice == "2":
            cursor.execute("SELECT * FROM sales WHERE account_no = %s", (acc_no,))
            orders = cursor.fetchall()

            if not orders:
                print("No orders found.")
            else:
                print("\n--- Your Orders ---")
                for order in orders:
                    print(f"Order ID: {order[0]}, Food: {order[2]}, Price: ₹{order[3]}, Address: {order[4]}, Date: {order[5]}")

        elif choice == "3":
            try:
                order_id = int(input("Enter Order ID to update address: "))
                new_address = input("Enter new address: ")

                cursor.execute("UPDATE sales SET address = %s WHERE id = %s AND account_no = %s",
                               (new_address, order_id, acc_no))
                conn.commit()
                if cursor.rowcount:
                    print("✅ Address updated.")
                else:
                    print("❌ No matching order found.")
            except ValueError:
                print("Invalid order ID!")

        elif choice == "4":
            print("Logging out. Thank you!")
            break
        else:
            print("Invalid choice.")

def main():
    try:
        conn = connect_db()
        if conn.is_connected():
            print("✅ Connected to MySQL")

        c1 = conn.cursor()
        create_tables(c1)

        while True:
            print("\n" + "=" * 50)
            print("       WELCOME TO THE FOOD ORDER SYSTEM")
            print("=" * 50)
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            print("=" * 50)

            choice = input("Enter your choice: ")

            if choice == "1":
                create_account(c1, conn)
            elif choice == "2":
                login(c1, conn)
            elif choice == "3":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice.")

    except sql.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    main()
