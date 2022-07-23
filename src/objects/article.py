class Article():
    def __init__(self, link, locFlag, coords, infobox, ibcontent, articleGraph, templates, 
            infoboxWkts, wikidataWkts, wikidataEntity, wikidata_one_hop_graph, parent_locations_and_relation,
            classes_with_labels, dates, times, microformats, datePublished, dateModified):
        self.link = link
        self.locFlag = locFlag
        self.coords = coords
        self.infobox = infobox
        self.ibcontent = ibcontent
        self.infoboxWkts = infoboxWkts
        self.wikidataWkts = wikidataWkts
        self.wikidataEntity = wikidataEntity
        self.wikidata_one_hop_graph = wikidata_one_hop_graph
        self.parent_locations_and_relation = parent_locations_and_relation
        self.classes_with_labels = classes_with_labels
        self.dates = dates
        self.times = times
        self.microformats = microformats
        self.datePublished = datePublished
        self.dateModified = dateModified
        
    
    