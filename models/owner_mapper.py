import xml.etree.ElementTree as ET



def getPostNumber(session, postnumber postOffice):
    pn = SqlHandler.getPostNumber(session, postnumber)
    if pn:
        return {"postnumber": pn, "post_office":SqlHandler.getPostOffice(session, postOffice)}
    else:
        po = SqlHandler.PostOffice(postOffice)
        SqlHandler.addItem(session,po)
        pn = SqlHandler.PostNumber(postnumber)
        SqlHandler.addItem(session,pn)
        return {"postnumber": pn, "post_office":po}






def addOwners():
    #modify map table to work with mapped xml file
    owner_map = {"omistaja"     : "name",
                 "osoite"       : "address",
                 "postinumero"  : getPostNumber,
                 "sahkoposti"   : "email",
                 "arkisto"      : "archive"
                 }
    
    tree = ET.parse('Omistajat.xml')
    root = tree.getroot()

    owner_list = []
    for child in root:
        param_dict = {}
        for tag in child:
            if tag.tag in owner_map:
                if isinstance(owner_map[tag.tag], str):
                    if tag.text:
                        param_dict[owner_map[tag.tag]] = tag.text
                else:
                    param_dict.update(owner_map[tag.tag](session,tag.text,child.find("postitoimipaikka").text))
        if valid_owner(param_dict):
            owner_list.append(SqlHandler.Owner(param_dict))

    SqlHandler.addItems(owner_list)

        







