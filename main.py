from components.agent import get_agent


def main(access_token: str):
    print("Welcome to the Calendar Assistant. Type 'quit' to exit.")
    
    agent = get_agent(access_token)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = agent.run(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main('EwCQA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAcz5m1U2R8mPb5EdRAGq4ZlLyGuqmw+AgRRAVl5Z5V69N4txMDoxDPx7h57KNIiMvjuqGkpZLWgXZiXJJk66G65nM5vKRJwLr6HhOHJaVM6bPk5jaOpTZLDY5MNPwsuZLEKv2zgvk7i0ctOYwANK30X9l93yX03RQ0bO9VeELFigme2MsA95WmfHj0RXKYnGoEahcVomIxCabs8Ot6bYbQwd2gJH4+2NWFseizGw3NliTRzDKnnVvlsKeFc0Eo/DaJWjAmgPHJyqx8faL3zhrGgfPYKiAo5dpDcuqPBNWCYx+EcqeJdODkwHkRlQrYrh8NyDdZ8QMoqvc9fmdOg0+gkDZgAACCTrsmt9/SxrYALtCB+ZXDF2QVf8hvBDJOyjeRJ8DO2xMkINRFyOh1LJzwqCDSm6Y3YT7RQ85N591OIhZlRd2g8o6WoIk1atPMVMyI+9pccxj3J6h2b17x52JipSobfrNyPI7dV8pFccu5qirTuFZvRMMg2tx5kX6s19jzlVr7isz++JX/c9iZtgVnUMs04RtBHUTBgnx3ODv4OmdCpvu10hI5bZ4ELxSgE2NvHxDrc9z2XpC6G9EOkLYcKvYFFmVXyyoY6zele9+74KlxN5prVMHQ3wx4nd4mm0yeShZCYhZZYPUpnyhJXKHbEJBo/BoTzuC/7PrwGuKS2RMKVVYyBQYbaBvK8Lm/1u98NmlSlxaXyvOEX8kqaatZsfkqSMqqc7GGs2RDZGqb3+9ujITz+N4/olsacmZql9p7pUBepaeCP+mVrLjGAHo50mFV4O6H4VwUxMp26PtXdSIoqLWHLrDu8kMlVPGbxS7OVxpXbFS7xslYhSJsoiDr7nbUOqIWIDXd3VPNRMLhtd1h+WTfwsQOIjtmgvDcPvUPiMaCl+n/VyCS6H1HL9BFHKLFL+Gqxn6xuINBYgstRV6xrIrCbxIEImTesb8YxASRuiuyncqd+quoJfVW8ZnOrdd4fPvijzxZkdo8XKpaDYISwIlKKio45Euj37DSgE5+4akEtMMRhxySyEWwmpCZK1gyUHi1t4fC2JTZJBNQAQxVfGbtlIod4IrrPcoXhagJ/GzLz8OAZ4+lNeLl8HqepsJX0a2jGPXF6irmoRfUtbblP9nDo46TrFDoM7IDPhkH0ZxU9t8bq7gFYQs2tmb44C')