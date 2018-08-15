"""@package tests
Bose (Dark Phoenix) project:
C10415 (check_method = 'bom_table')
C10416 (check_method = 'clipboard')
C10417 (check_method = 'preview')

BOM - Create and verify a BOM report (within BOM tab) & export to excel & html preview
Not going to install excel on the Jenkins machines - so just parsing and checking 
the data from the clipboard. Project settings covered in another test

Currently only intended to verify one speaker type at a time

author Rob Brooks
"""

#global setup
source(findFile("scripts", "BAT.py"))

#imports
from lib_BAT_Test_Execution import *
from lib_BAT_Navigation import *
from lib_BAT_File_IO import *
from lib_BAT_System import *
from lib_BAT_BOM import *

import dputils

@bat_test()
def main():
    
    check_method = 'bom_table' #default bom_table
    if "params" in params() and "check_method" in params()["params"]:
        check_method = params()["params"]["check_method"]
            
    do_new_project()
    select_view_tab('speaker')
            
    for scenario in testData.dataset('data_test.tsv'):

        quantity = integer(testData.field(scenario, 'sQuantity'))
        modules = integer(testData.field(scenario, 'sModuleCount'))
        speaker = testData.field(scenario, 'sSpeaker')
        spkr_info = lookup_BOM_product_info('ITEM',speaker)
        
        test.log('Adding %s x %s with %s modules' %(quantity, speaker, modules))
        for count in xrange(1, quantity +1):
            add_speaker() # can't specify type yet

            if modules > 0:
                speaker_name = spkr_info['NAME'] + ' ' + str(count)
                edit_speaker(speaker_name, {'Beam_Modules' : modules})
        
        snooze(2) #allow time for calculations
        select_view_tab('bom')
        
        if check_method == 'bom_table':
            bom_data = get_BOM_data_from_table()
            test.log('Checking BOM Table')
            
        elif check_method == 'clipboard':
            copy_BOM_to_clipboard()
            bom_data = get_BOM_from_clipboard()
            test.log('Checking BOM copied to Clipboard')
            
        elif check_method == 'preview':
            generate_BOM_preview_and_close()
            bom_data = get_BOM_from_preview_file('data')
            test.log('Checking BOM from preview')
        else:
            test.fatal('Invalid value for check_method - %s' % check_method) ; return

        c_item = testData.field(scenario, 'cItem')
        c_qty = testData.field(scenario, 'cQuantity')
        c_sku = spkr_info['SKU']
        c_desc = spkr_info['DESCRIPTION']
        expected_data = [c_item, c_sku, c_desc, c_qty]
        
        test.compare(bom_data[1],expected_data,'BOM should be: ' + ', '.join(expected_data))
        
        select_view_tab('speaker')       
        delete_speakers(selectAll=True)
 