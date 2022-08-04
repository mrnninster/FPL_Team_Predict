# imports
import logging

from black import json
from typing import Optional, List
from config import LogConfig,Settings
from logging.config import dictConfig
from fastapi import APIRouter, Depends
from routers.routeModels import CreatePlayer
from concurrent.futures import ThreadPoolExecutor
from fastapi.security import HTTPBasicCredentials,HTTPBearer
from utils.db_utils import saveNewPlayer, updatePlayer, requestPlayerList, check_id, deletePlayer, playersPick

# App Settings
settings = Settings()

# App Logging
dictConfig(LogConfig().dict())
logger = logging.getLogger("Engine")

router = APIRouter()
router = APIRouter(prefix="/api", responses={404: {"description": "Not found"}})

positions_array = ["defender","midfielder","forward"]
skills_array = ["defense","attack","speed","strength","stamina"]

# authorization scheme
security = HTTPBearer()

# Check Health
@router.get("/health")
async def health():
    return {"status": "ok"}


# Create Player
@router.post("/create_player")
async def create_player(new_player: CreatePlayer) -> dict:
    try:

        if new_player.name == "":
            return {"message": f"invalid value for name:{new_player.name}. Player name cannot be empty."}

        if new_player.position == "":
            return{"message": f"invalid value for position:{new_player.position}. Player position can't be empty"}

        if new_player.position not in positions_array:
            return{"message": f"invalid value for position:{new_player.position}. Player position needs to be one of {positions_array}"}

        i = 0
        while i < len(new_player.playerSkills):
            curSkillKeys = list(new_player.playerSkills[i].keys())

            if (new_player.playerSkills[i] == {}) or (len(curSkillKeys) < 1):
                return {"message": f"invalid value for playerskill:{new_player.playerSkills[i]}. Player skill can't be empty."}

            elif ("skill" not in curSkillKeys):
                return {"message":f"invalid value for playerskill: {new_player.playerSkills[i]}. Player skill is missing"}

            elif (new_player.playerSkills[i]["skill"] not in skills_array):
                return {"message": f"invalid value for skill:{new_player.playerSkills[i]['skill']}. Player skill needs to be one of {skills_array}"}

            elif new_player.playerSkills[i]["skill"] in skills_array:
                i += 1

            else:
                return {"message": f"uncaught error for playerskill:{new_player.playerSkills[i]}."}

        # Save Player
        save = saveNewPlayer(new_player)
        save.savePlayer()
        save.getPlayerID()
        save.savePlayerSkills()
        response = save.getPlayerInfo()
        return response
    
    except Exception as e:
        logger.exception(e)
        return {"message": f"uncaught error:{e.__class__}:{e}"}


# Update Player 
@router.post("/update_player/{player_id}")
async def update_player(player_id:str, updateData: CreatePlayer) -> dict:

    try:
        # Perform Data Checks
        if updateData.name == "":
            return {"message": f"invalid value for name:{updateData.name}. Player name can't be empty."}

        if updateData.position == "":
            return{"message": f"invalid value for position:{updateData.position}. Player position can't be empty"}

        if updateData.position not in positions_array:
            return{"message": f"invalid value for position:{updateData.position}. Player position needs to be one of {positions_array}"}

        i = 0
        while i < len(updateData.playerSkills):
            curSkillKeys = list(updateData.playerSkills[i].keys())

            if (updateData.playerSkills[i] == {}) or (len(curSkillKeys) < 1):
                return {"message": f"invalid value for playerskill:{updateData.playerSkills[i]}. Player skill can't be empty."}

            elif ("skill" not in curSkillKeys):
                return {"message":f"invalid value for playerskill: {updateData.playerSkills[i]}. Player skill is missing"}

            elif (updateData.playerSkills[i]["skill"] not in skills_array):
                return {"message": f"invalid value for skill:{updateData.playerSkills[i]['skill']}. Player skill needs to be one of {skills_array}"}

            elif (updateData.playerSkills[i]["skill"] in skills_array):
                i += 1

            else:
                return {"message": f"uncaught error for playerskill:{updateData.playerSkills[i]}."}
                
        # If Checks are Passed, Check If Player ID is valid
        validity_status= check_id(player_id)
        
        if validity_status == True:
                        
            # Update Player If Player Is Valid
            update = updatePlayer(player_id,updateData)
            update.updatePlayer()
            response = update.getPlayerInfo()
            return response
            
        else:
            return {"message": f"invalid value for player_id:{player_id}. Player ID is not valid"}
    
    except Exception as e:
        logger.exception(e)
        return {"message": f"uncaught error:{e.__class__}:{e}"}


#  Get Single Player
@router.get("/get_player/{player_id}")
async def get_player(player_id:str) -> dict:
    try:
        # Check If Player ID is valid
        validity_status= check_id(player_id)
        
        if validity_status == True:
            # Get Player Info
            SinglePlayer = requestPlayerList(player_id)
            response = SinglePlayer.fetchSinglePlayer()
            return response
        else:
            return {"message": f"invalid value for player_id:{player_id}. Player ID is not valid"}
    
    except Exception as e:
        logger.exception(e)
        return {"message": f"uncaught error:{e.__class__}:{e}"}


# List All Players
@router.get("/list_players")
async def list_players() -> dict:
    try:
        playerList = requestPlayerList()
        response = playerList.fetchSinglePlayer()
        return response
    except Exception as e:
        logger.exception(e)
        return {"message": f"uncaught error:{e.__class__}:{e}"}


def _authorized(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials
    return token


# Delete Player
@router.get("/delete_player/{player_id}")
async def player_delete(player_id: str, token: str = Depends(_authorized)) -> dict: 
    
    # Verify Bearer Token
    app_token = settings.app_bearer_token

    if app_token == token:
        # Validate Player Exists
        validity_status = check_id(player_id)

        if validity_status == True:
            response = deletePlayer(player_id)
            return response
        
        else:
            return {"message": f"Invalid value for player_id:{player_id}"}
    else:
        return {"message": "Access Denied, Unauthorised."}


# Team Selection
@router.post("/create_team")
async def create_team(team_specification: list) -> list:

    treated_positions: dict = {}
    team_list: list = []
    
    # Create Team
    for specification in team_specification:

        # Perform Data Checks
        if specification["position"] not in positions_array:
            return{"message": f"invalid value for position:{specification['position']}. Player position needs to be one of {positions_array}"}

        if specification["mainSkill"] not in skills_array:
            return {"message": f"invalid value for mainSkill:{specification['mainSkill']}. Player skill needs to be one of {skills_array}"}

        if (specification["position"] in treated_positions.keys()) and (specification["mainSkill"] != treated_positions[specification["position"]]):
            return {"message": f"Invalid team selection request, multiple skills requested for position: {specification['position']}."}

        elif (specification["position"] in treated_positions.keys()):
            return {"message": f"Invalid team selection request, repeated position: {specification['position']}"}
        
        else:
            treated_positions[specification["position"]] = specification["mainSkill"]
            with ThreadPoolExecutor() as executor:
                exec_response = executor.submit(
                    playersPick,
                    specification["position"], 
                    specification["mainSkill"], 
                    specification["numberOfPlayers"]
                    )
            players = exec_response.result()
            
            for player in players:
                if "ErrorMessage" in player.keys():
                    return {"message": player["ErrorMessage"]}
                else:
                    team_list.append(player)
    return team_list

