from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field


class MeetingType(Enum):
    DEFECT_TRIAGE = "defect_triage"
    STEERCO = "steerco"
    WEEKLY_STATUS = "weekly_status"
    SPRINT_PLANNING = "sprint_planning"
    SPRINT_RETROSPECTIVE = "sprint_retrospective"
    SPRINT_REVIEW = "sprint_review"
    DAILY_STANDUP = "daily_standup"
    ARCHITECTURE_REVIEW = "architecture_review"
    CODE_REVIEW = "code_review"
    TECHNICAL_DESIGN = "technical_design"
    PRODUCT_ROADMAP = "product_roadmap"
    RELEASE_PLANNING = "release_planning"
    INCIDENT_POSTMORTEM = "incident_postmortem"
    PERFORMANCE_REVIEW = "performance_review"
    ONBOARDING = "onboarding"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    SECURITY_REVIEW = "security_review"
    DATABASE_REVIEW = "database_review"
    DEPLOYMENT_PLANNING = "deployment_planning"
    CAPACITY_PLANNING = "capacity_planning"


@dataclass
class MeetingAgenda:
    title: str
    description: str
    duration_minutes: int
    topics: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)


@dataclass
class Meeting:
    meeting_type: MeetingType
    title: str
    description: str
    participants: List[str]
    duration_minutes: int = 60
    agenda: Optional[MeetingAgenda] = None
    scheduled_time: Optional[datetime] = None
    location: str = "Virtual"
    organizer: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    
    def add_note(self, note: str):
        self.notes.append(note)
    
    def add_action_item(self, assignee: str, task: str, due_date: Optional[datetime] = None):
        self.action_items.append({
            "assignee": assignee,
            "task": task,
            "due_date": due_date,
            "status": "pending"
        })
    
    def add_decision(self, decision: str):
        self.decisions.append(decision)
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "type": self.meeting_type.value,
            "title": self.title,
            "participants": self.participants,
            "duration": self.duration_minutes,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "notes_count": len(self.notes),
            "action_items_count": len(self.action_items),
            "decisions_count": len(self.decisions)
        }


class MeetingParticipantSelector:
    MEETING_PARTICIPANTS = {
        MeetingType.DEFECT_TRIAGE: [
            "qa_engineer",
            "backend_developer",
            "frontend_developer",
            "product_manager",
            "scrum_master"
        ],
        MeetingType.STEERCO: [
            "cto",
            "engineering_manager",
            "product_manager",
            "devops_manager",
            "it_manager"
        ],
        MeetingType.WEEKLY_STATUS: [
            "scrum_master",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "devops_engineer",
            "qa_engineer",
            "data_engineer"
        ],
        MeetingType.SPRINT_PLANNING: [
            "scrum_master",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "qa_engineer",
            "devops_engineer",
            "ui_ux_designer"
        ],
        MeetingType.SPRINT_RETROSPECTIVE: [
            "scrum_master",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "qa_engineer",
            "devops_engineer",
            "data_engineer"
        ],
        MeetingType.SPRINT_REVIEW: [
            "scrum_master",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "qa_engineer",
            "ui_ux_designer"
        ],
        MeetingType.DAILY_STANDUP: [
            "scrum_master",
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "qa_engineer",
            "devops_engineer"
        ],
        MeetingType.ARCHITECTURE_REVIEW: [
            "solutions_architect",
            "cloud_architect",
            "backend_developer",
            "frontend_developer",
            "devops_engineer",
            "data_engineer",
            "security_engineer"
        ],
        MeetingType.CODE_REVIEW: [
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "qa_engineer",
            "security_engineer"
        ],
        MeetingType.TECHNICAL_DESIGN: [
            "solutions_architect",
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "devops_engineer",
            "data_engineer",
            "database_administrator"
        ],
        MeetingType.PRODUCT_ROADMAP: [
            "product_manager",
            "project_manager",
            "engineering_manager",
            "backend_developer",
            "frontend_developer",
            "ui_ux_designer"
        ],
        MeetingType.RELEASE_PLANNING: [
            "project_manager",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "devops_engineer",
            "devops_manager",
            "qa_engineer"
        ],
        MeetingType.INCIDENT_POSTMORTEM: [
            "site_reliability_engineer",
            "devops_engineer",
            "backend_developer",
            "security_engineer",
            "qa_engineer",
            "devops_manager"
        ],
        MeetingType.PERFORMANCE_REVIEW: [
            "engineering_manager",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "devops_engineer"
        ],
        MeetingType.ONBOARDING: [
            "engineering_manager",
            "product_manager",
            "backend_developer",
            "frontend_developer",
            "technical_writer"
        ],
        MeetingType.KNOWLEDGE_SHARING: [
            "backend_developer",
            "frontend_developer",
            "fullstack_developer",
            "devops_engineer",
            "qa_engineer",
            "data_engineer",
            "data_analyst",
            "technical_writer"
        ],
        MeetingType.SECURITY_REVIEW: [
            "security_engineer",
            "devops_engineer",
            "backend_developer",
            "network_engineer",
            "qa_engineer",
            "cloud_architect"
        ],
        MeetingType.DATABASE_REVIEW: [
            "database_administrator",
            "data_engineer",
            "backend_developer",
            "devops_engineer",
            "data_analyst"
        ],
        MeetingType.DEPLOYMENT_PLANNING: [
            "devops_engineer",
            "devops_manager",
            "site_reliability_engineer",
            "backend_developer",
            "frontend_developer",
            "qa_engineer",
            "cloud_architect"
        ],
        MeetingType.CAPACITY_PLANNING: [
            "engineering_manager",
            "devops_manager",
            "product_manager",
            "devops_engineer",
            "site_reliability_engineer",
            "backend_developer",
            "data_engineer",
            "cloud_architect"
        ]
    }
    
    MEETING_DURATIONS = {
        MeetingType.DEFECT_TRIAGE: 60,
        MeetingType.STEERCO: 90,
        MeetingType.WEEKLY_STATUS: 45,
        MeetingType.SPRINT_PLANNING: 120,
        MeetingType.SPRINT_RETROSPECTIVE: 90,
        MeetingType.SPRINT_REVIEW: 60,
        MeetingType.DAILY_STANDUP: 15,
        MeetingType.ARCHITECTURE_REVIEW: 90,
        MeetingType.CODE_REVIEW: 45,
        MeetingType.TECHNICAL_DESIGN: 120,
        MeetingType.PRODUCT_ROADMAP: 90,
        MeetingType.RELEASE_PLANNING: 120,
        MeetingType.INCIDENT_POSTMORTEM: 60,
        MeetingType.PERFORMANCE_REVIEW: 60,
        MeetingType.ONBOARDING: 60,
        MeetingType.KNOWLEDGE_SHARING: 45,
        MeetingType.SECURITY_REVIEW: 60,
        MeetingType.DATABASE_REVIEW: 60,
        MeetingType.DEPLOYMENT_PLANNING: 90,
        MeetingType.CAPACITY_PLANNING: 90
    }
    
    @classmethod
    def get_participants(cls, meeting_type: MeetingType, additional_participants: Optional[List[str]] = None) -> List[str]:
        participants = cls.MEETING_PARTICIPANTS.get(meeting_type, []).copy()
        
        if additional_participants:
            for participant in additional_participants:
                if participant not in participants:
                    participants.append(participant)
        
        return participants
    
    @classmethod
    def get_duration(cls, meeting_type: MeetingType) -> int:
        return cls.MEETING_DURATIONS.get(meeting_type, 60)
    
    @classmethod
    def create_meeting(
        cls,
        meeting_type: MeetingType,
        title: str,
        description: str,
        additional_participants: Optional[List[str]] = None,
        scheduled_time: Optional[datetime] = None,
        organizer: Optional[str] = None,
        custom_duration: Optional[int] = None
    ) -> Meeting:
        participants = cls.get_participants(meeting_type, additional_participants)
        duration = custom_duration if custom_duration else cls.get_duration(meeting_type)
        
        return Meeting(
            meeting_type=meeting_type,
            title=title,
            description=description,
            participants=participants,
            duration_minutes=duration,
            scheduled_time=scheduled_time,
            organizer=organizer
        )
