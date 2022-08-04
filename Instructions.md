<!-- Project Name -->
# PLAYER TEAM GENERATOR WEBAPI
Web api solution for selecting the best team of players.
The app needs to be served at http://localhost:3000 and 
the API requests should be available at http://localhost:3000/api/.

<!-- INSTRUCTIONS -->
## INSTRUCTIONS
- Host at port 3000
- Build an API that will manage players with some skills and select the best players with the desired position/skill.
    - add
    - update
    - list
    - delete

- The players will need to have
    - name
    - position
    - list of skills
 
- The available positions for players are:
    - defender
    - midfielder
    - forward
    
- The skill will have:
    - skill name
    - value
    
- The available skills for a player are:
    - defense
    - attack
    - speed
    - strength
    - stamina
 
- The player needs to have at least one skill
- The player does not need to have values for all available skills.
- Valid player in JSON data is
    ``` 
    {
        "name": "player name",
        "position": "midfielder",
        "playerSkills": [
            {
                "skill": "defense",
                "value": 60
            },
            {
                "skill": "speed",
                "value": 80
            }
        ]
    }
    ```

## API REQUIREMENTS
* Error Response
    * In case of errors, the body should return the correct error message
        - if the skill "defenese" inside "playerskills" array has an error the error response should contain both the skill and the invalid input the error response 
        following this pattern:
            ```
            {
                "message": "Invalid value for position: midfielder1"
            }
            ```


        - if the field with invalid input and the invalid input data is midfielder1, the error response should follow this pattern:
            ```
            {
                "message": "Invalid value for position: midfielder1"
            }
            ```

    * The solution should return only the first error found. 
    * If the request to create the player has invalid values for position and skill fields, the solution should return only the message for one of those fields. The validation rules do not need to follow any specific order.

* Routes
    * CREATE PLAYER (http://localhost:3000/api/create_player)
        * The request should contain the player data in json format, sample:
            ```
            {
                "name": "player name 2",
                "position": "midfielder",
                "playerSkills": [
                    {
                        "skill": "attack",
                        "value": 60
                    },
                    {
                        "skill": "speed",
                        "value": 80
                    }
                ]
            }
            ```
        * The response should contain player data and additional identification properties, sample:
            ```
            {
                "id": 1,
                "name": "player name 2",
                "position": "midfielder",
                "Team": "Not Specified",
                "playerSkills": [
                    {
                        "id": 1,
                        "skill": "attack",
                        "value": 60,
                        "playerId": 1
                    },
                    {
                        "id": 2,
                        "skill": "speed",
                        "value": 80,
                        "playerId": 1
                    }
                ]
            }
            ```

    * UPDATE PLAYER (http://localhost:3000/api/update_player/{player_id})
        * The request should contain player data in json format
            ```
            {
                "name": "player name updated",
                "position": "midfielder",
                "Team": "Not Specified",
                "playerSkills": [
                    {
                        "skill": "strength",
                        "value": 40
                    },
                    {
                        "skill": "stamina",
                        "value": 30
                    }
                ]
            }
            ```
        * The response should contain updated user data in json format
            ```
            {
                "id": 1,
                "name": "player name updated",
                "position": "midfielder",
                "Team": "Not Specified",
                "playerSkills": [
                    {
                        "id": 3,
                        "skill": "strength",
                        "value": 40,
                        "playerId": 1
                    },
                    {
                        "id": 4,
                        "skill": "stamina",
                        "value": 30,
                        "playerId": 1
                    }
                ]
            }
            ```
    
    * LIST PLAYERS (http://localhost:3000/api/list_players)
        * This returns a json response containing the list of all the players
        in the database
            ```
            [
                {
                    "id": 1,
                    "name": "player name 1",
                    "position": "defender",
                    "Team": "Not Specified",
                    "playerSkills": [
                        {
                            "id": 1,
                            "skill": "defense",
                            "value": 60,
                            "playerId": 1
                        },
                        {
                            "id": 2,
                            "skill": "speed",
                            "value": 80,
                            "playerId": 1
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "player name 2",
                    "position": "midfielder",
                    "Team": "Not Specified",
                    "playerSkills": [
                        {
                            "id": 3,
                            "skill": "attack",
                            "value": 20,
                            "playerId": 2
                        },
                        {
                            "id": 4,
                            "skill": "speed",
                            "value": 70,
                            "playerId": 2
                        }
                    ]
                }
            ]
            ```

    * LIST TEAM PLAYERS (http://localhost:3000/api/view_players/{team})
        * This returns a json response containing the list of all the players
        in the database that belong to the specified team
            ```
            [
                {
                    "id": 1,
                    "name": "player name 1",
                    "position": "defender",
                    "Team": "Team A",
                    "playerSkills": [
                        {
                            "id": 1,
                            "skill": "defense",
                            "value": 60,
                            "playerId": 1
                        },
                        {
                            "id": 2,
                            "skill": "speed",
                            "value": 80,
                            "playerId": 1
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "player name 2",
                    "position": "midfielder",
                    "Team": "Team A",
                    "playerSkills": [
                        {
                            "id": 3,
                            "skill": "attack",
                            "value": 20,
                            "playerId": 2
                        },
                        {
                            "id": 4,
                            "skill": "speed",
                            "value": 70,
                            "playerId": 2
                        }
                    ]
                }
            ]
            ```

    * DELETE PLAYER (http://localhost:3000/api/delete_player/{player_id})
        * route is protected by bearer token using authorization header
        * The value of the Authorization Header should be: Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE= 

    * TEAM SELECTION (http://localhost:3000/api/create_team)
        * This selects players out of all the players in the database 
        based on some parameters sent in the request.
        * The sample request is shown below 
            ```
            [
                {
                    "position": "midfielder",
                    "mainSkill": "speed",
                    "numberOfPlayers": 1
                },
                {
                    "position": "defender",
                    "mainSkill": "strength",
                    "numberOfPlayers": 2
                }
            ]  
            ```
        * A sample response to this request would be json response
            ```
            [
                {
                    "name": "player name 2",
                    "position": "midfielder",
                    "playerSkills": [
                        {
                            "skill": "speed",
                            "value": 90
                        }
                    ]
                },
                {
                    "name": "player name 3",
                    "position": "defender",
                    "playerSkills": [
                        {
                            "skill": "strength",
                            "value": 50
                        }
                    ]
                },
                {
                    "name": "player name 4",
                    "position": "defender",
                    "playerSkills": [
                        {
                            "skill": "strength",
                            "value": 37
                        }
                    ]
                }
            ]
            ```
    * TEAM SELECTION 2 (http://localhost:3000/api/fpl_team_create)
        * This selects players out of all the players in the database 
        belonging to the requested teams based on some parameters sent
        in the request.
        * The sample request is shown below 
            ```
            [   {
                    "Teams": [
                        "Team A",
                        "Team B",
                        "Team C",
                    ],
                },
                {
                    "position": "midfielder",
                    "mainSkill": "speed",
                    "numberOfPlayers": 1
                },
                {
                    "position": "defender",
                    "mainSkill": "strength",
                    "numberOfPlayers": 2
                }
            ]  
            ```
        * A sample response to this request would be json response
            ```
            [
                {
                    "name": "player name 2",
                    "position": "midfielder",
                    "Team": "Team A",
                    "playerSkills": [
                        {
                            "skill": "speed",
                            "value": 90
                        }
                    ]
                },
                {
                    "name": "player name 3",
                    "position": "defender",
                    "Team": "Team B",
                    "playerSkills": [
                        {
                            "skill": "strength",
                            "value": 50
                        }
                    ]
                },
                {
                    "name": "player name 4",
                    "position": "defender",
                    "Team": "Team B",
                    "playerSkills": [
                        {
                            "skill": "strength",
                            "value": 37
                        }
                    ]
                }
            ]
            ```
* Team Selection Rules
    * Given a position and the skill desired for that position, the app should be able to find the best player in the database with that skill and position.
    If there are more than one player with the highest skill value, the solution can select any of those players.
    
    * The request should allow only one skill per position. The same skill can be used in different positions. For example: you cannot send a request for defender with highest speed and defense skill.

    * The position of the player should not be repeated in the request. For example: you cannot ask for defender with highest speed, and defender with highest strength in the same request.

    * If there are no players in the database with the desired skill, the app should find the highest skill value for any players in the selected position. For example, if in the database we have 3 defenders with these skills:
        * player 1 has {speed: 90}
        * player 2 has {strength: 20}
        * player 3 has {stamina: 95}

        And the requirements ask for a defender with defense skill, the app should select player 3, because there are no defenders with defense skill, and the defender with highest skill value is player 3. The same rule should be applied if the player has multiple skills, so if we have in the database the following players:
        
        * player 1 has {stamina: 90, speed: 100, strength: 20}
        * player 2 has {stamina: 80, speed: 80, strength: 80}
        * player 3 has {stamina: 95, speed 90, strength: 50}

        And the requirements specify a defender with defense skill, the app should select player 1, because it is the player with highest skill: speed 100.
    
    * The app should always fill the number of required players with the correct position. For example, if the requirement is for 2 defenders, the app should find the best 2 defenders with the desired skill and use rule number 4 if there are no available defenders with the desired skill.

    * The app should return an error if there are no available players in the required position. For example, if the request requires 2 defenders and there is only one defender in the database, the app should return an error with the message: “Insufficient number of players for position: defender”. This rule should only be applied for positions. The skill requirement should follow the rules described in point 4.
    