# day5 : random_game
import random

def validate(color):
    if color < 0 or color > 2:
        return False
    return True

def print_choice(color,name):
    colors = ['赤','白','黒']
    print(name + 'は' + colors[color] + 'を選択しました')

def judge(player,computer):
    if player == computer:
        return '成功'
    else:
        return '失敗'
print('相手が出す色を予想してください')
print('色を選択(0:赤, 1:白, 2:黒)')
player_choice = int(input('数字を入力：'))

if validate(player_choice):
    computer_choice = random.randint(0,2)
    print_choice(player_choice,'あなた')
    print_choice(computer_choice,'コンピューター')

    result = judge(player_choice,computer_choice)
    print(result)
else:
    print('正しい数値を選択')