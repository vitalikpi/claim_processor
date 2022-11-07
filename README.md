# be_assessment

## Task
Your task is to create a dockerized service, **claim_process**  to process claims. 

## Requirements
1. **claim_process** transforms a JSON payload representing a single claim input with multiple lines and stores it into a RDB.
   - An example payload (note that this  in CSV format) is provided under transform/sample (note that the names are not consistent in capitalization).
2. **claim_process** generates a unique id per claim
3. **claim_process** computes the *“net fee”* as a result per the formula below.
*“net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”* (note that the names are not consistent in capitalization).
4. A downstream service, **payments**, will consume *“net fee”* computed by claim_process


## Task Instructions
1. You’re free to choose any python compatible framework as you see fit: FastApi, Django, Flask.
2. Use sqlite as a db. Use an ORM of your choice - SQLModel/Sqlalchemy/Tortoise.
3. Please add data validation for *“submitted procedure”* and *“Provider NPI”* columns. *“Submitted procedure”* always begins with the letter ‘D’ and *“Provider NPI”* is always a 10 digit number. The data validation should be flexible to allow for other validation rules as needed.
4. Write pseudo code or comments in your code to indicate how **claim_process** will communicate with **payments**. There are multiple choices here but make reasonable assumptions based on:
   - What needs to be done if there is a failure in either service and steps need to be unwinded.
   - Multiple instances of either service are running concurrently to handle a large volume of claims.
