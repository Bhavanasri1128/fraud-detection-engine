from database import init_db
from engine import score_transaction, resolve_alert, get_all_alerts

def main():
    init_db()
    while True:
        print("\n--- MULTI-BANK FRAUD DETECTION ENGINE ---")
        print("1. Score New Transaction")
        print("2. View Fraud Alerts")
        print("3. Resolve Alert (Confirm Fraud / False Positive)")
        print("4. Exit")

        choice = input("Choose option: ").strip()
        try:
            if choice == "1":
                token = input("Card Token (TOK_101 or TOK_102): ").strip()
                amount = float(input("Amount (Rs.): "))
                device = input("Device ID (e.g., DEV_01): ").strip()
                score, decision, reason = score_transaction(token, amount, device)
                print(f"Risk Score: {score}/100 | Decision: {decision} | Reason: {reason}")

            elif choice == "2":
                alerts = get_all_alerts()
                if not alerts:
                    print("No alerts recorded yet.")
                for a in alerts:
                    print(f"Alert #{a[0]} | Card: {a[1]} | Rs. {a[2]} | Score: {a[3]} | {a[4]} [{a[5]}]")

            elif choice == "3":
                aid = int(input("Enter Alert ID: "))
                ans = input("Confirm Fraud? (yes/no): ").strip().lower()
                resolve_alert(aid, ans == "yes")
                print(f"Alert #{aid} resolved!")

            elif choice == "4":
                print("Exiting.")
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
