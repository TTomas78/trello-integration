
# Trello integration

This integration was created as a result of a technical challenge


## Installation

It's recomended to create a virtual environment to install the dependencies in an isolated environment

If you don't know anything about it, you can read https://virtualenv.pypa.io/en/latest/


```bash
virtualenv venv
```

Once it's created it's necessary to activate it

On Windows  (Powershell)
```bash
./venv/script/activate
```
On Linux

```bash
./venv/bin/activate
```

Once it's activated, the dependencies can be installed through the requirements.txt and pip

```bash
pip install -r requirements.txt
```

After installing the dependencies, it's neccesary to create the .env file which will contain all the configuration neccesary to start up the application.

Theres an EXAMPLE.env which contain an example of the required fields

```bash
TRELLO_API_KEY=0595dd8f6f
TRELLO_TOKEN=ATTAe5309a764b477f9def11e038b8bADC98F6C
TRELLO_BOARD_ID=d8f6d8f6d8f6
TRELLO_LIST_NAME=ToDo
```


## Documentation

Here's a secuence diagram about how the different clases on the app interects to acchieve the green path of one of the use cases:

[insert image here]

Theres three entities that this application handles properly:

1. An issue: This represents a business feature that needs implementation, they will provide a short title and a description.

2. A bug: This represents a problem that needs fixing. They will only provide a description, the title needs to be randomized with the following pattern: bug-{word}-{number}. It doesn't matter that they repeat internally. The bugs should be assigned to a random member of the board and have the “Bug” label.

3. A task: This represents some manual work that needs to be done. It will count with just a title and a category (Maintenance, Research, or Test) each corresponding to a label in trello. 

All entities are created trhough the same endpoint (the root endpoint)

[insert image of the payloads]

## Atention

Is mandatory to have at least one list on trello named "ToDo" in the targeted board, otherwise it will throw an exception.