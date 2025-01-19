DELIMITER //

CREATE TRIGGER insert_board_trigger
AFTER INSERT ON board
FOR EACH ROW
BEGIN
    DECLARE cmd VARCHAR(255);
    DECLARE event_type VARCHAR(10);

    -- case_2 : '클래스룸 게시판' (cno != 1)
    -- case_3 : '전체 공지사항' (cno = 1)
    IF NEW.cno = 1 THEN
        SET event_type = 'INS03'; -- 전체 공지사항
    ELSE
        SET event_type = 'INS02'; -- 클래스룸 게시판
    END IF;

    -- API 서버로 이벤트 전달 (curl 명령 실행)
    SET cmd = CONCAT(
        'curl -X POST -H "Content-Type: application/json" ',
        '-d \'{"event_type": "', event_type, '", "reference_id": "', NEW.id, '"}\' ',
        'http://api_server:8000/events'
    );
    DO sys_exec(cmd);
END;
//

DELIMITER //
