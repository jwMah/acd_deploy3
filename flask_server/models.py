from app import db
class img_upload(db.Model):
    __tablename__ = 'adult_detector_db'

    
    id = db.Column(db.Integer,primary_key=True)
    video_name = db.Column(db.String())
    imgdir = db.Column(db.Text)
    time = db.Column(db.String(6))
    censored = db.Column(db.Integer)

    def __init__(self, video_name, imgdir, time, censored):
        self.video_name = video_name
        self.imgdir = imgdir
        self.time = time
        self.censored = censored

    # def __repr__(self):
    #     return '<id {}>'.format(self.name)

    # def serialize(self):
    #     return {
    #         'img_type': self.img_type,
    #         'imgdir': self.imgdir,
    #     }