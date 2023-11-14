import tldextract
import validators
import json
def count(word: list):
    #longest word
    maxLength = max(word, key=len)
    #count mart
    mc=[x.lower() for x in word].count("mart")
    #change URL for Domain If is the longest
    word[word.index(maxLength)]= tldextract.extract(maxLength).domain if  validators.url(maxLength) == True else maxLength
    maxLength= tldextract.extract(maxLength).domain if  validators.url(maxLength) == True else maxLength
    #Variables Temp
    end,nL,enc,uc,lc=dict(),dict(),'',0,0
    #Count Letters and erase Special Characters
    for i in maxLength:
        if str(i).isalpha(): #evaluate Character
            num = ord(str(i))
            num += 3 if len(maxLength) > 25 else len(maxLength) #number for encrypt
            #Count each letter
            nL[str(i).lower()]=nL.get(i,0)+1

            if str(i).isupper():
                uc+=1
                if num > ord('Z'):num -= 26
                elif num < ord('A'):num += 26
            else:
                lc+=1
                if num > ord('z'):num -= 26
                elif num < ord('a'):num += 26
            enc +=chr(num)
    #Create Dictionary answer
    end["Uppercase"]=uc
    end["Lowercase"]=lc
    end["Specialcase"]=len(maxLength)-uc-lc
    end["Caesar Encryption"]=enc
    end["length"] = len(maxLength)
    end["MART appear"] = mc
    end["Count letter"] = nL
    return end

if __name__ == '__main__':
    # print("url")  # Aqui pego todas las URLS
    lista = ["casa", "perro", "ConejiTO", "oso", "tejon","https://j2logo.com/python", "AbCdEfGhIjK", "QueOndaMipez!", "Mart", "MART", "MaRt", "mart"]
    print(count(lista))
    # print("json Format")
    # json_object = json.dumps(lista, indent=4)
    # print(json_object)
