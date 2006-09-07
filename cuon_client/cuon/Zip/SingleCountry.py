##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 
import sys
import os
sys.path.append(os.environ['CUON_PATH'])

from cuon.Databases.SingleData import SingleData
import logging
import threading

class SingleCountry(SingleData):

    
    def __init__(self, allTables):

        SingleData.__init__(self)
        # tables.dbd and address
        self.sNameOfTable =  "country"
        self.xmlTableDef = 0
        print 'allTables = ',`allTables`
        self.loadTable(allTables)
        
        self.listHeader['names'] = ['name', 'zip', 'city', 'Street', 'ID']
        self.listHeader['size'] = [25,10,25,25,10]
