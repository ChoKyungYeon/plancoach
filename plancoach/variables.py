from datetime import datetime

current_datetime =datetime.now()
current_date = current_datetime.date()

weekdaylist = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
]
subjectlist=[
    '국어',
    '영어',
    '수학',
    '물리',
    '지구과학',
    '화학',
    '생명과학',
    '생활과윤리',
    '윤리와사상',
    '한국지리',
    '세계지리',
    '동아시아사',
    '세계사',
    '경제',
    '정치와법',
    '사회문화',
    '한국사',
    '기타',
]

banklist=[
    'BNK부산은행',
    'DGB대구은행',
    'IBK기업은행',
    'KB국민은행',
    'MG새마을금고',
    'SC제일은행',
    'Sh수협은행',
    '광주은행',
    '농협',
    '신한은행',
    '신협',
    '우리은행',
    '우체국은행',
    '저축은행',
    '카카오뱅크',
    '케이뱅크',
    '토스',
    '하나은행'
]

schoollist=[
    '가천대학교',
    '가톨릭관동대학교',
    '가톨릭대학교',
    '강원대학교',
    '건국대학교',
    '건양대학교',
    '경북대학교',
    '경상국립대학교',
    '경희대학교',
    '계명대학교',
    '고려대학교',
    '고신대학교',
    '단국대학교',
    '대구가톨릭대학교',
    '동국대학교(경주)',
    '동아대학교',
    '부산대학교',
    '서울대학교',
    '성균관대학교',
    '순천향대학교',
    '아주대학교',
    '연세대학교(서울)',
    '연세대학교(미래)',
    '영남대학교',
    '울산대학교',
    '원광대학교',
    '을지대학교',
    '이화여자대학교',
    '인제대학교',
    '인하대학교',
    '전남대학교',
    '전북대학교',
    '제주대학교',
    '조선대학교',
    '중앙대학교',
    '차의과학대학교',
    '충남대학교',
    '충북대학교',
    '한림대학교',
    '한양대학교'
]
bankdictionary={
    bank: f'/static/banks/{bank}.png' for bank in banklist
}
subjectdictionary={
    subject: f'/static/subjects/{subject}.png' for subject in subjectlist
}
weekdaydictionary={
    weekday: f'/static/weekdays/{weekday}.png' for weekday in weekdaylist
}