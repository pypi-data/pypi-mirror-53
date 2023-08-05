
class Algorithm:
    id = 0


    @classmethod
    async def verify_rrset(cls,key,  rrset, rrsig):
        pass

    @classmethod
    def find_by_id(cls, id):
        for subtype in Algorithm.__subclasses__():
            for subclass in subtype.__subclasses__():
                if subclass.id == id:
                    return subclass
        else:
            raise Exception('Unknown algorithm id')

    @classmethod
    def sign_rrset(cls, key, rrset):
        pass