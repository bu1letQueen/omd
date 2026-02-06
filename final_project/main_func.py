#!/usr/bin/env python

"""
Bot for playing tic tac toe game with multiple CallbackQueryHandlers.
"""
import random
from copy import deepcopy
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [ [FREE_SPACE for _ in range(3) ] for _ in range(3) ]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'X (your) turn! Please, put X to the free place', reply_markup=reply_markup)
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    users_cross = update.callback_query.data
    field = context.user_data['keyboard_state']
    users_row = int(users_cross[0])
    users_col = int(users_cross[1])

    restart_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Play Again", callback_data='play_again')]])

    # Проверка занято или нет
    if field[users_row][users_col] != FREE_SPACE:
        await update.callback_query.answer("Cell is occupied!", show_alert=True)
        return CONTINUE_GAME

    # ХОД ИГРОКА
    field[users_row][users_col] = CROSS

    # Проверка победы игрока
    if won(field):
        await update.callback_query.edit_message_text("You won!", reply_markup=restart_markup)

        return FINISH_GAME

    empty_cells = [(row, col) for row in range(3) for col in range(3) if field[row][col] == FREE_SPACE]

    # Проверка на ничью
    if not empty_cells:
        await update.callback_query.edit_message_text("Draw!", reply_markup=restart_markup)
        return FINISH_GAME

    best_move = get_best_move(field)
    if best_move:
        bot_row, bot_col = best_move
        field[bot_row][bot_col] = ZERO

    # Проверка победы Бота
    if won(field):
        reply_markup = InlineKeyboardMarkup(generate_keyboard(field))
        await update.callback_query.edit_message_text("You lost!", reply_markup=restart_markup)
        return FINISH_GAME

    # Если никто не победил и место есть
    reply_markup = InlineKeyboardMarkup(generate_keyboard(field))
    await update.callback_query.edit_message_text(
        text="X (your) turn! Please, put X to the free place",
        reply_markup=reply_markup
    )
    return CONTINUE_GAME


def check_win_sim(board, player):
    """Проверяет, выиграл ли кто-то и кто именно"""

    for i in range(3):
        if all([board[i][j] == player for j in range(3)]): return True
        if all([board[j][i] == player for j in range(3)]): return True

    if board[0][0] == board[1][1] == board[2][2] == player: return True
    if board[0][2] == board[1][1] == board[2][0] == player: return True
    return False


def won(fields: list[str]) -> bool:
    return check_win_sim(fields, CROSS) or check_win_sim(fields, ZERO)

def find_optimal_move(board, depth, bots_turn):
    if check_win_sim(board, ZERO): return 10 - depth
    if check_win_sim(board, CROSS): return depth - 10
    if not any(FREE_SPACE in row for row in board): return 0

    if bots_turn:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == FREE_SPACE:
                    board[row][col] = ZERO
                    score = find_optimal_move(board, depth+1, False)
                    board[row][col] = FREE_SPACE
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == FREE_SPACE:
                    board[row][col] = CROSS
                    score = find_optimal_move(board, depth+1, True)
                    board[row][col] = FREE_SPACE
                    best_score = min(best_score, score)
        return best_score


def get_best_move(board):
    best_score = -float('inf')
    move = None

    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == FREE_SPACE]
    if len(empty_cells) == 9:
        return (1, 1)
    if len(empty_cells) == 8 and board[1][1] == FREE_SPACE:
        return (1, 1)

    for row in range(3):
        for col in range(3):
            if board[row][col] == FREE_SPACE:
                board[row][col] = ZERO
                score = find_optimal_move(board, 0, False)
                board[row][col] = FREE_SPACE

                if score > best_score:
                    best_score = score
                    move = (row, col)

    return move


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


async def play_again(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сбрасывает игру и рисует чистое поле"""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        text='New game! X (your) turn!',
        reply_markup=reply_markup
    )
    return CONTINUE_GAME


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                             CallbackQueryHandler(play_again, pattern='^play_again$')
                         ] + [
                             CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                             for r in range(3)
                             for c in range(3)
                         ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
