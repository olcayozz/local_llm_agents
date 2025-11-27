import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from orchestrator import AgentOrchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AgentOrchestrator(
            model_name="llama3.2",
            temperature=0.7,
            role_folder="Role"
        )
    
    def test_list_agents(self):
        agents = self.orchestrator.list_agents()
        self.assertIsInstance(agents, list)
        self.assertIn("backend_developer", agents)
        self.assertIn("devops_engineer", agents)
        self.assertIn("product_manager", agents)
    
    def test_get_agent(self):
        agent = self.orchestrator.get_agent("backend_developer")
        self.assertIsNotNone(agent)
    
    def test_get_agent_invalid(self):
        with self.assertRaises(ValueError):
            self.orchestrator.get_agent("invalid_agent")
    
    def test_get_agent_info(self):
        info = self.orchestrator.get_agent_info("product_manager")
        self.assertIsInstance(info, dict)
        self.assertIn('title', info)
    
    def test_clear_agent_memory(self):
        agent = self.orchestrator.get_agent("backend_developer")
        agent.chat("Hello")
        self.orchestrator.clear_agent_memory("backend_developer")
        history = agent.get_conversation_history()
        self.assertEqual(len(history), 0)

if __name__ == '__main__':
    unittest.main()
