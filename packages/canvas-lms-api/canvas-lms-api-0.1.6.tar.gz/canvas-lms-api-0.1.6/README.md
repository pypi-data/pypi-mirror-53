# Installation
This will be updated with the "formal" pypi repo eventually, but for now it's located here.

    python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ canvas-lms-api

Alternatively, you can download the source code and pip install from that:

    git clone https://github.gatech.edu/omscs-ta/canvas-lms-api
    cd canvas-lms-api
    pip install .

# Usage:
## Get Canvas Token
Found here: Canvas > Account > Settings > Approved Integrations: > New Access Token.

## Get Course Number
There are really 2 ways. 
1. Use this tool to find all the courses and then use the number below (cours is optional so you can set it later)
2. Login to canvas
    * Go to your course
    * eg: https://gatech.instructure.com/courses/46234
    * The value for canvas_course is "46234"


## Get Assignments Example

````
from canvas_lms_api import Canvas
grader = Canvas(base="https://gatech.instructure.com", token=YOUR TOKEN, course=Your Course Number)
grader.GetAssignments()
````
