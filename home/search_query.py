from .models import Item

def makeQuery(search_tags, search_category):
    search_tags = [t.strip().lower() for t in search_tags]
    query = []
    tags_length = len(search_tags)

    for i in range(tags_length):
        if search_category == 'all':
            items = Item.objects.filter(subcategory=search_tags[i], in_search=True, searchable=True)
        else:
            items = Item.objects.filter(category=search_category,subcategory=search_tags[i], in_search=True, searchable=True)
        query.extend(items)

    all_items = Item.objects.all()
    for index, item in enumerate(all_items):
        tags = [tag.strip().lower() for tag in item.search_tags.split(',')]
        common_tags = list(set(tags).intersection(set(search_tags)))
        if item.in_search == True and item.searchable == True:
            if search_category == 'all':
                if len(common_tags) > 0:
                    query.append(item)
            else:
                if len(common_tags) > 0 and item.category == search_category:
                    query.append(item)

    query = list(set(query))

    return query