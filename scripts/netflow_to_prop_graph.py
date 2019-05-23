import collections
#import networkx as nx
import numpy as np
import os, sys
import pandas as pd
 
def update_property(prop_map, key, value):
  if key not in prop_map:
    prop_map[key] = set()
  prop_map[key].add(value)
  return

def update_count(counter, key, count):
  counter[key] += int(count)
  return

def discretize_values(prop_map):
  median = np.median(np.asarray(list(prop_map.values())))
  new_map = dict()
  for k,v in prop_map.items():
    new_map[k] = 1 if v > median else 0
  return new_map

def get_id(node_id_map, node_str):
  if node_str not in node_id_map:
    node_id_map[node_str] = str(len(node_id_map))
  return node_id_map[node_str]

def transform_node_ids(prefix):
  node_id_map = dict()
  in_edge_path = prefix + '.TEMP.edges'
  in_labels_path = prefix + '.TEMP-labels.txt'  
  out_edge_path = prefix + '.edges'
  out_labels_path = prefix + '-labels.txt'  
  out_ids_path = prefix + '.ids.tsv'

  f_out_edges = open(out_edge_path, 'w')
  with open(in_edge_path) as f_in:
    for line in f_in:
      tokens = line.strip().split('\t')
      u = get_id(node_id_map, tokens[0])  
      v = get_id(node_id_map, tokens[1])  
      f_out_edges.write(u + '\t' + v + '\n')
  f_out_edges.close()

  f_out_labels = open(out_labels_path, 'w')
  line_count = 0 
  with open(in_labels_path) as f_in:
    node_labels = dict()
    for line in f_in:
      line_count += 1
      if line_count == 1:
        continue
      tokens = line.strip().split('\t')
      node_labels[get_id(node_id_map, tokens[0])] = '\t'.join(tokens[1:])
    for node_id in sorted(node_labels.keys()):
      f_out_labels.write(node_labels[node_id] + '\n')
  f_out_labels.close() 

  with open(out_ids_path, 'w') as f:
    for k in sorted(node_id_map.keys()):
      f.write(k + '\t' + node_id_map[k] + '\n') 

def process_flow(path, netflow_field_index, out_prefix):
  sep = ','
  line_count = 0
  edge_list = []
  incoming_ports = dict()
  incoming_protocols = dict()
  outgoing_protocols = dict()
  incoming_packets = collections.Counter()
  outgoing_packets = collections.Counter()
  incoming_bytes = collections.Counter()
  outgoing_bytes = collections.Counter()
  num_in_flows = collections.Counter()
  num_out_flows = collections.Counter()

  with open(path) as f_in:
    print('Reading file ...')
    last_s = ''
    last_d = ''
    last_s_port = ''
    last_d_port = ''
    last_line = ''
    for line in f_in:
      line_count += 1
      if line_count == 1:
        continue
      tokens = [t.strip() for t in line.strip().split(sep)]
      src_ip = tokens[netflow_field_index['SrcAddr']]
      dst_ip = tokens[netflow_field_index['DstAddr']]    
      if src_ip == last_d and dst_ip == last_s and src_port == last_d_port and dst_port == last_s_port:
        continue
      src_port = tokens[netflow_field_index['Sport']]
      dst_port = tokens[netflow_field_index['Dport']]
      protocol = tokens[netflow_field_index['Proto']]
      num_packets = tokens[netflow_field_index['TotPkts']]
      num_bytes = tokens[netflow_field_index['TotBytes']]
      edge_list.append(src_ip + '\t' + dst_ip)
      update_property(incoming_ports, dst_ip, dst_port)
      update_property(incoming_protocols, dst_ip, protocol)
      update_property(outgoing_protocols, src_ip, protocol)
      
      update_count(incoming_packets, dst_ip, num_packets)
      update_count(outgoing_packets, src_ip, num_packets)
      update_count(incoming_bytes, dst_ip, num_bytes)
      update_count(outgoing_bytes, src_ip, num_bytes)
      num_in_flows[dst_ip] += 1
      num_out_flows[src_ip] += 1

      last_s = src_ip
      last_d = dst_ip
      last_s_port = src_port
      last_d_port = dst_port
      last_line = line
  
  print('Read ' + str(line_count-1) + ' records')
  print('Number of edges = ' + str(len(edge_list))) 
  print('Building additional counters ...')
  incoming_port_counts = dict([(k, len(v)) for k,v in incoming_ports.items()])
  incoming_protocol_counts = dict([(k, len(v)) for k,v in incoming_protocols.items()])
  outgoing_protocol_counts = dict([(k, len(v)) for k,v in outgoing_protocols.items()])

  print('Computing binary features ...')
  incoming_port_counts_bin = discretize_values(incoming_port_counts)
  incoming_protocol_counts_bin = discretize_values(incoming_protocol_counts)
  outgoing_protocol_counts_bin = discretize_values(outgoing_protocol_counts)
  incoming_packets_bin = discretize_values(incoming_packets)
  outgoing_packets_bin = discretize_values(outgoing_packets)
  incoming_bytes_bin = discretize_values(incoming_bytes)
  outgoing_bytes_bin = discretize_values(outgoing_bytes)
  incoming_flows_bin = discretize_values(num_in_flows)
  outgoing_flows_bin = discretize_values(num_out_flows)

  print('Creating input to dataframe ...')
  label_data = { 'incoming_port_counts_high': pd.Series(list(incoming_port_counts_bin.values()), \
                index=incoming_port_counts_bin.keys()),\
           #'incoming_protocol_counts_high': pd.Series(incoming_protocol_counts_bin.values(), \
                #index=incoming_protocol_counts_bin.keys()), \
           #'outgoing_protocol_counts_high': pd.Series(outgoing_protocol_counts_bin.values(), \
                #index=outgoing_protocol_counts_bin.keys()), \
           #'incoming_packet_counts_high': pd.Series(incoming_packets_bin.values(), \
                #index=incoming_packets_bin.keys()), \
           #'outgoing_packet_counts_high': pd.Series(outgoing_packets_bin.values(), \
                #index=outgoing_packets_bin.keys()), \
           'incoming_bytes_high': pd.Series(list(incoming_bytes_bin.values()), \
                index=incoming_bytes_bin.keys()), \
           'outgoing_bytes_high': pd.Series(list(outgoing_bytes_bin.values()), \
                index=outgoing_bytes_bin.keys()), \
           #'incoming_flows_high': pd.Series(incoming_flows_bin.values(), \
                #index=incoming_flows_bin.keys()), \
           #'outgoing_flows_high': pd.Series(outgoing_flows_bin.values(), \
                #index=outgoing_flows_bin.keys()) \
          }

  out_temp_edges = out_prefix + '.TEMP.edges'
  out_temp_labels = out_prefix + '.TEMP-labels.txt'
  with open(out_temp_edges, 'w') as f:
    for e in edge_list:
      f.write(e + '\n')

  print('Creating dataframe ...')
  label_df = pd.DataFrame.from_dict(label_data).fillna(0).astype(np.int8)
  print('Saving dataframes ...')
  label_df.to_csv(out_temp_labels, sep = '\t', index_label='ip_addr')

  transform_node_ids(out_prefix)

def createFieldIndex(path):
  field_index = {"SrcAddr" : None, "DstAddr": None, 'Sport': None, 'Dport': None, 'Proto': None, 'TotPkts': None, 'TotBytes': None}
  header = ""
  with open(path) as fp:
    sep = ","
    ##In case file has a empty line prior to header
    while header == "" :
      header = fp.readline()
    fp.close()

  tokens = []
  for h in header.strip().split(sep):
    if h == '':
      continue
    tokens.append(h.strip())

  field_index = getIndex(field_index,tokens)
  status, invalidCol = checkFieldIndex(field_index)
  if status:
    return field_index
  else:
    print("Error. Cannot find column corresponding to " + str(invalidCol))
    exit()


def getIndex(field_index, header):
  keys = list(field_index.keys())
  for i,col in enumerate(header):
    if col in keys:
      field_index[col] = i
  return field_index

def checkFieldIndex(field_index):
  keys = list(field_index.keys())
  for key in keys:
    if field_index[key] == None and key != None:
      return False, key
  return True,None

def driver():
  if len(sys.argv) < 3:
    print("File Expects 2 Arguments:")
    print("1. Path To Data")
    print("2. Path To Output")
    exit()   
  path = sys.argv[1]
  out_dir = sys.argv[2]
  field_index = createFieldIndex(path)
  out_prefix = out_dir + '/' + os.path.basename(path)
  process_flow(path, field_index, out_prefix)

if __name__ == '__main__':
  driver()

