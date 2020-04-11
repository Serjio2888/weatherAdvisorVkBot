import psycopg2
from weatherAdvisorVkBot.credentials import host, port, db_pass, db_name, username


def connect():
    conn = psycopg2.connect(host=host,
                            port=port,
                            database=db_name,
                            user=username,
                            password=db_pass)
    return conn


def get_user_info(uid):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("Select uid, name, city from vkuser where uid=%s", (uid,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return record, True
    else:
        return "No such user", False


def update_town(uid, town):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE vkuser set city=%s where uid=%s",
                   (town, uid))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def update_timer(hour, uid):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE vkuser set timer=%s where uid=%s",
                   (hour, uid))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def add_user(uid, town, name, surname):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vkuser (uid, city, name, surname) VALUES(%s, %s, %s, %s)",
                   (uid, town, name, surname))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_users_by_time(now):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("Select uid, name, city, timer from vkuser where timer=%s", (now,))
    records = cursor.fetchall()
    users = []
    flag = False
    if len(records):
        for record in records:
            users.append({"uid": record[0], "name": record[1], "city": record[2], "timer": record[3]})
            flag = True
    cursor.close()
    conn.close()
    return users, flag

