import re


# 카톡 대화록 받기
with open('fulltext.txt', encoding='utf-8') as file:
    fullString = file.read()
    file.close()

# 쓸데없는거 지우기
fullString = re.sub(r"\n--------------- .*? ---------------", '', fullString)
fullString = re.sub(r"\nThe team name has been changed.", '', fullString)
fullString = re.sub(r"\n.*? invited .*?", '', fullString)
# 태그 아직 안지움

# 이름시간, 메시지 리스트 따로 만들기
exp1 = r"\n(\[.*?\] \[오.*?\]) "
exp2 = r"\n\[.*?\] \[오.*?\] "
nameTime = re.findall(exp1, fullString)
messageOnly = re.split(exp2, fullString)

# 두 리스트 합침
lineList = []
for i in range(len(nameTime)):
    message = nameTime[i] + ' ' + messageOnly[i+1]
    lineList.append(message)

# 말하는 인간들의 리스트를 만듬
personList = []
for i in lineList:
    person = i[1:i.find(']')]
    if person not in personList: personList.append(person)
personList = [i for i in personList if i]

# 인간 수 만큼 루프 돌리기
for i in personList:
    text = ''
    name = '['+i+']'
    print(name)
    for j in lineList:
        if name == j[:len(name)]:
            sentMessage = j[j.find(']'):]
            sentMessage = sentMessage[3:]

            # 일단 필요할진 모르지만 시간 분리함
            timeSent = sentMessage[:sentMessage.find(']')]
            sentMessage = sentMessage[sentMessage.find(']')+2:]

            # 추임새 제거
            sentMessage = re.sub(r'[ㄱ-ㅎ]', '', sentMessage)
            sentMessage = re.sub(r'[ㅏ-ㅣ]', '', sentMessage)

            # 5자보다 짧은 메시지 제외
            if len(sentMessage) > 4:
                text += sentMessage + '. '
    text = text[:-2]

    # text가 한 사람이 말한것들 다 추합한거
    print(text)
    print('\n')
    
    # 파일 쓰기
    f = open(i+".txt", 'w', encoding='utf-8')
    f.write(text)
    f.close()