import requests

"""
Sending the request for weather data through the terminal.
"""
def main():

    while True: 
        print("\nWeather data\n 1. Get data for a city\n 2. Get stored data for all cities\n 3. Exit")
        choice = int(input('Enter choice (1-3)'))

        if choice == 1:

            endpoint = 'http://127.0.0.1:5000/get-weather/'
            data = {
                'city':input('Enter city name: ')
            }

            responds = requests.post(endpoint,json=data) 
            print(f'Responds from server: \n {responds.text}') 

        elif choice ==2:

            get_endpoint = 'http://127.0.0.1:5000/get-data/'

            responds = requests.get(get_endpoint)

            print(f'Responds from server: \n {responds.text}')

        elif choice ==3:
            break
        else:
            print('Invalid choice. Choose (1-3) ')

if __name__ == '__main__':
    main()