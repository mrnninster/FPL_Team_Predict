# Import declarative base
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey, create_engine, select
from sqlalchemy.orm import declarative_base, relationship, Session

# Create DB Connection Sessio
def db_create_session():
    # Create Connection Engine
    engine = create_engine("sqlite:///fpl.db",echo=True)

    # Make session
    session_maker = Session(bind=engine)

    return session_maker

# Create An Instance Of Declarative Base
Base = declarative_base()

# Database Models
class Player(Base):
    __tablename__ = "player"

    id = Column(String, unique=True, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    team = Column(String, nullable=True, default="Not Speified")
    created = Column(DateTime, nullable=False)
    skills = relationship("Skill")

    def __repr__(self):
        return f"<Player {self.id}>"

    def dict(self):
        return(
            {
                "id": self.id,
                "name": self.name,
                "position": self.position,
                "playerSkills": [skill.dict() for skill in self.skills]
            }
        )


class Skill(Base):
    __tablename__ = "skill"

    owner_id = Column(String, ForeignKey("player.id"))
    id = Column(String, nullable=False, primary_key=True, unique=True)
    skill = Column(String, nullable=False)
    skill_rating = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<skill {self.id}>"

    def dict(self):
        return(
            {
                "id": self.id,
                "skill": self.skill,
                "rating": self.skill_rating
            }
        )