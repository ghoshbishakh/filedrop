API / Protocol / Data Formats for LAN-Chat
==========================================

##The following are the request and response formats for LAN-chat:
+ All data are sent and recieved in *JSON* format.
+ The action or command is specified by the *usage* string.
+ The *data* string or object or array contains all data sent or recieved.

###Get a list of connected users
    {
        "usage":"getList"
    }

#### Response:
    {
        "usage": "userList"
        "data": ["user1", "user2","like this.."]
    } 

###Send message to all users (shout)
    {
        "usage":"shout"
        "data":"Your Message Here"
    }
    
###Send private message to specific user (whisper)
    {
        "usage":"whisper"
        "data":{
                    "to":"username of the user"
                    "message":"Your Message Here"
               }
    }


###Recieve a broadcast (shout)
    {
        "usage":"shout"
        "data":{
                    "from":"username"
                    "message":"Shout Message Here"
               }
    }
###Recieve a private message
    {
        "usage":"whisper"
        "data":{
                "from":"username of the user"
                "message":"Your Message Here"
               }
    }        
