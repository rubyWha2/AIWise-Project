class FakeCursor:
    def __init__(self, *, fetchone=None, fetchall=None, rowcount=1):
        self.fetchone_values = list(fetchone or [])
        self.fetchall_value = fetchall or []
        self.rowcount = rowcount
        self.queries = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def execute(self, query, params=None):
        self.queries.append((query, params))

    def fetchone(self):
        if self.fetchone_values:
            return self.fetchone_values.pop(0)
        return None

    def fetchall(self):
        return self.fetchall_value


class FakeConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


def login_as(client, user_id=1, username="admin1", role_id=1):
    with client.session_transaction() as session:
        session["user_id"] = user_id
        session["username"] = username
        session["role_id"] = role_id
