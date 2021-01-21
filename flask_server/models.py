from app import db

class img_upload(db.Model):
    __tablename__ = 'adult_detector_db'

    id = db.Column(db.INTEGER,primary_key=True)
    video_name = db.Column(db.VARCHAR)
    imgdir = db.Column(db.Text)
    time = db.Column(db.VARCHAR(6))
    censored = db.Column(db.INTEGER)

    # img_type = db.Column(db.String())
    # imgdir = db.Column(db.Text,primary_key=True)

    def __init__(self, video_name, imgdir, time, censored):
        self.video_name = video_name
        self.imgdir = imgdir
        self.time = time
        self.censored = censored
