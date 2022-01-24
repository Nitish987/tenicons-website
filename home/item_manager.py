from random import random
from .models import Item

class ItemManager:

    def __init__(self, item_id):
        self.item = Item.objects.get(item_id=item_id)

    def getItem(self):
        return self.item

    def getUserID(self):
        return self.item.uuid

    def getItemID(self):
        return self.item.item_id

    def getItemName(self):
        return self.item.name

    def getItemPath(self):
        return self.item.path

    def getItemCategory(self):
        return self.item.category

    def getSubcategory(self):
        return self.item.subcategory

    def getLikes(self):
        return self.item.likes

    def haveRightToLike(self):
        return self.item.right_to_like

    def isSearchable(self):
        return self.item.searchable

    def getDownloadsCount(self):
        return self.item.downloads_count

    def getDate(self):
        return self.item.date

    def getSearchTags(self):
        return self.item.search_tags

    def inSearch(self):
        return self.item.in_search

    def getLikeBy(self):
        return self.item.liked_by.split('|')

    # function
    def getLikeCount(self):
        return len(self.item.liked_by.split('|'))

def item_category(sno):
    category = ['image','icon','wallpaper','illustration']
    return category[sno - 1]

def item_category_sno(title):
    category = ['image','icon','wallpaper','illustration']
    return category.index(title) + 1

def item_subcategory(sno):
    subcategory = ['3d','abstract','animals','anime','art','black','cars','city','dark','fantasy','flowers','food','holidays','love','macro','minimalism','motorcycles','music','nature','similes','space','sports','technologies','textures','vector','words','quotes','girls','boys','others']
    return subcategory[sno - 1]

def item_subcategory_sno(title):
    subcategory = ['3d','abstract','animals','anime','art','black','cars','city','dark','fantasy','flowers','food','holidays','love','macro','minimalism','motorcycles','music','nature','similes','space','sports','technologies','textures','vector','words','quotes','girls','boys','others']
    return subcategory.index(title) + 1

# returns true if item exists
def item_exists(itemID):
    return Item.objects.filter(item_id=itemID).exists()

# creates an item
def create_item(uuid, itemName, path, category, subcategory, searchTags, liked_by):
    c = '1234567890'
    itemID = ''
    for i in range(20):
        itemID = itemID + c[int(random()*10)]

    item = Item(
        uuid=uuid,
        item_id=itemID,
        name=itemName,
        path=path,
        category=category,
        subcategory=subcategory,
        search_tags=searchTags,
        liked_by=liked_by,
    )
    return item

def create_item_download_name(default_item_name):
    name = default_item_name.split('.')
    c = '1234567890'
    item_name = ''
    for i in range(20):
        item_name = item_name + c[int(random() * 10)]
    return [item_name + '-' + 'tenicons.com.' + name[len(name) - 1], name[len(name) - 1]]