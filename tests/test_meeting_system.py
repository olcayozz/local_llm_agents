import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from agents.utils.meeting import Meeting, MeetingType, MeetingParticipantSelector, MeetingAgenda
from datetime import datetime, timedelta


def test_meeting_type_enum():
    print("Testing MeetingType enum...")
    assert MeetingType.DEFECT_TRIAGE.value == "defect_triage"
    assert MeetingType.STEERCO.value == "steerco"
    assert MeetingType.SPRINT_PLANNING.value == "sprint_planning"
    print("✓ MeetingType enum works correctly")


def test_meeting_creation():
    print("\nTesting Meeting creation...")
    meeting = Meeting(
        meeting_type=MeetingType.DEFECT_TRIAGE,
        title="Test Meeting",
        description="Test Description",
        participants=["backend_developer", "qa_engineer"],
        duration_minutes=60
    )
    
    assert meeting.title == "Test Meeting"
    assert meeting.meeting_type == MeetingType.DEFECT_TRIAGE
    assert len(meeting.participants) == 2
    assert meeting.duration_minutes == 60
    print("✓ Meeting creation works correctly")


def test_meeting_notes():
    print("\nTesting Meeting notes...")
    meeting = Meeting(
        meeting_type=MeetingType.DAILY_STANDUP,
        title="Daily Standup",
        description="Daily sync",
        participants=["backend_developer"]
    )
    
    meeting.add_note("First note")
    meeting.add_note("Second note")
    
    assert len(meeting.notes) == 2
    assert meeting.notes[0] == "First note"
    print("✓ Meeting notes work correctly")


def test_meeting_action_items():
    print("\nTesting Meeting action items...")
    meeting = Meeting(
        meeting_type=MeetingType.SPRINT_PLANNING,
        title="Sprint Planning",
        description="Plan sprint",
        participants=["product_manager"]
    )
    
    due_date = datetime.now() + timedelta(days=7)
    meeting.add_action_item("backend_developer", "Implement feature X", due_date)
    meeting.add_action_item("qa_engineer", "Write test cases", due_date)
    
    assert len(meeting.action_items) == 2
    assert meeting.action_items[0]["assignee"] == "backend_developer"
    assert meeting.action_items[0]["task"] == "Implement feature X"
    assert meeting.action_items[0]["status"] == "pending"
    print("✓ Meeting action items work correctly")


def test_meeting_decisions():
    print("\nTesting Meeting decisions...")
    meeting = Meeting(
        meeting_type=MeetingType.ARCHITECTURE_REVIEW,
        title="Architecture Review",
        description="Review architecture",
        participants=["backend_developer"]
    )
    
    meeting.add_decision("Approved microservices architecture")
    meeting.add_decision("Use PostgreSQL for main database")
    
    assert len(meeting.decisions) == 2
    assert "microservices" in meeting.decisions[0]
    print("✓ Meeting decisions work correctly")


def test_meeting_summary():
    print("\nTesting Meeting summary...")
    meeting = Meeting(
        meeting_type=MeetingType.WEEKLY_STATUS,
        title="Weekly Status",
        description="Weekly sync",
        participants=["backend_developer", "frontend_developer"],
        scheduled_time=datetime.now()
    )
    
    meeting.add_note("Note 1")
    meeting.add_action_item("backend_developer", "Task 1")
    meeting.add_decision("Decision 1")
    
    summary = meeting.get_summary()
    
    assert summary["type"] == "weekly_status"
    assert summary["title"] == "Weekly Status"
    assert len(summary["participants"]) == 2
    assert summary["notes_count"] == 1
    assert summary["action_items_count"] == 1
    assert summary["decisions_count"] == 1
    print("✓ Meeting summary works correctly")


def test_participant_selector():
    print("\nTesting MeetingParticipantSelector...")
    
    # Test defect triage participants
    participants = MeetingParticipantSelector.get_participants(MeetingType.DEFECT_TRIAGE)
    assert "qa_engineer" in participants
    assert "backend_developer" in participants
    assert "frontend_developer" in participants
    assert "product_manager" in participants
    
    # Test sprint planning participants
    participants = MeetingParticipantSelector.get_participants(MeetingType.SPRINT_PLANNING)
    assert "product_manager" in participants
    assert "backend_developer" in participants
    assert "qa_engineer" in participants
    
    print("✓ MeetingParticipantSelector works correctly")


def test_participant_selector_with_additional():
    print("\nTesting MeetingParticipantSelector with additional participants...")
    
    participants = MeetingParticipantSelector.get_participants(
        MeetingType.CODE_REVIEW,
        additional_participants=["devops_engineer"]
    )
    
    assert "backend_developer" in participants
    assert "frontend_developer" in participants
    assert "qa_engineer" in participants
    assert "devops_engineer" in participants
    
    print("✓ Additional participants work correctly")


def test_meeting_duration():
    print("\nTesting meeting duration...")
    
    # Test default durations
    assert MeetingParticipantSelector.get_duration(MeetingType.DAILY_STANDUP) == 15
    assert MeetingParticipantSelector.get_duration(MeetingType.SPRINT_PLANNING) == 120
    assert MeetingParticipantSelector.get_duration(MeetingType.DEFECT_TRIAGE) == 60
    
    print("✓ Meeting durations work correctly")


def test_create_meeting_helper():
    print("\nTesting create_meeting helper...")
    
    meeting = MeetingParticipantSelector.create_meeting(
        meeting_type=MeetingType.DEFECT_TRIAGE,
        title="Test Defect Triage",
        description="Test meeting",
        scheduled_time=datetime.now(),
        organizer="product_manager"
    )
    
    assert meeting.title == "Test Defect Triage"
    assert meeting.meeting_type == MeetingType.DEFECT_TRIAGE
    assert meeting.duration_minutes == 60  # Default for defect triage
    assert "qa_engineer" in meeting.participants
    assert meeting.organizer == "product_manager"
    
    print("✓ create_meeting helper works correctly")


def test_all_meeting_types_have_participants():
    print("\nTesting all meeting types have participants...")
    
    for meeting_type in MeetingType:
        participants = MeetingParticipantSelector.get_participants(meeting_type)
        assert len(participants) > 0, f"{meeting_type} has no participants"
        
        duration = MeetingParticipantSelector.get_duration(meeting_type)
        assert duration > 0, f"{meeting_type} has no duration"
    
    print(f"✓ All {len(MeetingType)} meeting types configured correctly")


def test_meeting_agenda():
    print("\nTesting MeetingAgenda...")
    
    agenda = MeetingAgenda(
        title="Sprint Planning Agenda",
        description="Plan next sprint",
        duration_minutes=120,
        topics=["Review backlog", "Estimate stories", "Commit to sprint"],
        objectives=["Define sprint goal", "Commit to deliverables"]
    )
    
    assert agenda.title == "Sprint Planning Agenda"
    assert len(agenda.topics) == 3
    assert len(agenda.objectives) == 2
    
    print("✓ MeetingAgenda works correctly")


def run_all_tests():
    print("=" * 80)
    print(" MEETING SYSTEM UNIT TESTS")
    print("=" * 80)
    
    try:
        test_meeting_type_enum()
        test_meeting_creation()
        test_meeting_notes()
        test_meeting_action_items()
        test_meeting_decisions()
        test_meeting_summary()
        test_participant_selector()
        test_participant_selector_with_additional()
        test_meeting_duration()
        test_create_meeting_helper()
        test_all_meeting_types_have_participants()
        test_meeting_agenda()
        
        print("\n" + "=" * 80)
        print(" ALL TESTS PASSED ✓")
        print("=" * 80)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
