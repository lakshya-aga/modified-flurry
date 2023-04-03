import orjson
import os
import sys
import time

from collections import defaultdict
import flake.src.flake.filters.filter as filter

master_node_dict = defaultdict()

class W3CFilter(filter.Filter):
    """
    Initialize the filter.
    """
    def __init__(self):
        filter.Filter.__init__(self)
        master_node_dict.clear()
        print(" -----------------------------------------   W3C INIT ----------------------------------------------")
        print("\n W3C :", master_node_dict)
        print(" Total Length Master Dict: ", len(master_node_dict))

    def parse_nodes_for_edge(self, prov_type, values):
        src_node = ""
        dst_node = ""

        if prov_type == "wasGeneratedBy":
            src_node = values["prov:entity"]
            dst_node = values["prov:activity"]
        elif prov_type == "used":
            src_node = values["prov:activity"]
            dst_node = values["prov:entity"]
        elif prov_type == "wasInformedBy":
            src_node = values["prov:informant"]
            dst_node = values["prov:informed"]
        elif prov_type == "wasInfluencedBy":
            src_node = values["prov:influencee"]
            dst_node = values["prov:influencer"]
        elif prov_type == "wasAssociatedWith":
            src_node = values["prov:agent"]
            dst_node = values["prov:activity"]
        elif prov_type == "wasDerivedFrom":
            src_node = values["prov:generatedEntity"]
            dst_node = values["prov:usedEntity"]
        # not currently supported by CamFlow
        elif prov_type == "wasStartedBy" or prov_type == "wasEndedBy":
            src_node = values["prov:trigger"]
            dst_node = values["prov:activity"]
        elif prov_type == "wasInvalidatedBy":
            src_node = values["prov:activity"]
            dst_node = values["prov:entity"]
        elif prov_type == "wasAttributedTo":
            src_node = values["prov:entity"]
            dst_node = values["prov:agent"]
        elif prov_type == "actedOnBehalfOf":
            src_node = values["prov:delegate"]
            dst_node = values["prov:responsible"]
        elif prov_type == "specializationOf":
            src_node = values["prov:specificEntity"]
            dst_node = values["prov:generalEntity"]
        return src_node, dst_node

    def load_data(self, data, G):
        object = orjson.loads(data)
        features = {}
        type = ""
        #print("\n MASTER LOAD DATA CALLED")
        #print("\n MASTER DICT BEFORE")
        #print(master_node_dict)
        

        for prov_type in object:

            if prov_type == "activity":
                for node in object[prov_type]:
                    features = object[prov_type][node]
                    if self.node_granularity == "fine":
                        type = object[prov_type][node]["prov:type"]
                    else:
                        type = prov_type
                    id = G.add_node(type, features)
                    master_node_dict[node] = id
                    #print("  Master Push Activity: ",master_node_dict[node], " Type : ", type)

            elif prov_type == "entity":
                for node in object[prov_type]:
                    if "cf:camflow" in object[prov_type][node]:
                        continue
                    features = object[prov_type][node]
                    if self.node_granularity == "fine":
                        type = object[prov_type][node]["prov:type"]
                    else:
                        type = prov_type
                    id = G.add_node(type, features)
                    master_node_dict[node] = id
                    #print("  Master Push Entity: ",master_node_dict[node], " Type : ", type)

            elif prov_type == "agent":
                for node in object[prov_type]:
                    features = object[prov_type][node]
                    if self.node_granularity == "fine":
                        type = object[prov_type][node]["prov:type"]
                    else:
                        type = prov_type
                    id = G.add_node(type, features)
                    master_node_dict[node] = id
                    #print("  Master Push Agent: ",master_node_dict[node], " Type : ", type)

            elif prov_type == "prefix":
                continue
            else:
                for edge in object[prov_type]:
                    features = object[prov_type][edge]
                    jiffies = int(object[prov_type][edge]["cf:jiffies"])
                    if self.edge_granularity == "fine":
                        type = object[prov_type][edge]["prov:type"]
                    else:
                        type = prov_type
                    src_node, dst_node = self.parse_nodes_for_edge(prov_type, features)
                    if src_node in master_node_dict and dst_node in master_node_dict:
                        #print(" Total Length Master Dict: ", len(master_node_dict))
                        #print(features)
                        #print(" Master Dict: \n", master_node_dict)
                        #for key, value in master_node_dict.items():
                        #  print("  Master Value: ",value," key: ", key)
                        G.add_edge(type, master_node_dict[src_node], master_node_dict[dst_node], features, jiffies)
            #print("\n  DATA\n",data)
            #print("\n MASTER DICT AFTER")
            #print(master_node_dict)
            
            #Print Master Dict
            #for key, value in master_node_dict.items():
            #   print("  Master Value: ",value," key: ", key)
            #print("\n\n Total Length Master Dict: ", len(master_node_dict))
            #print("\n MASTER DICT CLEANED")
            #master_node_dict.clear()
            #print(master_node_dict)

    """
    Load the specified graph from file, using the filter to parse the data.
    params: input_path, the full file path to the camflow data.
    params: G, the flake object we are loading to
    """
    def load_data_from_file(self, data, G):
        print("Loading data now...")
        logcount = 0
        start = time.time()
        for line in data:
            load_data(line[0], G)
            logcount +=1
            if logcount % 5000 == 0:
                end = time.time()
                hours, rem = divmod(end-start, 3600)
                minutes, seconds = divmod(rem, 60)
                print("loaded " + str(round(((logcount/len(json_data))*100), 2)) + "% of data in " +
                    ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)) + " seconds.")
                start = time.time()
        print("Data loaded! Added " + str(logcount) + " logs.")
