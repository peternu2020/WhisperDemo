import main as buckets
import dynamo as db
import uuid

b = buckets.b

#for obj in b.objects.all():
#    print(obj.key)
#db.putId('asdf', '1', 'sample speech to text')

#a = db.getIdByRp(1)

def postToCloud(file, id, rpId, txt):
    # file = .wav
    # id = unique ID from server
    # rpId = which rasberrypi {1,2,3,4} for now
    # txt = the speech to text
    print("Uploading to cloud")
    buckets.uploadFileToAws(file)
    db.putId(id,rpId,txt)
    return 

def retrieveByRasberryPiId(id):
    lst = db.getId(id)
    return lst

#postToCloud("crucifixion1.wav", "1", hex(uuid.getnode()),"honestly this did not stand out much compared to the many depictions of the crucifixion the only original part was the swan in the birds overlooking it as Christ is supposed to")
print(retrieveByRasberryPiId("1"))