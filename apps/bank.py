from horserace import calculate_prices

class BankClient:
    def __init__(self):
        # Dictionary to store player accounts with their balances
        self.accounts = {}

    def add_player(self, player_name, initial_balance):
        """Adds a new player with an initial balance."""
        if player_name in self.accounts:
            raise ValueError(f"Player '{player_name}' already exists.")
        self.accounts[player_name] = [initial_balance, 0, 0, 0, 0] # 0 represent number of shares for each racer
    
    def get_balance(self, player_name):
        """Returns the balance of the specified player."""
        if player_name not in self.accounts:
            raise ValueError(f"Player '{player_name}' does not exist.")
        return self.accounts[player_name]

    def make_purchase(self, player_name, racer, num_shares, price):
        """Deducts the purchase amount from the player's account."""
        if player_name not in self.accounts:
            raise ValueError(f"Player '{player_name}' does not exist.")
        if num_shares < 0:
            raise ValueError("Number of shares cannot be negative.")
        purchase_amount = num_shares * price
        if purchase_amount < 0:
            raise ValueError("Purchase amount cannot be negative.")
        if self.accounts[player_name][0] < purchase_amount:
            raise ValueError(f"Player '{player_name}' does not have enough balance.")
        self.accounts[player_name][0] -= purchase_amount
        self.accounts[player_name][racer+1] += num_shares # First index is the balance, so we add 1 to the index of the racer

    def deposit(self, player_name, racer, num_shares, price):
        """Deposits a specified amount into the player's account."""
        if player_name not in self.accounts:
            raise ValueError(f"Player '{player_name}' does not exist.")
        if self.accounts[player_name][racer+1] < num_shares:
            raise ValueError(f"Player '{player_name}' does not have enough shares to sell.")
        amount = num_shares * price
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative.")
        self.accounts[player_name][0] += amount
        self.accounts[player_name][racer+1] -= num_shares
        
    


    def __str__(self):
        """Returns a string representation of all player accounts."""
        return "\n".join([f"{player}: {balance}" for player, balance in self.accounts.items()])


def interactive_menu():
    client = BankClient()

    bank_buy_prices = [0, 0, 0, 0]
    bank_sell_prices = [0, 0, 0, 0]
    print("Welcome to the Bank Client!")
    while True:
        print("\nMenu:")
        print("1. Add Player")
        print("2. Check Balance")
        print("3. Buy Shares")
        print("4. Sell Shares")
        print("5. Show All Accounts")
        print("6. Display Offered Prices")
        print("7. Buy Via Total Cost")
        print("8. Sell Via Total Cost")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            player_name = input("Enter player name: ")
            try:
                initial_balance = float(input("Enter initial balance: "))
                client.add_player(player_name, initial_balance)
                print(f"Player '{player_name}' added with balance {initial_balance}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            player_name = input("Enter player name: ")
            try:
                balance = client.get_balance(player_name)
                print(f"Player '{player_name}' has a balance of {balance}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            player_name = input("Enter player name: ")
            try:
                ls = list(map(int, input("Enter the racer and amount of shares space separated (e.g 2 25): ").split() ))
                if len(ls) != 2:
                    raise ValueError("Please enter exactly two values.")
                racer, num_shares = ls[0], ls[1]
                if racer < 0 or racer > 3:
                    raise ValueError("Racer must be between 0 and 3.")
                if num_shares < 0:
                    raise ValueError("Number of shares cannot be negative.")
                client.make_purchase(player_name, racer, num_shares, bank_sell_prices[racer]) # Exchanges money for shares
                print(f"Purchase of {num_shares} shares of racer {racer} by '{player_name}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            player_name = input("Enter player name: ")
            try:
                ls = list(map(int, input("Enter the racer and amount of shares space separated (e.g 2 25): ").split() ))
                if len(ls) != 2:
                    raise ValueError("Please enter exactly two values.")
                racer, num_shares = ls[0], ls[1]
                if racer < 0 or racer > 3:
                    raise ValueError("Racer must be between 0 and 3.")
                if num_shares < 0:
                    raise ValueError("Number of shares cannot be negative.")
                client.deposit(player_name, racer, num_shares, bank_buy_prices[racer]) # Exchanges shares for money
                print(f"Sold {num_shares} shares of racer {racer} by player '{player_name}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("\nAll Accounts:")
            print(client)

        elif choice == "6":
            input_state = input("Enter board state (e.g. 0 1 2 1): ")
            try:
                prices = calculate_prices(input_state)
                bank_buy_prices = prices.copy()
                bank_sell_prices = [price * 1.01 for price in prices] # Assuming a 1% markup for selling, will fix this later
                print("Offered Prices:", prices) # Could make look better
            except ValueError as e:
                print(f"Error: {e}")

        # TODO 7 and 8
        elif choice == "7":
            player_name = input("Enter player name: ")
            try:
                ls = list(map(int, input("Enter the racer and total cost space separated (e.g 2 25): ").split() ))
                if len(ls) != 2:
                    raise ValueError("Please enter exactly two values.")
                racer, total_cost = ls[0], ls[1]
                if racer < 0 or racer > 3:
                    raise ValueError("Racer must be between 0 and 3.")
                if total_cost < 0:
                    raise ValueError("Total cost cannot be negative.")
                num_shares = int(total_cost / bank_sell_prices[racer])
                client.make_purchase(player_name, racer, num_shares, bank_sell_prices[racer]) # Exchanges money for shares
                print(f"Purchase of {num_shares} shares of racer {racer} by '{player_name}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "8":
            player_name = input("Enter player name: ")
            try:
                ls = list(map(int, input("Enter the racer and total cost space separated (e.g 2 25): ").split() ))
                if len(ls) != 2:
                    raise ValueError("Please enter exactly two values.")
                racer, total_cost = ls[0], ls[1]
                if racer < 0 or racer > 3:
                    raise ValueError("Racer must be between 0 and 3.")
                if total_cost < 0:
                    raise ValueError("Total cost cannot be negative.")
                num_shares = int(total_cost / bank_buy_prices[racer])
                client.deposit(player_name, racer, num_shares, bank_buy_prices[racer]) # Exchanges shares for money
                print(f"Sold {num_shares} shares of racer {racer} by player '{player_name}'.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "9":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    interactive_menu()