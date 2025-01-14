DELIMITER //

CREATE TRIGGER insert_trigger
-- case_1 : '출결' 메뉴에 새롭게 글이 작성됨 (attendance) : 매니저
-- case_2 : '클래스룸 게시판' 에 새롭게 글이 작성됨 (board / cno != 1) : 해당 채널
-- case_3 : '전체 공지사항' 에 새롭게 글이 작성됨 (board / cno = 1) : 모든 채널
-- case_4 : '강사 출결' 에 출석 외의 다른 건이 체크된 경우 (attend_teacher_detail) : 매니저 + 교육생
AFTER INSERT ON attendance
FOR EACH ROW
BEGIN
    DECLARE cmd VARCHAR(255);

    -- API 서버로 이벤트 전달 (curl 명령 실행)
    
    SET cmd = CONCAT(
        'curl -X POST -H "Content-Type: application/json" ',
        '-d \'{"event_type": "INSERT", "reference_id": "', NEW.id, '"}\' ',
        'http://api_server:8000/events'
    );
    DO sys_exec(cmd); -- MariaDB의 sys_exec() 사용
END;
//

DELIMITER ;
