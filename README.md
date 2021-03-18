## Project Setup

poetry new ocr

poetry env use python3

poetry add fastapi

poetry env list

poetry env show

poetry show --tree

https://www.youtube.com/watch?v=JC5q22g3yQM&list=RDCMUCbsI5Rw9_yLccfoMEYYxDCg&start_radio=1&t=446

https://github.com/SouravJohar/ocr-tool/blob/main/templates/index.html


## Virtual Env

/Users/colm/Library/Caches/pypoetry/virtualenvs/coacher-w_mNJxVv-py3.8

### Dependencies

fastapi
uvicorn
sqlalchemy
jinja2

## Application Requirements

1. Add a Player with first name, last name, date of birth, school, address, a "1 to many" relationship with Guardians
1. Add a Guardian with first name, last name, mobile number, a "1 to many" relationship with Players

## Technical Requirements

1. Use Poetry to manage dependencies
1. Use fastAPI to build api
1. Use https://semantic-ui.com/ for UI
1. Use Async where possible
1. Build functionality as a library that can be imported
1. Front end tests to be built with pylenium
