class lists_addresses:
    def __init__(self):
        pass
    
   
    def readSearchDatafields(self):
        dicSearchfields = {}
        dicSearchfields['eLastnameFrom'] = self.getWidget('eLastnameFrom').get_text()
        dicSearchfields['eLastnameTo'] = self.getWidget('eLastnameTo').get_text()

        dicSearchfields['eFirstnameFrom'] = self.getWidget('eFirstnameFrom').get_text()
        dicSearchfields['eFirstnameTo'] = self.getWidget('eFirstnameTo').get_text()
        
        dicSearchfields['eCityFrom'] = self.getWidget('eCityFrom').get_text()
        dicSearchfields['eCityTo'] = self.getWidget('eCityTo').get_text()

        dicSearchfields['eCountryFrom'] = self.getWidget('eCountryFrom').get_text()
        dicSearchfields['eCountryTo'] = self.getWidget('eCountryTo').get_text()

        dicSearchfields['eInfoContains'] = self.getWidget('eInfoContains').get_text()
        dicSearchfields['eNewsletterContains'] = self.getWidget('eNewsletterContains').get_text()
        

        return dicSearchfields
    
