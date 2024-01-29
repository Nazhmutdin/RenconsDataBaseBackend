from sqlalchemy import event

from app.db_engine import get_session


class SQLalchemyUnitOfWork:
    def __enter__(self):
        self.session = get_session()
        self.connection = self.session.connection()
        self.engine = self.connection.engine
        self.count = 0

        event.listen(self.engine, "before_cursor_execute", self.callback)

        return self


    def __exit__(self, *args, **kwargs):
        self.session.close()
        event.remove(self.engine, "before_cursor_execute", self.callback)

    
    def commit(self) -> None:
        self.session.commit()


    def rollback(self) -> None:
        self.session.rollback()


    def callback(self, *args, **kwargs) -> None:
        self.count += 1
