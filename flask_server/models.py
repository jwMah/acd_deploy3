from app import db
from sqlalchemy import ForeignKey, sql
class video_table(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.INTEGER,primary_key=True)
    video_type = db.Column(db.VARCHAR(100))
    contents_name = db.Column(db.VARCHAR(255))
    location = db.Column(db.Text)
    censored = db.Column(db.VARCHAR(50))
    create_time = db.Column(db.DateTime(timezone=True))
    update_time = db.Column(db.DateTime(timezone=True))

    # img_type = db.Column(db.String())
    # imgdir = db.Column(db.Text,primary_key=True)
    # sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now())
    def __init__(self, video_type, contents_name, location):
        self.video_type=video_type
        self.contents_name = contents_name
        self.location = location
        self.censored = None
        self.create_time = sql.func.now()
        self.update_time = None

class img_table(db.Model):
    __tablename__ = 'contents_analysis'

    id = db.Column(db.INTEGER, primary_key=True)
    contents_id = db.Column(db.INTEGER, ForeignKey('contents.id'))
    location = db.Column(db.VARCHAR(512))
    file_name = db.Column(db.VARCHAR(512))
    time_frame = db.Column(db.INTEGER)
    ml_censored = db.Column(db.VARCHAR(50))
    admin_censored = db.Column(db.VARCHAR(50))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def __init__(self, contents_id, location, file_name, time_frame, ml_censored):
        self.contents_id = contents_id
        self.location = location
        self.file_name = file_name
        self.time_frame = time_frame
        self.ml_censored = ml_censored
        self.admin_censored = None
        self.create_time = sql.func.now()
        self.update_time = None