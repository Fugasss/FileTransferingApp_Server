# from fastapi.testclient import TestClient
# from unittest.mock import patch, MagicMock
# import psycopg2
# 
# from src import settings
# from src.apps.admin.database.DAOs.userDAO import get_all_users
# 
# 
# class TestDatabaseFunction(TestClient):
# 
#     @patch('psycopg2.connect')
#     def setUp(self, mock_connect):
#         self.mock_connection = MagicMock()
#         self.mock_cursor = MagicMock()
# 
#         mock_connect.return_value = self.mock_connection
#         self.mock_connection.cursor.return_value = self.mock_cursor
# 
#     def test_create_users(self):
#         # expected_data = tuple()
#         # self.mock_cursor.fetchall.return_value = expected_data
#         # 
#         # result = get_all_users()
#         # self.assertEqual(result, expected_data)
#         pass
# 
# 
