class Categories:
    """Maintain the category list and provide some methods."""
    def __init__( self ):
        """Initialize Categories."""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view( self ):
        """Return the categories with indentation."""
        def view_categories( categories, level = 0 ):
            if categories == None: return
            if type( categories ) == list:
                result = ''
                for child in categories:
                    result += view_categories( child, level + 1 ) 
                return result
            else:
                return f'{" " * 2 * ( level - 1 )}- {categories}\n'
        return view_categories( self._categories ) 
    
    def is_category_valid( self, category ):
        """Check whether a category name is in the list of categories."""
        def check_category( category, categories ):
            if type( categories ) == list:
                for v in categories:
                    result = check_category( category, v )
                    if result == True:
                        return True
            return category == categories
        return check_category( category, self._categories ) 
    
    def find_subcategories( self, category ):
        """Get the list containing the target category and its subcategories."""
        def find_subcategories_gen( category, categories, found = False ):
            if type( categories ) == list:   # recursive case
                for i, child in enumerate( categories ):
                    yield from find_subcategories_gen( category, child, found )
                    if child == category and i + 1 < len( categories ) and type( categories[i + 1] ) == list:
                        yield from find_subcategories_gen( category, categories[i + 1], True )
            else:   # base case
                if categories == category or found == True:
                    yield categories
        
        return [i for i in find_subcategories_gen( category, self._categories )] 
