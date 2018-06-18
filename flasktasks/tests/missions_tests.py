import unittest
from flasktasks import db
from flasktasks.tests.flasktasks_testcase import FlaskTasksTestCase
from flasktasks.models import Color, Tag, Board, Status


class BoardsTest(FlaskTasksTestCase):
	def setUp(self):
		super().setUp()
		self.valid_tag = Tag('valid tag', Color.BLUE)
		db.session.add(self.valid_tag)
		db.session.commit()

	def test_boards_page(self):
		first_board = Board('board a', 'description', self.valid_tag.id)
		second_board = Board('board b', 'description', self.valid_tag.id)
		db.session.add(first_board)
		db.session.add(second_board)
		db.session.commit()

		response = self.app.get('/boards')
		assert b'board a' in response.data
		assert b'board b' in response.data

	def test_new_board_form(self):
		response = self.app.get('/boards/new')
		assert b'New Board' in response.data

	def test_board_creation(self):
		data = { 'title':'some board', 'description':'a useful description',
				 'tag_id':self.valid_tag.id }
		response = self.app.post('/boards/new', data=data)
		assert response.status_code == 302

		response = self.app.get('/boards')
		assert b'some board' in response.data

if __name__ == '__main__':
	unittest.main()
