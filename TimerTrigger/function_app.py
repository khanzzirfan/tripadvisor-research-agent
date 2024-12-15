# function_app.py
import azure.functions as func
import logging
from dotenv import load_dotenv
import json
from travel_planner import create_travel_plan

# Load environment variables
load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.timer_trigger(schedule="0 0 */1 * * *", arg_name="myTimer") # Run once every hour
def travel_planner_trigger(myTimer: func.TimerRequest) -> None:
    try:
        if myTimer.past_due:
            logging.info('The timer is past due!')

        # Example input data - in production, this could come from a queue or database
        input_data = {
            "origin": "Sydney",
            "cities": ["Gold Coast", "Queensland"],
            "range": "10-JAN-2025 15-Jan-2025",
            "interests": ["beach", "culture", "food"]
        }

        # Process the travel plan
        result = create_travel_plan(input_data)
        
        # Log the result
        logging.info(f'Travel plan created successfully: {json.dumps(result, indent=2)}')
        
    except Exception as e:
        logging.error(f'Error in travel planner function: {str(e)}')
        raise