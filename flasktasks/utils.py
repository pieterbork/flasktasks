from flasktasks.models import Board, List, Task, Icon, Color

def apply_template(board, template):
    if template == 1:
        list1 = List("To Do", Icon.FIRE.value, board.id, 0, Color.RED.value)
        list2 = List("Doing", Icon.FLASH.value, board.id, 1, Color.BLUE.value)
        list3 = List("Done", Icon.SEND.value, board.id, 2, Color.GREEN.value)
        board.lists.append(list1)
        board.lists.append(list2)
        board.lists.append(list3)
    return board
