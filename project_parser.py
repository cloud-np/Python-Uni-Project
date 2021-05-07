from net import *
from node import *
from design import *
import re

path_to_nets = r"C:\Users\lenovo\Desktop\Python_Project\Python-Uni-Project\data\design.nets"
path_to_nodes = r"C:\Users\lenovo\Desktop\Python_Project\Python-Uni-Project\data\design.nodes"
path_to_pl = r"C:\Users\lenovo\Desktop\Python_Project\Python-Uni-Project\data\design.pl"
path_to_scl = r"C:\Users\lenovo\Desktop\Python_Project\Python-Uni-Project\data\design.scl"

def get_node_stats():

    # Make list here with size of len(nodes)
    nodes_list = []
    with open(path_to_nodes, 'r') as nodes_file:
        nodes = nodes_file.readlines()[7:]
        nodes_counter = 0

        for line in nodes:
            if re.match(re.compile(r"\s*[a|p]{1}[0-9]{1,2}\s*"), line):

                nodes_counter += 1
                i = 0
                while i < len(line):

                    # Getting the names of the nodes
                    if re.match(re.compile(r"[a|p]"), line[i-2]) and re.match(re.compile(r"[0-9]"), line[i-1]) and re.match(re.compile(r"[0-9]|\s"), line[i]):
                        if re.match(re.compile(r"[0-9]"), line[i]):
                            #print(line[i-2] + line[i-1] + line[i])
                            name = line[i-2] + line[i-1] + line[i]
                            #print(name)

                        elif re.match(re.compile(r"\s"), line[i]):
                            #print(line[i-2] + line[i-1])
                            name = line[i-2] + line[i-1]
                            #print(name)

                        # Getting the width of the nodes
                        if re.match(re.compile(r"\s"), line[i+11]):
                            #print(line[i+12])
                            width = line[i+12]
                            #print(width)
                        elif re.match(re.compile(r"\s"), line[i+12]):
                            if re.match(re.compile(r"\s"), line[i+10]):
                                #print(line[i + 11])
                                width = line[i + 11]
                                #print(width)
                            else:
                                #print(line[i + 10] + line[i+11])
                                width = line[i + 10] + line[i+11]
                                #print(width)
                        else:
                            #print(line[i+11] + line[i+12])
                            width = line[i+11] + line[i+12]
                            #print(width)

                        # Getting the height of the nodes
                        if re.match(re.compile(r"\s"), line[i + 23]):
                            if re.match(re.compile(r"\s"), line[i + 21]):
                                #print(line[i+22])
                                height = line[i+22]
                                #print(height)
                            else:
                                #print(line[i+21] + line[i+22])
                                height = line[i+21] + line[i+22]
                                #print(height)
                        else:
                            #print(line[i+22] + line[i+23])
                            height = line[i+22] + line[i+23]
                            #print(height)
                    i += 1

                # append to list here
                nodes_list.append( Node(nodes_counter, name, width, height) )

        # Test prints of the nodes_list down here:
        print(len(nodes_list))
