# -*- coding: utf-8 -*-
"""
JSON to Table converter
Author: Ernesto Monroy
Created: 10/06/2019
"""
class converter:
    
    def __init__(self):
        self.tree=dict()
        self.paths=[]
        
    #User funcions
    def set_paths(self, paths):
        #Type check
        if type(paths) != list:
            raise TypeError('The function expected a list of dictionaries with shape [{"$.path":"Custom Column Name"},{"$.other.path":"Other Column"}, ...] The containing object is not a list')
        for p in paths:
            if type(p) != dict:
                raise TypeError('The function expected a list of dictionaries with shape [{"$.path":"Custom Column Name"},{"$.other.path":"Other Column"}, ...] Some items in the list are not dictionaries')
            if len(p) != 1:
                raise TypeError('The function expected a list of dictionaries with shape [{"$.path":"Custom Column Name"},{"$.other.path":"Other Column"}, ...] Some dictionaries in the list have more tha one key:value entry')

        self.paths = paths
        self.tree = dict()
        for p in self.paths:
            self.tree=self.tree_generator(next(iter(p)).split('.'),self.tree,[]) 
        
    def convert_json (self, in_content):
        records=self.recurse(self.tree["$"],in_content)
        self.records=records
        columns={records[0][i]:i for i in range(len(records[0]))}
        return [[list(p.values())[0] for p in self.paths]] + [[r[columns[next(iter(p))]] for p in self.paths] for r in records[1:]]
        
    #----- Auxiliary functions -------------
    def tree_generator(self, nodes,in_tree,previous_nodes):
        if len(nodes)==1:
            new_tree = {None:'.'.join(previous_nodes+nodes)}
        else:        
            if nodes[0] in in_tree:
                new_tree=self.tree_generator(nodes[1:],in_tree[nodes[0]],previous_nodes+[nodes[0]])
            else:
                new_tree=self.tree_generator(nodes[1:],dict(),previous_nodes+[nodes[0]])
        if nodes[0] in in_tree:
            new_tree = {**in_tree[nodes[0]], **new_tree}
        return {nodes[0]:new_tree}
    
    def convert_output(self, in_content):
        #Convert types
        if in_content==None:
            in_content=in_content
        elif type(in_content)==int:
            in_content=in_content
        else:
            in_content=str(in_content)
        return in_content

    def recurse (self, tree,in_content,k=0):
        original_content=in_content
        if type(in_content)!= list:
            in_content=[in_content]
        only_header= (in_content==[])

        if only_header:
            in_content=[[]]
        records=[]
        for i in range(len(in_content)): #For every element at the level
            results=[[]]
            for node in tree: # For every leaf of the element

                # DERIVE THE RESULT OF THE NODE (flattened array) -----------------------------

                #Final value
                if node == None:
                    #If its the only node
                    if len(tree)==1:
                        return [[tree[node]],[self.convert_output(original_content)]]
                    else:
                        new_result = [[tree[node]],[self.convert_output(original_content)]]
                #Function nodes
                elif node == '~':
                    if type(original_content)==dict:
                        new_result = self.recurse ({'*':tree[node]},list(original_content.keys()),k+1)
                    else:
                        new_result = self.recurse (tree[node],i,k+1)
                elif node == '*':
                    if type(original_content)==dict:
                        new_result = self.recurse ({'*':tree[node]},list(original_content.values()),k+1)
                    else:
                        new_result = self.recurse (tree[node],in_content[i],k+1)
                #No more content to explore
                elif in_content[i] == None:
                    new_result = self.recurse (tree[node],None,k+1) 
                #If the node is matched to the content, then go into the leaf
                elif type(in_content[i])==dict and node in in_content[i]:
                    new_result = self.recurse (tree[node],in_content[i][node],k+1)
                else:
                    new_result = self.recurse (tree[node],None,k+1)           

                # JOINING OF NODE RESULT ABOVE TO THE BODY OF RESULTS -----------------------------

                #When a result is empty, it still has a row of null results, in this case remove it
                if only_header:
                    new_result=[new_result[0]]
                
                #If  the new and existing results have both more than 1 row (Not empty) and are NOT children of a function (*,~)
                # Then expand both result sets to be permuted later (e.g. [[a]] , [[b,c]] => [[a,b],[a,c]])
                if (len(results)>1 and len(new_result)>1):
                    if results[0][0].split('.')[0:k+2][-1] not in ['*','~'] or new_result[0][0].split('.')[0:k+2][-1] not in ['*','~']:
                        results = [results[0]]+[r for r in results[1:] for _ in range(len(new_result)-1)]
                        new_result=[new_result[0]]+new_result[1:]*int((len(results)-1)/(len(new_result)-1))

                # Join both results
                # If both contain more than 1 row they need to be permuted
                if (len(results)>1 or (results[0]==[])) and (len(new_result)>1 or (new_result[0]==[])):
                    results=results+[results[-1] for _ in range (len(new_result)-len(results))]
                    new_result=new_result+[new_result[-1] for _ in range (len(results)-len(new_result))]
                    results=[results[i]+new_result[i] for i in range(len(new_result))]
                # Otherwise they can simply be joined
                else:
                    results=[results[0]+new_result[0]]

            #Join with records from other elements of the same level
            records= [results[0]]+records[1:]+results[1:]
            
        if only_header:
            return [records[0]]
        else:
            return records