from app import db
class img_upload(db.Model):
    __tablename__ = 'imgdir_table'

    
    img_type = db.Column(db.String())
    imgdir = db.Column(db.Text,primary_key=True)

    def __init__(self, img_type, imgdir):
        self.img_type = img_type
        self.imgdir = imgdir

    # def __repr__(self):
    #     return '<id {}>'.format(self.name)

    # def serialize(self):
    #     return {
    #         'img_type': self.img_type,
    #         'imgdir': self.imgdir,
    #     }