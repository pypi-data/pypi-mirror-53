'''
persist data to db
'''
from datetime import date
import json
from peewee import *
import logging
db = SqliteDatabase('bus.db')

logger = logging.getLogger(__name__)


class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class ExistError(Exception):
    pass


class Item(BaseModel):
    '''
    item table
    '''
    title = CharField()
    fanhao = CharField()
    url = CharField(unique=True)
    add_date = DateField()
    meta_info = TextField()

    def __repr__(self):
        return f'<Item {self.title}>'

    @staticmethod
    def saveit(meta_info):
        item_add_date = date.fromisoformat(meta_info.pop('add_date'))
        item_fanhao = meta_info.pop('fanhao')
        item_title = meta_info.pop('title')
        item_url = meta_info.pop('url')
        item_meta = json.dumps(meta_info)
        try:
            item = Item.create(fanhao=item_fanhao, title=item_title, url=item_url,
                               add_date=item_add_date, meta_info=item_meta)
            logger.debug(f'save item:  {item}')
        except IntegrityError as ex:
            raise ExistError()
        return item


class Tag(BaseModel):
    '''
    tag table
    '''
    type_ = CharField(column_name='type')
    value = CharField(unique=True)
    url = CharField()

    def __repr__(self):
        return f'<Tag {self.value}>'

    @staticmethod
    def saveit(tag_info):
        try:
            tag = Tag.create(type_=tag_info.type, value=tag_info.value,
                             url=tag_info.link)
            logger.debug(f'save tag:  {tag}')
        except IntegrityError as ex:
            tag = Tag.get(Tag.value == tag_info.value)

        return tag


class ItemTag(BaseModel):
    item = ForeignKeyField(Item, backref='tags')
    tag = ForeignKeyField(Tag, backref='items')

    @staticmethod
    def saveit(item, tag):
        try:
            item_tag = ItemTag.create(item=item, tag=tag)
            logger.debug(f'save tag_item: {item_tag}')
        except Exception as ex:
            logger.exception(ex)

        return item_tag

    def __repr__(self):
        return f'<ItemTag {self.item.title} - {self.tag.value}>'


def save(meta_info, tags):
    item_title = meta_info['title']
    try:
        item = Item.saveit(meta_info)
    except ExistError:
        logger.debug(f'item exists: {item_title}')
    else:
        for tag_info in tags:
            tag = Tag.saveit(tag_info)
            ItemTag.saveit(item, tag)


def test_save():
    item_url = 'https://www.cdnbus.bid/MADM-116'
    item_title = 'test item'
    item_add_date = date(2019, 7, 19)
    item_meta_info = ''
    item = Item(title=item_title, url=item_url,
                add_date=item_add_date, meta_info=item_meta_info)
    item.save()

    tag1 = Tag.create(type_='genre', value='素人',
                      url='https://www.cdnbus.bid/genre/s1')
    tag2 = Tag.create(type_='star', value='樱田',
                      url='https://www.cdnbus.bid/star/dbd')
    tag3 = Tag.create(type_='genre', value='高清',
                      url='https://www.cdnbus.bid/genre/x1')
    ItemTag.create(item=item, tag=tag1)
    ItemTag.create(item=item, tag=tag2)


def init():
    db.connect()
    db.create_tables([Item, Tag, ItemTag])


init()
