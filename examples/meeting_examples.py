import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).parent.parent))

from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType


def print_separator(title: str = ""):
    print("\n" + "=" * 80)
    if title:
        print(f" {title}")
        print("=" * 80)


def example_defect_triage_meeting():
    print_separator("DEFECT TRIAGE MEETING EXAMPLE")
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7
    )
    
    meeting = orchestrator.create_meeting(
        meeting_type=MeetingType.DEFECT_TRIAGE,
        title="Weekly Defect Triage - Sprint 23",
        description="Review and prioritize critical defects found in the latest release",
        scheduled_time=datetime.now() + timedelta(days=1),
        organizer="product_manager"
    )
    
    print(f"\nMeeting Created:")
    print(f"  Type: {meeting.meeting_type.value}")
    print(f"  Title: {meeting.title}")
    print(f"  Duration: {meeting.duration_minutes} minutes")
    print(f"  Participants: {', '.join(meeting.participants)}")
    
    discussion_topics = [
        "Critical bug in payment processing - affects 15% of transactions",
        "UI rendering issue on mobile devices",
        "Performance degradation in search functionality",
        "Data inconsistency in user profile updates"
    ]
    
    print("\nConducting meeting...")
    result = orchestrator.conduct_meeting(meeting, discussion_topics)
    
    print("\nMeeting Responses:")
    for participant, response in result["responses"].items():
        print(f"\n{participant.replace('_', ' ').title()}:")
        print(f"  {response[:200]}...")
    
    meeting.add_action_item(
        assignee="backend_developer",
        task="Fix payment processing bug",
        due_date=datetime.now() + timedelta(days=3)
    )
    meeting.add_action_item(
        assignee="frontend_developer",
        task="Resolve mobile UI rendering issue",
        due_date=datetime.now() + timedelta(days=2)
    )
    meeting.add_decision("Payment bug marked as P0 - immediate fix required")
    
    summary = orchestrator.get_meeting_summary(meeting)
    print("\nMeeting Summary:")
    print(f"  Notes: {summary['summary']['notes_count']}")
    print(f"  Action Items: {summary['summary']['action_items_count']}")
    print(f"  Decisions: {summary['summary']['decisions_count']}")


def example_sprint_planning_meeting():
    print_separator("SPRINT PLANNING MEETING EXAMPLE")
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7
    )
    
    meeting = orchestrator.create_meeting(
        meeting_type=MeetingType.SPRINT_PLANNING,
        title="Sprint 24 Planning",
        description="Plan user stories and tasks for the upcoming sprint",
        scheduled_time=datetime.now() + timedelta(days=2),
        organizer="product_manager"
    )
    
    print(f"\nMeeting Created:")
    print(f"  Type: {meeting.meeting_type.value}")
    print(f"  Title: {meeting.title}")
    print(f"  Duration: {meeting.duration_minutes} minutes")
    print(f"  Participants: {', '.join(meeting.participants)}")
    
    discussion_topics = [
        "User Story: Implement OAuth2 authentication",
        "User Story: Add real-time notifications",
        "User Story: Optimize database queries for reporting",
        "Technical Debt: Refactor legacy payment module"
    ]
    
    print("\nConducting meeting...")
    result = orchestrator.conduct_meeting(meeting, discussion_topics)
    
    print("\nMeeting Responses:")
    for participant, response in result["responses"].items():
        print(f"\n{participant.replace('_', ' ').title()}:")
        print(f"  {response[:200]}...")


def example_architecture_review_meeting():
    print_separator("ARCHITECTURE REVIEW MEETING EXAMPLE")
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7
    )
    
    meeting = orchestrator.create_meeting(
        meeting_type=MeetingType.ARCHITECTURE_REVIEW,
        title="Microservices Architecture Review",
        description="Review proposed microservices architecture for the new platform",
        scheduled_time=datetime.now() + timedelta(days=3),
        organizer="backend_developer",
        additional_participants=["product_manager"]
    )
    
    print(f"\nMeeting Created:")
    print(f"  Type: {meeting.meeting_type.value}")
    print(f"  Title: {meeting.title}")
    print(f"  Duration: {meeting.duration_minutes} minutes")
    print(f"  Participants: {', '.join(meeting.participants)}")
    
    discussion_topics = [
        "Service boundaries and domain modeling",
        "Inter-service communication patterns (REST vs gRPC vs Message Queue)",
        "Data consistency and distributed transactions",
        "Deployment strategy and CI/CD pipeline",
        "Monitoring and observability"
    ]
    
    print("\nConducting meeting...")
    result = orchestrator.conduct_meeting(meeting, discussion_topics)
    
    print("\nMeeting Responses:")
    for participant, response in result["responses"].items():
        print(f"\n{participant.replace('_', ' ').title()}:")
        print(f"  {response[:200]}...")


def example_steerco_meeting():
    print_separator("STEERING COMMITTEE (STEERCO) MEETING EXAMPLE")
    
    orchestrator = AgentOrchestrator(
        model_name="llama3.2",
        temperature=0.7
    )
    
    meeting = orchestrator.create_meeting(
        meeting_type=MeetingType.STEERCO,
        title="Q4 Strategic Review",
        description="Review project progress, risks, and strategic decisions",
        scheduled_time=datetime.now() + timedelta(days=7),
        organizer="product_manager"
    )
    
    print(f"\nMeeting Created:")
    print(f"  Type: {meeting.meeting_type.value}")
    print(f"  Title: {meeting.title}")
    print(f"  Duration: {meeting.duration_minutes} minutes")
    print(f"  Participants: {', '.join(meeting.participants)}")
    
    discussion_topics = [
        "Q4 project delivery status and milestones",
        "Budget review and resource allocation",
        "Technical risks and mitigation strategies",
        "Platform scalability for 2024 growth targets",
        "Technology stack modernization roadmap"
    ]
    
    print("\nConducting meeting...")
    result = orchestrator.conduct_meeting(meeting, discussion_topics)
    
    print("\nMeeting Responses:")
    for participant, response in result["responses"].items():
        print(f"\n{participant.replace('_', ' ').title()}:")
        print(f"  {response[:200]}...")


def list_all_meeting_types():
    print_separator("AVAILABLE MEETING TYPES")
    
    orchestrator = AgentOrchestrator()
    meeting_types = orchestrator.get_available_meeting_types()
    
    print("\nAll Available Meeting Types:")
    for i, mt in enumerate(meeting_types, 1):
        participants = orchestrator.get_meeting_participants_for_type(MeetingType(mt))
        print(f"\n{i}. {mt.replace('_', ' ').title()}")
        print(f"   Participants: {', '.join(participants)}")


def main():
    print("\n" + "=" * 80)
    print(" MULTI-AGENT MEETING SYSTEM DEMONSTRATION")
    print("=" * 80)
    
    print("\nThis example demonstrates the meeting system with various meeting types.")
    print("Each meeting type automatically selects appropriate participants.")
    
    list_all_meeting_types()
    
    print("\n\nRunning example meetings...")
    print("(Note: These examples will make actual LLM calls)")
    
    choice = input("\nWhich example would you like to run? (1-4, or 'all'): ")
    
    if choice == "1" or choice.lower() == "all":
        example_defect_triage_meeting()
    
    if choice == "2" or choice.lower() == "all":
        example_sprint_planning_meeting()
    
    if choice == "3" or choice.lower() == "all":
        example_architecture_review_meeting()
    
    if choice == "4" or choice.lower() == "all":
        example_steerco_meeting()
    
    print_separator("DEMONSTRATION COMPLETE")


if __name__ == "__main__":
    main()
