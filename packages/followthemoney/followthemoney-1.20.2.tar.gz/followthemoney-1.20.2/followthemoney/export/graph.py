import json
import stringcase
import networkx as nx
from pprint import pprint  # noqa
from banal import ensure_list
from networkx.readwrite.gexf import generate_gexf

from followthemoney.types import registry
from followthemoney.export.common import Exporter

DEFAULT_EDGE_TYPES = (registry.entity.name,)


def edge_types():
    return [t.name for t in registry.types if t.matchable]


class GraphExporter(Exporter):
    """Base functions for exporting a property graph from a stream
    of entities."""

    def __init__(self, edge_types=DEFAULT_EDGE_TYPES):
        self.edge_types = edge_types

    def get_attributes(self, proxy):
        attributes = {}
        for prop, values in proxy._properties.items():
            if prop.type.name not in self.edge_types:
                attributes[prop.name] = prop.type.join(values)
        return attributes

    def get_id(self, type_, value):
        return str(type_.rdf(value))

    def write_edges(self, proxy):
        attributes = self.get_attributes(proxy)
        attributes['weight'] = 1
        for (source, target) in proxy.edgepairs():
            self.write_edge(proxy, source, target, attributes)

    def write(self, proxy):
        if proxy.schema.edge:
            self.write_edges(proxy)
        else:
            self.write_node(proxy)
            for prop, values in proxy._properties.items():
                if prop.type.name not in self.edge_types:
                    continue
                for value in ensure_list(values):
                    weight = prop.specificity(value)
                    if weight == 0:
                        continue
                    self.write_link(proxy, prop, value, weight)


class NXGraphExporter(GraphExporter):
    """Write to NetworkX data structure, which in turn can be exported
    to the file formats for Gephi (GEXF) and D3."""

    def __init__(self, fh, edge_types=DEFAULT_EDGE_TYPES):
        super(NXGraphExporter, self).__init__(edge_types=edge_types)
        self.graph = nx.MultiDiGraph()
        self.fh = fh

    def _make_node(self, id, attributes):
        if not self.graph.has_node(id):
            self.graph.add_node(id, **attributes)
        else:
            self.graph.node[id].update(attributes)

    def write_edge(self, proxy, source, target, attributes):
        source = self.get_id(registry.entity, source)
        self._make_node(source, {})

        target = self.get_id(registry.entity, target)
        self._make_node(target, {})

        attributes['schema'] = proxy.schema.name
        self.graph.add_edge(source, target, **attributes)

    def write_node(self, proxy):
        node_id = self.get_id(registry.entity, proxy.id)
        attributes = self.get_attributes(proxy)
        attributes['label'] = proxy.caption
        attributes['schema'] = proxy.schema.name
        self._make_node(node_id, attributes)

    def write_link(self, proxy, prop, value, weight):
        node_id = self.get_id(registry.entity, proxy.id)
        other_id = self.get_id(prop.type, value)
        attributes = {}
        if prop.type != registry.entity:
            attributes['label'] = value
            attributes['schema'] = prop.type.name
        self._make_node(node_id, attributes)
        self.graph.add_edge(node_id, other_id,
                            weight=weight,
                            schema=prop.qname)

    def finalize(self):
        for line in generate_gexf(self.graph, prettyprint=False):
            self.fh.write(line)


class CypherGraphExporter(GraphExporter):
    """Cypher query format, used for import to Neo4J. This is a bit like
    writing SQL with individual statements - so for large datasets it
    might be a better idea to do a CSV-based import."""
    # https://www.opencypher.org/
    # MATCH (n) DETACH DELETE n;

    def __init__(self, fh, edge_types=DEFAULT_EDGE_TYPES):
        super(CypherGraphExporter, self).__init__(edge_types=edge_types)
        self.fh = fh

    def _to_map(self, data):
        values = []
        for key, value in data.items():
            value = '%s: %s' % (key, json.dumps(value))
            values.append(value)
        return ', '.join(values)

    def _make_node(self, attributes, label):
        cypher = 'MERGE (p { %(id)s }) ' \
                 'SET p += { %(map)s } SET p :%(label)s;\n'
        self.fh.write(cypher % {
            'id': self._to_map({'id': attributes.get('id')}),
            'map': self._to_map(attributes),
            'label': ':'.join(ensure_list(label))
        })

    def _make_edge(self, source, target, attributes, label):
        cypher = 'MATCH (s { %(source)s }), (t { %(target)s }) ' \
                 'MERGE (s)-[:%(label)s { %(map)s }]->(t);\n'
        label = [stringcase.constcase(l) for l in ensure_list(label)]
        self.fh.write(cypher % {
            'source': self._to_map({'id': source}),
            'target': self._to_map({'id': target}),
            'label': ':'.join(label),
            'map': self._to_map(attributes),
        })

    def write_edge(self, proxy, source, target, attributes):
        source = self.get_id(registry.entity, source)
        source_prop = proxy.schema.get(proxy.schema.edge_source)
        self._make_node({'id': source}, source_prop.range.name)

        target = self.get_id(registry.entity, target)
        target_prop = proxy.schema.get(proxy.schema.edge_target)
        self._make_node({'id': target}, target_prop.range.name)
        self._make_edge(source, target, attributes, proxy.schema.name)

    def write_node(self, proxy):
        node_id = self.get_id(registry.entity, proxy.id)
        attributes = self.get_attributes(proxy)
        attributes['name'] = proxy.caption
        attributes['id'] = node_id
        self._make_node(attributes, proxy.schema.names)

    def write_link(self, proxy, prop, value, weight):
        node_id = self.get_id(registry.entity, proxy.id)
        other_id = self.get_id(prop.type, value)
        label = prop.type.name
        attributes = {'id': other_id}
        if prop.type == registry.entity and prop.range:
            label = prop.range.name
        else:
            attributes['name'] = value
        self._make_node(attributes, label)
        attributes = {'weight': weight}
        self._make_edge(node_id, other_id, attributes, prop.name)
