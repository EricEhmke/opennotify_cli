#Open Notify CLI#

## Description
A simple CLI and python wrapper for the Open-Notify API. This CLI returns the current position of 
the ISS along with information about current astronauts and their spacecrafts.


## Usage
Clone this git repo and run `cli.py` from the command line.

Available commands:
- `loc` : Get the current coordinates for the ISS
- `people` : Get the names of people currently in space, along with the spacecraft they are on.  
- '-h': View help
    
## Original Prompt 
Implement a Python script that will accept the following command-line arguments, along with any required information, and print the expected results.  Please also use python data-classes to create a python native interface for the responses from the api.

    loc 

        print the current location of the ISS
        Example: “The ISS current location at {time} is {LAT, LONG}”

    people 

        for each craft print the details of those people that are currently in space
        Example: “There are {number} people aboard the {craft}. They are {name[0]}…{name[n]}”

 


Sometimes the open-notify API will have some endpoints that are not available due to load, your application should be able to handle this case and you can use some mock data to show how it would work 

 

For location the following would be some mock data from the api:

 

`{“message”:  “success”, “timestamp”: 123456789, “iss_position”: {“longitude”: “-10.1234”, “latitude”: “31.41592”}}`

 

For the current crew on the iss, an example might be:

 

`{“message”: “success”, “number”: 4, “people”: [{“name”: “James Tiberius Kirk”, “craft”: “NCC-1701”}, {“name”: “Chris Hadfield”, “craft”: “ISS”}, {“craft”: “NCC-1701”, “name”: “S’chn T’gai Spock”}, {“name”: “Hikaru Kato Sulu”}]}`

## Assumptions and Implementation Questions
These are question I would have asked during the design phase to clarify ambiguous requirements.

- "Implement a Python script that will accept the following command-line arguments":
    - Does this CLI need to accept multiple arguments at one or just one at a time? I opted to design the CLI to only
    accept a single argument at a time in order to simplify the output. It is easier to parse a single result and run 
    the application a second time than to assume the consumer will have the ability to parse multiple results.
    
    Processing multiple args at a time would be a good use case for async requests or at least an interesting exercise.
- "...along with any required information..."
    - This prompt asked for the ability to submit required information, but no other information is required to fulfill 
    the design requirements. The ability to supply & process flags could be easily added with argeparse and the existing
    router.    
