import json

def upload(gridfsObject, fileObj):
    fid = gridfsObject.put(fileObj)
    if fid:
        return fid, "File uploaded successfully - {fileObj}"

    
    # message = {
    #     "video_fid" : str(fid),
    #     "mp3_fid" : None,
    #     "username": access["username"],
    # }

    # try:
    #     channel.basic_publish(
    #         exchange="",
    #         routing_key="video",
    #         body = json.dumps(message),
    #         properties = pika.BasicProperties(
    #             delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
    #         ),
    #     )
    # except Exception as err:
    #     fs.delete(fid)
    #     return err , 500
