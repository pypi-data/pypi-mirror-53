from py2neo import Graph, Node, Relationship, NodeMatcher


class GraphUtils():
    def __init__(self, graph):
        self.graph = graph

    def paragraphs_for_filename(self, filename):
        kwargs = { "filename": filename }
        cursor = self.graph.run("""
            MATCH(paragraph :p {filename:{filename}})-[:facs]->(zone :zone)
            RETURN paragraph
        """, kwargs)

        paragraphs = []
        while cursor.forward():
            for paragraph in cursor.current:
                paragraphs.append(paragraph)

        return paragraphs

    def concatenation_exists(self, node):
        cypher = """
        MATCH (node1)-[r :CONCATENATED]->(node2)
        WHERE ID(node1) = {node_id}
        RETURN r
        """
        cursor = self.graph.run(cypher, parameters={"node_id": node.identity})

        # return 1 if there exists a relation
        return cursor.forward()

    def tokens_in_filename(self, filename):
        kwargs = { "filename": filename }
        cursor = self.graph.run("""
        MATCH(paragraph :p {filename:{filename}})-[:facs]->(zone :zone)
        RETURN paragraph, zone
        """, kwargs)

        while cursor.forward():
            pass
 

    def tokens_in_paragraph(self, paragraph:Node, concatenated=0):
        """For a given paragraph, this method returns all nodes
        connected via a NEXT relationship. 
        If concatenated=1, it will return a concatenated version of the textpath.
        Returns all nodes in the found textpath.
        """

        cypher="""
        MATCH (para)-[:NEXT]->(t),
        textpath = shortestPath((t)-[:NEXT*]->(lt))
        WHERE ID(para)={paragraph_id}
        AND (para)-[:LAST]->(lt)
        AND ALL (
            rel IN relationships(textpath)
            WHERE (rel.concatenated IS NULL OR rel.concatenated = {concatenated})
        )
        RETURN nodes(textpath)
        """
        # NOTE: it is assumed that a path containing a concatenated (non-hyphened)
        # word will be always shorter than a path containing a hyphened word.
        # The non-concatenated textpath actually never has the relation-attribute 
        # rel.concatenated=0 (it is always NULL)

        cursor = self.graph.run(
            cypher, 
            parameters={
                "paragraph_id": paragraph.identity,
                "concatenated": concatenated
            }
        ) 

        nodes = [] 
        while cursor.forward():
            for entry in cursor.current:
                for node in entry:
                    nodes.append(node)
                
        return nodes


    def create_unhyphenated(self, tokens):
        """tokens=Array of all tokens in a paragraph, as returned
        by GraphUtils.tokens_in_paragraph(para). This procedures looks for linebreaks with type=hyph
        If found, it looks forward and backwards to find the hyphened wordparts
        It then concatenates the wordparts, creates a new Node and new Releations.
        """
        tx = self.graph.begin()

        for i, token in enumerate(tokens):
            j=0
            k=0
            if token.has_label('lb'):
                wordstart = None
                wordend = None
                if token.get('type') == 'hyph':
                    
                    # walk back and find a token which is a wordpart
                    # and not any punctuation or similar
                    j=i-1
                    while j>0:
                        #print("j = {}".format(j))
                        if tokens[j].has_label('token') \
                        and tokens[j]["string"] \
                        and not tokens[j]["is_punct"]: 
                            #print("TRY: "+str(tokens[j]))
                            wordstart = tokens[j]
                            break
                        else:
                            j = j-1

                    # walk forward and find a token
                    k=i+1
                    while k>0 and tokens[k]:
                        #print("k = {}".format(k))
                        if tokens[k].has_label('token'):
                            #print("TRY END: "+str(tokens[k]))
                            wordend = tokens[k]
                            break
                        else:
                            k = k+1
                          
                    concat_word = ''
                    if wordstart and wordend and not self.concatenation_exists(wordstart):
                        #print("---START: "+str(wordstart))
                        #print("---  END: "+str(wordend))
                        if any(
                            wordstart["string"].endswith(s) for s\
                            in ['-', '\N{NOT SIGN}', '\N{NON-BREAKING HYPHEN}']
                        ):
                            concat_word = wordstart["string"][:-1]
                        else:
                            concat_word = wordstart["string"]
                            
                        concat_word += wordend["string"]
                        
                        # create new concatenated token
                        # with blank as whitespace
                        labels = list(
                            set(
                                ['token', 'concatenated'] + list(wordstart.labels) + list(wordend.labels)
                            )
                        )
                        attrs = { 
                            "string"    : concat_word,
                            "whitespace": wordend["whitespace"],
                            "filename"  : wordstart["filename"],
                            "idno"      : wordstart["idno"],
                        }
                        concat_node = Node(
                            *labels,
                            **attrs
                        )
                        #print("+ {}".format(concat_word))
                        tx.create(concat_node)
                        
                        # create relations from hyphened wordpards to concatenated word
                        rs = Relationship(
                            wordstart,
                            "CONCATENATED",
                            concat_node
                        )
                        rs2 = Relationship(
                            wordend,
                            "CONCATENATED",
                            concat_node
                        )
                        tx.create(rs)                
                        tx.create(rs2)
                        
                        # create direct connection for non-hyphened version
                        # of the thext
                        if j >0:
                            before_wordstart = tokens[j-1]
                            rs3 = Relationship(
                                before_wordstart,
                                "NEXT",
                                concat_node,
                                concatenated=1
                            )
                            tx.create(rs3)
                            
                        if len(tokens) > k+1:
                            after_wordend = tokens[k+1]
                            rs4 = Relationship(
                                concat_node,
                                "NEXT",
                                after_wordend,
                                concatenated=1
                            )
                            tx.create(rs4)

        tx.commit()

