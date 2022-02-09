
class ElementNotFoundException(Exception):
   
   """
   Element not found exception
   """
   
   def __init__(self, element_name, class_ = "", id = ""):
      self.element_name = element_name
      self.class_ = class_
      self.id = id

   def __str__(self):
      
      if self.class_ != "":
         return "Element '{}' with class '{}' not found.".format(self.element_name, self.class_)
      elif self.id != "":
         return "Element '{}' with id '{}' not found.".format(self.element_name, self.id)
      
      return "Element '{}' not found.".format(self.element_name)
