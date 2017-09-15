
def overlap(bbox1, bbox2):
    area1 = bbox1["width"] * bbox1["height"]
    area2 = bbox2["width"] * bbox2["height"]
    x1 = max(bbox1["left"], bbox2["left"])
    y1 = max(bbox1["top"], bbox2["top"])
    x2 = min(bbox1["left"] + bbox1["width"], bbox2["left"] + bbox2["width"])
    y2 = min(bbox1["top"] + bbox1["height"], bbox2["top"] + bbox2["height"])
    area_o = (x2-x1) * (y2-y1)
    if x2 < x1 or y2 < y1:
        area_o = 0
    return area_o / min(area1, area2)

def merge_ct(ct_hf, ct_bd):
    for ct_hf_item in ct_hf["result"]:
        for ct_bd_item in ct_bd["result"]:
            if overlap(ct_hf_item["location"], ct_bd_item["location"]) > 0.5:
                for key in ct_bd_item.keys():
                    ct_hf_item[key] = ct_bd_item[key]

def keywithmaxval(d):
    """ a) create a list of the dict's keys and values; 
     b) return the key with the max value"""  
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))]