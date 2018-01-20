from src.entities.entity_factory import build_entity


class Battlefield(object):

    pass


class Group(object):

    def __init__(self):
        self.state = {}

    def add(self, entity_name):
        if entity_name not in self.state:
            self.state[entity_name] = []
        entity = build_entity(entity_name)
        thang = {'entity_index': len(self.state[entity_name]),
                 'wounds': entity.wounds,
                 'name': entity.name}
        self.state[entity_name].append(thang)

    def remove(self, entity_name, entity_index=-1):
        entity_list = self.state[entity_name]
        del entity_list[entity_index]
        self.state[entity_name] = entity_list

    @property
    def frontend(self):
        entities = {}
        for entity_name, something in self.state.iteritems():
            print something
            if len(something) <= 1:
                entities[something[0]['name']] = {
                    'wounds': something[0]['wounds']}
            else:
                for entity_information in something:
                    index = entity_information['entity_index'] + 1
                    entities[entity_information['name'] + '_' +
                             str(index)] = {'wounds': entity_information['wounds']}
        return entities
