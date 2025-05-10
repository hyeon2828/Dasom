filename = 'KakaoTalk_analyzer_project.txt'
kt_file = open(filename, 'r', encoding = 'utf8')
kt_file_content = kt_file.readlines()
kt_file.close()

def kakaotalkAnalyzer():

    #불필요한 요소 삭제
      
    for i in kt_file_content:
        if (i.count("님을 초대하였습니다.")==1):   #초대 알림 삭제
            kt_file_content.remove(i)
            
    for i in kt_file_content:
        if (i.count("---------------")==2):    #날짜 삭제
            kt_file_content.remove(i)

    del kt_file_content[0:3]  #대화 내용 첫머리 불필요 부분 삭제
 
    #필요한 리스트 만들기

    no_enter_sentence = []
    
    for i in kt_file_content:
        if (i.count("] [")==0):
            continue
        no_enter_sentence.append(i)

    #emter쳐진 문장 이어붙이기
            
    kt_file_content_arranged1 = []  #enter가 정리된 리스트

    for i in kt_file_content:
        if (i==kt_file_content[-1]):   #반복문 종료용
            break
        elif (i.count("] [")!=0 and kt_file_content[kt_file_content.index(i)+1].count("] [")!=0):
            kt_file_content_arranged1.append(i)
        elif (i.count("] [")!=0 and kt_file_content[kt_file_content.index(i)+1].count("] [")==0):
            combine_start = kt_file_content.index(i)
            combine_cut = kt_file_content.index(no_enter_sentence[no_enter_sentence.index(i)+1])
            combined = ''.join(kt_file_content[combine_start:combine_cut])
            kt_file_content_arranged1.append(combined)

    #[이름,시간,내용] 정리
    
    kt_file_content_arranged2 = []
    for i in kt_file_content_arranged1:
        kt_file_content_arranged2.append(i.split("] ",2))

    for i in kt_file_content_arranged2: 
        i[0] = i[0].replace('[','')       #이름
        i[2] = i[2].replace('\n',' ')     #내용
        del i[1]                          #시간

    #단어 검색

    laugh = ['ㅋ','ㅌ','ㅎ','^^','~','😊']
    cry = ['ㅠ','ㅜ','흑','힝','..','미안','서운','(슬픔)']
    swear = ['ㅅㅂ','ㅗ','ㅂㅅ','꺼져','새끼','새키','샛기']

    word_counting = {}

    while True:
        word = input("검색할 단어: ")

        if word=="\stop":
            print("종료합니다")
            break

        for name in kt_file_content_arranged2:    # 다시 실행할 때 횟수 초기화
            word_counting[name[0]] = 0    

        if word=="\laugh":
            for i in kt_file_content_arranged2:
                for l in laugh:
                    if l in i[1]:
                        word_counting[i[0]] += 1
            print_counting(word_counting)
        elif word=="\cry":
            for i in kt_file_content_arranged2:
                for l in cry:
                    if l in i[1]:
                        word_counting[i[0]] += 1
            print_counting(word_counting)
        elif word=="\swear":
            for i in kt_file_content_arranged2:
                for l in swear: 
                    if l in i[1]:
                        word_counting[i[0]] += 1
            print_counting(word_counting)
        elif word == "\\talk":
            for i in kt_file_content_arranged2:
                word_counting[i[0]] += 1
            print_counting(word_counting)
        else:
            for i in kt_file_content_arranged2:
                if word in i[1]:
                    word_counting[i[0]] += 1
            print_counting(word_counting)
        
def print_counting(word_counting):
    for name, count in word_counting.items():
        print(f"{name}: {count}")

kakaotalkAnalyzer()