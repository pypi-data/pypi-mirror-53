import sys
assert sys.version_info >= (3, 5)  # at least Python 3.5 or higher

import os
from bs4 import BeautifulSoup, Comment
from py2neo import Graph, Node, Relationship, NodeMatcher
import spacy
from lxml import etree
import re
from collections import defaultdict

#from .tei_elements import *
import keyword
import inspect

nlp = spacy.load('de_core_news_sm')

# Attributes that link to other nodes
# These attributes occur in <pb> <p> <join> elements and point to an xml:id attribute.
# Example: <p facs="#facs_6_r7" xml:id="p.WYzmFK" prev="#p.N87sF3" next="20_MS_230_7.xml#p.o6Zx1j">
# 1. points to facsimile with xml:id="facs_6_r7"
# 2. points to previous paragraph with xml:id="p.N87sF3"
# 3. points to next paragraph on XML file 20_MS_230_7.xml with xml:id="p.o6Zx1j" 
link_attributes = ["facs", "next", "prev", "target", "ref"]

# lb element contains a facs attribute which currently points to nowhere
elements_not_to_link = ["lb"]

VERBOSE = 1
PARSE_STRING = 0
CREATE_NODE = 0
GET_CLASS_FOR_NODE = 0
CHANGE_BASE_CLASS = 0
WALK_CHILD_NODES = 0
PARENT_CHILD_RELATION = 0

def parse(filename, start_with_tag='TEI', idno=None):
    status = defaultdict(list)
    status['attrs'] = defaultdict(dict)
    status['handshift'] = {}
    status['links'] = defaultdict(dict)
    attrs = {} 
    filename_only = os.path.basename(filename)
    #attrs['filename'] = filename_only
    status['attrs']['filename'] = filename_only

    # 1. parse the XML using lxml and etree.
    # It will apply the DTD validation and replace strings like &stern_1; with
    # the correct unicode symbol, which is described in the DTD file.
    parser = etree.XMLParser(dtd_validation=True, recover=True)
    tree = etree.parse(filename, parser)
    # output of XML document as unicode string
    unicode_string = etree.tostring(tree.getroot(), encoding='unicode')

    # 2. parse the TEI XML file (the unicode string), using lxml-xml parser
    # which is not assuming html and thus does not automatically add html or remove body tags.
    soup = BeautifulSoup(unicode_string, 'lxml-xml')

        # find the primary key of the document and attach it to the soup
    if not idno:
        idno = soup.find('idno').string
    
    status['attrs']['idno'] = idno

    tei_node = soup.find(start_with_tag)
    if tei_node is None:
        raise ValueError("Did not find a tag named '{}'".format(start_with_tag))

    # find a matching class, create an object from it
    # and return it
    class_name = start_with_tag.lower()
    if class_name in globals():
        if GET_CLASS_FOR_NODE: print("  * found in globals(): {}".format(globals()[class_name]))
        cls = globals()[class_name]
        doc = cls(
            node=tei_node, node_name=tei_node.name, status=status,
            attrs=attrs
        )
        return doc, status, soup
    else:
        raise ValueError("no such class available: {}".format(class_name))


# TEI section
class tei():
    """This is the base class for all elements in a TEI document.
    """

    def __init_subclass__( 
        cls, 
        parent_child_relation='CONTAINS', child_parent_relation=None, 
        isleaf=False, 
        do_not_store_this_node=False,
        pass_label_to_children=None,
        unpack_elements=False, 
        create_empty_token_nodes=False,
        from_relation_attr = None,
        to_relation_attr = None,
        group_similar_siblings = None,
        pass_attributes_to_children=False,
        cache_object=False,
        **kwargs
    ):
        super().__init_subclass__(**kwargs)
        # Parent defines,  how the relation from Parent to Child is defined
        cls.parent_child_relation = parent_child_relation
        # Child defines, how the relation from Child to Parent is defined
        cls.child_parent_relation = child_parent_relation
        cls.isleaf = isleaf  # extract all text inside this element
        cls.unpack_elements = unpack_elements # ignore this node, just add the elements
        # if an empty <sic/> element is encountered, create a token node
        # even the element contains no tokens at all
        cls.create_empty_token_nodes = create_empty_token_nodes
        cls.from_relation_attr = from_relation_attr
        cls.to_relation_attr   = to_relation_attr
        cls.group_similar_siblings = group_similar_siblings           # see 
        cls.pass_label_to_children = pass_label_to_children           # add additional label to graph-node
        cls.pass_attributes_to_children = pass_attributes_to_children # add attributes of xml-node to graph-node
        cls.cache_object=cache_object
        cls.do_not_store_this_node = do_not_store_this_node


    def get_class_for_node(self, node):
        # add an underscore to the node name in case it is a reserved python word
        # which can't be used as a class name
        node_name = node.name
        if node_name in keyword.kwlist:
            node_name += '_'

        # inspect all subclasses in a class (and their parents)
        # and try to find a matching class to the given 
        # node_name (aka tag, element) in the XML file
        # return the class as soon as it is found, using 
        # C3 mro (method resolution order)

        if GET_CLASS_FOR_NODE: print("**** looking here in get_class_for_node for: ", node_name)
        for cls in inspect.getmro(self.__class__):
            if cls.__name__ == 'object':
                continue
            if GET_CLASS_FOR_NODE: print("   - looking for members in class: {}".format(cls))

            for subclass_tuple in inspect.getmembers(cls, predicate=lambda cl:(inspect.isclass(cl))):
                if GET_CLASS_FOR_NODE: print("      - looking at tuple: {}".format(subclass_tuple))
                if node_name.lower() == subclass_tuple[0].lower():
                    return subclass_tuple[1]

        # still no matching class found. Try to find a base class
        if GET_CLASS_FOR_NODE: print("   - looking in globals()")
        if node_name.lower() in globals():
            if GET_CLASS_FOR_NODE: print("  * found in globals(): {}".format(globals()[node_name.lower()]))
            return globals()[node_name.lower()]
        else:
            if GET_CLASS_FOR_NODE:
                print("XXXXXXXXXXXXX no class found for {}".format(node_name))
            return None

    def handle_whitespace(self, node, status, new_parent_attrs, new_parent_labels):
        return []

    def parse_string(self, node, status, parent_attrs, parent_labels):
        """Gets the string  within an opening and a closing tag:
        <title>some string</title>
        ... and stores it as an attribute: object.string
        This method can be overriden to parse the string and create
        individual token objects instead.
        returns an array containing the object
        """
        # either get the string directly found in the tag
        # or within all children
        string = getattr(node, 'string', '') or getattr(node, 'text', '')
        # remove all leading and trailing whitespace
        self.attrs['string'] = string.strip()

    def parse_comment(self, node, status):
        comment_instance = comment(
            node=node, 
            node_name=node.name,
            status=status
        )
        return [comment_instance]

    def _change_base_class(self):
        """During object initialization we will change the parents (base classes)
        of the object dynamically.
        Nested classes like A.B.C do not inherit from each other and there is no way
        to make it work:

        class A(tei):
            class B(A, tei):
                class C(B, A, special_class, tei):
                    ...
        
        Will already fail on compile time.

        To make an object inherit from the classes it is nested in, we need to change
        its base classes, i.e. object.__class__.__bases__. This can be achieved on
        runtime.

        So if we declare our classes like this:
        
        class A(tei):
            class B(tei):
                class C(special_class, tei):
                    pass
        
        the resulting objects will behave as if the classes were defined like this:

        class A(tei):
            class B(A, tei)
                class C(special_class, A.B, A, tei)

        
        Why would we want to have nested classes? Isn't this bad practice?
        ------------------------------------------------------------------

        When parsing a TEI document, we do not treat similar elements
        always the same way.
        For example, a paragraph element <p> can occur almost everywhere
        inside the <text> or <body> elements. 
        It also appears in the <teiHeader>, but there its content
        needs to be treated differently. We could define a general class p which has
        a lot of ifs to decide how to behave in which situation. To avoid this, we
        rather define a class

            text.body.p

        which is a completely different class than

            teiheader.p

        At the same time, we want text.body.p to use some of the specialised methods
        defined in the class text.body, for example.

        The resulting code will be declarative, easy to read and maintain.

        """
        #------------ start changing base class of object --------------
        # get the qualified name of our class without the module name,
        # e.g. 'A.B.C', not '__main__.A.B.C' and not just 'A'
        # NOTE: only works with Python 3.3 and onwards!
        fqn = self.__class__.__qualname__
        class_names = fqn.split('.')

        # get the list of classes we already inherit from
        result_classes = list(self.__class__.__bases__)
        if CHANGE_BASE_CLASS: print("### starting with result_classes: {}".format(list(self.__class__.__bases__)))

        # from the fully qualified class (e.g. A.B.C) we want the given class to
        # inherit from A.B, A (in this order). We put this classes in front of
        # the already present classes (thus insert not append)
        for i in range(1, len(class_names)):
            cls_name = '.'.join(class_names[0:i])
            try:
                cls = eval(cls_name)
                if cls not in result_classes:
                    result_classes.insert(0,cls)
            except AttributeError:
                # class is not explicitly defined (only as virtual metaclass)
                pass
    
        # change the __class__.__bases__ of our newly created object
        # which now is of Classes A.B.C, A.B, A and any other classes it inherits 
        if CHANGE_BASE_CLASS: print("### bases before-> {}".format(self.__class__.__bases__))
        if CHANGE_BASE_CLASS: print("### result_classes-> {}".format(result_classes))
        self.__class__.__bases__ = tuple(result_classes)
        #------------ finish changing base class of object --------------


    def __init__(
            self, node=None, node_name=None, status=None,
            attrs=None, parent_attrs=None, parent_labels=None,
            string=None
        ):
        """ tei class is the parent class for all tei elements.
            node: the current node in the tei-xml file
            node_name: name of the current element (e.g. p, lb, teiheader)
            status: during parsing, certain events like handShift needs to be registered
                  these events affect all next elements
            attrs: attributes inside an element
            parent_attrs: attributes that are passed to all children elements
                Attributes of children might overwrite them again, much like in css.
            string: the actual value (or payload) of an element. Header information
                is not getting interpreted any further, whereas the text itself
                is interpreted (by the parse_string function)
            parent_labels: labels that are passed to all children elements,
                much like parent_attrs.
          
        """

        # make nested classes inherit from each other
        # by dynamically changing their base classes
        self._change_base_class()

        self.xml_node = node

        # set the name of the node, in case it was not provided
        if node_name is None:
            setattr(self, 'node_name', self.__class__.__name__)
        else:
            setattr(self, 'node_name', node_name)

        # add the name of the node as the default label
        self.labels = set()
        self.labels.add(node_name)


        self.child_parent_relation= None

        # If there are any parent attributes, merge them into
        # the attributes of the current child object.
        # make sure the parent attributes are overwritten if a child
        # has the same attributes.
        self.attrs = defaultdict()
        if attrs is None:
            attrs = {}
        if parent_attrs is None:
            parent_attrs = {}
        self.attrs = {**self.attrs, **parent_attrs, **attrs}

        # collect all the attributes we stored in self.attrs 
        # and merge them with node attributes
        node_attrs = getattr(node, 'attrs', {})
        self.attrs = { **self.attrs, **node_attrs}

        # collect all attributes we stored in status['attrs']
        # including the primary key (idno) of the document
        if status is not None:
            for key in status['attrs']:
                self.attrs[key] = status['attrs'][key]

        if parent_labels is None:
            parent_labels = []

        # add delSpan label if we have such a status
        if status.get('delSpan'):
            self.labels.add('delSpan')
            # add delSpan attribute with anchor id
            self.attrs['delSpan'] = status.get('delSpan')

        # add any incoming parent labels to self.labels
        # and make a copy into new_parent_labels
        new_parent_labels = []
        for parent_label in parent_labels:
            self.labels.add(parent_label)
            new_parent_labels.append(parent_label)

        # new_parent_labels now contains all the labels that need to be
        # passed to all children objects
        if getattr(self, 'pass_label_to_children', False):
            new_parent_labels.append(self.pass_label_to_children)

        self.child_instances = []

        # Parse the string of the element itself
        if getattr(self, 'isleaf', False):
            # the node is declared as a leaf, do not parse the node in more detail
            # just extract the text
            self.parse_string(node, status, parent_attrs, parent_labels)
        elif node is None or node.name is None:
            # we encountered just text, which has no node.name and no children either.
            pass
        else:
            # Walk through children of the current node
            new_parent_attrs = {}
            if getattr(self, 'pass_attributes_to_children', False):
                new_parent_attrs = self._get_node_attributes()
                # do not inherit xml:id attribute to children
                if 'xml:id' in new_parent_attrs:
                    new_parent_attrs.pop('xml:id')
            new_parent_attrs = {**parent_attrs, **new_parent_attrs}
        
            for child_node in node.children:
                """- walk through the children of the current node
                - find a corresponding class, either directly or indirectly
                - create an instance of it
                - append the child_instances to the object.child_instances attribute
                """
                if WALK_CHILD_NODES: print("--------WALK_CHILD_NODES-------")
                if WALK_CHILD_NODES: print(child_node)
                if WALK_CHILD_NODES: print("-------------------------------")

                if child_node.isspace is not None and child_node.isspace():
                    # we did not find any characters, just whitespace
                    child_instances = self.handle_whitespace(
                        child_node, status, new_parent_attrs, new_parent_labels
                    )
                    self.child_instances += child_instances
                    continue

                elif child_node.name is None:
                    # we encountered TEXT or COMMENT, which is not enclosed in tags 
                    # but occurs after a tag (e.g. after a linebreak <lb>)
                    if isinstance(child_node, Comment):
                        # COMMENT
                        continue
                        #self.child_instances += self.parse_comment(child_node, status)
                    else:
                        # we need to parse the TEXT, which means: 
                        # we tokenize it and create token objects
                        child_instances = self.parse_string(
                            child_node, status, new_parent_attrs, new_parent_labels
                        )
                        if child_instances is not None:
                            self.child_instances += child_instances

                else:
                    #
                    # we encountered an child-node (child-element)
                    # find class for child_node
                    targetClass = self.get_class_for_node(child_node)
                    if WALK_CHILD_NODES: print ("got class: {}".format(targetClass))

                    # if we do not find a matching class,
                    # we will ignore the entire element and all its children
                    if targetClass is None:
                        if WALK_CHILD_NODES: print("## node ignored, skipping...")
                        continue
                    else:
                        # we found a matching class: create an instance of it and
                        # append it to self.child_instances
                        if WALK_CHILD_NODES: print("targetClass ----> {} ".format(targetClass))

                        instance = targetClass(
                            node=child_node, node_name=child_node.name,
                            status=status, parent_attrs=new_parent_attrs,
                            parent_labels=new_parent_labels
                        )

                        # if class has the attribute unpack_elements=True
                        # we want to directly append the children of the children
                        # to the current instance.
                        if instance.unpack_elements:
                            if instance.create_empty_token_nodes \
                                and len(instance.child_instances) == 0:
                                token_obj = Token(
                                    node=child_node, node_name='token',
                                    status=status, 
                                    attrs={"string": "", "whitespace": ""},
                                    parent_labels=new_parent_labels+[instance.node_name]
                                ) 
                                self.child_instances.append(token_obj)

                            for child_instance in instance.child_instances: 
                                self.child_instances.append(
                                    child_instance
                                )
                        else:
                            self.child_instances.append(instance)

        self.create_parent_child_relationships(status)
        self.create_sibling_relationships(status)
        self._group_similar_siblings(status)


    def _get_node_attributes(self):
        """returns all attributes of an XML element as a dict
        """
        attrs = {}
        for attr in self.xml_node.attrs:
            attrs[attr] = self.xml_node.attrs[attr]
        return attrs


    def create_parent_child_relationships(self, status):
        """This is the default relation between parent and child objects: CONTAINS
        Certain classes (like p) might implement their own, specific relations.
        If you just want to override the default, add parent_child_relation='WHATEVER'
        to your class definition
        """
        self.relationships=[]
        label = getattr(self, 'parent_child_relation', 'CONTAINS')
        for i, child_instance in enumerate(self.child_instances):
            if PARENT_CHILD_RELATION: print(self.__class__.__name__ + " CONTAINS " + child_instance.__class__.__name__)
            self.relationships.append({
                "from": self,
                "to": child_instance,
                "label": label,
            })

    def create_sibling_relationships(self, status):
        """Create relationships between all siblings within a given node.
        """
        pass

    def _group_similar_siblings(self, status):
        """Creates additional relationships between similar siblings
        e.g. NEXT_LB, NEXT_TOKEN
        Also creates relationships that point to the first and last element:
        FIRST_LB, LAST_LB
        Classes must be declared this way:
        class body(tei, group_similar_siblings=['p'])
        """
        if getattr(self, 'group_similar_siblings', None) is None:
            return

        prev_instance = {}
        counter = defaultdict(int)
        for instance in [
            child_instance for child_instance in self.child_instances\
                if child_instance.node_name in self.group_similar_siblings
        ]:
            counter[instance.node_name] += 1
            # FIRST appearance
            if counter[instance.node_name] == 1:
                self.relationships.append({
                    "from" : self, 
                    "to"   : instance,
                    "label": "FIRST_"+instance.node_name.upper()
                })

            if prev_instance.get(instance.node_name):
                self.relationships.append({
                    "from" : prev_instance[instance.node_name],
                    "to"   : instance,
                    "label": "NEXT_"+instance.node_name.upper()
                })
                #self.relationships.append({
                #    "from"   : instance,
                #    "to" : prev_instance[instance.node_name],
                #    "label": "PREV_"+instance.node_name.upper()
                #})

            prev_instance[instance.node_name] = instance
            
        # LAST
        for node_name in self.group_similar_siblings:
            if prev_instance.get(node_name):
                self.relationships.append({
                    "from" : self, 
                    "to"   : prev_instance[node_name],
                    "label": "LAST_"+ node_name.upper()
                })


    def _node_for_obj(self, obj, tx, node_cache):
        attrs = getattr(obj, 'attrs', {})

        if not getattr(obj, 'node', False):
            if CREATE_NODE: print("creating Node: {}".format(obj.node_name))
            if CREATE_NODE: print("               {}".format(attrs.get('string')))
            #if attrs.get('string') == 'B':
            #    import pdb; pdb.set_trace()
                

            labels = list(obj.labels)
            if CREATE_NODE: print("LABELS: {}".format(labels))

            # if we got a node with an xml:id we first want to check whether we
            # already have an empty node to update
            xml_id = attrs.get('xml:id')
            filename = attrs.get('filename')
            matcher = NodeMatcher(tx.graph)
            if xml_id and filename:
                node=None
                if filename in node_cache and xml_id in node_cache[filename]:
                    # search in cache
                    node = node_cache[filename][xml_id]
                else:
                    # search in database
                    search_attrs = {
                        'filename' : filename,
                        'xml:id'   : xml_id
                    }
                    node = matcher.match(**search_attrs).first()

                if node:
                    # we found a node, either in the current transaction
                    # or in the database
                    for label in labels:
                        node.add_label(label)
                    for attr in attrs:
                        node[attr] = attrs[attr]

                    if tx.exists(node):
                        # update node in transaction:
                        # we need to delet it and create it again
                        tx.delete(node)
                        tx.create(node)
                    else:
                        # existing node in database:
                        # update database
                        tx.graph.push(node)
                else:
                    # create a new node object
                    node = Node(
                        *labels,
                        **attrs
                    )
                    tx.create(node)
                if not filename in node_cache:
                    node_cache[filename] = {}
                # store node in cache
                node_cache[filename][xml_id] = node
            else:
                # create node
                node = Node(
                    *labels,
                    **attrs
                )
                tx.create(node)
                # we do not need to store this node in the node_cache, since
                # it has no xml:id and therefore can't be referenced.


            """ 
            if the element links to another node:
            1. check if that node already exists (xml:id, filename)
               a) check it in the current status cache (because node is not saved yet)
               b) check in the current graph
               -> exists: create relationship with attribute name as label
               -> does not exist: create placeholder node and relationship

            """ 
            
            create_links = True
            for label in labels:
                if label in elements_not_to_link:
                    create_links = False
                    

            if create_links:
                for link_attribute in link_attributes:
                    if link_attribute in attrs:
                        for link in attrs[link_attribute].split():
                            (filename, xml_id) = link.split("#")

                            if not filename:
                                filename = attrs['filename']
                            if not filename:
                                raise ValueError("filename not found in attribute: {}".format(link_attribute))
                            if not xml_id:
                                raise ValueError("xml:id not found in attribute: {}".format(link_attribute))

                            ex_node = None
                            if filename in node_cache and xml_id in node_cache[filename]:
                                ex_node = node_cache[filename][xml_id]

                            if not ex_node:
                                # try to find that node in the database instead
                                search_attrs = {}
                                search_attrs['filename'] = filename
                                search_attrs['xml:id'] = xml_id
                                ex_node = matcher.match(**search_attrs).first()
                            
                            if ex_node:
                                # we found an existing node:
                                # create a relationship to that existing node
                                rs = Relationship(
                                    node,
                                    link_attribute,
                                    ex_node
                                )
                                tx.create(rs)

                                # Create the Backlink (BL)
                                rs2 = Relationship(
                                    ex_node,
                                    link_attribute+'BL',
                                    node,
                                )
                                tx.create(rs2)
                            else:
                                # we only got a reference to a node, but not the node itself:
                                # create an «empty» ref_node and a relation to it:
                                ref_node = Node(**search_attrs)
                                tx.create(ref_node)
                                # store the reference node in the node_cache as well,
                                # there might be more than one reference to it
                                if not filename in node_cache:
                                    node_cache[filename] = {}
                                node_cache[filename][xml_id] = ref_node
                                
                                rs = Relationship(
                                    node,
                                    link_attribute,
                                    ref_node
                                )
                                tx.create(rs)

                                # Backlink (BL)
                                rs2 = Relationship(
                                    ref_node,
                                    link_attribute+'BL',
                                    node,
                                )
                                tx.create(rs2)
            
            obj.node = node
        return obj.node

    def save(self, tx, node_cache=None):
        """Recursively walk through all child_instances generated and 
        create nodes and relationships in the graph database
        """
        if node_cache is None:
            node_cache = {}

        # create node for the current element
        # adding element attributes, e.g. <p attr1="one" attr2="two">
        # as attributes to the node itself

        # create all nodes (if they do not exist yet) and relationships
        for relationship in self.relationships:
            from_node = self._node_for_obj(relationship['from'], tx, node_cache)
            to_node   = self._node_for_obj(relationship['to'], tx, node_cache)
            attr = relationship.get('attr', {})
            rs = Relationship(
                from_node,
                relationship['label'],
                to_node,
                **attr
            )
            tx.create(rs)

        for child_instance in self.child_instances:
            child_instance.save(tx, node_cache)


class ParseString(tei):
    def parse_string(self, node, status, parent_attrs, parent_labels):
        """This method is parsing the string between elements by dividing
        it into Token objects
        - all token objects are stored in a variable token_objs which is then
            returned.
        It detects if a token represents a hyphened word fragment by either:
        - checking if it is the token ends with a - or a non-breaking hyphen
        - looking behind if it is the first word after a line break and the
        - line break is of type="hyph"
        """
        line = getattr(node, 'string', '')
        if line is None:
            return []

        line = str(line)

        # remove leading newlines and tabs
        # keep other whitespace (blanks) as we need to preserve this information!
        line = re.sub(r'\A(?:[\n\r\t]*)', '', line, flags=re.MULTILINE)
        # remove trailing newlines and tabs
        line = re.sub(r'(?:[\n\r\t]*)\Z', '', line, flags=re.MULTILINE)

        # we did not see anything other than tabs and newlines...
        if line == '':
            return []
        # (but we are still interested in space ;-)

        # finally do the tokenization using spacy's nlp
        tokens = nlp(line)

        token_objs = []
        # Walk through text-tokens and create Token objects
        if PARSE_STRING: print("TOKENS: «{}»".format(tokens))
        for i, token in enumerate(tokens):
            is_hyphened = False
            if any(
                token.text.endswith(s) for s\
                in ['-', '\N{NOT SIGN}', '\N{NON-BREAKING HYPHEN}']
            ):
                is_hyphened = True

            attrs = {
                'is_punct'        : token.is_punct,
                'pos'             : token.pos_,
                'tag'             : token.tag_,
                'is_hyphened'     : is_hyphened,
                'string'          : token.text,
                'whitespace'      : token.whitespace_,  # token is followed by a whitespace
                # from handshift
                'medium': status.get('handshift').get('medium'),
                'script': status.get('handshift').get('script'),
            }

            # Merge parent_attrs into attrs
            # but let them to be overwritten by the child elements
            if parent_attrs:
                attrs = {**parent_attrs, **attrs}

            # Create a Token object for every token
            token_obj = Token(
                node=node, node_name='token',
                status=status, attrs=attrs, parent_labels=parent_labels
            ) 

            # add it to our collection of token objects
            token_objs.append(token_obj)

        # these token objects get appended to .child_instances
        return token_objs

    handle_whitespace=parse_string


class ConnectSiblings:
    """This class defines how siblings, i.e. elements on the same hierarchical level,
    are connected with
    - each other
    - between their parents and their children, especially the first and last child
    """
    def __init_subclass__(cls, 
        previous_next_sibling_relation='NEXT', 
        previous_next_relation_attr=None,
        next_previous_sibling_relation=None, 
        next_previous_relation_attr=None, 
        **kwargs
    ):
        super().__init_subclass__(**kwargs)
        cls.previous_next_sibling_relation = previous_next_sibling_relation
        if previous_next_relation_attr is None:
            previous_next_relation_attr = {}
        cls.previous_next_relation_attr = previous_next_relation_attr

        cls.next_previous_sibling_relation = next_previous_sibling_relation
        if next_previous_relation_attr is None:
            next_previous_relation_attr = {}
        cls.next_previous_relation_attr = next_previous_relation_attr

    def create_parent_child_relationships(self, status):
        """Replaces the usual parent-child relationships (CONTAINS)
        by pointing from the parent to the FIRST sibling, 
        then connecting to the NEXT sibling
        and finally pointing from the parent to the LAST sibling
        """
        prev_child_instance = None
        self.relationships=[]
        for i, child_instance in enumerate(self.child_instances):
            if child_instance.do_not_store_this_node:
                # ignore elements like handhift when saving
                continue
            if i == 0:
                self.relationships.append({
                    "from": self,
                    "to": child_instance,
                    "label": "NEXT"
                })
            if prev_child_instance is not None:
                self.relationships.append({
                    "from": prev_child_instance,
                    "to": child_instance,
                    "label": self.previous_next_sibling_relation,
                    "attr": self.previous_next_relation_attr,
                })

            if i == len(self.child_instances)-1: # last 
                self.relationships.append({
                    "from": self,
                    "to": child_instance,
                    "label": "LAST"
                })
                self.relationships.append({
                    "from": child_instance,
                    "to": self,
                    "label": "NEXT"
                })
            prev_child_instance = child_instance

class Connect_first_last():
    """ connects the current node with the first of its siblings (default: FIRST)
    connects the current node with the last of its siblings (default: LAST)
    """
    def __init_subclass__(cls,
        first_relation='FIRST',
        last_relation='LAST', 
        **kwargs
    ):
        super().__init_subclass__(**kwargs)
        cls.first_relation = first_relation
        cls.last_relation = last_relation
        # do not connect parent->child with a CONTAINS relation, since
        # we already connect them otherwise
        cls.parent_child_relation = None


class include_all_elements():
    def get_class_for_node(self, node):
        """Inside a given section we want to follow every element, 
        even the ones we have no class definition for.
        We therefore have to instantly create a new class using type()
        """
        cls = super().get_class_for_node(node)
        if cls is None and node.name is not None:
            node_name = node.name

            if GET_CLASS_FOR_NODE: print("...creating new class for node: {}".format(node_name))
            parent_classes = [parent.name for parent in node.parents][:-2]
            parent_classes.reverse()
            parent_classes.append(node_name)

            # add an underscore to the class name 
            # in case it is a reserved python word
            # --> reserved python words cannot be used as a class name
            for i, class_name in enumerate(parent_classes):
                if class_name in keyword.kwlist:
                    parent_classes[i] = class_name + '_'

            class_name = ".".join(parent_classes)
            class_name = class_name.lower()
            if GET_CLASS_FOR_NODE: print("...creating new class: {}".format(class_name))

            return type(class_name, (tei, object), {})
        else:
            return cls


# TEIHEADER section
# only the elements listed here are being parsed and
# added to the database. Strings in an element are,
# as opposed to the BODY section, not being tokenized
# (split into words etc.). 
class teiheader(tei):
    class filedesc(include_all_elements, tei):
        pass

    class encodingdesc(tei):
        class editorialdecl(tei, isleaf=True):
            pass

    class profiledesc(include_all_elements, tei):
        pass

    class revisiondesc(include_all_elements, tei):
        pass


# FACSIMILE section
# the facsimilies section defines zones (coordinates) on the image itself
# every zone contains an xml:id which is used in paragraphs to refer to: <p facs="#facs_1_r3">
class facsimile(tei, cache_object=True):
    class surface(tei):
        class graphic(tei):
            pass
        class zone(tei, cache_object=True):
            pass
    

# TEXT section
# <text> is actually holding the real content in every TEI document
class text(include_all_elements, tei):
    def get_class_for_node(self, node):
        """Inside the <text> section we want to follow every element, 
        even the ones we have no class definition for.
        We therefore have to instantly create a new class using type()
        """
        cls = super().get_class_for_node(node)
        if cls is None and node.name is not None:
            node_name = node.name

            if VERBOSE > 1: print("...creating new class for node: {}".format(node_name))
            parent_classes = [parent.name for parent in node.parents][:-2]
            parent_classes.reverse()
            parent_classes.append(node_name)

            # add an underscore to the class name 
            # in case it is a reserved python word
            # --> reserved python words cannot be used as a class name
            for i, class_name in enumerate(parent_classes):
                if class_name in keyword.kwlist:
                    parent_classes[i] = class_name + '_'


            if VERBOSE > 1: print("...creating: {}".format(parent_classes))
            class_name = ".".join(parent_classes)
            if VERBOSE > 1: print("...creating new class: {}".format(class_name))

            return type(class_name, (tei, object), {})
        else:
            return cls

    class front(tei):
        pass

    class body(tei):

        class p(
            ConnectSiblings, 
            ParseString,
            group_similar_siblings=['lb'],
        ):
            """ handles all paragraphs tags <p> within the <body> tag
            """
            def __init__(self, 
                node=None, node_name=None, status=None,
                parent_attrs=None, parent_labels=None
            ):
                super().__init__(
                    node=node, node_name=node_name, status=status,
                    parent_attrs=parent_attrs, parent_labels=parent_labels     
                )
                    
        class lb(ParseString):
            """When connecting tokens, this class will
            a) point to the first token after the linebreak
            b) if not type=hyph: connect previous token with next token
               with a NEXT
            c) if type=hyph: 
                - create a new node Word of previous and next token
                - create a new relation pre-previous and this new Word:
                  NEXT_TOKEN { non_hyphened=True }
                - make sure the relation between pre-previous and previous token is
                  NEXT_TOKEN { hyphened=True }

                To query the non-hyphened string later, from START to END:
                MATCH (START), (END),
                shortestPath((START)-[:NEXT_TOKEN*]->(END))
                WHERE ALL (
                    rel IN relationships(p)
                    WHERE (rel.non_hypened IS NULL OR rel.non_hypened = True)
                    AND rel.hyphened != True
                )
                RETURN path

                To query the hyphened string later, from START to END:
                MATCH (START), (END),
                shortestPath((START)-[:NEXT_TOKEN*]->(END))
                WHERE ALL (
                    rel IN relationships(p)
                    WHERE (rel.hypened IS NULL OR rel.hypened = True)
                    AND rel.unhyphened != True
                )
                RETURN path
            """
              
            def __init__(
                self, node=None, node_name=None, status=None,
                attrs=None, parent_attrs=None, parent_labels=None,
                string=None
            ):
                if node.attrs.get('type') == 'hyph':
                    status['next_token_is_word_fragment'] = True
                    status['next_token_is_hyphened'] = True
                else:
                    status['next_token_is_word_fragment'] = False
                    status['next_token_is_hyphened'] = False
                    
                super().__init__(node=node, node_name=node_name, status=status)

        class pb(ParseString):
            pass
        class fw(ParseString):
            pass
        class undo(ParseString):
            pass
    class back(ParseString):
        pass

class comment(tei):
    pass


class Token(
    ConnectSiblings, 
    Connect_first_last, 
    tei,
):
    pass


class Word(
    ConnectSiblings,
    Connect_first_last,
    tei,
):
    pass


class join(tei, do_not_store_this_node=True):
    def __init__(
        self, node=None, node_name=None, status=None,
        attrs=None, parent_attrs=None, parent_labels=None,
        string=None
    ):
        if 'joins' not in status:
            status['joins'] = {}

        target = node.get('target')
        if target is not None:
            node1, node2 = target.split()
            # add the filename to a relative link
            if node1.startswith('#'):
                node1 = status['attrs']['filename']+node1
            if node2.startswith('#'):
                node2 = status['attrs']['filename']+node2

        status['joins'][node1] = node2

        super().__init__(node=node, node_name=node_name, status=status)


class handshift(tei, do_not_store_this_node=True):
    def __init__(
        self, node=None, node_name=None, status=None, 
        attrs=None, parent_attrs=None, parent_labels=None,
        string=None
    ):

        # only overwrite the latest handshifts, keep everything else.
        if node.get('new'):
            status['handshift']['new'] = node.get('new')
        if node.get('medium'):
            status['handshift']['medium'] = node.get('medium')
        if node.get('script'):
            status['handshift']['script'] = node.get('script')

        super().__init__(node=node, node_name=node_name, status=status)


class delspan(tei):
    """a delSpan element marks all following elements to be deleted,
    until an anchor element appears that contains the ID of the spanTo attribute.
    Albeit currently not needed, we still store this node in the graph.
    """
    def __init__(
        self, node=None, node_name=None, status=None, 
        attrs=None, parent_attrs=None, parent_labels=None,
        string=None
    ):

        if node.get('spanTo'):
            spanTo = node.get('spanTo')
            # find first occurence of the anchor tag #
            # and store this
            spanTo = spanTo[spanTo.find('#')+1:]
            status['delSpan'] = spanTo

        super().__init__(node=node, node_name=node_name, status=status)


class anchor(tei):
    """a delSpan element always points to an anchor object. Because of this, we need
    to alter the status back to normal when we encounter an anchor object.
    """
    def __init__(
        self, node=None, node_name=None, status=None, 
        attrs=None, parent_attrs=None, parent_labels=None,
        string=None
    ):

        if status.get('delSpan'):
            if status.get('delSpan') == node.get('xml:id'):
                status.pop('delSpan')

        super().__init__(node=node, node_name=node_name, status=status)


class unclear(ParseString, 
    unpack_elements=True,
    pass_label_to_children="unclear", 
    pass_attributes_to_children=True
):
    """ Elements <unclear> will not create a node in the graph,
    but they will pass their attributes to the children they contain
    and add an additional label :unclear
    """
    pass


class add(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="add",
    pass_attributes_to_children=True,
):
    """During parsing, this class should add the label "add"
    to every child element and all attributes should be passed to its children.
    """

class del_(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="del",
    pass_attributes_to_children=True,
):
    """During parsing, this class should add the label "del"
    to every child element and all attributes should be passed to its children.
    """

class subst(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="subst",
    pass_attributes_to_children=True,
):

    """
    Substitutions add some interpretation to the text,
    e.g. they suggest that a correction is done in one
    single pass. The del and add elements inside a subst
    are therefore grouped together.
    """

class metamark(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="metamark",
    pass_attributes_to_children=True,
):
    pass

class hi(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="hi",
    pass_attributes_to_children=True,
):
    pass


class sic(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="sic",
    create_empty_token_nodes=True,
    pass_attributes_to_children=True
):
    pass

class corr(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="corr",
    pass_attributes_to_children=True
):
    pass

class choice(
    ParseString,
    unpack_elements=True,
    pass_label_to_children="choice",
):
    pass
