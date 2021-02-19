import io
import logging
import base64
import random
import names
import lorem
import py_avataaars
from PIL import Image
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

try:
    import database
    from issue import Issue
except ImportError:
    import adminpanel.database as database
    from adminpanel.issue import Issue

def r(enum_):
        return random.choice(list(enum_))

def get_issue() -> Issue:
    bytes_ = io.BytesIO()
    py_avataaars.PyAvataaar(
        style=py_avataaars.AvatarStyle.CIRCLE,
        # style=py_avataaars.AvatarStyle.TRANSPARENT,
        skin_color=r(py_avataaars.SkinColor),
        hair_color=r(py_avataaars.HairColor),
        facial_hair_type=r(py_avataaars.FacialHairType),
        facial_hair_color=r(py_avataaars.FacialHairColor),
        top_type=r(py_avataaars.TopType),
        hat_color=r(py_avataaars.ClotheColor),
        mouth_type=r(py_avataaars.MouthType),
        eye_type=r(py_avataaars.EyesType),
        eyebrow_type=r(py_avataaars.EyebrowType),
        nose_type=r(py_avataaars.NoseType),
        accessories_type=r(py_avataaars.AccessoriesType),
        clothe_type=r(py_avataaars.ClotheType),
        clothe_color=r(py_avataaars.ClotheColor),
        clothe_graphic_type=r(py_avataaars.ClotheGraphicType),
    ).render_png_file(bytes_)
    pillow_img = Image.open(bytes_)
    resized_img = pillow_img.resize((100, 100))
    resized_bytes = io.BytesIO()
    resized_img.save(resized_bytes, format='PNG')
    image = base64.encodebytes(resized_bytes.getvalue()).decode().replace('\n','')
    issue = Issue(id= database.get_next_id(threading = True),
        author=names.get_full_name(),
        subject=lorem.get_sentence(),
        description=lorem.get_paragraph(random.randint(1,4)), date=str(datetime.now()),
        image= image)
    return issue

def issue_scheduler(interval=0.5):
    def callback():
        logging.info('Creating new synthetical issue')
        database.add_issue(get_issue(), threading = True)
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    scheduler.add_job(callback, 'interval', minutes=interval)
    scheduler.start()
