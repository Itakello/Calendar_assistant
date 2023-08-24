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
    main('EwCYA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAQ0Hztmy0tu0in3M9B5PM3p+F22HZFtLN5roZu60SMIVAqn6NkJFKFuCnALptFW+FN9RmlMW4BNSjzgzQNoqK05LGyttYXNS3/FbfqiVY9KufwJRbjNYQjm3Jze5rKsPCq4LJaCGmOGLmHSZZIDSUcNY6UypeW0u4kSjVSVG72jvZ+njYLS2g+Wt/w74fZn4Wc2eVsRiOpNsWry+boyDccHbeG8MYDVUDh3tycFa6pv1nINPbYf3kIhQkIhTHOrePAMoqrUZcnI0K40/JXqijBz3gwR9vAS8Q4Pgfx2D4A6Aq+nApRa2fvIgARy8VFm0qwqLUgpSx3JXyM/foNFxBAYDZgAACIZm0SioTGtRaAIBk5f6ZBoRp1AlvztLh5LTlkWxJ1cpGTBG7NP6QhHSUonWhfyKCJoRHVGyW++gmhbm0ZPnKZzLQ36nELSJOH3O5NPnMivSJLXE45DQLv+3JLLEZ2tW2UAGUZP0wPFo4Ya9R0aBbeXF10F9cfTDFw63P20MPyye8zprtfIhnzrvpjnNjUuLl3Nq8EbbMQph15tVZdOW5IP24QS2CrVOKi/A2genhs0UCa0cfaT6pnd0oY/u/f2jEJ+j7vmPTDYOBe9g0rWe49ap6dOJ2NcGSMi/a2R1yKWv9mmnhgHYkhQdWwPrrkW8HqZkE/dHYA4VU/xABHN912daG/tpSovUQVApWGJ3ZqzMh7rtpUMpJ6R+4MEE1CntgWP+KXNNmeXFnus5prRNdtfRBXHTk9nIZdvoSm+ui0McSGdg8VuTkGcROeka6QTiNpkO9ZG5yzU7xQ+3Y/itbcO06QG5kwV2d4bivIYPhzbZ6IjtNR1naYcCLNupp6YxoWEcnpGW1b9vfzWcnUrc+BgwmmPgYH+kLhmwIYfkFO1wE455Yfbe8DWFC48XT0ZHOd5dsH5yEymfwHFcGoPn1X46qCnBH+uUiFoSe72VqHb9g1QqAFv4i2KNWAavNzMooEtuupoc8GTKrOn1kj3euENEIuzvrGgkHI4MbPkLvo25oRkVz+eQnfFHP6QPbsp1FhcliFyF0d3dNej1TltTymz+5Chc3JazsiUNZ+OLTS6gqK8Z1PlCJO+ImjP91oFUJ7ZgwGwaRhfDOusjSYKjdD/VmiuV0e6GG1OIRPY9s4sfHwjac2VFOx86C8cc0zEp4knwjgI=')