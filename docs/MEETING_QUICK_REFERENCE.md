# Meeting System Quick Reference

## Import Statements

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType, Meeting, MeetingParticipantSelector
from datetime import datetime, timedelta
```

## Create Meeting

```python
orchestrator = AgentOrchestrator()

meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.DEFECT_TRIAGE,
    title="Weekly Defect Triage",
    description="Review critical defects",
    scheduled_time=datetime.now() + timedelta(days=1),
    organizer="product_manager"
)
```

## Conduct Meeting

```python
topics = [
    "Critical bug in payment processing",
    "UI rendering issue on mobile",
    "Performance degradation"
]

result = orchestrator.conduct_meeting(meeting, topics)

# Access responses
for participant, response in result["responses"].items():
    print(f"{participant}: {response}")
```

## Add Meeting Outcomes

```python
# Add action item
meeting.add_action_item(
    assignee="backend_developer",
    task="Fix payment bug",
    due_date=datetime.now() + timedelta(days=3)
)

# Add decision
meeting.add_decision("Payment bug marked as P0")

# Add note
meeting.add_note("Team agreed to daily sync")
```

## Get Meeting Summary

```python
summary = orchestrator.get_meeting_summary(meeting)
print(summary)
```

## List All Meetings

```python
meetings = orchestrator.list_meetings()
for meeting in meetings:
    print(f"{meeting['title']} - {meeting['type']}")
```

## Available Meeting Types

```python
# Get all meeting types
types = orchestrator.get_available_meeting_types()

# Get participants for a type
participants = orchestrator.get_meeting_participants_for_type(
    MeetingType.SPRINT_PLANNING
)
```

## Meeting Types Reference

| Meeting Type | Duration | Participants |
|-------------|----------|--------------|
| DAILY_STANDUP | 15 min | Backend, Frontend, QA, DevOps |
| SPRINT_PLANNING | 120 min | PM, Backend, Frontend, QA, DevOps |
| SPRINT_REVIEW | 60 min | PM, Backend, Frontend, QA |
| SPRINT_RETROSPECTIVE | 90 min | All team members |
| DEFECT_TRIAGE | 60 min | QA, Backend, Frontend, PM |
| ARCHITECTURE_REVIEW | 90 min | Backend, Frontend, DevOps, Data |
| CODE_REVIEW | 45 min | Backend, Frontend, QA |
| TECHNICAL_DESIGN | 120 min | Backend, Frontend, DevOps, Data |
| STEERCO | 90 min | PM, Backend, Frontend, DevOps, Data |
| WEEKLY_STATUS | 45 min | All team members |
| PRODUCT_ROADMAP | 90 min | PM, Backend, Frontend |
| RELEASE_PLANNING | 120 min | PM, Backend, Frontend, DevOps, QA |
| INCIDENT_POSTMORTEM | 60 min | DevOps, Backend, QA |
| PERFORMANCE_REVIEW | 60 min | PM, Backend, Frontend, DevOps |
| ONBOARDING | 60 min | PM, Backend, Frontend |
| KNOWLEDGE_SHARING | 45 min | Backend, Frontend, DevOps, QA, Data |
| SECURITY_REVIEW | 60 min | DevOps, Backend, QA |
| DATABASE_REVIEW | 60 min | Data, Backend, DevOps |
| DEPLOYMENT_PLANNING | 90 min | DevOps, Backend, Frontend, QA |
| CAPACITY_PLANNING | 90 min | PM, DevOps, Backend, Data |

## Advanced Options

### Custom Duration
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Extended Sprint Planning",
    description="Complex sprint",
    custom_duration=180  # 3 hours
)
```

### Additional Participants
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.CODE_REVIEW,
    title="Security Code Review",
    description="Review security changes",
    additional_participants=["devops_engineer"]
)
```

### With Agenda
```python
from agents.utils.meeting import MeetingAgenda

agenda = MeetingAgenda(
    title="Sprint Planning Agenda",
    description="Plan next sprint",
    duration_minutes=120,
    topics=["Review backlog", "Estimate stories"],
    objectives=["Define sprint goal"]
)

meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan sprint 24",
    agenda=agenda
)
```

## Common Patterns

### Pattern 1: Defect Triage
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.DEFECT_TRIAGE,
    title="Weekly Defect Triage",
    description="Review P0/P1 bugs"
)

topics = ["Bug #123: Payment failure", "Bug #456: UI crash"]
result = orchestrator.conduct_meeting(meeting, topics)

meeting.add_action_item("backend_developer", "Fix bug #123", due_date)
meeting.add_decision("Bug #123 is P0")
```

### Pattern 2: Sprint Planning
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan deliverables"
)

topics = [
    "User Story: OAuth2 authentication",
    "User Story: Real-time notifications"
]
result = orchestrator.conduct_meeting(meeting, topics)

meeting.add_action_item("backend_developer", "Implement OAuth2", due_date)
meeting.add_decision("Commit to 15 story points")
```

### Pattern 3: Architecture Review
```python
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.ARCHITECTURE_REVIEW,
    title="Microservices Review",
    description="Review architecture"
)

topics = [
    "Service boundaries",
    "Communication patterns",
    "Data consistency"
]
result = orchestrator.conduct_meeting(meeting, topics)

meeting.add_decision("Approved microservices architecture")
```

## Error Handling

```python
try:
    meeting = orchestrator.create_meeting(
        meeting_type=MeetingType.DEFECT_TRIAGE,
        title="Test Meeting",
        description="Test"
    )
    result = orchestrator.conduct_meeting(meeting, topics)
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Clear Titles**: Use descriptive meeting titles
2. **Specific Topics**: Provide specific, actionable discussion topics
3. **Document Outcomes**: Always add action items and decisions
4. **Review Responses**: Analyze agent responses for insights
5. **Track Follow-ups**: Use action items to track follow-ups

## Running Examples

```bash
# Run all examples
python examples/meeting_examples.py

# Run tests
python tests/test_meeting_system.py
```

## Documentation

- Full Documentation: `docs/MEETING_SYSTEM.md`
- Implementation Summary: `docs/MEETING_IMPLEMENTATION_SUMMARY.md`
- Source Code: `agents/utils/meeting.py`
- Examples: `examples/meeting_examples.py`
- Tests: `tests/test_meeting_system.py`
