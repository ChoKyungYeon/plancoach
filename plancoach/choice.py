from datetime import date, datetime

from plancoach.variables import banklist, schoollist, subjectlist

schoolyearchoice = []
for i in range(12, int(datetime.now().date().strftime("%y")) + 1):
    schoolyearchoice.append((i, i))

yearchoice = []
for i in range(2015, int(datetime.now().date().strftime("%Y")) + 1):
    yearchoice.append((i, i))

durationchoice = (
    ('약 3개월', '약 3개월'),
    ('약 6개월', '약 6개월'),
    ('약 9개월', '약 9개월'),
    ('1년 이상', '1년 이상'),
    ('진행중', '진행중')
)

sexchoice=(
    ('male', '남자'),
    ('female', '여자')
)



userstatechoice=(
    ('student', '학생'),
    ('teacher', '선생님'),
    ('superuser', '관리자')
)
refusaltypechoice=(
    ('matching', '매칭 종료'),
    ('consult', '수업 종료'),
    ('teacherapply', '수업 신청 종료'),
    ('refund', '수업 환불 완료')
)


teacherstatechoice=(
    ('abled', '모집중'),
    ('disabled', '모집 중지')
)

consultstatechoice=(
    ('unextended', '미연장'),
    ('extended', '연장'),
    ('new', '신규'),
)

bankchoice = [(bank, bank) for bank in banklist]
subjectchoice = [(subject, subject) for subject in subjectlist]

weekdatechoice=(
    ('월요일', '월요일'),
    ('화요일', '화요일'),
    ('수요일', '수요일'),
    ('목요일', '목요일'),
    ('금요일', '금요일'),
    ('토요일', '토요일'),
    ('일요일', '일요일'),
)

applicationstatechoice=(
    ('applied', '신청완료'),
    ('matching', '매칭중'),
)



agechoice=(
    ('graden', 'N수'),
    ('grade3', '3학년'),
    ('grade2', '2학년'),
    ('grade1', '1학년'),
    ('middle', '중등'),
)
teacheragechoice = []
for i in range(19, 36):
    teacheragechoice .append((i, i))


highschooltypechoice = (
    ('영재고', '영재고'),
    ('과학고', '과학고'),
    ('국제고', '국제고'),
    ('외고', '외고'),
    ('자사고', '자사고'),
    ('자공고', '자공고'),
    ('일반고', '일반고'),
    ('기타', '기타'),
)

accepttypechoice = (
    ('학생부교과', '학생부교과'),
    ('학생부종합', '학생부종합'),
    ('논술', '논술'),
    ('특기자', '특기자'),
    ('정시', '정시'),
    ('기타', '기타'),
)


consulttypechoice=(
    ('정시', '정시'),
    ('내신', '내신'),
    ('학생부', '학생부'),
    ('중등', '중등'),
)

#deploy check
tuitionchoice=(
    (1600, '160000 (4주/16만원)'),
    (1800, '180000 (4주/18만원)'),
    (2000, '200000 (4주/20만원)'),
    (2200, '220000 (4주/22만원)'),
    (2400, '240000 (4주/24만원)'),
    (2600, '260000 (4주/26만원)'),
    (2800, '280000 (4주/28만원)'),
    (3000, '300000 (4주/30만원)'),
    (3200, '320000 (4주/32만원)'),
)



schoolchoice = []
for i in schoollist:
    schoolchoice.append((i, i))

