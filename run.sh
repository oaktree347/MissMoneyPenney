docker run -d -it --name $1 -v "$PWD":/usr/src/legobot -w /usr/src/legobot python:3 sh -c 'pip install -r requirements.txt && python chatbot.py'
