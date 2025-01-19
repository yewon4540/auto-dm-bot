DELIMITER //

CREATE TRIGGER insert_teacher_attendance_trigger
AFTER INSERT ON attend_teacher_detail
FOR EACH ROW
BEGIN
    DECLARE cmd VARCHAR(255);
    DECLARE event_type VARCHAR(10);

    -- case_4 : 강사 출결에서 출석 외 다른 건이 체크된 경우
    -- (1) 지각인 경우
    IF NEW.type = '지각' THEN
        SET event_type = 'INS04'; -- 매니저 + 교육생 알림
    END IF;

    -- API 서버로 이벤트 전달 (curl 명령 실행)
    IF event_type IS NOT NULL THEN
        SET cmd = CONCAT(
            'curl -X POST -H "Content-Type: application/json" ',
            '-d \'{"event_type": "', event_type, '", "reference_id": "', NEW.id, '"}\' ',
            'http://api_server:8000/events'
        );
        DO sys_exec(cmd);
    END IF;
END;
//

DELIMITER //
