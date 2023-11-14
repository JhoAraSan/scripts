from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.items import ListEntity,ListsEntity
from models.model_db import Dict_list,Item
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT,HTTP_401_UNAUTHORIZED

import tldextract
import validators

list_data = APIRouter()

@list_data.get('/list_db/{password}', response_model=list[Dict_list], tags=["Control DB"])
def all_list(password:str):
    if password == "Delete":
        x=conn.local.lista.find()
    else:
        x=[]
    return ListsEntity(x)


@list_data.delete('/list_db/{id}:{password}',status_code=status.HTTP_204_NO_CONTENT, tags=["Control DB"])
def delete_list(id:str,password:str):
    if password == "Delete":
        ListEntity(conn.local.lista.find_one_and_delete({"_id": ObjectId(id)}))
        x=Response(status_code=HTTP_204_NO_CONTENT)
    else:
        x=Response(status_code=HTTP_401_UNAUTHORIZED)
    return x

@list_data.post("/readlist",response_model=dict, tags=["Longest"])
def count(word: Item):
#longest word
    maxLength = max(word.Items, key=len)
    #count mart
    mc=[x.lower() for x in word.Items].count("mart")
    #change URL for Domain If is the longest
    word.Items[word.Items.index(maxLength)]= tldextract.extract(maxLength).domain if  validators.url(maxLength) == True else maxLength
    maxLength= tldextract.extract(maxLength).domain if  validators.url(maxLength) == True else maxLength
    print(maxLength)
    #Variables Temp
    end,nL,enc,uc,lc=dict(),dict(),'',0,0
    #Count Letters and Special Characters
    for i in maxLength:
        #Count each letter
        nL[str(i).lower()]=nL.get(i,0)+1
        if str(i).isalpha(): #evaluate Character
            num = ord(str(i))
            num += 3 if len(maxLength) > 25 else len(maxLength) #number for encrypt
            if str(i).isupper():
                uc+=1
                if num > ord('Z'):num -= 26
                elif num < ord('A'):num += 26
            else:
                lc+=1
                if num > ord('z'):num -= 26
                elif num < ord('a'):num += 26
            enc +=chr(num)
        else:
            enc +=i
    #Create Dictionary answer
    end["Uppercase"]=uc
    end["Lowercase"]=lc
    end["Other characters"]=len(maxLength)-uc-lc
    end["Caesar Encryption"]=enc
    end["length"] = len(maxLength)
    end["MART appear"] = mc
    end["Count Character"] = nL
    new_list ={"lt":word.Items,"answer":end}
    id = conn.local.lista.insert_one(new_list).inserted_id
    lista = conn.local.lista.find_one({"_id":id})
    return ListEntity(lista)