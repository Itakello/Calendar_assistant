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
    main('EwCYA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAdjiXyZV5qeIHC1Nuomzfy4PvIlRtkJI5t05PGFMUafWK/QjmWqNgkBjRr4WvLNxreFXldiAsAlcs2jJRx3DxJ60EF23HrNHCDf9OQ27y86EPfO3kkGV91Q9xccV+ppy+kbNTmV4CEG8dGkHumjVE/Ae17gubi5UGIcLm4sZXOt9baGiTh6Vp+poOYwL6WLJsUPSetngkvR8aqSj0g9qRaGr5i4l0xR10YdnniB553mm04uiRUdDRfRB6gyi0Kk+hKYOxU3/gOIffANbz0UAFypZbrPaSfSORTsQzvY+m5NEo77LFS/qI+/iPVE5AtHnEAQ8mccEgFVNdtCnKPnFEQADZgAACDwuCeHR3LKGaAKyUPqLP1ryN7YNXMoldv9Qs60fFuwXACA/Fpl7/wyHokWXxzTm1RdUoo3llYeMOScHi9yn5OGDAvPn+SDmJ5q9u8NdPamD3BzelFsL0Cze11myMCTlkfgM1Rsfsf28feoR7ePrbwOMlDfgqGd6tEFVsJ4LS+0ZpR166pQc0ZxExzO4v3cfg/YXfozF4Uul7L97w6LoxCR0+YzJovzwR4JsZHS4T1+2JSS/CPe+yt1BvTZPnWhpxti4fTNQYl3SButY6IqAKZ/0v+uMzhPS+dMgdkAu1ex9MCvdCXkRxzgiYqLE3/ZA4o6SKQiUFgz9/6/R6IWejxr6OMhTT3/r6Db8l3fMDKW0yJ1J+Jj7jQsA9eEmG41Vo2dIuriQkceZy0WZBiIli9yl0R6eAX0yIuPJlWFEg0R2iAenryRgKIGzhBWS7joPN0r3mDvEb0VA6O3r3dlzmnqVDZQ02nADgSAJ80y9jP3Z0DbenQDVK1Y6qXsjt8dORk179LJTTtMPIIjZ/vez+gDsbrMNHdYpS5wnphL59usGWGwdMj4535OZpLZpn5gcmYYWlnzp8kZpTnZw6qMbg4wpgLeZgA5CHKJa1Ern1KVkAFLVSkYmZZa4Y3v+IsU4elZte1vCPXDlBgfUNbb1f6onIYw0wtxi96f8mlIpSrJxgYe1vNLcoxGvQLGvaqgyF3qiHVifZ3qwHANAFZADFbyQixgR3nJcAc6FQoV3rOhyqm4IylfxWV4fqc5JUj4aHnqKP2QkLE/mT/xKkH5QfQwrZTWLr9Dqk3yEfPu7Q+pWb8kOG0bGFeQ1Q4b/H7EMWxjCjgI=')