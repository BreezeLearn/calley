# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from cal import main
from cal2 import api
from typing import Optional, Type
import json


class CalenderTool(BaseTool):
    name = "Calender"
    description = "useful for when you need to fetch the events on my calendar"

    def _run(self, query: str):
        return api.list_calendars()

    async def _arun(self, query: str):
        raise NotImplementedError

    @property
    def _subcommand(self) -> str:
        return "cal"

    @property
    def _subcommand_description(self) -> str:
        return "useful for when you need to fetch the events on my calendar"


class ScheduleEvent(BaseModel):
    input_doc: str
    


class ScheduleEventTool(BaseTool):
    name = "Schedule_Event"
    description = "useful for when you need to schedule an event with Calender, Input should be a stringified JSON object of summary, description, start_date, end_date, attendee_email. ask the user to provide the input / these details about the event "
    args_schema: Type[BaseModel] = ScheduleEvent

    def _run(self, input_doc, verbose: bool = True):
        """use the tool"""
        input_doc = json.loads(input_doc)
        summary, description, start_date, end_date, attendee_email = input_doc['summary'], input_doc['description'], input_doc['start_date'], input_doc['end_date'], input_doc['attendee_email']
        return api.schedule_event('primary', summary, description, start_date, end_date, attendee_email, )

    async def _arun(self, query: str):
        raise NotImplementedError
