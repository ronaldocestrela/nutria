from typing import List, Optional
from tinydb import Query
from datetime import datetime
from base_repository import BaseRepository
from models import Report

class ReportRepository(BaseRepository):
    def __init__(self) ->  None:
        super().__init__()
        self.report_table = self.get_table('reports')
    
    def create_report(self, user_id: int, content: str) -> Report:
        """
        Create a new report.
        """
        new_report = Report(
            user_id=user_id,
            content=content
        )
        
        self.report_table.insert(new_report.model_dump())
        return new_report
    
    def get_reports_by_user_and_date(self, user_id: int, date: datetime) -> List[Report]:
        """
        Get reports by user ID and date.
        """
        start_date = datetime.combine(date.date(), datetime.min.time())
        end_date = datetime.combine(date.date(), datetime.max.time())
        
        ReportQuery = Query()
        results = self.report_table.search(
            (ReportQuery.user_id == user_id) & 
            (ReportQuery.generated_at >= start_date) &
            (ReportQuery.generated_at <= end_date)
        )
        
        return [Report(**report) for report in results] if results else []
    
    def delete_report(self, report_id: int) -> None:
        """
        Delete a report by ID.
        """
        ReportQuery = Query()
        self.report_table.remove(ReportQuery.id == report_id)
        return None
    
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """
        Get a report by ID.
        """
        ReportQuery = Query()
        result = self.report_table.get(ReportQuery.id == report_id)
        
        return Report(**result) if result else None
    
    def get_all_reports(self) -> List[Report]:
        """
        Get all reports.
        """
        results = self.report_table.all()
        
        return [Report(**report) for report in results] if results else []