# imports
from audioop import reverse
import uuid
import logging

from config import LogConfig
from datetime import datetime
from logging.config import dictConfig
from utils.db_models import db_create_session, Player, Skill


dictConfig(LogConfig().dict())
logger = logging.getLogger("Engine")

# generate Unique User ID
def gen_uuid(_tablename: str):
    created_id = str(uuid.uuid4())
    new_session = db_create_session()

    with new_session as session:
        if _tablename == "player":
            response = session.query(Player).filter_by(id=created_id).first()

        elif _tablename == "skill":
            response = session.query(Skill).filter_by(id=created_id).first()

        if response != None:
            gen_uuid(_tablename)
        else:
            return created_id


# Check Player ID is Valid
def check_id(player_id: str):
    new_session = db_create_session()

    with new_session as session:
        response = session.query(Player).filter_by(id=player_id).first()

        if response != None:
            return True
        else:
            return False


def deletePlayer(player_id: str):
    new_session = db_create_session()

    with new_session as session:
        try:
            # Delete Skills
            skills = session.query(Skill).filter_by(owner_id=player_id).all()
            for skill in skills:
                session.delete(skill)
                session.commit()

            # Delete Player
            player = session.query(Player).filter_by(id=player_id).first()
            session.delete(player)
            session.commit()
        
        except Exception as e:
            logger.exception(e)


# Pick Player From Database For Team Selection
def playersPick(position: str, mainSkill: str, total_count: int) -> dict:
    Temp_team = {}
    new_session = db_create_session()
    
    # Select Players That Meet Specified Requirements 
    with new_session as session:

        # Query Db For Player With Specified Skill and Position
        skilledPlayerList = session.query(Player).filter_by(position=position).join(Player.skills).filter_by(skill=mainSkill).all()
        if skilledPlayerList != None:
        
            # Check If No Of Players Meet Required Total Count
            if len(skilledPlayerList) < total_count:
                return [{"ErrorMessage":f"InsufficientPlayerError: Insufficient players for position:{position}"}]
            
            else:
                # Process Request
                for x in skilledPlayerList:
                    skills = x.dict()["playerSkills"]
                    for skill in skills:
                        if skill["skill"] == mainSkill:
                            Temp_team[f"{skill['rating']}_{skill['id']}"] = x.dict()

                result = [Temp_team[j] for j in sorted(Temp_team.keys(), reverse=True)[:total_count]]
                return result

        # Select General Players That have requested Position
        else:
            generalPlayerList = session.query(Player).filter_by(position = position).all()
            if generalPlayerList == None:
                return [{"ErrorMessage": f"NoPlayerError: There are no players in specified position: {position}"}]

            elif(len(generalPlayerList) < total_count):
                return [{"ErrorMessage":f"InsufficientPlayerError: Insufficient players for position:{position}"}]

            else:
                # Process Request
                for x in generalPlayerList:
                    skills = x.dict()["playerSkills"]
                    skill_collection: list = []
                    for skill in skills:
                        skill_collection.append(skill['rating'])
                    Temp_team[f"{max(skill_collection)}_{skill['id']}"] = x.dict()
                
                result = [Temp_team[j] for j in sorted(Temp_team.keys(), reverse=True)[:total_count]]
                return result



# Save New Player
class saveNewPlayer:
    def __init__(self, player: dict):
        self.new_session = db_create_session()
        self.now_time = datetime.utcnow()
        self.player_id = None
        self.player = player

    def savePlayer(self):
        with self.new_session as session:
            newPlayer = Player(
                id=gen_uuid("player"),
                name=self.player.name,
                position=self.player.position,
                created=self.now_time,
            )
            session.add(newPlayer)
            session.commit()

    def getPlayerID(self):
        with self.new_session as session:
            getPlayer = (
                session.query(Player)
                .filter_by(
                    name=self.player.name,
                    position=self.player.position,
                    created=self.now_time,
                )
                .first()
            )
            self.player_id = getPlayer.id

    def savePlayerSkills(self):
        skills = self.player.playerSkills
        with self.new_session as session:
            for cur_skill in skills:
                if cur_skill != {}:
                    newSkill = Skill(
                        id=gen_uuid("skill"),
                        owner_id=self.player_id,
                        skill=cur_skill["skill"],
                        skill_rating=cur_skill["value"]
                        if "value" in list(cur_skill.keys())
                        else 0,
                        created=self.now_time,
                        updated=self.now_time,
                    )
                    session.add(newSkill)
                    session.commit()

    def getPlayerInfo(self):
        with self.new_session as session:
            getPlayer = session.query(Player).filter_by(id=self.player_id).first()
            return getPlayer.dict()


class updatePlayer:
    def __init__(self, player_id: str, updateData: dict) -> None:
        self.new_session = db_create_session()
        self.now_time = datetime.utcnow()
        self.player_id = player_id
        self.updateData = updateData
        self.updated = False
        self.playerData = None

    def updatePlayer(self):
        # Update Player Data
        with self.new_session as session:
            player = session.query(Player).filter_by(id=self.player_id).first()
            self.playerData = player.dict()

            updateSkills = self.updateData.playerSkills
            savedSkills = [skill for skill in self.playerData["playerSkills"]]

            player.name = self.updateData.name
            player.position = self.updateData.position
            player.team = (
                self.updateData.team
                if "team" in list(dict(self.updateData).keys())
                else "Not Specified"
            )
            session.commit()

            if len(updateSkills) > 0:
                for cur_skill in updateSkills:
                    if (cur_skill != {}) and ("skill" in list(cur_skill.keys())):

                        # Update Skill
                        for _skill in savedSkills:
                            if _skill["skill"] == cur_skill["skill"]:
                                fetchSkill = (
                                    session.query(Skill)
                                    .filter_by(
                                        owner_id=self.player_id, skill=_skill["skill"]
                                    )
                                    .first()
                                )
                                print(fetchSkill.dict())
                                fetchSkill.skill_rating = cur_skill["value"]
                                session.commit()
                                self.updated = True
                                break

                        # Write New Skill
                        if self.updated == False:
                            newSkill = Skill(
                                id=gen_uuid("skill"),
                                owner_id=self.player_id,
                                skill=cur_skill["skill"],
                                skill_rating=cur_skill["value"]
                                if "value" in list(cur_skill.keys())
                                else 0,
                                created=self.now_time,
                                updated=self.now_time,
                            )
                            session.add(newSkill)
                            session.commit()

                        # Reset Update Flag
                        self.updated = False

    def getPlayerInfo(self):
        with self.new_session as session:
            getPlayer = session.query(Player).filter_by(id=self.player_id).first()
            return getPlayer.dict()


class requestPlayerList:
    def __init__(self, player_id: str = None) -> None:
        self.new_session = db_create_session()
        self.player_id = player_id
        self.playerList = []

    def fetchSinglePlayer(self):
        with self.new_session as session:
            if self.player_id != None:
                getPlayer = session.query(Player).filter_by(id=self.player_id).first()
                self.playerList.append(getPlayer.dict())
            else:
                self.playerList = [player.dict() for player in session.query(Player).all()]
            
            return self.playerList
