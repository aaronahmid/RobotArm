"""
Contains Hadler for handling states related funtions
"""
import states


class StateHandler:
    """
    handles state related funtions
    """
    SUPPORTED_FRAMEWORKS = {
        'django': 'states.django_state.DjangoState'
    }

    def setCurrentState(self, id):
        """
        Sets The current state to use

        Args:
            id [uuid]: unique identifier of states object
        
        Returns:
            None if state does not exists
        """
        if id is None:
            return "id cannot be empty"

        if id in states.storage.all().keys():
            states.storage.__states['current_state'] = id
            states.storage.save()
            return states.storage.get(id)['name']
        return None

    def activate(self, id):
        """
        activates a state by setting it as current state

         Args:
            id [uuid]: unique identifier of states object
        
        Returns:
            None if setCurrentState returns None
        """
        state_name = self.setCurrentState(id)
        return state_name

    def createState(self, file_name):
        """
        Parses a Yaml File into a python native dictionary objects
        and creats a state

         Args:
            file_name [string]: name of or path to file
        
        Returns:
            
        """
        yaml_dict = self.parseYamlFile(file_name)

        if yaml_dict:
            framework = yaml_dict['framework']
            try:
                eval(self.SUPPORTED_FRAMEWORKS[framework])(**yaml_dict)
                states.storage.save()
            except KeyError:
                exit(f'Oops {framework} not supported yet')

    def deleteState(self, id):
        """
        deletes a state object

         Args:
            id [uuid]: unique identifier of states object
        
        Returns:
            None if state does not exists
        """
        try:
            states.storage.delete(id)
        except Exception:
            return None
