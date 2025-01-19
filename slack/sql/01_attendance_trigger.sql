DELIMITER //

CREATE TRIGGER insert_trigger
AFTER INSERT ON attendance
FOR EACH ROW
BEGIN
    DECLARE cmd VARCHAR(255);
    DECLARE event_type VARCHAR(10);

    -- case_1 : '출결' 메뉴에 새롭게 글이 작성됨 (attendance) : 매니저
    SET event_type = 'INS01';

    -- API 서버로 이벤트 전달 (curl 명령 실행)
    SET cmd = CONCAT(
        'curl -X POST -H "Content-Type: application/json" ',
        '-d \'{"event_type": "', event_type, '", "reference_id": "', NEW.id, '"}\' ',
        'http://api_server:8000/events'
    );
    DO sys_exec(cmd); -- MariaDB의 sys_exec() 사용
END;
//

DELIMITER //
