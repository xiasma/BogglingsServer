*******Do once:
In the AWS account, you need to create DynamoDB tables:

BogglingsGames
    partition key: gameId
    sort key: turnIndex

BogglingsPlayers
    partition key: playerId

BogglingsPlayerTurns
    partition key: playerTurnId
    sort key: turnId

BogglingsTurns
    partition key: turnId
    sort key: turnIndex

In AWS IAM
create a user called BogglingsUser

Add permissions polices
    AmazonDynamoDBFullAccess
    AmazonDynamoDBFullAccess_v2
    AmazonDynamoDBFullAccesswithDataPipeline
    AmazonDynamoDBReadOnlyAccess



On your computer:

Install python - I'm using 3.13.3 so ideally use the same version.
Install VSCode
In VSCode, from the Terminal menu, New Terminal
In the terminal, enter
    pip install --upgrade pip
    python -m venv venv

Create a folder ".aws" and in it, create a file "credentials"
[default]
aws_access_key_id=********************
aws_secret_access_key=****************************************
region=sa-east-1

Populate it with the details of your AWS account.


*******Each time you load the project in VSCode:
In VSCode, from the Terminal menu, New Terminal
In the terminal, enter
    ./venv/Scripts/Activate.ps1
    git pull
    pip install -r requirements.txt

********To run the code:
Open the "app.py" file in VSCode
Hit F5 or go to the Run menu and Start Debugging.  Use the defaults of anything it offers.




---------------------------------------
The code:

game_objects.py contains the classes that define the data structures.
If you want to extend or change any of these, you will need to 
-extend/change the corresponding method(s) in app.py
-extend/change the corresponding method(s) in repositories.py


repositories.py is the layer that talks to the database.
As the database is a "nosql" database (DynamoDb), it means its structure  doesn't need to be changed.
You simply the fields you want, and the new records will contain them.
BEWARE: if you add fields, they won't exist for records that already exist.
Note that in the "get_" methods, it is 
- getting the record
- then updating the "lastUpdated" value in the database
- then returning the record (with the value of lastUpdated previously retrieved, not the new value)


app.py
This is the web server.

.aws/credentials
Contains your AWS connection secrets.  Looks like this:
[default]
aws_access_key_id=********************
aws_secret_access_key=****************************************
region=sa-east-1


---------------------------------------
My understanding of Bogglings server.

The game (Bogglings) needs to pass a string to define state.  This string is called "turnState" in the class turnState

