import unittest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.role_loader import RoleLoader

class TestRoleLoader(unittest.TestCase):
    def setUp(self):
        self.role_loader = RoleLoader(role_folder="Role")
    
    def test_load_role(self):
        content = self.role_loader.load_role("Product_Manager.txt")
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
    
    def test_get_role_prompt(self):
        prompt = self.role_loader.get_role_prompt("DevOps_Engineer.txt")
        self.assertIn("You are an AI agent", prompt)
        self.assertGreater(len(prompt), 100)
    
    def test_list_available_roles(self):
        roles = self.role_loader.list_available_roles()
        self.assertIsInstance(roles, list)
        self.assertGreater(len(roles), 0)
        self.assertIn("Product_Manager.txt", roles)
    
    def test_get_role_metadata(self):
        metadata = self.role_loader.get_role_metadata("Product_Manager.txt")
        self.assertIsInstance(metadata, dict)
        self.assertIn('title', metadata)
        self.assertIn('level', metadata)

if __name__ == '__main__':
    unittest.main()
