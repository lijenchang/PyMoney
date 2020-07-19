#! /usr/bin/env python3.7

import sys 
import tkinter
from datetime import date
from pyrecord import Record, Records
from pycategory import Categories

# Define callback functions
def apply_category_search():
    target_categories = categories.find_subcategories( find_cat_str.get() )
    matched = records.find( target_categories )
    result_box.delete( 0, tkinter.END )
    total = 0
    for i, v in enumerate( matched ):
        result_box.insert( i, v ) 
        total += int( v.split()[3] ) 
    balance_str.set( f'Now you have {total} dollars.' )

def show_all_records():
    all = records.view() 
    result_box.delete( 0, tkinter.END )
    for i, v in enumerate( all ):
        result_box.insert( i, v ) 
    balance_str.set( f'Now you have {records.balance} dollars.' ) 
    # clean up the entry
    find_cat_str.set( '' )

def update_init_money():
    records.update_initial_money( init_money_str.get() ) 
    balance_str.set( f'Now you have {records.balance} dollars.' ) 
    show_all_records()
    # clean up the entry
    init_money_str.set( '' ) 

def add_record():
    record_str = ' '.join( [date_str.get(), category_str.get(), desc_str.get(), amount_str.get()] )
    records.add( record_str, categories ) 
    show_all_records() 
    # clean up the entries
    date_str.set( date.today().isoformat() ) 
    category_str.set( '' )
    desc_str.set( '' )
    amount_str.set( '' )

def delete_record():
    try:
        cur_idx = result_box.curselection()[0] 
    except IndexError:
        sys.stderr.write( 'Need to select an entry. Fail to delete a record.\n' )
    else:
        selected = result_box.get( cur_idx )
        total = int( balance_str.get().split()[3] ) - int( selected.split()[3] ) 
        # find the order
        order = 1
        for i, v in enumerate( result_box.get( 0, tkinter.END ) ):
            if i == cur_idx: break
            if v == selected:
                order += 1

        records.delete( ' '.join( selected.split() ), order ) 
        result_box.delete( cur_idx )
        balance_str.set( f'Now you have {total} dollars.' )

# Instantiation 
categories = Categories()
records = Records()

# Main Components
root = tkinter.Tk()
root.title( 'PyMoney' )
f = tkinter.Frame( root, borderwidth = 5 )

find_cat_label = tkinter.Label( f, text = 'Find category' )

find_cat_str = tkinter.StringVar()
find_cat_entry = tkinter.Entry( f, width = 25, textvariable = find_cat_str )

find_cat_btn = tkinter.Button( f, text = 'Find', command = apply_category_search )

reset_btn = tkinter.Button( f, text = 'Reset', command = show_all_records )

result_box = tkinter.Listbox( f, width = 50, font = ( 'Courier', 8 ) )

balance_str = tkinter.StringVar()
balance_str.set( f'Now you have {records.balance} dollars.' )
balance_label = tkinter.Label( f, textvariable = balance_str )

init_money_label = tkinter.Label( f, text = 'Initial money', justify = tkinter.CENTER )

init_money_str = tkinter.StringVar()
init_money_entry = tkinter.Entry( f, width = 25, textvariable = init_money_str )

init_money_btn = tkinter.Button( f, text = 'Update', command = update_init_money )

date_label = tkinter.Label( f, text = 'Date', justify = tkinter.CENTER )

date_str = tkinter.StringVar()
date_str.set( date.today().isoformat() ) 
date_entry = tkinter.Entry( f, width = 25, textvariable = date_str )

category_label = tkinter.Label( f, text = 'Category', justify = tkinter.CENTER )

category_str = tkinter.StringVar()
category_entry = tkinter.Entry( f, width = 25, textvariable = category_str )

desc_label = tkinter.Label( f, text = 'Description', justify = tkinter.CENTER )

desc_str = tkinter.StringVar()
desc_entry = tkinter.Entry( f, width = 25, textvariable = desc_str )

amount_label = tkinter.Label( f, text = 'Amount', justify = tkinter.CENTER )

amount_str = tkinter.StringVar()
amount_entry = tkinter.Entry( f, width = 25, textvariable = amount_str )

add_record_btn = tkinter.Button( f, text = 'Add a record', command = add_record )

delete_btn = tkinter.Button( f, text = 'Delete', command = delete_record )

categories_view = tkinter.Label( f, text = 'Categories:\n' + categories.view(), font = ( 'Courier', 8 ), justify = tkinter.LEFT )

# Grid Layout
f.grid( row = 0, column = 0 )
find_cat_label.grid( row = 0, column = 0 )
find_cat_entry.grid( row = 0, column = 1, columnspan = 4 )
find_cat_btn.grid( row = 0, column = 5 ) 
reset_btn.grid( row = 0, column = 6 )
result_box.grid( row = 1, column = 0, rowspan = 8, columnspan = 7 )
balance_label.grid( row = 9, column = 0, columnspan = 2 )
init_money_label.grid( row = 1, column = 7 )
init_money_entry.grid( row = 1, column = 8, columnspan = 4 )
init_money_btn.grid( row = 2, column = 11 )
date_label.grid( row = 5, column = 7 )
date_entry.grid( row = 5, column = 8, columnspan = 4 )
category_label.grid( row = 6, column = 7 )
category_entry.grid( row = 6, column = 8, columnspan = 4 )
desc_label.grid( row = 7, column = 7 )
desc_entry.grid( row = 7, column = 8, columnspan = 4 )
amount_label.grid( row = 8, column = 7 )
amount_entry.grid( row = 8, column = 8, columnspan = 4 )
add_record_btn.grid( row = 9, column = 11 )
delete_btn.grid( row = 9, column = 6 )
categories_view.grid( row = 1, column = 12, rowspan = 9, columnspan = 6, padx = (10, 2) )

show_all_records() 
tkinter.mainloop() 
records.save() 
