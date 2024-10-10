import os
from dotenv import load_dotenv
import inquirer
import requests

session = requests.Session()
load_dotenv()

api_key = os.getenv('API_KEY')
url = os.getenv('API_URL')

if api_key is None:
    raise Exception('API_KEY is not set')

if url is None:
    raise Exception('API_URL is not set')

session.headers['X-API-Key'] = api_key

def join(route: str):
    return f"{url}{route}"
    
print("Welcome to the admin panel")
print("Validating connection to the API...")

# validate connection to the API
try:
    response = session.get(join('/validate'))
    response.raise_for_status()
    print("Connection to the API is successful")
except requests.exceptions.RequestException as e:
    print(f"Failed to connect to the API: {e}")
    exit(1)


def select_user():
    response = session.get(join('/users'))
    response.raise_for_status()
    users = [user['id'] for user in response.json()]

    if len(users) == 0:
        print("No users found, please create a user first")
        return None

    questions = [
        inquirer.List('user',
            message="Select a user",
            choices=users,
        )
    ]

    answer = inquirer.prompt(questions)
    
    if answer is None:
        return None

    return answer['user']

def select_poll():
    response = session.get(join('/polls'))
    response.raise_for_status()
    polls = response.json()

    if len(polls) == 0:
        print("No polls found")
        return None

    questions = [
        inquirer.List('poll',
            message="Select a poll",
            choices=[(f"{poll['prompt']} (ID: {poll['id']})", poll['id']) for poll in polls],
        )
    ]

    answer = inquirer.prompt(questions)
    
    if answer is None:
        return None

    return answer['poll']

def select_response(poll_id: str):
    response = session.get(join(f'/poll/{poll_id}'))
    response.raise_for_status()
    poll = response.json()

    if len(poll['responses']) == 0:
        print("No responses found")
        return None

    questions = [
        inquirer.List('response',
            message="Select a response",
            choices=[(f"{response['response']} (ID: {response['id']})", response['id']) for response in poll['responses']],
        )
    ]

    answer = inquirer.prompt(questions)

    if answer is None:
        return None

    return answer['response']
    
def polls():
    while True:
        questions = [
            inquirer.List('action',
                message="What would you like to do with the polls?",
                choices=['Create', 'Delete', 'List', 'Get Responses', 'Update Status', 'Back'],
            )
        ]

        answer = inquirer.prompt(questions)

        if answer is None:
            print("No action selected, returning to main menu...")
            break

        # create a new poll
        if answer['action'] == 'Create':
            user_id = select_user()
            if user_id is None:
                print("No user selected, returning to poll menu...")
                continue
            prompt = inquirer.text(message="Enter the poll prompt")
            n_responses = inquirer.text(message="Enter the number of responses", validate=lambda _, x: x.isdigit())

            if prompt is None or n_responses is None:
                print("No prompt or number of responses entered, returning to poll menu...")
                continue

            try:
                session.post(join('/poll'), json={
                    'user_id': user_id,
                    'prompt': prompt,
                    'n_responses': int(n_responses)
                })
                print(f"Created poll for user: {user_id}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to create poll: {e}")

        # delete a poll
        elif answer['action'] == 'Delete':
            poll_id = select_poll()
            if poll_id is None:
                print("No poll selected, returning to poll menu...")
                continue
            try:
                session.delete(join(f'/poll/{poll_id}'))
                print(f"Deleted poll with ID: {poll_id}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to delete poll: {e}")

        # list all polls
        elif answer['action'] == 'List':
            response = session.get(join('/polls'))
            response.raise_for_status()
            polls = response.json()

            if len(polls) == 0:
                print("No polls found")
                continue

            print("Polls:")
            for poll in polls:
                print(f"{poll['id']} ({'active' if poll['active'] else 'inactive'}): {poll['prompt']}")

        # get responses for a poll
        elif answer['action'] == 'Get Responses':
            poll_id = select_poll()
            if poll_id is None:
                print("No poll selected, returning to poll menu...")
                continue

            response = session.get(join(f'/poll/{poll_id}/responses'))
            response.raise_for_status()
            responses = response.json()

            print("Responses:")
            for response in responses:
                print(f"{response['id']}: {response['text']}")

        

        # update the status of a poll
        elif answer['action'] == 'Update Status':
            poll_id = select_poll()
            if poll_id is None:
                print("No poll selected, returning to poll menu...")
                continue

            response = session.patch(join(f'/poll/{poll_id}'))
            response.raise_for_status()
            poll = response.json()


            print(f"Updated poll with ID: {poll['id']} to {'active' if poll['active'] else 'inactive'}")
        elif answer['action'] == 'Back':
            break

        print("\n")  # Add a newline for better readability between actions

def users():
    while True:
        questions = [
            inquirer.List('action',
                message="What would you like to do with the users?",
                choices=['Create', 'Delete', 'List', 'Back'],
            )
        ]

        answer = inquirer.prompt(questions)

        if answer is None:
            print("No action selected, returning to main menu...")
            break

        # create a new user
        if answer['action'] == 'Create':
            try:
                response = session.post(join('/user'))
                user = response.json()
                print(f"Created user with ID: {user['id']}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to create user: {e}")

        # delete a user
        elif answer['action'] == 'Delete':
            user_id = select_user()
            if user_id is None:
                print("No user selected, returning to user menu...")
                continue
            try:
                session.delete(join(f'/user/{user_id}'))
                print(f"Deleted user with ID: {user_id}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to delete user: {e}")

        # list all users
        elif answer['action'] == 'List':
            try:
                response = session.get(join('/users'))
                users = response.json()
                print("Users:")
                for user in users:
                    print(user['id'])
            except requests.exceptions.RequestException as e:
                print(f"Failed to list users: {e}")

        elif answer['action'] == 'Back':
            break

        print("\n")  # Add a newline for better readability between actions

while True:
    print("\n")
    questions = [
        inquirer.List('action',
            message="What model would you like to manage?",
            choices=['Users', 'Polls', 'Exit'],
        )
    ]

    answer = inquirer.prompt(questions)

    if answer is None:
        print("No action selected, returning to main menu...")
        continue

    if answer['action'] == 'Users':
        users()
    elif answer['action'] == 'Polls':
        polls()
    elif answer['action'] == 'Exit':
        break