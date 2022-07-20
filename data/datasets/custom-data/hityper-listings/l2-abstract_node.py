# File: miyakogi.wdom/wdom/node.py
# Human annotation: AbstractNode
# Typilus: ForeachClauseNode HiTyper


class Node(AbstractNode):
    """Base Class for Node interface."""

    @property
    def connected(self) -> bool:
        """When this instance has any connection, return True."""
        return False

    def __init__(self, parent: AbstractNode = None) -> None:
        """Initialize node object with parent node.
        :param Node parent: parent node.
        """
        super().__init__()  # Need to call init in multiple inheritce
        self.__children = list()  # type: List[Node]
        self.__parent = None
        if parent:
            parent.appendChild(self)

    def __bool__(self) -> bool:
        """Return always True."""
        return True

    def __len__(self) -> int:
        """Return number of child nodes."""
        return self.length

    def __contains__(self, other: AbstractNode) -> bool:
        return other in self.__children

    # DOM Level 1
    @property
    def length(self) -> int:
        """Return number of child nodes."""
        return len(self.childNodes)

    @property
    def parentNode(self) -> Optional[AbstractNode]:
        """Return parent node.
        If this node does not have a parent, return ``None``.
        """
        return self.__parent

    @property
    def childNodes(self) -> 'NodeList':
        """Return child nodes of this node.
        Returned object is an instance of NodeList, which is a list like object
        but not support any modification. NodeList is a **live object**, which
        means that changes on this node is reflected to the object.
        """
        return NodeList(self.__children)

    @property
    def firstChild(self) -> Optional[AbstractNode]:
        """Return the first child node.
        If this node does not have any child, return ``None``.
        """
        if self.hasChildNodes():
            return self.childNodes[0]
        return None

    @property
    def lastChild(self) -> Optional[AbstractNode]:
        """Return the last child node.
        If this node does not have any child, return ``None``.
        """
        if self.hasChildNodes():
            return self.childNodes[-1]
        return None

    @property
    def previousSibling(self) -> Optional[AbstractNode]:
        """Return the previous sibling of this node.
        If there is no previous sibling, return ``None``.
        """
        parent = self.parentNode
        if parent is None:
            return None
        return parent.childNodes.item(parent.childNodes.index(self) - 1)

    @property
    def nextSibling(self) -> Optional[AbstractNode]:
        """Return the next sibling of this node.
        If there is no next sibling, return ``None``.
        """
        parent = self.parentNode
        if parent is None:
            return None
        return parent.childNodes.item(parent.childNodes.index(self) + 1)

    # DOM Level 2
    @property
    def ownerDocument(self) -> Optional[AbstractNode]:
        """Return the owner document of this node.
        Owner document is an ancestor document node of this node. If this node
        (or node tree including this node) is not appended to any document
        node, this property returns ``None``.
        :rtype: Document or None
        """
        if self.nodeType == Node.DOCUMENT_NODE:
            return self
        elif self.parentNode:
            return self.parentNode.ownerDocument
        return None

    # Methods
    def _append_document_fragment(self, node: AbstractNode) -> AbstractNode:
        for c in tuple(node.childNodes):
            self._append_child(c)
        return node

    ''' THESE METHODS -------------------------------- '''

    def _append_element(self, node: AbstractNode) -> AbstractNode:
        if node.parentNode:
            node.parentNode.removeChild(node)
        self.__children.append(node)
        node.__parent = self
        return node

    def _append_child(self, node: AbstractNode) -> AbstractNode:
        if not isinstance(node, Node):
            raise TypeError(
                'appndChild() only accepts a Node instance, but get {}. '
                'If you want to add string or mupltiple nodes once, '
                'use append() method instead.'.format(type(node)))
        if node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            return self._append_document_fragment(node)
        return self._append_element(node)

    ''' -------------------------------------------- '''

    def appendChild(self, node: AbstractNode) -> AbstractNode:
        """Append the node at the last of this child nodes."""
        return self._append_child(node)

    '''
    def index(self, node: AbstractNode) -> int:
        """Return index of the node.
        If the node is not a child of this node, raise ``ValueError``.
        """
        if node in self.childNodes:
            return self.childNodes.index(node)
        elif isinstance(node, Text):
            for i, n in enumerate(self.childNodes):
                # should consider multiple match?
                if isinstance(n, Text) and n.data == node:
                    return i
        raise ValueError('node is not in this node')
    '''

    def _insert_document_fragment_before(self, node: AbstractNode,
                                         ref_node: AbstractNode
                                         ) -> AbstractNode:
        for c in tuple(node.childNodes):
            self._insert_before(c, ref_node)
        return node

    def _insert_element_before(self, node: AbstractNode,
                               ref_node: AbstractNode) -> AbstractNode:
        if node.parentNode:
            node.parentNode.removeChild(node)
        self.__children.insert(self.index(ref_node), node)
        node.__parent = self
        return node

    def _insert_before(self, node: AbstractNode, ref_node:
                       AbstractNode) -> AbstractNode:
        if not isinstance(node, Node):
            raise TypeError(
                'insertBefore() only accepts a Node instance, but get {}.'
                'If you want to insert string or mupltiple nodes, '
                'use ref_node.before() instead.'.format(type(node)))
        if node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            return self._insert_document_fragment_before(node, ref_node)
        return self._insert_element_before(node, ref_node)

    def insertBefore(self, node: AbstractNode,
                     ref_node: AbstractNode) -> AbstractNode:
        """Insert a node just before the reference node."""
        return self._insert_before(node, ref_node)

    def hasChildNodes(self) -> bool:
        """Return True if this node has child nodes, otherwise return False."""
        return bool(self.childNodes)

    def _remove_child(self, node: AbstractNode) -> AbstractNode:
        if node not in self.__children:
            raise ValueError('node to be removed is not a child of this node.')
        self.__children.remove(node)
        node.__parent = None
        return node

    def removeChild(self, node: AbstractNode) -> AbstractNode:
        """Remove a node from this node.
        If node is not a child of this node, raise ``ValueError``.
        """
        return self._remove_child(node)

    def _replace_child(self, new_child: AbstractNode,
                       old_child: AbstractNode) -> AbstractNode:
        self._insert_before(new_child, old_child)
        return self._remove_child(old_child)

    def replaceChild(self, new_child: AbstractNode,
                     old_child: AbstractNode) -> AbstractNode:
        """Replace an old child with new child."""
        return self._replace_child(new_child, old_child)

    def hasAttributes(self) -> bool:
        """Return True if this node has attributes."""
        return hasattr(self, 'attributes') and bool(self.attributes)

    def _clone_node(self) -> 'Node':
        clone = type(self)()
        return clone

    def _clone_node_deep(self) -> 'Node':
        clone = self._clone_node()
        for child in self.childNodes:
            clone.appendChild(child._clone_node_deep())
        return clone

    def cloneNode(self, deep: bool=False) -> AbstractNode:
        """Return new copy of this node.
        If optional argument ``deep`` is specified and is True, new node has
        clones of child nodes of this node (if presents).
        """
        if deep:
            return self._clone_node_deep()
        return self._clone_node()

    __copy__ = _clone_node  # alias

    def __deepcopy__(self, memo: Any) -> 'Node':
        return self.cloneNode(True)

    def _empty(self) -> None:
        for child in tuple(self.__children):
            self._remove_child(child)

    def empty(self) -> None:
        """[Not Standard] Remove all child nodes from this node.
        This is equivalent to ``node.textContent = ''``.
        """
        self._empty()

    def _get_text_content(self) -> str:
        return ''.join(child.textContent for child in self.childNodes)

    def _set_text_content(self, value: str) -> None:
        self._empty()
        if value:
            self._append_child(Text(value))

    @property
    def textContent(self) -> str:
        """Return text contents of this node and all chid nodes.
        When any value is set to this property, all child nodes are removed and
        new value is set as a text node.
        """
        return self._get_text_content()

    @textContent.setter
    def textContent(self, value: str) -> None:
        """Remove all child nodes and set new text."""
        self._set_text_content(value)
