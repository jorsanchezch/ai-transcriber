import abc
from google.cloud import language_v1
from proto.enums import Enum
from .utils import match_strings

class Service(abc.ABC):
    pass

class Analysis(Service):
    def __init__(self):
        self.lang = language_v1.LanguageServiceClient()

    # I may do this instead by prompting a generative AI, passing the fields and asking to return the mentions of user's inputs.
    # I may also train an entity model myself.
    def analyze(self, text): 
        doc = language_v1.Document(
            content=text, 
            type=language_v1.Document.Type.PLAIN_TEXT,
        )
        
        return self.lang.analyze_entities(document=doc)
    
    def match_entity(self, type: Enum, field):
        return match_strings(type.name, field)
    
    def match_entities(self, analysis: language_v1.AnalyzeEntitiesResponse, fields):
        matches = {}

        for field in fields:
            matches[field] = set()
            
            for entity in analysis.entities:
                if (self.match_entity(entity.type_, field)):
                    matches[field].add(entity.name)
                    
                for mention in entity.mentions:
                    if (self.match_entity(mention.type_, field)):
                        matches[field].add(mention.name)
                    
        return matches
        