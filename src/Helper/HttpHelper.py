def getContentLength(content: dict) -> str:
    try:
        return str(len("​id=%s&roomid=%s&type=%s&csrf_token=%s&csrf=%s&visit_id=" % (
            content.get('id'), content.get('roomid'), content.get('keyword'), content.get('csrf_token'), content.get('csrf')))-1)
    except:
        raise KeyError
        return "0"


def addRecordMsg(record: dict, roomid: str, msg: str, success=-1):
    try:
        if success != -1:
            record['score'] += success
        record.get('values').append(
            {'success': success, 'message': ("%s roomid=%s" % (msg, roomid))})
    except:
        raise KeyError
