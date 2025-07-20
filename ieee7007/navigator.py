import networkx as nx
import matplotlib.pyplot as plt


class PropertyRelation:
    def __init__(self, prop, source, target):
        self.prop = prop
        self.source = source
        self.target = target

    def __repr__(self):
        return f'property: {self.prop}, source: {self.source}, target: {self.target}'


class OntologyNavigator:
    def __init__(self, ontology):
        self.__onto__ = ontology

    @property
    def all_individuals(self):
        return self.__onto__.world.individuals()

    @property
    def all_classes(self):
        return self.__onto__.world.classes()

    @property
    def all_properties(self):
        return list(self.__onto__.world.properties())

    @property
    def all_rules(self):
        return list(self.__onto__.world.rules())

    def get_number_of_individuals(self):
        return len(list(self.all_individuals))

    def dump_ontology(self):
        print("\nindividuals:")
        for i in self.all_individuals:
            print(f"\n\t{i}")
            if (properties := self.get_all_properties_of_an_individual(i)):
                print("\tproperties:")
            for p in properties:
                for _, target in p.get_relations():
                    print(f"\t\t{p} {target}")

            if (inv_p := self.get_all_inverse_properties_of_an_individual(i)):
                print("\tinverse properties:")
            for source, p in inv_p:
                print(f"\t\t{source} {p}")

    def _get_individual_label(self, individual):
        return f"{individual.is_a}\n{individual.get_name()}"

    def _get_edge_id(self, source, relation, target):
        return hash(f"{source.name}{relation.name}{target.name}")

    def __add_individual_to_plot(self, plot, nodes: set, individual):
        if individual.get_name() in nodes:
            return
        _label = self._get_individual_label(individual)
        plot.add_node(_label, t=len(_label))
        nodes.add(individual.get_name())

    def __add_relation_to_plot(self, plot, edges: set, relation, source, target):
        _edge_id = self._get_edge_id(source, relation, target)
        if _edge_id in edges:
            return

        _source_label = self._get_individual_label(source)
        _target_label = self._get_individual_label(target)
        plot.add_edge(_source_label, _target_label, r=relation)
        edges.add(_edge_id)

    def plot(self, draw=True):
        G = nx.DiGraph()
        nodes = set()
        edges = set()

        for i in self.all_individuals:
            self.__add_individual_to_plot(G, nodes, i)
            for p in self.get_all_properties_of_an_individual(i):
                for _, target in p.get_relations():
                    self.__add_individual_to_plot(G, nodes, target)
                    self.__add_relation_to_plot(G, edges, p, i, target)

        options = {
            "font_size": 7,
            "node_size": 3000,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 2,
            "width": 2,
        }
        # pos = nx.spring_layout(G, k=1, iterations=20)
        pos = nx.nx_agraph.graphviz_layout(G, prog="neato")

        edge_labels = nx.get_edge_attributes(G, 'r')
        nx.draw_networkx(G, pos=pos, **options)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        if draw:
            plt.show()
        plt.close('all')

    def plot_individual(self, individual, individual_color='#557dd4', draw=True):
        G = nx.DiGraph()
        nodes = set()
        edges = set()

        self.__add_individual_to_plot(G, nodes, individual)
        for p in self.get_all_properties_of_an_individual(individual):
            for source, target in p.get_relations():
                if source != individual:
                    continue
                print(individual, source)
                self.__add_individual_to_plot(G, nodes, target)
                self.__add_relation_to_plot(G, edges, p, individual, target)

        for p in self.get_all_inverse_properties_of_an_individual(individual):
            source, prop = p
            self.__add_individual_to_plot(G, nodes, source)
            self.__add_relation_to_plot(G, edges, prop, source, individual)

        color_map = [individual_color if n == individual.get_name() else 'white' for n in nodes]
        options = {
            "font_size": 7,
            "node_size": 3000,
            "node_color": color_map,
            "edgecolors": "black",
            "linewidths": 2,
            "width": 2,
        }
        # pos = nx.spring_layout(G, k=1, iterations=20)
        pos = nx.nx_agraph.graphviz_layout(G, prog="neato")

        edge_labels = nx.get_edge_attributes(G, 'r')
        nx.draw_networkx(G, pos=pos, **options)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        if draw:
            plt.show()
        plt.close('all')

    def search_individual_by_name(self, name, strict=False):
        name = name if strict else f'*{name}*'
        search_result = self.__onto__.search(iri=name)
        return search_result

    def get_individual_by_name(self, name):
        for i in self.all_individuals:
            if i.name == name:
                return i
        return None

    def get_class_by_name(self, name, strict=False):
        possible_classes = list()
        for cls in self.all_classes:
            if strict and cls.name == name:
                possible_classes.append(cls)
            if not strict and name in cls.name:
                possible_classes.append(cls)
        return possible_classes

    def get_individuals_of_a_class(self, cls):
        individuals = list(x for x in self.all_individuals if cls in x.is_a)
        return individuals

    def get_individuals_of_a_class_by_class_name(self, classname, strict=False):
        search_result = list()
        for cls in self.get_class_by_name(classname):
            search_result.extend(self.__onto__.search(type=cls))
        return search_result

    def get_all_properties_of_an_individual(self, individual):
        return list(individual.get_properties())

    def get_all_inverse_properties_of_an_individual(self, individual):
        return list(individual.get_inverse_properties())

    def get_target_of_property(self, property_):
        pass

    def get_all_individuals(self):
        return list(self.all_individuals)

    def get_all_properties_relations_of_an_individual(self, individual):
        _props = self.get_all_properties_of_an_individual(individual)
        _all_relations = {x: list(x.get_relations()) for x in _props}

        _relations = list()

        for p, relation_list in _all_relations.items():
            for relation in relation_list:
                if relation[0] != individual:
                    continue

                _relations.append(PropertyRelation(p, relation[0], relation[1]))

        return _relations

    def get_individual_by_index(self, index):
        return self.get_all_individuals()[index]

    def get_property_of_individual_by_index(self, individual, index):
        return self.get_all_properties_of_an_individual(individual)[index]

    def get_inverse_property_of_individual_by_index(self, individual, index):
        return self.get_all_inverse_properties_of_an_individual(individual)[index]

    def search_relation_between_individual_and_class(self, individual, target_class, ignore_list=[]):
        original_individual = individual
        previous_visited = list()
        return self._recursive_deep_search_class_from_individual(original_individual,
                                                                 target_class.value,
                                                                 previous_visited, ignore_list)

    def _recursive_deep_search_class_from_individual(self, individual, target_class, visited_list,
                                                     ignore_list):

        if individual not in ignore_list and target_class in [x.name for x in individual.is_a]:
            return individual

        if individual in visited_list:
            return None

        _tmp = self.get_all_properties_relations_of_an_individual(individual)

        for property_relation in _tmp:
            next_hop = self._recursive_deep_search_class_from_individual(property_relation.target,
                                                                         target_class,
                                                                         visited_list,
                                                                         ignore_list)
            if next_hop:
                return (property_relation.source, property_relation.prop, next_hop)

            visited_list.append(individual)

    def search_inverse_relation_between_individual_and_class(self, individual, target_class, ignore_list=[]):
        original_individual = individual
        previous_visited = list()
        return self._recursive_inverse_deep_search_class_from_individual(original_individual,
                                                                         target_class,
                                                                         previous_visited,
                                                                         ignore_list)

    def _recursive_inverse_deep_search_class_from_individual(self, individual, target_class,
                                                             visited_list, ignore_list):

        if individual not in ignore_list and target_class in [x.name for x in individual.is_a]:
            return individual

        if individual in visited_list:
            return None

        _tmp = self.get_all_inverse_properties_of_an_individual(individual)

        for relation in _tmp:
            next_hop = self._recursive_inverse_deep_search_class_from_individual(
                relation[0],
                target_class,
                visited_list,
                ignore_list)
            if next_hop:
                return (individual, relation[1], next_hop)
            visited_list.append(individual)
