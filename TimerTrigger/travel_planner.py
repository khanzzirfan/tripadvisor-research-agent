# travel_planner.py
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.tools import Tool
from typing import Dict, Any
import logging

def create_agents():
    """Create and return the agents needed for travel planning."""
    serper_tool = SerperDevTool()

    agents = {
        "city_selection_expert": Agent(
            role="City Selection Expert",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            goal="Select the best city based on weather, season, and prices",
            verbose=True,
            allow_delegation=True,
            tools=[serper_tool]
        ),
        "local_expert": Agent(
            role="Local Expert",
            backstory="A knowledgeable local guide with extensive information about the city",
            goal="Provide the BEST insights about the selected city",
            verbose=True,
            allow_delegation=True,
            tools=[serper_tool]
        ),
        "travel_concierge": Agent(
            role="Travel Concierge",
            backstory="Specialist in travel planning and logistics with decades of experience",
            goal="Create amazing travel itineraries with budget and packing suggestions",
            allow_delegation=False,
            verbose=True,
            tools=[serper_tool]
        )
    }
    
    return agents

def create_tasks(agents: Dict[str, Agent], input_data: Dict[str, Any]) -> list:
    """Create tasks for the travel planning crew."""
    task_descriptions = {
        "city_selection": """
            Analyze and select the best city for the trip based on specific criteria.
            Consider weather patterns, seasonal events, and travel costs.
            Compare multiple cities, current weather conditions, upcoming events, and expenses.
            
            Your final answer must be a detailed report including:
            - Chosen city justification
            - Flight costs
            - Weather forecast
            - Key attractions
            
            Traveling from: {origin}
            City Options: {cities}
            Trip Date: {range}
            Traveler Interests: {interests}
        """,
        "local_guide": """
            Create an in-depth local guide for the selected city including:
            - Key attractions and hidden gems
            - Local customs and cultural insights
            - Special events during the visit
            - Daily activity recommendations
            - Weather forecasts
            - Cost estimates
            
            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}
        """,
        "travel_plan": """
            Create a detailed 7-day travel itinerary including:
            - Daily schedule with specific places and activities
            - Restaurant recommendations with reasons
            - Hotel suggestions
            - Weather-appropriate packing list
            - Detailed budget breakdown
            
            Format as markdown with clear sections.
            Include why each place was chosen and what makes it special.
            
            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}
        """
    }

    tasks = [
        Task(
            description=task_descriptions["city_selection"].format(**input_data),
            agent=agents["city_selection_expert"]
        ),
        Task(
            description=task_descriptions["local_guide"].format(**input_data),
            agent=agents["local_expert"]
        ),
        Task(
            description=task_descriptions["travel_plan"].format(**input_data),
            agent=agents["travel_concierge"]
        )
    ]
    
    return tasks

def create_travel_plan(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a travel plan based on the input data.
    
    Args:
        input_data (dict): Dictionary containing travel parameters
        
    Returns:
        dict: The complete travel plan
    """
    try:
        # Create agents and tasks
        agents = create_agents()
        tasks = create_tasks(agents, input_data)
        
        # Create and configure the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process="sequential",
            verbose=True,
            memory=False,
            cache=True,
            max_rpm=1000
        )
        
        # Execute the travel planning process
        result = crew.kickoff(inputs=input_data)
        
        return {"status": "success", "travel_plan": result}
        
    except Exception as e:
        logging.error(f"Error creating travel plan: {str(e)}")
        return {"status": "error", "message": str(e)}