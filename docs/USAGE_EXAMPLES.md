# Usage Examples and Tutorials

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Examples](#basic-examples)
3. [Advanced Examples](#advanced-examples)
4. [Real-World Scenarios](#real-world-scenarios)
5. [Integration Examples](#integration-examples)
6. [Best Practices](#best-practices)

---

## Getting Started

### Installation and Setup

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.2

# Clone repository
git clone https://github.com/yourusername/local_llm_agents.git
cd local_llm_agents

# Install dependencies
pip install -r requirements.txt

# Verify installation
python tests/test_all_agents.py
```

### First Agent Interaction

```python
from agents.orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Chat with an agent
response = orchestrator.chat_with_agent(
    "backend_developer",
    "What's the best way to implement user authentication?"
)

print(response)
```

---

## Basic Examples

### Example 1: Single Agent Consultation

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Consult backend developer
response = orchestrator.chat_with_agent(
    "backend_developer",
    "How should I design a REST API for a blog platform?"
)

print("Backend Developer:", response)

# Consult security engineer
response = orchestrator.chat_with_agent(
    "security_engineer",
    "What security measures should I implement for the blog API?"
)

print("Security Engineer:", response)
```

### Example 2: Multi-Agent Consultation

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Get opinions from multiple agents
responses = orchestrator.multi_agent_consultation(
    query="Should we use microservices or monolithic architecture for our e-commerce platform?",
    agent_names=[
        "solutions_architect",
        "backend_developer",
        "devops_engineer",
        "cloud_architect"
    ]
)

for agent, response in responses.items():
    print(f"\n{'='*60}")
    print(f"{agent.upper()}")
    print(f"{'='*60}")
    print(response)
```

### Example 3: Simple Meeting

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType

orchestrator = AgentOrchestrator()

# Create meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.DAILY_STANDUP,
    title="Daily Standup - Jan 15",
    description="Daily team sync"
)

# Conduct meeting
topics = [
    "Yesterday's progress",
    "Today's plan",
    "Blockers"
]

result = orchestrator.conduct_meeting(meeting, topics)

# Print summary
summary = orchestrator.get_meeting_summary(meeting)
print(summary)
```

---

## Advanced Examples

### Example 4: Collaborative Workflow

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Define workflow
workflow = [
    {"agent": "product_manager", "action": "chat"},
    {"agent": "solutions_architect", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"},
    {"agent": "frontend_developer", "action": "chat"},
    {"agent": "security_engineer", "action": "chat"},
    {"agent": "devops_engineer", "action": "chat"},
    {"agent": "qa_engineer", "action": "chat"}
]

# Execute collaborative task
results = orchestrator.collaborative_task(
    task_description="Design and implement a secure payment processing system",
    workflow=workflow
)

# Print each agent's contribution
for result in results:
    print(f"\n{'='*60}")
    print(f"{result['agent'].upper()}")
    print(f"{'='*60}")
    print(result['response'])
```

### Example 5: Complex Meeting with Outcomes

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from datetime import datetime, timedelta

orchestrator = AgentOrchestrator()

# Create sprint planning meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan deliverables for next 2-week sprint"
)

# Define user stories
topics = [
    "User Story: As a user, I want to reset my password via email",
    "User Story: As an admin, I want to view user analytics dashboard",
    "User Story: As a user, I want to enable two-factor authentication",
    "Technical Debt: Refactor authentication module",
    "Bug Fix: Payment gateway timeout issues"
]

# Conduct meeting
result = orchestrator.conduct_meeting(meeting, topics)

# Add action items
meeting.add_action_item(
    assignee="backend_developer",
    task="Implement password reset API endpoints",
    due_date=datetime.now() + timedelta(days=5)
)

meeting.add_action_item(
    assignee="frontend_developer",
    task="Create password reset UI flow",
    due_date=datetime.now() + timedelta(days=5)
)

meeting.add_action_item(
    assignee="qa_engineer",
    task="Create test cases for password reset",
    due_date=datetime.now() + timedelta(days=7)
)

meeting.add_action_item(
    assignee="devops_engineer",
    task="Setup email service for password reset",
    due_date=datetime.now() + timedelta(days=3)
)

# Add decisions
meeting.add_decision("Approved password reset implementation using JWT tokens")
meeting.add_decision("Use SendGrid for email delivery")
meeting.add_decision("Implement rate limiting for password reset requests")

# Add notes
meeting.add_note("Team velocity: 40 story points")
meeting.add_note("Sprint goal: Complete authentication improvements")

# Get detailed summary
summary = orchestrator.get_meeting_summary(meeting)
print(summary)
```

### Example 6: Custom Agent Configuration

```python
from agents.orchestrator import AgentOrchestrator

# Initialize with custom configuration
orchestrator = AgentOrchestrator(
    model_name="mistral",  # Use different model
    temperature=0.5,       # Lower temperature for more focused responses
    role_folder="Role"
)

# Use specific agents with custom behavior
response = orchestrator.chat_with_agent(
    "security_engineer",
    "Review this code for security vulnerabilities: [code snippet]"
)

print(response)
```

---

## Real-World Scenarios

### Scenario 1: New Feature Development

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from datetime import datetime, timedelta

orchestrator = AgentOrchestrator()

# Step 1: Product Manager defines requirements
pm_response = orchestrator.chat_with_agent(
    "product_manager",
    "We need to add a real-time chat feature to our application. What are the key requirements?"
)

print("Product Requirements:")
print(pm_response)

# Step 2: Architecture Review Meeting
arch_meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.ARCHITECTURE_REVIEW,
    title="Real-time Chat Architecture Review",
    description="Design architecture for chat feature"
)

arch_topics = [
    "Technology stack: WebSocket vs Server-Sent Events vs Polling",
    "Message persistence and history",
    "Scalability and load balancing",
    "Security and encryption",
    "Integration with existing authentication"
]

arch_result = orchestrator.conduct_meeting(arch_meeting, arch_topics)

# Step 3: Security Review
security_meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SECURITY_REVIEW,
    title="Chat Feature Security Review",
    description="Review security implications"
)

security_topics = [
    "End-to-end encryption",
    "Message content filtering",
    "Rate limiting and abuse prevention",
    "Data privacy and GDPR compliance"
]

security_result = orchestrator.conduct_meeting(security_meeting, security_topics)

# Step 4: Sprint Planning
sprint_meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Chat Feature Sprint Planning",
    description="Plan implementation sprints"
)

sprint_topics = [
    "Backend: WebSocket server implementation",
    "Backend: Message persistence layer",
    "Frontend: Chat UI components",
    "Frontend: Real-time message handling",
    "DevOps: Infrastructure and deployment",
    "QA: Testing strategy"
]

sprint_result = orchestrator.conduct_meeting(sprint_meeting, sprint_topics)

# Add action items
sprint_meeting.add_action_item(
    assignee="backend_developer",
    task="Implement WebSocket server with Socket.io",
    due_date=datetime.now() + timedelta(days=7)
)

sprint_meeting.add_action_item(
    assignee="frontend_developer",
    task="Create chat UI components",
    due_date=datetime.now() + timedelta(days=7)
)

sprint_meeting.add_action_item(
    assignee="devops_engineer",
    task="Setup Redis for message queue",
    due_date=datetime.now() + timedelta(days=3)
)

# Print comprehensive summary
print("\n" + "="*80)
print("FEATURE DEVELOPMENT SUMMARY")
print("="*80)
print(orchestrator.get_meeting_summary(arch_meeting))
print(orchestrator.get_meeting_summary(security_meeting))
print(orchestrator.get_meeting_summary(sprint_meeting))
```

### Scenario 2: Production Incident Response

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from datetime import datetime

orchestrator = AgentOrchestrator()

# Step 1: Initial incident assessment
sre_response = orchestrator.chat_with_agent(
    "site_reliability_engineer",
    "Production database is experiencing high CPU usage (95%+) and slow query times. What should we check first?"
)

print("SRE Initial Assessment:")
print(sre_response)

# Step 2: Multi-agent incident analysis
incident_responses = orchestrator.multi_agent_consultation(
    query="Database CPU at 95%, queries timing out. Application showing 500 errors. What could be the cause?",
    agent_names=[
        "site_reliability_engineer",
        "database_administrator",
        "backend_developer",
        "devops_engineer"
    ]
)

print("\nIncident Analysis:")
for agent, response in incident_responses.items():
    print(f"\n{agent}:")
    print(response)

# Step 3: Incident postmortem meeting
postmortem = orchestrator.create_meeting(
    meeting_type=MeetingType.INCIDENT_POSTMORTEM,
    title="Database Performance Incident - Jan 15, 2024",
    description="Analyze root cause and prevention measures"
)

postmortem_topics = [
    "Timeline of events",
    "Root cause: Unoptimized query in new feature",
    "Impact: 2 hours downtime, 1000+ affected users",
    "Immediate fix: Query optimization and index addition",
    "Prevention: Enhanced monitoring and query review process"
]

postmortem_result = orchestrator.conduct_meeting(postmortem, postmortem_topics)

# Add action items
postmortem.add_action_item(
    assignee="database_administrator",
    task="Add missing indexes on user_activity table",
    due_date=datetime.now()
)

postmortem.add_action_item(
    assignee="site_reliability_engineer",
    task="Setup alerts for slow queries (>1s)",
    due_date=datetime.now() + timedelta(days=1)
)

postmortem.add_action_item(
    assignee="backend_developer",
    task="Implement query performance testing in CI/CD",
    due_date=datetime.now() + timedelta(days=3)
)

postmortem.add_action_item(
    assignee="devops_manager",
    task="Update incident response runbook",
    due_date=datetime.now() + timedelta(days=5)
)

# Add decisions
postmortem.add_decision("All database queries must be reviewed before deployment")
postmortem.add_decision("Implement automated query performance testing")
postmortem.add_decision("Add database performance monitoring dashboard")

print("\nPostmortem Summary:")
print(orchestrator.get_meeting_summary(postmortem))
```

### Scenario 3: Technology Migration

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType

orchestrator = AgentOrchestrator()

# Step 1: Executive decision meeting
steerco = orchestrator.create_meeting(
    meeting_type=MeetingType.STEERCO,
    title="Microservices Migration Decision",
    description="Evaluate migration from monolith to microservices"
)

steerco_topics = [
    "Business drivers for migration",
    "Technical benefits and challenges",
    "Resource requirements and timeline",
    "Risk assessment",
    "ROI analysis"
]

steerco_result = orchestrator.conduct_meeting(steerco, steerco_topics)

# Step 2: Architecture design
arch_workflow = [
    {"agent": "cto", "action": "chat"},
    {"agent": "solutions_architect", "action": "chat"},
    {"agent": "cloud_architect", "action": "chat"},
    {"agent": "backend_developer", "action": "chat"},
    {"agent": "devops_engineer", "action": "chat"}
]

arch_results = orchestrator.collaborative_task(
    task_description="Design microservices architecture for e-commerce platform migration",
    workflow=arch_workflow
)

# Step 3: Detailed technical design
tech_design = orchestrator.create_meeting(
    meeting_type=MeetingType.TECHNICAL_DESIGN,
    title="Microservices Technical Design",
    description="Detailed design for migration"
)

tech_topics = [
    "Service boundaries and domain modeling",
    "API gateway and service mesh",
    "Data management and consistency",
    "Authentication and authorization",
    "Monitoring and observability",
    "Deployment strategy (strangler pattern)"
]

tech_result = orchestrator.conduct_meeting(tech_design, tech_topics)

# Step 4: Capacity planning
capacity = orchestrator.create_meeting(
    meeting_type=MeetingType.CAPACITY_PLANNING,
    title="Microservices Infrastructure Planning",
    description="Plan infrastructure requirements"
)

capacity_topics = [
    "Kubernetes cluster sizing",
    "Database requirements per service",
    "Network bandwidth and latency",
    "Cost estimation",
    "Scaling strategy"
]

capacity_result = orchestrator.conduct_meeting(capacity, capacity_topics)

print("Migration Planning Complete")
print(orchestrator.get_meeting_summary(steerco))
print(orchestrator.get_meeting_summary(tech_design))
print(orchestrator.get_meeting_summary(capacity))
```

### Scenario 4: Security Audit

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType

orchestrator = AgentOrchestrator()

# Step 1: Comprehensive security review
security_review = orchestrator.create_meeting(
    meeting_type=MeetingType.SECURITY_REVIEW,
    title="Annual Security Audit",
    description="Comprehensive security assessment"
)

security_topics = [
    "Application security (OWASP Top 10)",
    "Infrastructure security",
    "Network security",
    "Data encryption and privacy",
    "Access control and authentication",
    "Compliance (GDPR, SOC2, HIPAA)",
    "Security monitoring and incident response"
]

security_result = orchestrator.conduct_meeting(security_review, security_topics)

# Step 2: Detailed assessments by area
areas = [
    ("backend_developer", "Review application code for security vulnerabilities"),
    ("security_engineer", "Assess overall security posture and compliance"),
    ("network_engineer", "Review network architecture and firewall rules"),
    ("cloud_architect", "Evaluate cloud security configuration"),
    ("devops_engineer", "Review CI/CD pipeline security"),
    ("database_administrator", "Assess database security and encryption")
]

print("\nDetailed Security Assessments:")
for agent, query in areas:
    response = orchestrator.chat_with_agent(agent, query)
    print(f"\n{agent.upper()}:")
    print(response)

# Step 3: Action planning
security_review.add_action_item(
    assignee="security_engineer",
    task="Implement Web Application Firewall (WAF)",
    due_date=datetime.now() + timedelta(days=14)
)

security_review.add_action_item(
    assignee="backend_developer",
    task="Fix SQL injection vulnerabilities",
    due_date=datetime.now() + timedelta(days=7)
)

security_review.add_action_item(
    assignee="devops_engineer",
    task="Enable encryption at rest for all databases",
    due_date=datetime.now() + timedelta(days=10)
)

security_review.add_decision("Implement zero-trust security model")
security_review.add_decision("Conduct quarterly security audits")

print("\nSecurity Audit Summary:")
print(orchestrator.get_meeting_summary(security_review))
```

---

## Integration Examples

### Example 7: Jira Integration

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from jira import JIRA

# Initialize
orchestrator = AgentOrchestrator()
jira = JIRA(server='https://your-domain.atlassian.net', basic_auth=('email', 'token'))

# Get sprint stories
sprint_issues = jira.search_issues('sprint = 24 AND status != Done')

# Create sprint planning meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.SPRINT_PLANNING,
    title="Sprint 24 Planning",
    description="Plan sprint deliverables"
)

# Discuss each story
topics = [f"{issue.key}: {issue.fields.summary}" for issue in sprint_issues]
result = orchestrator.conduct_meeting(meeting, topics)

# Create subtasks from action items
for action_item in meeting.action_items:
    # Find parent issue
    parent_key = action_item.task.split(':')[0] if ':' in action_item.task else None
    
    if parent_key:
        jira.create_issue(
            project='PROJ',
            summary=action_item.task,
            description=f"Assigned to: {action_item.assignee}",
            issuetype={'name': 'Sub-task'},
            parent={'key': parent_key}
        )
```

### Example 8: Slack Integration

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from slack_sdk import WebClient

# Initialize
orchestrator = AgentOrchestrator()
slack_client = WebClient(token='your-slack-token')

# Create meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.DAILY_STANDUP,
    title="Daily Standup",
    description="Daily team sync"
)

topics = ["Yesterday", "Today", "Blockers"]
result = orchestrator.conduct_meeting(meeting, topics)

# Post summary to Slack
summary = orchestrator.get_meeting_summary(meeting)
slack_client.chat_postMessage(
    channel='#engineering',
    text=f"*Daily Standup Summary*\n\n{summary}"
)

# Notify assignees of action items
for action_item in meeting.action_items:
    # Get Slack user ID from agent name
    user_id = get_slack_user_id(action_item.assignee)
    
    slack_client.chat_postMessage(
        channel=user_id,
        text=f"New action item: {action_item.task}\nDue: {action_item.due_date}"
    )
```

### Example 9: GitHub Integration

```python
from agents.orchestrator import AgentOrchestrator
from agents.utils.meeting import MeetingType
from github import Github

# Initialize
orchestrator = AgentOrchestrator()
github = Github('your-github-token')
repo = github.get_repo('your-org/your-repo')

# Get open pull requests
pull_requests = repo.get_pulls(state='open')

# Create code review meeting
meeting = orchestrator.create_meeting(
    meeting_type=MeetingType.CODE_REVIEW,
    title="Weekly Code Review",
    description="Review open pull requests"
)

# Review each PR
topics = [f"PR #{pr.number}: {pr.title}" for pr in pull_requests]
result = orchestrator.conduct_meeting(meeting, topics)

# Add comments to PRs
for pr in pull_requests:
    pr_topic = f"PR #{pr.number}: {pr.title}"
    if pr_topic in result['discussions']:
        comments = result['discussions'][pr_topic]
        
        # Compile agent feedback
        feedback = "\n\n".join([
            f"**{agent}**: {response}"
            for agent, response in comments.items()
        ])
        
        # Add comment to PR
        pr.create_issue_comment(
            f"## AI Agent Code Review\n\n{feedback}"
        )
```

---

## Best Practices

### 1. Agent Selection

```python
# Good: Choose agents based on expertise
responses = orchestrator.multi_agent_consultation(
    query="How should we implement caching?",
    agent_names=[
        "backend_developer",      # Implementation
        "devops_engineer",        # Infrastructure
        "site_reliability_engineer"  # Performance
    ]
)

# Bad: Using irrelevant agents
responses = orchestrator.multi_agent_consultation(
    query="How should we implement caching?",
    agent_names=["ui_ux_designer", "technical_writer"]  # Not relevant
)
```

### 2. Topic Definition

```python
# Good: Specific, focused topics
topics = [
    "API Design: REST endpoint structure for user management",
    "Security: JWT token expiration and refresh strategy",
    "Performance: Database query optimization for user search"
]

# Bad: Vague, broad topics
topics = [
    "API stuff",
    "Make it secure",
    "Performance"
]
```

### 3. Memory Management

```python
# Clear memory for fresh context
orchestrator.clear_agent_memory("backend_developer")

# Or clear all
orchestrator.clear_all_memories()

# Use separate orchestrator instances for different contexts
auth_orchestrator = AgentOrchestrator()
payment_orchestrator = AgentOrchestrator()
```

### 4. Error Handling

```python
try:
    response = orchestrator.chat_with_agent("backend_developer", query)
except ValueError as e:
    print(f"Agent not found: {e}")
except Exception as e:
    print(f"Error: {e}")
    # Fallback or retry logic
```

### 5. Performance Optimization

```python
# Use parallel execution for independent queries
responses = orchestrator.multi_agent_consultation(
    query="Review this architecture",
    agent_names=["solutions_architect", "cloud_architect", "security_engineer"]
)  # Executes in parallel

# Use collaborative workflow for dependent tasks
workflow = [
    {"agent": "product_manager"},
    {"agent": "solutions_architect"},  # Builds on PM's output
    {"agent": "backend_developer"}     # Builds on architect's output
]
results = orchestrator.collaborative_task("Design feature", workflow)
```

---

## Conclusion

These examples demonstrate the flexibility and power of the Multi-Agent Orchestrator System. From simple single-agent consultations to complex multi-meeting workflows, the system can handle a wide range of software development scenarios.

For more information, see:
- [API Reference](API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Meeting System Documentation](MEETING_SYSTEM.md)
