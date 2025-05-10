# Day4: ユーザ入力で合計・合否判定（for だけ使用）
total_score = 0   
subjects = ['国語','算数','理科','社会','英語']
for subject_name in subjects:
    print('----------------------------------')
    print('各教科は100点満点です')
    print('合格点は総得点350/500です')

    input_score = input(subject_name + 'の点数を入力してください：')
    print(subject_name + 'の点数は' + input_score + '点です')

    score = int(input_score)
    total_score = total_score + score
    print('現在の合計点は' + str(total_score) + '点です')

    if total_score >= 350:
            print('合格ラインを超えました(残りの科目があれば続けて入力)')
    else:
            print('まだ合格圏外です(続けて入力)')
        
print('==================================')
if total_score >= 350:
        print(f"最終得点 {total_score} 点：合格です")
else:
        print(f"最終得点 {total_score} 点：不合格です")