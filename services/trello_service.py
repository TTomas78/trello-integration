from services.http_handler_service import HTTPHandlerService


import requests

class TrelloService():
    instance=None

    def __init__(self, api_key, token, trello_board_id, list_name)-> "TrelloService":
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
        board_ids = self.get_boards()

        if trello_board_id in board_ids:
            self.board_id = trello_board_id
        else:
            raise Exception("Trello board id is not valid")
        
        self.list_id = self.get_list_id(list_name)

    @classmethod
    def get_or_create(cls,api_key=None, token=None, trello_board_id=None, list_name=None)-> "TrelloService":
        """
        This method is used to create a singleton of the TrelloService,
        this way we can avoid creating multiple instances of the service
        """
        if cls.instance is None:
            cls.instance = TrelloService(api_key, token, trello_board_id, list_name)
        return cls.instance

    def get_board_valid_members(self, board_id) -> list[dict]:
        """
        Request the valid members of a board (not deactivated)

        """
        response = HTTPHandlerService.request('GET',f"{self.base_url}/boards/{self.board_id}/memberships",headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token})
        data = response.json()
        valid_members = [member.get('idMember') for member in data if not member.get("deactivated", False)]
        return valid_members

    def get_boards(self) -> list[str]:
        """
        Request the valid boards for the user who provided the autentication
        """
        response = HTTPHandlerService.request('GET',f"{self.base_url}/members/me",headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token})
        data = response.json()
        try:
            return data["idBoards"]
        except KeyError:
            raise Exception("cannot get the boards from Trello")

    def get_list_id(self, list_name) -> str:
        """
        Given a list name returns the specific list id
        """
        lists = self.get_board_lists()
        for list in lists:
            if list["name"] == list_name:
                return list["id"]
        raise Exception("List not found")
        

    def get_board_labels(self) -> list[dict]:
        """
        Get the board labels
        """
        response = HTTPHandlerService.request('GET',f"{self.base_url}/boards/{self.board_id}/labels",headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token})
        data = response.json()
        return data

    def create_label(self, name, color=None):
        """
        Create a label in the board
        """
        label_info = {
            "name": name,
            "color": '' if color is None else color
        }

        response = HTTPHandlerService.request('POST',f"{self.base_url}/boards/{self.board_id}/labels",headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token, **label_info})
        data = response.json()
        return data["id"]

    def get_or_create_label(self, name, color=None):
        """
        Returns the label id if the label exists, if not it creates the label and returns the id
        """
        labels = self.get_board_labels()
        for label in labels:
            if label["name"] == name:
                return label["id"]
        return self.create_label(name, color)
        

    def create_card(self, card) -> dict:
        """
        Create a new card in the board
        }"""
        response = HTTPHandlerService.request('POST',f"{self.base_url}/cards",headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token, **card})
        data = response.json()
        return data


    def get_board_lists(self):
        """
        Expected response structure
        [
            {
                "id": "5abbe4b7ddc1b351ef961414",
                "name": "Things to buy today",
                "closed": true,
                "pos": 2154,
                "softLimit": "<string>",
                "idBoard": "<string>",
                "subscribed": true,
                "limits": {
                "attachments": {
                    "perBoard": {}
                    }
                }
            }
        ]
        """
        response = HTTPHandlerService.request('GET',f"{self.base_url}/boards/{self.board_id}/lists", headers={'Accept': 'application/json'}, params={"key": self.api_key, "token": self.token})
        data = response.json()
        return data

    


