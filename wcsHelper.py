# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 21:35:41 2018

Adapted by Dmetri Hayes for the Spring 2018 version of CogSci 88

@author: dmetri
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['readChipData', 'get_chip_to_rgb', 'get_chip_to_munsell', 
           'readNamingData', 'readFociData', 'readSpeakerData', 'makeModeMap',
           'naming2grid', 'plotColorGrid']

### Utility function
def _read_lines(filename):
    '''
    Reads in the lines of raw text from a filename.
    '''
    with open(filename, 'r') as f:
        text = f.read()
    lines = text.rstrip().split('\n')
    
    return lines

### Color chip information
def _get_munsell_dicts(lines):
    '''
    Gets the Munsell coordinates to chip number dictionary 
    and the inverse from the lines of the raw text.
    '''
    munsell_to_chip = {}
    chip_to_munsell = {}
    for row in lines:
        vals = row.split('\t')
        # the index is first
        index = int(vals[0])
        # the Munsell coordinates are the last two values
        L, H = vals[-2:]
        # link each Munsell coordinates to the corresponding chip number
        munsell_to_chip[L+H] = index
        # link each chip number to its Munsell coordinate tuple        
        chip_to_munsell[index] = (L, int(H))
        
    return munsell_to_chip, chip_to_munsell

def _get_clab_dict(lines):
    '''
    Gets the chip number to CIELAB coordinates 
    dictionary from the lines of the raw text.
    '''
    chip_to_clab = {}
    for row in lines:
        vals = row.split('\t')
        # the index is first
        index = int(vals[0])
        # the CIELAB coordinates are 4:7
        clab = [float(v) for v in vals[4:7]]
        # link each chip number to its CIELAB coordinates
        chip_to_clab[index] = tuple(clab)
        
    return chip_to_clab

def _get_rgb_dict(lines):
    '''
    Gets the chip number to RGB values 
    dictionary from the lines of the raw text.
    '''
    chip_to_rgb = {}
    for row in lines:
        vals = row.split('\t')
        # the index is first
        index = int(vals[0])
        # the RGB values are 1:4
        rgb = [int(v) for v in vals[1:4]]
        # link each chip number to its RGB values tuple
        chip_to_rgb[index] = tuple(rgb)
        
    return chip_to_rgb

def readChipData(filename='chipnum-info.txt', getFrame=False):
    '''
    Reads the color information for each of the color 
    chips as either a series of dictionaries or as a 
    Pandas DataFrame.
    
    Args:
        filename (str, optional): the path to the chip data
        getFrame (bool, optional): if True, returns 
            the information as a DataFrame. Otherwise, 
            the information is returned as a series of
            dictionaries.
    
    Returns:
        four dictionaries, mapping:
            -each chip number to its Munsell coordinates
            -Munsell coordinates to the chip number
            -each chip number to its CIELAB values
            -each chip number to its RGB values
        
        or a DataFrame containing the chip number, 
        lightness, hue, R, G, B, l a*, and b* values for
        each of the color chips
    
    Examples:
        >>> data = readChipData('chipnum-info.txt')
        >>> munsell_to_chip, chip_to_munsell, chip_to_clab, chip_to_rgb = data
        ...
        >>> df_chip = readChipData('chipnum-info.txt', getFrame=True)
    '''
    if getFrame:
        data = pd.read_table(filename, header=None)
        # add the column names
        columns = ['ChipNum', 'R', 'G', 'B', 'l', 'a', 'b', 'Lightness', 'Hue']
        data.columns = columns
        return data
    # otherwise, read in a series of dictionaries
    lines = _read_lines(filename)
    
    # link each Munsell coordinates to the corresponding chip number
    # link each chip number to its Munsell coordinate tuple
    munsell_to_chip, chip_to_munsell = _get_munsell_dicts(lines)
        
    # link each chip number to its CIELAB coordinates
    chip_to_clab = _get_clab_dict(lines)
    
    # link each chip number to its RGB values tuple
    chip_to_rgb = _get_rgb_dict(lines)
    
    return munsell_to_chip, chip_to_munsell, chip_to_clab, chip_to_rgb

def get_chip_to_rgb(filename_or_dataframe):
    '''
    Gets the chip number to RGB values dictionary, either
    by loading it from a file or extracting it from a 
    Pandas DataFrame.
    
    Args:
        filename_or_dataframe (str or `DataFrame`): the
            path to the chip data or a DataFrame containing 
            the chip numbers and RGB values
    
    Returns:
        a dictionary mapping each chip number to its RGB values
    
    Examples:
        >>> chip_to_rgb = get_chip_to_rgb('chipnum-info.txt')
        ...
        >>> chip_to_rgb = get_chip_to_rgb(df_chip)
    '''
    if type(filename_or_dataframe) == str:
        lines = _read_lines(filename_or_dataframe)
        chip_to_rgb = _get_rgb_dict(lines)
    elif type(filename_or_dataframe) == pd.DataFrame:
        df_chip = filename_or_dataframe
        # get the chip numbers and the RGB values
        chips = df_chip['ChipNum'].values
        rgb_vals = df_chip[['R', 'G', 'B']].values
        # create the dictionary
        chip_to_rgb = {}
        for i in range(len(chips)):
            chip_to_rgb[chips[i]] = tuple(rgb_vals[i])
    else:
        print('Warning: No data provided.')
        chip_to_rgb = {}
        
    return chip_to_rgb
    
def get_chip_to_munsell(filename_or_dataframe):
    '''
    Gets the chip number to Munsell coordinates dictionary, 
    either by loading it from a file or extracting it from 
    a Pandas DataFrame.
    
    Args:
        filename_or_dataframe (str or `DataFrame`): the
            path to the chip data or a DataFrame containing 
            the chip numbers and Munsell coordinates
    
    Returns:
        a chip number mapping each chip number to its 
        Munsell coordinates
    
    Examples:
        >>> chip_to_munsell = get_chip_to_munsell('chipnum-info.txt')
        ...
        >>> chip_to_munsell = get_chip_to_munsell(df_chip)
    '''
    if type(filename_or_dataframe) == str:
        lines = _read_lines(filename_or_dataframe)
        _, chip_to_munsell = _get_munsell_dicts(lines)
    elif type(filename_or_dataframe) == pd.DataFrame:
        df_chip = filename_or_dataframe
        # get the chip numbers and the RGB values
        chips = df_chip['ChipNum'].values
        munsell_vals = df_chip[['Lightness', 'Hue']].values
        # create the dictionary
        chip_to_munsell = {}
        for i in range(len(chips)):
            chip_to_munsell[chips[i]] = tuple(munsell_vals[i])
    else:
        print('Warning: No data provided.')
        chip_to_munsell = {}
        
    return chip_to_munsell

### Naming data
def readNamingData(filename='term.txt', getFrame=False):
    '''
    Loads the naming data into a hierarchical dictionary 
    or as a Pandas DataFrame.
    
    Args:
        filename (str, optional): the path to the naming data
        getFrame (bool, optional): if True, returns 
            the information as a DataFrame. Otherwise, 
            the information is returned as a hierarchical
            dictionaries.
            
    Returns:
        a hierarchical dictionary mapping each language 
        to each speaker's naming data, which maps each 
        color index to their given color term, or a 
        DataFrame with this same information
    
    Examples:
        >>> namingData = readNamingData('term.txt')
        ...
        >>> df_naming = readNamingData('term.txt', getFrame=True)
    '''
    if getFrame:
        data = pd.read_table(filename, header=None)
        # add the column names
        columns = ['Language', 'Speaker', 'ChipNum', 'Term']
        data.columns = columns
        return data
    # otherwise, read in as a hierarchical dictionary
    lines = _read_lines(filename)
    # create a nested dictionary
    namingData = {}
    # loop through the lines and add them to the dictionary
    for l in lines:
        # get the information from the line
        [lang, spkr, chipNum, term] = l.split('\t')
        # add the language dict if it doesn't exist
        if int(lang) not in namingData.keys():
            namingData[int(lang)] = {}
        # get the language naming dictionary
        langDict = namingData[int(lang)]
        # add the speaker dict if it doesn't exist
        if int(spkr) not in langDict.keys():
            langDict[int(spkr)] = {}
        # get the speaker naming dictionary
        spkrDict = langDict[int(spkr)]
        # add the speaker's term for this chip number
        spkrDict[int(chipNum)] = term
        
    return namingData

### Foci data
def readFociData(filename='foci-exp.txt', getFrame=False):
    '''
    Loads the foci data into a hierarchical dictionary 
    or as a Pandas DataFrame.
    
    Args:
        filename (str, optional): the path to the foci data
        getFrame (bool, optional): if True, returns 
            the information as a DataFrame. Otherwise, 
            the information is returned as a hierarchical
            dictionaries.
            
    Returns:
        a hierarchical dictionary mapping each language 
        to each speaker's naming data, which maps each 
        color term to its foci Munsell coordinates, or a 
        DataFrame with this same information
    
    Examples:
        >>> fociData = readNamingData('foci-exp.txt')
        ...
        >>> df_foci = readFociData('foci-exp.txt', getFrame=True)
    '''
    if getFrame:
        data = pd.read_table(filename, header=None)     
        # add the column names
        columns = ['Language', 'Speaker', 'TermNum', 'Term', 'Foci']
        data.columns = columns
        # fix bad WCS entries: collapse A1-40 to A0 and J1-40 to J0
        data['Foci'] = data['Foci'].str.replace('A.*', 'A0')
        data['Foci'] = data['Foci'].str.replace('J.*', 'J0')
        # separate lightness and hue values with a colon
        # create a function to apply to the columns
        myFun = lambda x: ('%s:%s' % (str(x)[0], str(x)[1:]))
        # get the new foci values
        newFoci = data['Foci'].apply(myFun)
        # replace the old foci values
        data['Foci'] = newFoci
        return data
    # otherwise, read in as a hierarchical dictionary
    lines = _read_lines(filename)
    # create a nested dictionary
    fociData = {}
    # loop through the lines and add them to the dictionary
    for l in lines:
        # get the information from the line (TermNum isn't used)
        [lang, spkr, _, term, foci] = l.split('\t')
        # add the language dict if it doesn't exist
        if int(lang) not in fociData.keys():
            fociData[int(lang)] = {}
        # get the language foci dictionary
        langDict = fociData[int(lang)]
        # add the speaker dict if it doesn't exist
        if int(spkr) not in langDict.keys():
            langDict[int(spkr)] = {}
        # get the speaker foci dictionary
        spkrDict = langDict[int(spkr)]
        # add the speaker's foci list if it doesn't exit
        if term not in spkrDict.keys():
            spkrDict[term] = []
        
        # fix bad WCS entries: collapse A1-40 to A0 and J1-40 to J0
        if (foci[0] == 'A'):
            foci = 'A0'
        if (foci[0] == 'J'):
            foci = 'J0'
        
        # separate lightness and hue values with a colon
        newFoci = '%s:%s' % (foci[0], foci[1:])
        # add this foci data
        spkrDict[term].append(newFoci)
        
    return fociData

### Speaker data
def readSpeakerData(filename='spkr-lsas.txt', getFrame=False):
    '''
    Loads the speaker's age and gender information into a 
    dictionary or a Pandas DataFrame.
    
    Args:
        filename (str, optional): the path to the speaker data
        getFrame (bool, optional): if True, returns 
            the information as a DataFrame. Otherwise, 
            the information is returned as a dictionary.
    
    Returns:
        a dictionary mapping each language to a list of its 
        speakers' age and gender information, or a DataFrame
        containing the same information
    
    Examples:
        >>> speakerData = readSpeakerData('spkr-lsas.txt')
        ...
        >>> df_speaker = readSpeakerData('spkr-lsas.txt', getFrame=True)
    '''
    if getFrame:
        data = pd.read_table(filename, header=None)     
        # add the column names
        columns = ['Language', 'Speaker', 'Age', 'Gender']
        data.columns = columns
        return data
    # otherwise, read in as a dictionary
    lines = _read_lines(filename)
    speakerData = {}
    # loop through the lines and add them to the dictionary
    for l in lines:
        # get the information from the line
        [lang, spkr, age, gender] = l.split('\t')
        # add the language dict if it doesn't exist
        if int(lang) not in speakerData.keys():
            speakerData[int(lang)] = {}
        # get the language demographic dictionary
        langDict = speakerData[int(lang)]
        # add the speaker's age and gender
        langDict[int(spkr)] = (int(age), gender)
        
    return speakerData

### Mode maps
def makeModeMap(data, lang=None):
    """
    Finds the mode map for a language given its naming data.
    
    Args:
        data (dict): a dictionary containing either the full naming dictionary 
            or the naming dictionary of a single language
        lang (str, optional): the name of the language. if lang is 
            not provided then data should be the naming data of a single 
            language
            
    Returns:
        a dictionary indexed by chip number with the modal values for each 
        color
    
    Examples:
        >>> mm_lang1 = makeModeMap(namingData, lang=1)
        ...
        >>> lang1 = namingData[1]
        >>> mm_lang1 = makeModeMap(lang1)
    """
    # get the language naming data
    if lang != None:
        langData = data[lang]
    else:
        langData = data
    
    # create an empty mode map
    modeMap = {}

    # create a dictionary with all of the terms
    allTerms = {}
    # get the speaker naming data
    for spkrData in langData.values():
        # get the chip and color term
        for chip, term in spkrData.items():
            # if the chip isn't in allTerms, add it
            if not (chip in allTerms.keys()):
                allTerms[chip] = []
            # append color term to allTerms
            allTerms[chip].append(term)
            
    def findMode(aList):
        freq = {}
        for i in aList: freq[i] = freq.get(i, 0) + 1
        freqlist = sorted(freq, key=freq.get, reverse=True)
        mode = freqlist[0]
        return mode

    for chip, terms in allTerms.items():
        mode = findMode(terms)
        modeMap[chip] = mode

    return modeMap

### Grid colors
def naming2grid(data, chip_to_rgb):
    '''
    Converts naming data to a grid of mean RGB values.
    
    Args:
        data (dict): a dictionary mapping each chip number 
            to a color term
        chip_to_rgb (dict): a dictionary mapping each chip
            number to its RGB values
    
    Returns:
        a NumPy array containing the RGB values for each 
        chip number, with values equal to the mean RGB 
        values across all chips named by each color term
        
    Examples:
        >>> grid_lang1_spkr1 = naming2grid(namingdata[1][1], chip_to_rgb)
        ...
        >>> mm_lang1 = makeModeMap(namingData, lang=1)
        >>> grid_mode_lang1 = naming2grid(mm_lang1)
    '''
    term_colors = {}

    for term in set(data.values()):
        term_idx = np.where(np.array(list(data.values()))==term)[0]
        rgbs = []
        for chipnum in term_idx:
            rgbs.append(chip_to_rgb[chipnum+1])

        color_j_display_rbg = np.mean(np.array(rgbs),axis=0)/255.
        term_colors[term] = [color_j_display_rbg[0],color_j_display_rbg[1],color_j_display_rbg[2]]

    grid_colors = np.zeros((330,3))
    for i in range(1, len(chip_to_rgb) + 1):
        grid_colors[i-1] = term_colors[data[i]]

    return grid_colors

### Plotting
    
def _chip2ind(chipNum, chip_to_munsell):
    '''
    Returns the row and column index given 
    a chip number and a dictionary mapping the 
    chip number to its Munsell coordinates.
    '''
    ROWS = ['A','B','C','D','E','F','G','H','I','J']

    row = ROWS.index(chip_to_munsell[chipNum][0])
    col = int(chip_to_munsell[chipNum][1])

    return row, col 

def _grid2img(grid, chip_to_munsell):
    '''
    Turns a color grid into a plottable image, 
    given a dictionary mapping each chip 
    number to its Munsell coordinates.
    '''
    N_COLS = 41
    N_ROWS = 10

    img = np.ones((N_ROWS, N_COLS + 1, 3))
    for chipNum in range(1, len(grid) + 1):
        i , j = _chip2ind(chipNum, chip_to_munsell)
        j = j + 1 if j>0 else j
        img[i, j, :] = grid[chipNum - 1, :]
        if img[i, j, 0] == 50:
            img[i, j, :] = img[i, j, :]
    return img

def plotColorGrid(grid, chip_to_munsell, figsize=(20, 4)):
    '''
    Plots a color grid given a dictionary mapping 
    each chip number to its Munsell coordinates.
    
    Args:
        grid (dict): a NumPy array containing the 
            RGB values for each chip number
        chip_to_munsell (dict): a dictionary mapping
            each chip number to its Munsell coordinates
        figsize (tuple, optional): the figure size which
            is fed into `plt.figure`
    
    Returns:
        the figure and axes of the produced plot
    
    Examples:
        >>> grid = naming2grid(namingdata[1][1], chip_to_rgb)
        >>> plotColorGrid(grid, chip_to_munsell)
        ...
    '''
    rowNames = ['A','B','C','D','E','F','G','H','I','J']
    numCols = 41
    numRows = 10
            
    fig = plt.figure(figsize=figsize)
    axes = plt.axes()
    # get the image
    img = _grid2img(grid, chip_to_munsell)
    plt.imshow(img)
    for i in range(numRows):
        plt.text(0.7, i, rowNames[i],
                 fontsize=10,
                 style='italic',
                 horizontalalignment='left',
                 verticalalignment='center')
    for i in range(1, numCols):
        plt.text(i+.75, 0, str(i),
                 fontsize=10,
                 style='italic',
                 horizontalalignment='left',
                 verticalalignment='center')
    # ax.set_aspect('equal','datalim')
    plt.axis('off')
    return fig, axes
    

### 3D colorspace with plotly(?)