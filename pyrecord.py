import sys
from datetime import date

class Record:
    """Represent a record."""
    def __init__( self, date, category, description, amount ):
        """Initialize the Record."""
        self._date = date
        self._category = category
        self._description = description
        self._amount = amount
    # Operator Overloading for "=="
    def __eq__( self, right ):
        return ( self._date, self._category, self._description, self._amount ) == ( right.date, right.category, right.description, right.amount )
    # Getter Methods 
    @property
    def date( self ):
        """Get the attribute 'date'."""
        return self._date
    @property
    def category( self ):
        """Get the attribute 'category'."""
        return self._category
    @property
    def description( self ):
        """Get the attribute 'description'."""
        return self._description
    @property
    def amount( self ):
        """Get the attribute 'amount'."""
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__( self ):
        """Initialize Records."""
        self._initial_money = 0
        self._records = [] 
        try:
            fh = open( 'records.txt', 'r' ) 
            # Get the previously stored initial money and records 
            try:
                self._initial_money = int( fh.readline() ) 
                for line in fh.readlines():
                    entry = line.split() 
                    self._records.append( Record( date.fromisoformat( entry[0] ), entry[1], entry[2], int( entry[3] ) ) )  
            except:
                fh.close() 
                # Delete the contents in the file and clear the list of records
                open( 'records.txt', 'w' ).close() 
                self._records.clear() 
                sys.stderr.write( 'Invalid format in "records.txt". Deleting the contents.\n' ) 
                raise FileNotFoundError 
            else: 
                fh.close()
                print( 'Welcome back!' ) 
        except FileNotFoundError:
            self._initial_money = 0 
    
    @property
    def balance( self ):
        return self._initial_money + sum( [r.amount for r in self._records] )
    
    def update_initial_money( self, new_amount_str ):
        try:
            self._initial_money = int( new_amount_str )
        except:
            sys.stderr.write( 'Invalid value for money. Fail to update initial money.\n' ) 

    def add( self, record_str, categories ):
        """Add the given 'Record' into 'Records'."""
        try:
            detail = record_str.split() 
            # Check format
            if len( detail ) == 3:
                detail.insert( 0, date.today() ) 
            elif len( detail ) == 4:
                try:
                    detail[0] = date.fromisoformat( detail[0] ) 
                except ValueError:
                    sys.stderr.write( 'The format of date should be YYYY-MM-DD.\nFail to add a record.\n' ) 
                    return
            else:
                raise TypeError( 'Fail to add a record. Category, description, and amount are required.\n' ) 

            # Check category 
            if not categories.is_category_valid( detail[1] ):
                raise TypeError( 'The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.\n' ) 
            
            record = Record( detail[0], detail[1], detail[2], int( detail[3] ) )
            self._records.append( record ) 
        except TypeError as err:
            sys.stderr.write( str( err ) ) 
        except ValueError:
            sys.stderr.write( 'Invalid value for money. Fail to add a record.\n' ) 
    
    def view( self ):
        """Return the list of all the 'Record's in 'Records'."""
        return [f'{r.date.isoformat():<{10}} {r.category:<{15}} {r.description:<{15}} {r.amount:<{5}}' for r in self._records] 
    
    def delete( self, record_str, order ):
        """Delete a specified 'Record' from 'Records'."""
        try:
            detail = record_str.split() 
            if len( detail ) != 4:
                raise TypeError  

            target = Record( date.fromisoformat( detail[0] ), detail[1], detail[2], int( detail[3] ) )  
            cnt = self._records.count( target ) 
            if cnt == 0: 
                raise IndexError( 'No matched record. Fail to delete a record.\n' ) 
        except ( TypeError, ValueError ):     # Invalid format for deletion 
            sys.stderr.write( 'Fail to delete a record. Correct Format: <date:yyyy-mm-dd> <category> <desc> <amt>.\n' ) 
            return
        except IndexError as err:     # Wrong specification of the record name  
            sys.stderr.write( str( err ) ) 
            return

        if order > cnt: 
            sys.stderr.write( f"There's only {cnt} matched record{'s' if cnt > 1 else ''}. Fail to delete a record.\n" )
            return
        elif order < 1: 
            sys.stderr.write( 'Order should be greater than or equal to 1. Fail to delete a record.\n' )
            return

        for i, v in enumerate( self._records ):   # Need index to pop the certain element during iteration 
            if v == target and order == 1:
                self._records.pop( i ) 
                break 
            elif v == target and order > 1:
                order -= 1
    
    def find( self, target_categories ):
        """Return the list of 'Record's whose category are in the given list."""
        matched = filter( lambda r: r.category in target_categories , self._records )
        return [f'{r.date.isoformat():<{10}} {r.category:<{15}} {r.description:<{15}} {r.amount:<{5}}' for r in matched] 


    def save( self ):
        """Write the initial money and 'Record's into the file.""" 
        with open( 'records.txt', 'w' ) as fh:
            fh.write( str( self._initial_money ) + '\n' )
            L = [record.date.isoformat() + ' ' + record.category + ' ' + record.description + ' ' + str( record.amount ) + '\n' for record in self._records] 
            fh.writelines( L )
    