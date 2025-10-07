"""
Program: Currency Converter CLI
Problem Statement: Convert an amount in INR to USD, EUR, GBP, and JPY using fixed rates.

Input Example:
    Enter amount in INR: 1000

Output Example:
    1000 INR is:
      12.00 USD
      11.00 EUR
      9.60 GBP
      180.00 JPY

Notes:
  - Exchange rates are static for this beginner example.
  - Extendable: could be turned into a live API scraper.

Complexity: O(1) per conversion
"""

def convert_currency(inr):
    rates = {
        'USD': 0.012,
        'EUR': 0.011,
        'GBP': 0.0096,
        'JPY': 0.18
    }
    print(f"\n{inr} INR is:")
    for currency, rate in rates.items():
        print(f"  {inr * rate:.2f} {currency}")

if __name__ == "__main__":
    try:
        amount = float(input("Enter amount in INR: "))
        if amount < 0:
            print("Amount must be positive!")
        else:
            convert_currency(amount)
    except ValueError:
        print("Please enter a valid number.")
