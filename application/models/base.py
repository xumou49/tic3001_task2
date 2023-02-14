import datetime
from mongoengine import Document, DateTimeField
from datetime import datetime


class BaseDocument(Document):
    created_at = DateTimeField()
    updated_at = DateTimeField()
    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super().save(*args, **kwargs)

    def to_dict(self):
        res = {}
        for k in self._db_field_map:
            if k in frozenset(('created_at', 'updated_at')):
                continue
            if v := getattr(self, k):
                res[k] = v
        if 'id' in res:
            res["id"] = str(self["id"])
        if 'birthday' in res:
            res['birthday'] = res['birthday'].strftime('%Y-%m-%d')
        return res

