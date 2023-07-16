from datetime import date

from plancoach.variables import banklist, schoollist, subjectlist, current_date

schoolyearchoice = []
for i in range(12, int(current_date.strftime("%y")) + 1):
    schoolyearchoice.append((i, i))

yearchoice = []
for i in range(2015, int(current_date.strftime("%Y")) + 1):
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
    ('denied', '거절'),
    ('waiting', '입금대기'),
    ('ongoing', '진행중'),
)



agechoice=(
    ('graden', 'N수'),
    ('grade3', '3학년'),
    ('grade2', '2학년'),
    ('grade1', '1학년'),
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
    ('논술', '논술'),
)


tuitionchoice=(
    (16, '160000 (4주/16만원)'),
    (18, '180000 (4주/18만원)'),
    (20, '200000 (4주/20만원)'),
    (22, '220000 (4주/22만원)'),
    (24, '240000 (4주/24만원)'),
    (26, '260000 (4주/26만원)'),
    (28, '280000 (4주/28만원)'),
    (30, '300000 (4주/30만원)'),
    (32, '320000 (4주/32만원)'),
)



schoolchoice = []
for i in schoollist:
    schoolchoice.append((i, i))

