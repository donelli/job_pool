
class ElementNotFoundException(Exception):
   
   """
   Element not found exception
   """
   
   def __init__(self, element_name, class_ = "", id = ""):
      self.element_name = element_name
      self.class_ = class_
      self.id = id

   def __str__(self):
      return "Element '{}' not found.".format(self.element_name)
