import tkinter as tk
from tkinter import font  as tkfont
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import os
import json
import subprocess
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
import scipy.io as sio
from readValidationVideo import readValidationVideo

from mainZZ import mainZZ
from getTailExtremityFirstFrame import getTailExtremityFirstFrame
import popUpAlgoFollow

import configFilePrepareFunctions
import GUI_InitialFunctions
import configFileZebrafishFunctions
import adjustParameterInsideAlgoFunctions
from GUI_InitialClasses import FullScreenApp, StartPage, SeveralVideos, VideoToAnalyze, FolderToAnalyze, TailExtremityHE, ConfigFilePromp, Patience, ZZoutro, ResultsVisualization, ViewParameters
from configFilePrepare import ChooseVideoToCreateConfigFileFor, ChooseGeneralExperiment, WellOrganisation, CircularWells, NumberOfAnimals, IdentifyHeadCenter, IdentifyBodyExtremity, FinishConfig, ChooseCircularWellsLeft, ChooseCircularWellsRight, GoToAdvanceSettings
from configFileZebrafish import HeadEmbeded
from adjustParameterInsideAlgo import AdujstParamInsideAlgo, AdujstParamInsideAlgoFreelySwim

LARGE_FONT= ("Verdana", 12)

def getCurrentResultFolder():
  return currentResultFolder

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("ZebraZoom")
        self.currentResultFolder = "abc"
        self.homeDirectory = os.path.dirname(os.path.realpath(__file__))
        
        self.configFile = {}
        self.videoToCreateConfigFileFor = ''
        self.wellLeftBorderX = 0
        self.wellLeftBorderY = 0
        self.headCenterX = 0
        self.headCenterY = 0
        self.organism = ''
        
        self.numWell = 0
        self.numPoiss = 0
        self.numMouv = 0
        self.visualization = 0
        self.justEnteredViewParameter = 0
        self.dataRef = {}
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")   
        FullScreenApp(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) 
        self.container = container
        self.frames = {}
        for F in (StartPage, SeveralVideos, VideoToAnalyze, ChooseVideoToCreateConfigFileFor, ChooseGeneralExperiment, WellOrganisation, CircularWells, NumberOfAnimals, IdentifyHeadCenter, IdentifyBodyExtremity, ChooseCircularWellsLeft, ChooseCircularWellsRight, FinishConfig, FolderToAnalyze, TailExtremityHE, ConfigFilePromp, Patience, ZZoutro, ResultsVisualization, ViewParameters, HeadEmbeded, AdujstParamInsideAlgo, AdujstParamInsideAlgoFreelySwim, GoToAdvanceSettings):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def chooseVideoToAnalyze(self, justExtractParams, noValidationVideo):
        GUI_InitialFunctions.chooseVideoToAnalyze(self, justExtractParams, noValidationVideo)

    def chooseFolderToAnalyze(self, justExtractParams, noValidationVideo):
        GUI_InitialFunctions.chooseFolderToAnalyze(self, justExtractParams, noValidationVideo)
        
    def chooseFolderForTailExtremityHE(self):
        GUI_InitialFunctions.chooseFolderForTailExtremityHE(self)
    
    def chooseConfigFile(self):
        GUI_InitialFunctions.chooseConfigFile(self)
        
    def launchZebraZoom(self):
        GUI_InitialFunctions.launchZebraZoom(self)
        
    def showResultsVisualization(self):
        self.frames['ResultsVisualization'].destroy()
        frame = ResultsVisualization(parent=self.container,controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames['ResultsVisualization'] = frame
        self.show_frame("ResultsVisualization")

    def showValidationVideo(self, numWell, zoom, deb):
        GUI_InitialFunctions.showValidationVideo(self, numWell, zoom, deb)

    def printSomeResults(self, numWell, numPoiss, numMouv, changeVisualization=False):
        if changeVisualization:
            self.visualization = int(self.visualization + 1) % 3
        
        self.numWell  = int(numWell)
        self.numPoiss = int(numPoiss)
        self.numMouv  = int(numMouv)
        if self.numWell < 0:
            self.numWell = 0
        if self.numPoiss < 0:
            self.numPoiss = 0
        if self.numMouv < 0:
            self.numMouv = 0
        self.frames['ViewParameters'].destroy()
        frame = ViewParameters(parent=self.container,controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames['ViewParameters']=frame
        self.show_frame("ViewParameters")
        
    def exploreResultFolder(self, currentResultFolder):
        GUI_InitialFunctions.exploreResultFolder(self, currentResultFolder)
        
    def printNextResults(self, numWell, numPoiss, numMouv, nbWells, nbPoiss, nbMouv):
        GUI_InitialFunctions.printNextResults(self, numWell, numPoiss, numMouv, nbWells, nbPoiss, nbMouv)

    def printPreviousResults(self, numWell, numPoiss, numMouv, nbWells, nbPoiss, nbMouv):
        GUI_InitialFunctions.printPreviousResults(self, numWell, numPoiss, numMouv, nbWells, nbPoiss, nbMouv)

    def flagMove(self, numWell, numPoiss, numMouv):
        GUI_InitialFunctions.flagMove(self, numWell, numPoiss, numMouv)

    def saveSuperStruct(self, numWell, numPoiss, numMouv):
        GUI_InitialFunctions.saveSuperStruct(self, numWell, numPoiss, numMouv)
        
    def openConfigurationFileFolder(self, homeDirectory):
        GUI_InitialFunctions.openConfigurationFileFolder(self, homeDirectory)
        
    def openZZOutputFolder(self, homeDirectory):
        GUI_InitialFunctions.openZZOutputFolder(self, homeDirectory)
        
    # Config File preparation functions
    
    def chooseVideoToCreateConfigFileFor(self, controller):
        configFilePrepareFunctions.chooseVideoToCreateConfigFileFor(self, controller)
    
    def chooseGeneralExperiment(self, controller, freeZebra, headEmbZebra, drosophilia, rodent, other):
        configFilePrepareFunctions.chooseGeneralExperiment(self, controller, freeZebra, headEmbZebra, drosophilia, rodent, other)
        
    def wellOrganisation(self, controller, circular, roi, other):
        configFilePrepareFunctions.wellOrganisation(self, controller, circular, roi, other)
        
    def circularWells(self, controller, nbwells, nbRowsOfWells, nbWellsPerRows):
        configFilePrepareFunctions.circularWells(self, controller, nbwells, nbRowsOfWells, nbWellsPerRows)
        
    def finishConfig(self, controller, configFileNameToSave):
        configFilePrepareFunctions.finishConfig(self, controller, configFileNameToSave)
        
    def chooseCircularWellsLeft(self, controller):
        configFilePrepareFunctions.chooseCircularWellsLeft(self, controller)

    def chooseCircularWellsRight(self, controller):
        configFilePrepareFunctions.chooseCircularWellsRight(self, controller)

    def numberOfAnimals(self, controller, nbanimals, yes, noo):
      configFilePrepareFunctions.numberOfAnimals(self, controller, nbanimals, yes, noo)
        
    def chooseHeadCenter(self, controller):
        configFilePrepareFunctions.chooseHeadCenter(self, controller)

    def chooseBodyExtremity(self, controller):
        configFilePrepareFunctions.chooseBodyExtremity(self, controller)
    
    def chooseBeginningAndEndOfVideo(self, controller):
        configFilePrepareFunctions.chooseBeginningAndEndOfVideo(self, controller)

    def headEmbededGUI(self, controller, blackBack, whiteBack, noBoutDetect, boutDetection, optionExtendedDescentSearchOption, 
optionBackgroundExtractionOption):
        configFileZebrafishFunctions.headEmbededGUI(self, controller, blackBack, whiteBack, noBoutDetect, boutDetection, optionExtendedDescentSearchOption, optionBackgroundExtractionOption)

    def detectBouts(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo):
      adjustParameterInsideAlgoFunctions.detectBouts(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo)
      
    def adjustHeadEmbededTracking(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo):
      adjustParameterInsideAlgoFunctions.adjustHeadEmbededTracking(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo)
    
    def adjustFreelySwimTracking(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo):
      adjustParameterInsideAlgoFunctions.adjustFreelySwimTracking(self, controller, wellNumber, firstFrameParamAdjust, adjustOnWholeVideo)

    def calculateBackground(self, controller, nbImagesForBackgroundCalculation):
      adjustParameterInsideAlgoFunctions.calculateBackground(self, controller, nbImagesForBackgroundCalculation)
      
    def calculateBackgroundFreelySwim(self, controller, nbImagesForBackgroundCalculation):
      adjustParameterInsideAlgoFunctions.calculateBackgroundFreelySwim(self, controller, nbImagesForBackgroundCalculation)
    
    def chooseVideoToCreateConfigFileFor(self, controller, reloadConfigFile):
      configFilePrepareFunctions.chooseVideoToCreateConfigFileFor(self, controller, reloadConfigFile)

    def goToAdvanceSettings(self, controller, yes, no):
      configFilePrepareFunctions.goToAdvanceSettings(self, controller, yes, no)