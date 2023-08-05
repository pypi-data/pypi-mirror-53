from .domains.domain import Domain
from .rdata import rdata_cls
from bitstring import BitArray
from triton.dns.message.rdata import ResourceRecord

class Answer:
    class _Binary:
        def __init__(self, answer):
            self.answer = answer

        @property
        def full(self):
            print('encoding')
            result = self.answer._name.encode(self.answer.message) if self.answer._name else ''
            result += bin(self.answer._type)[2:].zfill(16)
            result += bin(self.answer._cls)[2:].zfill(16)
            result += bin(self.answer._ttl)[2:].zfill(32)
            result += bin(self.answer.rdlength)[2:].zfill(16)
            result += self.answer._rdata.Binary.full
            self.answer.message.offset += int(len(result) / 8)
            return result

        @property
        def full_canonical(self):
            result = self.answer._name.sub_encode(self.answer._name.label) if self.answer._name else ''
            result += bin(self.answer._type)[2:].zfill(16)
            result += bin(self.answer._cls)[2:].zfill(16)
            result += bin(self.answer._ttl)[2:].zfill(32)
            result += bin(self.answer.rdlength)[2:].zfill(16)
            result += self.answer._rdata.Binary.full
            if self.answer.message:
                self.answer.message.offset += int(len(result) / 8)
            return result

        @property
        def full_bytes(self):
            return BitArray(bin=self.full).bytes

        @property
        def full_canonical_bytes(self):
            return BitArray(bin=self.full_canonical).bytes

    def __init__(self, message):
        self.message = message
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, message):
        answer = cls(message)
        answer._name = Domain.decode(message)
        answer._type = message.stream.read('uint:16')
        answer._cls = message.stream.read('uint:16')
        answer._ttl = message.stream.read('uint:32')
        answer._rdlength = message.stream.read('uint:16')
        answer._rdata = await rdata_cls[int(answer._type)].parse_bytes(answer, answer._rdlength)
        return answer

    @classmethod
    async def parse_dict(cls, message, data):
        answer = cls(message)
        answer._name = Domain(data.get('name'), None)
        answer._type = data.get('type')
        answer._cls = data.get('class')
        answer._ttl = data.get('ttl')
        answer._rdata = await rdata_cls[int(answer._type)].parse_dict(answer, data.get('rdata'))
        return answer

    @property
    def rdlength(self):
        return int(len(self._rdata.Binary.full) / 8)

    @property
    def name(self):
        return self._name.label

    @property
    def type(self):
        return ResourceRecord.find_subclass_by_id(self._type).__name__

    @property
    def cls(self):
        return self.cls

    @property
    def ttl(self):
        return self._ttl

    @property
    def rdata(self):
        return self._rdata

    # def __dct__(self):
    #     return {'name': self._name.label,
    #             'type': self._type,
    #             'class': self._cls,
    #             'ttl': self._ttl,
    #             'rdata': self._rdata.__dict__}

    def __mydict__(self):
        return {'name': self._name.label if self._name else '',
                'type': self._type,
                'class': self._cls,
                'ttl': self._ttl,
                'rdata': self._rdata.__dict__}

    def __repr__(self):
        return str({'name': self._name.label if self._name else '',
                    'type': self.type,
                    'class': self._cls,
                    'ttl': self._ttl,
                    'rdata': self._rdata})


class AnswerStorage:
    class _Binary:
        def __init__(self, storage):
            self.storage = storage

        @property
        def full(self):
            result = ''
            for answer in self.storage.storage:
                answ_res = answer.Binary.full
                # self.storage.message.offset += int(len(answ_res) / 8)
                result += answ_res
            return result

    def __init__(self, message):
        self.message = message
        self.storage = []
        self.Binary = self._Binary(self)

    def append(self, answer: Answer):
        assert isinstance(answer, Answer), f'What the heck is that {self.__class__.__name__.lower()}?'
        self.storage.append(answer)

    @classmethod
    async def parse_dict(cls, message, data):
        instance = cls(message)
        for x in data:
            instance.append(await Answer.parse_dict(message, x))
        return instance

    def __len__(self):
        return len(self.storage)

    def __bool__(self):
        return True if self.storage else False

    def __iter__(self):
        return (x for x in self.storage)

    def __mydict__(self):
        return [x.__mydict__ for x in self.storage]

    def __getitem__(self, item):
        return self.storage[item]

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __delitem__(self, key):
        self.storage.pop(key)

    def __repr__(self):
        return '['+','.join([a.__repr__() for a in self.storage])+']'
