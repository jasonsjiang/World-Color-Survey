# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 16:06:23 2018

@author: dmetri
"""

from datascience import Table
from wcs_helper_functions import readChipData
from wcs_helper_functions import readClabData
from wcs_helper_functions import readNamingData
from wcs_helper_functions import readFociData
from wcs_helper_functions import readSpeakerData


def _get_sorted_keys_and_values(d):
    '''
    Returns the sorted keys and values from a dictionary
    '''
    # sort the keys and get the sorted values
    sorted_keys = [k for k in sorted(d.keys())]
    sorted_values = [d[k] for k in sorted_keys]
    return sorted_keys, sorted_values

def loadChipTables(*chipData):
    '''
    Loads the color chip information into two datascience Tables.
    
    Args:
        chipData (tuple or dict): a variable length argument consisting of 
            either a tuple with a dictionary mapping each Munsell coordinate 
            to its WCS chip number, and a dictionary mapping each WCS chip 
            number to its Munsell coordinates, or those dictionaries in 
            that order
            
    Returns:
        the same information in two datascience Table objects
        
    Examples:
        >>> munsellInfo = readChipData('./WCS_data_core/chip.txt')
        >>> coordToIndexTable, indexToCoordTable = loadChipTables(munsellInfo)
        ...
        >>> coord_to_index, index_to_coord = readChipData('./WCS_data_core/chip.txt')
        >>> coordToIndexTable, indexToCoordTable = loadChipTables(coord_to_index, 
                                                                  index_to_coord)
    '''
    if len(chipData) == 0:
        print('Warning: No data provided')
        return Table(), Table()
    if len(chipData) == 1:
        chipData = chipData[0]
    elif len(chipData) > 2:
        raise ValueError('chipData can accept at most two arguments')
    # coordinate to index
    # get the dictionaries
    coord_to_index = chipData[0]
    # sort the keys and get the sorted values
    sorted_keys, sorted_values = _get_sorted_keys_and_values(coord_to_index)

    coordToIndexTable = Table().with_columns('Coordinate', sorted_keys, 
                             'Index', sorted_values)

    # index to lightness, hue coordinate
    # get the dictionaries
    index_to_coord = chipData[1]
    # sort the keys and get the sorted values
    sorted_keys, sorted_values = _get_sorted_keys_and_values(index_to_coord)
    # unzip the lightness and hue values
    unzipped_values = [v for v in zip(*sorted_values)]
    # get the lightness and hue values
    lightness, hue = unzipped_values
    
    indexToCoordTable = Table().with_columns('Coordinate', sorted_keys, 
                             'Lightness', lightness, 'Hue', hue)

    return coordToIndexTable, indexToCoordTable
    
def loadClabTable(index_to_clab):
    '''
    Loads the stimulus CIELAB information information into a datascience Table.
    
    Args:
        index_to_clab (dict): a dictionary mapping each color index
            with its CIELAB coordinates: l (lightness), a (its position 
            between green and red/magenta), & b (its position between blue 
            and yellow)
            
    Returns:
        the same information in a datascience Table
    '''
    # sort the keys and get the sorted values
    sorted_keys, sorted_values = _get_sorted_keys_and_values(index_to_clab)
    # get the l, a and b values
    l = [v[0] for v in sorted_values]
    a = [v[1] for v in sorted_values]
    b = [v[2] for v in sorted_values]
    
    clabTable = Table().with_columns('Index', sorted_keys, 'l', l,
                    'a', a, 'b', b)
    return clabTable


def loadNamingTable(namingData):
    '''
    Loads the naming data into a datascience Table.
    
    Args:
        namingData (dict): a hierarchical dictionary mapping each language 
            to each speaker's naming data, which maps each color index to 
            their given color term
            
    Returns:
        the same information in a datascience Table
    '''
    # create lists for the information
    language = []
    speaker = []
    index = []
    color_term = []
    
    # loop through the languages
    for lang in namingData:
        # loop through the speakers
        for spkr in namingData[lang]:
            # loop through the color index
            for i in namingData[lang][spkr]:
                # get the color term
                term = namingData[lang][spkr][i]
                
                # add to the lists
                language.append(lang)
                speaker.append(spkr)
                index.append(i)
                color_term.append(term)
                
    # turn into a table
    namingTable = Table().with_columns('Language', language, 'Speaker', speaker,
                       'Index', index, 'Term', color_term)
    return namingTable
              
def loadFociTable(fociData):
    '''
    Loads the foci data into a datascience Table.
    
    Args:
        fociData (dict): a hierarchical dictionary mapping each language 
            to each speaker's foci data, which maps each color term to 
            that color's (perhaps multiple) foci coordinates
            
    Returns:
        the same information in a datascience Table
    '''
    # create lists for the information
    language = []
    speaker = []
    color_term = []
    foci_coord = []
    
    # loop through the languages
    for lang in fociData:
        # loop through the speakers
        for spkr in fociData[lang]:
            # loop through the color terms
            for term in fociData[lang][spkr]:
                # loop through the foci coordinates
                for coord in fociData[lang][spkr][term]:
                    # add to the lists
                    language.append(lang)
                    speaker.append(spkr)
                    color_term.append(term)
                    foci_coord.append(coord)
                
    # turn into a table
    fociTable = Table().with_columns('Language', language, 'Speaker', speaker,
                       'Term', color_term, 'Foci', foci_coord)
    return fociTable
    
def loadSpeakerTable(speakerData):
    '''
    Loads the speaker info into a datascience Table.
    
    Args:
        speakerData (dict): a dictionary mapping each language 
            to a list of its speakers' age and gender information
            
    Returns:
        the same information in a datascience Table
    '''
    # create lsits for the information
    language = []
    speaker = []
    age = []
    gender = []
    
    # loop through the languages
    for lang in speakerData:
        # loop through the speakers
        for spkr in speakerData[lang]:
            # add to the lists
            language.append(lang)
            speaker.append(spkr)
            # get the age and gender
            a, g = speakerData[lang][spkr][0]
            age.append(a)
            gender.append(g)
    
    # turn into a table
    speakerTable = Table().with_columns('Language', language, 'Speaker', 
                        speaker, 'Age', age, 'Gender', gender)
    return speakerTable

if __name__ == '__main__':
    # Munsell information
    munsellInfo = readChipData('./WCS_data_core/chip.txt')
    coordToIndexTable, indexToCoordTable = loadChipTables(munsellInfo)
    # test
#    coord_to_index, index_to_coord = readChipData('./WCS_data_core/chip.txt')
#    coordToIndexTable, indexToCoordTable = loadChipTables(coord_to_index, 
#                                                          index_to_coord)
    
    # CLAB Data
    index_to_clab = readClabData('./WCS_data_core/cnum-vhcm-lab-new.txt')
    clabTable = loadClabTable(index_to_clab)
    
    # Naming Data
    namingData = readNamingData('./WCS_data_core/term.txt')
    namingTable = loadNamingTable(namingData)
    
    # Foci Data
    fociData = readFociData('./WCS_data_core/foci-exp.txt')
    fociTable = loadFociTable(fociData)
    
    # Speaker Data
    speakerData = readSpeakerData('./WCS_data_core/spkr-lsas.txt')
    speakerTable = loadSpeakerTable(speakerData)
    
    
    

